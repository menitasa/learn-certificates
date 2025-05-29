# Mutual TLS (mTLS) Authentication Lab

## Purpose

This lab teaches you how to set up mutual TLS (mTLS) authentication, where both the server and client must present valid certificates. This is a critical skill for securing APIs, microservices, and internal systems.

## Learning Outcomes

By the end of this lab, you will be able to:

- Create and operate a Certificate Authority (CA)
- Generate and sign server and client certificates
- Configure a server to require client authentication
- Write a client that presents its certificate
- Troubleshoot mTLS issues
- Understand real-world mTLS use cases

---

This lab demonstrates how to set up mutual TLS authentication, where both the server and client need valid certificates to establish a connection. This is commonly used in:

- Microservices authentication
- API security
- IoT device authentication
- Zero-trust environments

## Prerequisites

- Completed Lab 1 (Basic SSL/TLS Web Server)
- OpenSSL installed
- Python 3.x
- Basic understanding of PKI concepts

---

## Lab Overview

In this lab, you will:

1. Create a Certificate Authority (CA)
2. Generate server certificate signed by your CA
3. Generate client certificate signed by your CA
4. Set up an HTTPS server that requires client certificates
5. Create a client script that presents its certificate
6. Test mutual authentication

---

## Step-by-Step Instructions

### 1. Set Up Directory Structure

**Why?** Keeping CA, server, and client files separate avoids confusion and makes troubleshooting easier.

```sh
mkdir mtls-lab
cd mtls-lab
mkdir ca
mkdir server
mkdir client
```

### 2. Create Certificate Authority (CA)

**Why?** The CA is the trust anchor. All certificates must chain up to this root.

```sh
# Generate CA private key
openssl genrsa -out ca/ca.key 4096

# Create CA certificate
openssl req -new -x509 -days 365 -key ca/ca.key -out ca/ca.crt \
    -subj "/C=US/ST=State/L=City/O=MyLabCA/CN=Lab Certificate Authority"
```

- The CA certificate is self-signed and will be used to sign both server and client certificates.

> **What If?**
> If you lose the CA key, you cannot sign new certificates or revoke old ones.

### 3. Create Server Certificate

**Why?** The server needs a certificate signed by the CA to prove its identity.

```sh
# Generate server private key
openssl genrsa -out server/server.key 2048

# Create server CSR
openssl req -new -key server/server.key -out server/server.csr \
    -subj "/C=US/ST=State/L=City/O=MyLabServer/CN=localhost"

# Sign server certificate with CA
openssl x509 -req -days 365 -in server/server.csr \
    -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out server/server.crt
```

- The server certificate is now trusted by your CA.

### 4. Create Client Certificate

**Why?** The client must also prove its identity to the server.

```sh
# Generate client private key
openssl genrsa -out client/client.key 2048

# Create client CSR
openssl req -new -key client/client.key -out client/client.csr \
    -subj "/C=US/ST=State/L=City/O=MyLabClient/CN=labclient"

# Sign client certificate with CA
openssl x509 -req -days 365 -in client/client.csr \
    -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out client/client.crt
```

- The client certificate is now trusted by your CA.

> **What If?**
> If you use the wrong CA or an expired certificate, authentication will fail.

### 5. Create HTTPS Server with Client Authentication

**Why?** The server must require and validate client certificates for mTLS.

Create `server/server.py`:

```python
import http.server
import ssl

class MTLSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Access client certificate information
        cert = self.connection.getpeercert()

        # Log client certificate details
        print("\nClient Certificate Details:")
        if cert:
            for field in cert.get('subject', []):
                print(f"  {field[0][0]}: {field[0][1]}")

        # Serve the request
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Server configuration
server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, MTLSHandler)

# SSL/TLS configuration with client authentication
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_verify_locations('../ca/ca.crt')
ssl_context.load_cert_chain('../server/server.crt', '../server/server.key')

# Wrap socket with SSL/TLS
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print(f'Starting HTTPS server with mTLS on https://localhost:4443')
print('Press Ctrl+C to stop the server')
httpd.serve_forever()
```

- The server will only accept clients with valid certificates signed by your CA.

### 6. Create Test Client

**Why?** The client must present its certificate and validate the server's certificate.

