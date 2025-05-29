# Certificate Cheat Sheet: Useful Commands

A quick reference for common OpenSSL and certificate-related commands. Use these to view, test, convert, and troubleshoot certificates and keys.

---

## 1. View Certificate Details

```sh
openssl x509 -in cert.pem -noout -text
```

- Shows all details of a certificate (subject, issuer, extensions, validity, etc.).

---

## 2. View CSR (Certificate Signing Request) Details

```sh
openssl req -in request.csr.pem -noout -text
```

- Shows the subject and requested extensions in a CSR.

---

## 3. View Private Key Details

```sh
openssl rsa -in private.key -check -noout -text
```

- Shows details of an RSA private key.

---

## 4. Check if a Private Key Matches a Certificate

```sh
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5
```

- The output hashes should match if the key and certificate belong together.

---

## 5. Test a Certificate Chain (with CA Bundle)

```sh
openssl verify -CAfile ca-bundle.pem cert.pem
```

- Verifies that a certificate is valid and trusted by the given CA bundle.

---

## 6. Test a TLS Connection to a Server

```sh
openssl s_client -connect example.com:443 -showcerts
```

- Connects to a server, shows the certificate chain and connection details.

---

## 7. Convert Certificate Formats

- **PEM to DER:**
  ```sh
  openssl x509 -in cert.pem -outform der -out cert.der
  ```
- **DER to PEM:**
  ```sh
  openssl x509 -in cert.der -inform der -out cert.pem
  ```
- **PEM to PKCS#12 (bundle cert and key):**
  ```sh
  openssl pkcs12 -export -out bundle.p12 -inkey private.key -in cert.pem -certfile ca-bundle.pem
  ```
- **PKCS#12 to PEM:**
  ```sh
  openssl pkcs12 -in bundle.p12 -out extracted.pem -nodes
  ```
- **PKCS#8 to PKCS#1 (RSA key format):**
  ```sh
  openssl rsa -in pkcs8.key -out pkcs1.key
  ```

---

## 8. Check Certificate Expiry Date

```sh
openssl x509 -enddate -noout -in cert.pem
```

- Shows the expiration date of a certificate.

---

## 9. Print Only the Subject or Issuer

```sh
openssl x509 -in cert.pem -noout -subject
openssl x509 -in cert.pem -noout -issuer
```

---

## 10. Decode a Base64 Certificate (PEM) to Human-Readable

```sh
cat cert.pem | openssl x509 -noout -text
```

---

## 11. Check a Certificate Revocation List (CRL)

```sh
openssl crl -in crl.pem -noout -text
```

---

## 12. Generate a Random Password (for key encryption)

```sh
openssl rand -base64 32
```

---

## 13. Troubleshoot TLS/SSL on a Remote Server

```sh
openssl s_client -connect example.com:443 -servername example.com
```

- Use `-servername` for SNI (Server Name Indication) support.

---

**Tip:** For more help, run `openssl <command> -help` or check the OpenSSL documentation.
