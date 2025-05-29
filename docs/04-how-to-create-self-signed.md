# How to Create a Self-Signed Certificate

A self-signed certificate is a certificate that is signed with its own private key, rather than by a Certificate Authority (CA). This is useful for testing, development, or internal use where trust is managed manually.

---

## 1. Generate a Private Key

```sh
openssl genrsa -out selfsigned-key.pem 2048
```

- This creates a 2048-bit RSA private key and saves it to `selfsigned-key.pem`.

---

## 2. Create a Self-Signed Certificate

You can create a self-signed certificate by providing the subject attributes that identify the certificate owner. These attributes include:

- **C** = Country (2-letter code, e.g., US)
- **ST** = State or Province (e.g., California)
- **L** = Locality or City (e.g., San Francisco)
- **O** = Organization (e.g., Example Corp)
- **OU** = Organizational Unit (e.g., IT Department)
- **CN** = Common Name (e.g., myserver.local)
- **emailAddress** = Email address (optional)

### Option 1: Interactive Prompt

If you omit the `-subj` flag, OpenSSL will prompt you to enter each attribute:

```sh
openssl req -new -x509 -key selfsigned-key.pem -out selfsigned-cert.pem -days 365
```

You will see prompts like:

```
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
```

### Option 2: Provide All Attributes with -subj

You can specify all attributes in one line using the `-subj` flag:

```sh
openssl req -new -x509 -key selfsigned-key.pem -out selfsigned-cert.pem -days 365 \
  -subj "/C=US/ST=California/L=San Francisco/O=Example Corp/OU=IT Department/CN=myserver.local/emailAddress=admin@example.com"
```

- This creates a self-signed certificate valid for 365 days, using the private key and the subject attributes you provide.
- The certificate is saved as `selfsigned-cert.pem`.

---

## 3. Extract the Public Key from the Private Key

```sh
openssl rsa -in selfsigned-key.pem -pubout -out selfsigned-pubkey.pem
```

- This command extracts the public key from the private key and saves it to `selfsigned-pubkey.pem`.

### Why Can You Extract the Public Key from the Private Key?

- In asymmetric cryptography (like RSA), the private key contains all the information needed to derive the public key.
- The public key is mathematically related to the private key, but not vice versa (you cannot derive the private key from the public key).
- This allows you to:
  - Share the public key freely (for encryption or verification)
  - Keep the private key secret (for decryption or signing)

### When Would You Extract the Public Key?

- To distribute your public key for others to verify signatures or encrypt data for you.
- To use the public key in systems that require it separately (e.g., SSH, JWT, or certificate pinning).

---

## Summary

- Generate a private key.
- Create a self-signed certificate with that key.
- Extract the public key from the private key if needed for other uses.