Create `client/client.py`:

```python
import urllib.request
import ssl
import json

def print_certificate_info(cert):
    """Print formatted certificate information"""
    print("\nServer Certificate Details:")
    if cert:
        for key, value in cert.items():
            if key == 'subject' or key == 'issuer':
                print(f"\n{key.title()}:")
                for field in value:
                    print(f"  {field[0][0]}: {field[0][1]}")
            elif key == 'notBefore' or key == 'notAfter':
                print(f"{key}: {value}")

# Create SSL context with client certificate
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('../ca/ca.crt')
context.load_cert_chain('../client/client.crt', '../client/client.key')
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

# Make HTTPS request
try:
    print("Attempting to connect to server with mTLS...")
    response = urllib.request.urlopen(
        'https://localhost:4443',
        context=context
    )

    # Get and print server certificate info
    server_cert = response.fp.raw._sock.getpeercert()
    print_certificate_info(server_cert)

    # Print response
    print("\nServer Response:")
    print(response.read().decode())
    print("\nConnection successful! Mutual TLS authentication worked.")

except ssl.SSLError as e:
    print(f"\nSSL Error: {e}")
    print("This might be due to:")
    print("- Invalid client certificate")
    print("- Server not recognizing our CA")
    print("- Certificate expired")

except ConnectionRefusedError:
    print("\nConnection refused. Is the server running?")

except Exception as e:
    print(f"\nError: {e}")
```

- The client will only connect if the server presents a valid certificate and the client's certificate is accepted.

### 7. Test the Setup

1. Start the server:

```sh
python3 server/server.py
```

2. In a new terminal, run the client:

```sh
python3 client/client.py
```

3. Try without client certificate (should fail):

```sh
curl https://localhost:4443
```

4. Try with client certificate:

```sh
curl --cacert ca/ca.crt \
     --cert client/client.crt \
     --key client/client.key \
     https://localhost:4443
```

---

## Understanding What Happened

1. **CA Creation**
   - You created a root of trust for your environment.
2. **Certificate Signing**
   - Both server and client certificates are signed by your CA.
3. **mTLS Enforcement**
   - The server only accepts clients with valid certificates.
   - The client only connects to trusted servers.

---

## Common Issues and Solutions

1. **Certificate Issues**

   - Verify all certificates are signed by the CA
   - Check certificate dates and CN values
   - Ensure proper file permissions on keys
   - If you see `ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`, check CA paths and certificate validity

2. **Connection Issues**

   - Verify server is running
   - Check if certificates are in the correct locations
   - Ensure all paths in scripts are correct
   - Try a different port if 4443 is in use

3. **Python Issues**

   - Check SSL module availability
   - Verify Python version compatibility
   - Check for proper SSL context configuration

4. **Client/Server Mismatch**
   - Make sure both use the same CA
   - Check for typos in file paths

---

## Optional Exercises

1. **Create More Clients**

   - Generate additional client certificates and test with them
   - Try connecting with an invalid or expired certificate

2. **Change Certificate Fields**

   - Use different CNs or O fields for clients and servers
   - See how the server logs different client identities

3. **Test with curl and browsers**

   - Use curl with and without certificates
   - Try importing the CA and client certificate into your browser and access the server

4. **Add Certificate Revocation**

   - Research and implement a simple CRL (Certificate Revocation List)

5. **Experiment with Certificate Expiry**

   - Create a certificate with a short validity and test what happens when it expires

6. **Try Different Key Types**
   - Use EC keys instead of RSA

---

## Suggested Variations

- Add Subject Alternative Names (SAN) to certificates
- Use different ports or hostnames
- Implement certificate pinning in the client
- Add more detailed logging to the server
- Try using a different programming language for the client or server

---

## Security Notes

1. In production:

   - Never share private keys
   - Use strong passwords for private keys
   - Implement proper certificate revocation
   - Use appropriate key lengths and algorithms

2. Best Practices:
   - Rotate certificates regularly
   - Implement certificate pinning
   - Monitor certificate expiration
   - Use secure key storage

---

## Next Steps

- Implement certificate revocation checking
- Add certificate pinning
- Create a certificate rotation process
- Implement programmatic certificate generation
- Add more security headers and configurations
