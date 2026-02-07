# Security Policy

## Cryptographic Design

| Primitive | Choice | Parameters |
|---|---|---|
| Encryption | AES-256-GCM | 256-bit key, 12-byte nonce, 16-byte authentication tag |
| Key derivation | PBKDF2-HMAC-SHA256 | 16-byte random salt, 1 200 000 iterations (default) |
| Nonce construction | `base_nonce XOR chunk_index` | 12 bytes, big-endian index |
| AAD per chunk | `b"chunk_<index>"` | Binds each chunk to its position |

- A fresh random salt and base nonce are generated for every encryption
  operation.
- The per-chunk nonce is derived deterministically from the base nonce and the
  chunk index via XOR, ensuring uniqueness without requiring storage of
  additional nonces.
- GCM authentication tags protect both confidentiality and integrity — any
  modification to the ciphertext, header, or chunk ordering is detected at
  decryption time.

## Threat Model

**In scope:**

- Confidentiality and integrity of data at rest (local files, cloud backups,
  USB drives, etc.).
- Detection of tampered or corrupted ciphertext.
- Protection against offline brute-force attacks on the password through
  high-iteration PBKDF2.

**Out of scope:**

- Resistance to an attacker who can observe the encryption process in real
  time (side-channel attacks, memory scraping).
- Hiding the *existence* or *size* of encrypted data (the file format header
  and part count are visible).
- Key management beyond a single user-supplied password.

## Known Limitations

1. **PBKDF2 vs. memory-hard KDFs** — PBKDF2-HMAC-SHA256 is well-studied and
   widely available, but it is not memory-hard. An attacker with GPU/ASIC
   resources can run many iterations in parallel more cheaply than with
   Argon2id or scrypt. The high default iteration count (1 200 000) mitigates
   this, but a strong, high-entropy password remains essential.

2. **Password strength** — vault-tar does not enforce password complexity rules.
   Encryption security is ultimately bounded by password entropy.

3. **No key rotation** — changing the password requires full re-encryption.
   There is no envelope-key / wrapping-key scheme.

4. **Metadata leakage** — file count, part-file sizes, and compression ratio
   are observable. The directory structure and file names are protected inside
   the encrypted archive, but their aggregate size is not hidden.

5. **No forward secrecy** — compromise of the password exposes all past and
   future data encrypted with that password.

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, **please do not open a public
issue.** Instead, use GitHub's
[private vulnerability reporting](https://github.com/l1asis/vault-tar/security/advisories/new)
to submit a report. You will receive an acknowledgement within **72 hours**.
