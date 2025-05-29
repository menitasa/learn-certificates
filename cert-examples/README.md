# Certificate Examples: How to Examine and Understand Them

This folder contains real-world example files for various certificate-related artifacts. Use these to learn how each file type looks, how to inspect them, and what their purpose is in the certificate lifecycle.

## File List and Purpose

| File           | Type               | Purpose                                            |
| -------------- | ------------------ | -------------------------------------------------- |
| ca.key         | CA Private Key     | The private key for the Certificate Authority (CA) |
| ca.crt         | CA Certificate     | The public certificate for the CA                  |
| server.key     | Server Private Key | The private key for the server                     |
| server.csr     | Server CSR         | Certificate Signing Request for the server         |
| server.crt     | Server Certificate | The server's certificate, signed by the CA         |
| client.key     | Client Private Key | The private key for the client                     |
| client.csr     | Client CSR         | Certificate Signing Request for the client         |
| client.crt     | Client Certificate | The client's certificate, signed by the CA         |
| selfsigned.key | Self-signed Key    | Private key for a self-signed certificate          |
| selfsigned.crt | Self-signed Cert   | Self-signed certificate (not signed by a CA)       |

---

## How to Open and Inspect Each File

### 1. Private Keys (`*.key`)

- **Command:**
  ```sh
  openssl rsa -in <file>.key -text -noout
  ```
- **What to look for:**
  - Key type (RSA, EC, etc.)
  - Key size (2048, 4096 bits, etc.)
  - Modulus and public exponent
- **Purpose:**
  - Used to sign CSRs and decrypt data. **Keep private!**

### 2. Certificate Signing Requests (CSRs) (`*.csr`)

- **Command:**
  ```sh
  openssl req -in <file>.csr -text -noout
  ```
- **What to look for:**
  - Subject fields (CN, O, C, etc.)
  - Requested extensions
  - Public key info
- **Purpose:**
  - Sent to a CA to request a signed certificate

### 3. Certificates (`*.crt`)

- **Command:**
  ```sh
  openssl x509 -in <file>.crt -text -noout
  ```
- **What to look for:**
  - Subject and Issuer fields
  - Validity period (Not Before/Not After)
  - Public key info
  - Extensions (Key Usage, SAN, etc.)
- **Purpose:**
  - Proves the identity of the holder (server, client, CA)

---

## Example Use Cases

- **CA files**: Used to sign other certificates and establish trust.
- **Server files**: Used by web servers to enable HTTPS.
- **Client files**: Used for client authentication (mTLS).
- **Self-signed files**: Used for testing or internal use, not trusted by browsers by default.

---

## Tips

- Never share your private keys (`*.key`).
- You can open these files in a text editor to see the PEM format (base64 with header/footer).
- Use the commands above to see human-readable details.
- Compare the Subject and Issuer fields to understand trust relationships.

---

## Learn More

- Try modifying and regenerating these files using OpenSSL commands from the labs.
- Experiment with different subject fields and key types.
- See the main lab guides for more hands-on exercises.
