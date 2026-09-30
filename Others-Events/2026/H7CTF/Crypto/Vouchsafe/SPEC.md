# H7 Passport - Relying Party Protocol Notes

H7 Passport is a passwordless SSO enrollment portal built as a WebAuthn / FIDO2
Relying Party. Staff register a passkey and then authenticate with it. The admin
console is gated: only credentials enrolled at the **enterprise** tier may drive
the privileged action behind `/assert/finish`.

This document is the integration note handed to partners. It describes the wire
format and the enrollment policy. It does not describe the server internals.

## Endpoints

All bodies are JSON. Binary fields are base64url (padding optional).

### `GET /register/begin`
Costs 1 Ledger credit. Returns:

```
{ "rpId": "...", "origin": "https://...", "challenge": "<b64url 32 bytes>",
  "pubKeyAlg": -7, "tiers": ["standard","enterprise"],
  "formats": ["packed","tpm","android-key"], "credits": <int> }
```

### `POST /register/finish`
```
{ "clientDataJSON": "<b64url>", "attestationObject": "<b64url CBOR>" }
```
`clientDataJSON` is the standard WebAuthn structure
`{"type":"webauthn.create","challenge":"<b64url>","origin":"..."}` and must echo
the challenge from `/register/begin`. `attestationObject` is CBOR:
`{ "fmt": <string>, "attStmt": {...}, "authData": <bytes> }`.

`authData` is the standard layout: `rpIdHash(32) || flags(1) || signCount(4) ||
attestedCredentialData`, where `attestedCredentialData = aaguid(16) ||
credIdLen(2) || credId || COSE_Key`. The credential key is COSE EC2 / P-256 /
ES256. The user-present (0x01), user-verified (0x04) and attested-credential
(0x40) flag bits apply as usual.

On success returns `{ "status":"enrolled", "tier": "...", "credentialId":"..." }`.

### `GET /assert/begin`
Costs 1 Ledger credit. Returns `{ "challenge":"<b64url 32 bytes>", "credits":<int> }`.

### `POST /assert/finish`
```
{ "credentialId":"<b64url>", "clientDataJSON":"<b64url>",
  "authenticatorData":"<b64url>", "signature":"<b64url DER ECDSA>" }
```
`clientDataJSON` type is `webauthn.get` and echoes the `/assert/begin` challenge.
The signature is computed over `authenticatorData || SHA256(clientDataJSON)`.
The user-verified flag must be set. If the credential's stored tier is
enterprise, the privileged action runs.

## Attestation formats

`packed`, `tpm` and `android-key` are accepted. For known authenticators the RP
pins the FIDO Alliance Metadata Service (MDS3) as its trust store: if the
credential's AAGUID is listed in the shipped MDS blob, the attestation
certificate chain is built and verified up to the pinned
`attestationRootCertificate` for that entry.

The RP also keeps a legacy **self-enrolled enterprise authenticator** path for
air-gapped corporate hardware that predates MDS registration, i.e. authenticators
whose AAGUID is not present in the metadata store. That path was written before
MDS existed and has been carried forward unchanged.

## Enterprise policy extension

Enterprise-tier corporate authenticators carry an internal policy extension on
their attestation leaf certificate:

```
id-h7-authnr-policy OBJECT IDENTIFIER ::= { 1 3 6 1 4 1 61387 2 7 4 }

AuthenticatorPolicy ::= SEQUENCE {
    version       INTEGER,
    aaguidCount   INTEGER,
    aaguids       SEQUENCE OF OCTET STRING,
    elevated  [7] BOOLEAN OPTIONAL,
    ...           -- additional context-tagged policy flags
}
```

`elevated` is the field the console consults. A consumer or standard corporate
authenticator ships `elevated` FALSE.

### Parser changelog (internal, v2.1)

> Policy fields were migrated from positional decoding to explicit
> context-tag numbering. The tag assigned to the trailing policy flags is now
> derived relative to the aaguid section rather than hard-coded, so the parser
> stays stable if earlier optional fields are added or removed.

## The Metadata blob

`mds_blob.json` is the frozen MDS3 JWT the RP pins. Its middle segment is the
base64url payload; `entries[].aaguid` and
`entries[].attestationRootCertificates` are what the RP trusts.

## Ledger

`/register/begin` and `/assert/begin` each cost one Ledger credit. Budget your
attempts.
