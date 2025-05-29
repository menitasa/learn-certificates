# Certificate Subject Fields, Extensions, and OpenSSL Config Files

## Key Certificate Concepts

- **x509:**

  - The standard format for public key certificates used in TLS/SSL, HTTPS, and many other security protocols.
  - Defines the structure, fields, and extensions for certificates.

- **Subject:**

  - The entity the certificate represents (the owner).
  - For a server certificate, the subject is the server (e.g., a domain name).
  - For a client certificate, the subject is the user or device.
  - Shown in the certificate as fields like CN (Common Name), O (Organization), etc.

- **Issuer:**

  - The entity that signed and issued the certificate (usually a CA).
  - For a self-signed certificate, the issuer and subject are the same.
  - For a CA-signed certificate, the issuer is the CA.

- **Distinguished Name (DN):**

  - The full set of identifying fields for the subject or issuer (e.g., CN, O, C, etc.).

- **Serial Number:**

  - A unique number assigned by the issuer to each certificate.

- **Signature Algorithm:**

  - The cryptographic algorithm used by the issuer to sign the certificate.

- **Public Key Info:**

  - Contains the public key and its algorithm (e.g., RSA, EC) for the subject.

- **Extensions:**

  - Extra fields that define how the certificate can be used (e.g., SAN, EKU, Key Usage).

- **PEM:**
  - The most common file format for certificates and keys (base64-encoded, with headers like `-----BEGIN CERTIFICATE-----`).

## Certificate Subject Fields

When you create a certificate or a Certificate Signing Request (CSR), you provide information about the identity the certificate represents. These are the subject fields:

- **C (Country):**
  - Two-letter country code (e.g., US)
- **ST (State or Province):**
  - Full name of the state or province (e.g., California)
- **L (Locality or City):**
  - City or locality name (e.g., San Francisco)
- **O (Organization):**
  - Legal name of your organization or company (e.g., Example Corp)
- **OU (Organizational Unit):**
  - Department or division within your organization (e.g., IT Department)
  - Optional, often left blank
- **CN (Common Name):**
  - Primary domain name or identity for the certificate (e.g., myserver.local)
  - For server certificates, this should match the domain name users will connect to
- **emailAddress:**
  - Email address associated with the certificate (e.g., admin@example.com)
  - Optional, mostly used for personal or S/MIME certificates

## Certificate Extensions

Extensions add extra information and control how a certificate is used. Some are required for basic operation, others are optional or for special use cases.

### Basic/Required Extensions

- **Basic Constraints:**

  - Indicates if a certificate is a CA (Certificate Authority) or an end-entity (server/client).
  - Example: `CA:TRUE` for CA certificates, `CA:FALSE` for server/client certificates.
  - Required for CA certificates.

- **Key Usage:**

  - Specifies what cryptographic operations the key can be used for.
  - Common values:
    - `digitalSignature` (signing data, e.g., TLS handshake)
    - `keyEncipherment` (encrypting keys, e.g., in TLS)
    - `keyCertSign` (signing other certificates, for CAs)
    - `crlSign` (signing certificate revocation lists, for CAs)
  - Required for most certificates.

- **Subject Alternative Name (SAN):**
  - Lists additional identities for the certificate (DNS names, IPs, email addresses, URIs, etc.).
  - **Required for all modern server certificates** (browsers ignore CN for hostname matching).
  - For client certificates, SAN can include an email address or user name (as an `rfc822Name` or `otherName`) to identify/authenticate the user.
  - Example:
    - `DNS:myserver.local, DNS:www.myserver.local, email:alice@example.com, URI:spiffe://myorg/user/alice`

### Common/Recommended Extensions

- **Extended Key Usage (EKU):**

  - Specifies the intended purpose(s) of the certificate.
  - Most certificates include one or both of:
    - `serverAuth` (for TLS servers)
    - `clientAuth` (for TLS clients)
  - Others: `codeSigning`, `emailProtection`, `timeStamping`, etc.
  - **Why most certificates use clientAuth and serverAuth:**
    - Many certificates are used for mutual TLS (mTLS), where both client and server authenticate each other. Including both usages allows the same certificate to be used for either role.

- **Authority Key Identifier (AKI):**

  - Identifies the public key of the CA that signed the certificate.
  - Helps clients build the certificate chain.

- **Subject Key Identifier (SKI):**

  - Identifies the public key in the certificate.
  - Useful for certificate management and chain building.

- **CRL Distribution Points:**

  - Specifies where to find the Certificate Revocation List (CRL) for this certificate.
  - Important for revocation checking.

- **Authority Information Access (AIA):**

  - Provides information about the issuing CA, such as a URL to download the CA certificate or OCSP responder.

- **OCSP (Online Certificate Status Protocol) URL:**
  - Specifies where to check the revocation status of the certificate in real time.

### Other Useful Extensions

- **Email Protection:**
  - Used for S/MIME certificates to secure email.
- **Code Signing:**
  - Used for certificates that sign software or code.
- **Time Stamping:**
  - Used for certificates that sign timestamps.

## OpenSSL Config Files

OpenSSL config files let you define all these extensions in one place, making certificate creation more reliable and repeatable.

### Example: Minimal OpenSSL Config for a Server Certificate

```ini
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
req_extensions     = req_ext
distinguished_name = dn

[ dn ]
C  = US
ST = California
L  = San Francisco
O  = Example Corp
CN = myserver.local

[ req_ext ]
subjectAltName = @alt_names
extendedKeyUsage = serverAuth, clientAuth
keyUsage = digitalSignature, keyEncipherment
basicConstraints = CA:FALSE

[ alt_names ]
DNS.1 = myserver.local
DNS.2 = www.myserver.local
email.1 = alice@example.com
URI.1 = spiffe://myorg/user/alice
```

- The `[dn]` section defines the subject fields.
- The `[req_ext]` section defines extensions like SAN, EKU, keyUsage, and basicConstraints.
- The `[alt_names]` section lists all SAN entries, including email and URI entries for client authentication.

### Using the Config File with OpenSSL

To generate a CSR using this config file:

```sh
openssl req -new -key private/server.key.pem -out server.csr.pem -config openssl-server.cnf
```

To sign a certificate with extensions:

```sh
openssl x509 -req -in server.csr.pem -CA certs/ca.cert.pem -CAkey private/ca.key.pem \
  -CAcreateserial -out certs/server.cert.pem -days 365 -sha256 \
  -extfile openssl-server.cnf -extensions req_ext
```

## Key Points

- **Basic Constraints, Key Usage, and SAN** are essential for most certificates.
- **EKU** defines what the certificate can be used for (server, client, etc.).
- **SAN** is required for server certs and can be used for client/user identity.
- Other extensions help with revocation, chain building, and special uses.
