# How to Create a Private CA and Sign Server/Client Certificates

This guide shows how to set up your own private Certificate Authority (CA) using OpenSSL, sign server and client certificates, and explains best practices for separation and mutual TLS (mTLS).

---

## Best Practice: Folder Structure for a PKI Environment

A clear and secure folder structure is essential for managing your CA, server, and client certificates and keys. Here's a recommended layout:

```
my-ca/
├── certs/           # All issued certificates (CA, server, client)
├── private/         # All private keys (CA, server, client) - keep this secure!
├── csr/             # Certificate Signing Requests (CSRs)
├── newcerts/        # OpenSSL uses this to store new certs (index)
├── crl/             # Certificate Revocation Lists
├── index.txt        # OpenSSL database of issued certs
├── serial           # Serial number counter for new certs
├── openssl-ca.cnf   # Your OpenSSL config file
```

- **certs/**: Store all public certificates here (never private keys).
- **private/**: Store all private keys here. Set permissions to restrict access (e.g., `chmod 700`).
- **csr/**: Store all CSRs here for record-keeping and auditing.
- **newcerts/**: Used by OpenSSL to keep track of issued certificates.
- **crl/**: Store Certificate Revocation Lists here if you use revocation.
- **index.txt, serial**: Required by OpenSSL to track issued and revoked certificates.
- **openssl-ca.cnf**: Your main config file for the CA.

**Tip:** Never store private keys in the same folder as public certificates. Always back up your CA private key securely and keep it offline if possible.

---

## 1. Create a Private CA with an OpenSSL Config File

### a. Prepare Directories and Files

```sh
mkdir my-ca && cd my-ca
mkdir certs private
chmod 700 private
cp /etc/ssl/openssl.cnf ./openssl-ca.cnf  # Or create your own config file
```

- `certs/`: Where issued certificates will be stored
- `private/`: Where private keys are kept (should be secure)

### b. Generate the CA Private Key and Self-Signed Root Certificate

```sh
openssl genrsa -out private/ca.key.pem 4096
chmod 400 private/ca.key.pem
openssl req -config openssl-ca.cnf -key private/ca.key.pem -new -x509 -days 3650 -sha256 -extensions v3_ca -out certs/ca.cert.pem
chmod 444 certs/ca.cert.pem
```

- The config file (`openssl-ca.cnf`) should have a `[ v3_ca ]` section for CA extensions (see below).

#### Example `[ v3_ca ]` Section in Config File

```ini
[ v3_ca ]
basicConstraints = critical,CA:true
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always
```

---

## 2. Create and Sign a Server Certificate

### a. Generate Server Private Key and CSR

```sh
openssl genrsa -out private/server.key.pem 2048
openssl req -new -key private/server.key.pem -out server.csr.pem \
  -subj "/C=US/ST=California/L=San Francisco/O=Example Corp/CN=server.example.com"
```

### b. Sign the Server Certificate with the CA

```sh
openssl x509 -req -in server.csr.pem -CA certs/ca.cert.pem -CAkey private/ca.key.pem \
  -CAcreateserial -out certs/server.cert.pem -days 365 -sha256 \
  -extfile openssl-ca.cnf -extensions server_cert
```

#### Example `[ server_cert ]` Section in Config File

```ini
[ server_cert ]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = server.example.com
DNS.2 = www.server.example.com
```

---

## 3. Create and Sign a Client Certificate

### a. Generate Client Private Key and CSR

```sh
openssl genrsa -out private/client.key.pem 2048
openssl req -new -key private/client.key.pem -out client.csr.pem \
  -subj "/C=US/ST=California/L=San Francisco/O=Example Corp/CN=alice/emailAddress=alice@example.com"
```

### b. Sign the Client Certificate with the CA

```sh
openssl x509 -req -in client.csr.pem -CA certs/ca.cert.pem -CAkey private/ca.key.pem \
  -CAcreateserial -out certs/client.cert.pem -days 365 -sha256 \
  -extfile openssl-ca.cnf -extensions client_cert
```

#### Example `[ client_cert ]` Section in Config File

```ini
[ client_cert ]
basicConstraints = CA:FALSE
keyUsage = digitalSignature
extendedKeyUsage = clientAuth
subjectAltName = email:alice@example.com
```

---

## 4. Why Separate CA, Server, and Client Certificates?

- **Security:** The CA private key should be kept offline and used only to sign CSRs. Never use the CA key for server or client authentication.
- **Trust:** Server and client certificates are used for different roles and should have different extensions (serverAuth vs clientAuth).
- **Revocation:** If a server or client key is compromised, you can revoke just that certificate, not the CA or all certs.
- **Best Practice:** Always use separate keys and certificates for CA, server, and client.

---

## 5. What is mTLS (Mutual TLS)?

- **mTLS** is a protocol where both the server and the client present certificates to authenticate each other.
- **Server certificate:** Proves the server's identity to the client (as in HTTPS).
- **Client certificate:** Proves the client's identity to the server (used in secure APIs, VPNs, etc.).
- **Why use mTLS?**
  - Strong, mutual authentication
  - Prevents unauthorized access even if passwords are leaked
  - Common in secure internal systems, APIs, and zero-trust networks

---

## Summary

- Create a private CA with a config file for proper extensions.
- Generate and sign separate server and client certificates.
- Use mTLS for strong, mutual authentication between client and server.
