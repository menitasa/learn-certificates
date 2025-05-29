# PKI and Certificate Authority (CA) Basics

## What is PKI?

A system for managing digital certificates and public-private key pairs. It ensures secure communication and identity verification.

### Key Components

- **Certificate Authority (CA):** Issues and signs certificates (e.g., Let's Encrypt, your own company CA)
- **Registration Authority (RA):** Verifies identities before a CA issues a certificate
- **Certificate Repository:** Stores certificates and revocation lists (CRL)

### How PKI Works

1. Generate a key pair (private/public)
2. Create a Certificate Signing Request (CSR) and send it to a CA
3. CA verifies your identity and signs your certificate
4. Others trust your certificate if they trust the CA

---

## Certificate Authorities (CA): Public vs. Private

- **Public CA:**

  - Trusted by browsers and operating systems out of the box
  - Used for public websites, APIs, etc.
  - Examples: Let's Encrypt, DigiCert, GlobalSign

- **Private CA:**

  - Used inside organizations for internal services, VPNs, dev/test environments
  - Not trusted by default; you must add the CA's root certificate to your systems

- **Root CA:**

  - Top-level CA, self-signed, widely trusted (for public CAs)
  - Signs intermediate CAs

- **Intermediate CA:**
  - Sits between the root CA and end-entity certificates
  - Adds security: root CA's private key can be kept offline

---

## Certificate Chains and Trust

- **Certificate Chain:**

  - Sequence: Your certificate → Intermediate CA(s) → Root CA
  - Each certificate is signed by the one above it

- **Trust:**
  - If your system trusts the root CA, and the chain is unbroken, it trusts your certificate
  - Browsers/OS have a list of trusted root CAs

**Example:**
When you visit `https://example.com`, your browser checks the certificate chain up to a trusted root CA. If any link is broken or untrusted, you get a warning.

#### Inspect a Certificate Chain (OpenSSL)

```sh
openssl s_client -connect example.com:443 -showcerts
```

---

## Self-Signed vs. CA-Signed Certificates

- **Self-Signed:**

  - Signed with its own private key
  - Not trusted by default (browsers will warn)
  - Good for internal/dev/test use

- **CA-Signed:**
  - Signed by a CA's private key
  - Trusted if the CA is trusted by your system

---

## Key Takeaways

- PKI and CAs are the foundation of digital trust
- Trust is established by following the chain up to a trusted root CA
- Self-signed certs are for internal use; CA-signed for public trust
