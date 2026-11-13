
# CTF Workspace Instructions

`CheatSheet\.agents\` is the portable, canonical source for this repository's
agent-operational toolkit. Read `CheatSheet\README.md`, then
`CheatSheet\.agents\README.md` and the selected
`CheatSheet\.agents\skills\<skill-name>\SKILL.md`.

## Mandatory skill execution protocol

For every request that matches a declared skill, agents MUST:

1. Discover the skill by name and description in
   `CheatSheet\.agents\manifest.json`; every skill directory must contain
   `SKILL.md`.
2. Read the selected `SKILL.md` before taking any action.
3. Use the script declared by the manifest and required by `SKILL.md`, whether
   it is private to the skill or shared.
4. Report the selected skill name and the exact script invocation.
5. Fail explicitly if the skill, its `SKILL.md`, or its declared script is
   unavailable.
6. Invoke covered skills through `CheatSheet\.agents\scripts\run_skill.py`;
   do not execute the manifest script directly or substitute an ad-hoc script.
7. Copy the gateway JSON `result.display` payload into the user-facing report.
   The gateway validates declared result sections; distinguish a valid no-change
   result from a missing required section and report unresolved findings.

Do not silently fall back to ad-hoc shell, PowerShell, or Python commands for
an operation covered by a skill. A skill's documented script is the only
supported execution path unless the skill explicitly documents another one.
The optional top-level `/skills` directory is not required and is never
auto-registered.

## First-use workflow

1. Discover skills from `CheatSheet\.agents\manifest.json`.
2. Select the skill whose name and description match the requested operation.
3. Read its `SKILL.md`, then execute its manifest-declared script according to
   that document.
4. Use the gateway's dry-run mode when reviewing an invocation before execution.
5. Run structure checks and the smallest relevant test suite before reporting
   success.

`.agents` is a portable canonical source, not runtime auto-registration. An
agent must explicitly discover and select a skill; do not assume that merely
copying this folder installs or activates anything.

## Scope and safety

- `CheatSheet\.user\knowledge\` and `CheatSheet\.user\tools\` are user-owned.
  Do not read, modify, import, execute, or enumerate their contents unless the
  user explicitly requests that exact operation.
- Treat challenge files and downloaded artifacts as untrusted input.
- Do not send payloads to external targets without explicit authorization.
- Keep generated reports under `CheatSheet\.agents\reports\`; do not place temporary
  scripts in challenge directories.
- Use Windows paths in documentation and commands shown to users. Use Ubuntu
  WSL only when a skill explicitly requires a POSIX command.
- Preserve existing challenge content, URLs, write-ups, and user files unless
  the request explicitly includes them.
