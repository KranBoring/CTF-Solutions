import { readFileSync } from "fs";
import sshpk from "sshpk";
import jwt from "jsonwebtoken";

const PRIVATE_KEY_PATH = "/secrets/key";
const PUBLIC_KEY_PATH = "/secrets/key.pub";

export function parseKey(
  type: "private" | "public",
  key: string,
  options: { format?: "pem" | "pkcs8" | "ssh" | "openssh" } = {},
): string {
  let parsedKey: sshpk.Key | sshpk.PrivateKey;
  if (type === "private") {
    parsedKey = sshpk.parsePrivateKey(key, "ssh");
  } else {
    parsedKey = sshpk.parseKey(key, "ssh", { filename: "publickey" });
  }
  return parsedKey.toString(options.format || "pem");
}

const privateRaw = readFileSync(PRIVATE_KEY_PATH, "utf8");

const publicRaw = readFileSync(PUBLIC_KEY_PATH, "utf8");

export function signToken(
  payload: object,
  expiresIn: jwt.SignOptions["expiresIn"] = "1h",
) {
  return jwt.sign(payload, parseKey("private", privateRaw), { algorithm: "ES256", expiresIn });
}

export function verifyToken<T = object>(token: string) {
  return jwt.verify(token, parseKey("public", publicRaw)) as T;
}
