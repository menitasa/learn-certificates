# Web Server SSL/TLS Lab

This lab will guide you through setting up a secure web server with SSL/TLS certificates. You'll learn how to:

1. Create and configure certificates
2. Set up a basic web server
3. Configure SSL/TLS
4. Test and verify the secure connection

## Prerequisites

- OpenSSL installed
- Python 3.x (for running a simple web server)
- A modern web browser
- Basic command line knowledge

## Lab Steps

### 1. Create Working Directory

```sh
mkdir ssl-webserver-lab
cd ssl-webserver-lab
mkdir certs
mkdir www
```

### 2. Create SSL Certificate

First, create a self-signed certificate for your local web server:

```sh
# Generate private key
openssl genrsa -out certs/server.key 2048

# Create CSR (Certificate Signing Request)
openssl req -new -key certs/server.key -out certs/server.csr \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -days 365 -in certs/server.csr \
    -signkey certs/server.key -out certs/server.crt
```

### 3. Create Simple Web Page

Create a test HTML file in the www directory:

```sh
echo "<html><body><h1>SSL Lab - Secure Website</h1><p>This page is served over HTTPS!</p></body></html>" > www/index.html
```

### 4. Set Up Python HTTPS Server

Create a Python script for the HTTPS server (`server.py`):

```python
import http.server
import ssl

server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# SSL/TLS configuration
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print(f'Starting HTTPS server on https://localhost:4443')
httpd.serve_forever()
```

### 5. Start the Server

```sh
# Change to www directory
cd www

# Start the HTTPS server
python3 ../server.py
```

### 6. Test the Connection

1. Open your web browser and navigate to:

   ```
   https://localhost:4443
   ```

2. You'll see a security warning (because we're using a self-signed certificate)

   - Click "Advanced" or "More Information"
   - Click "Proceed" or "Accept the Risk"

3. You should now see your secure webpage!

### 7. Verify Certificate (Optional)

In a new terminal, test the SSL/TLS connection:

```sh
openssl s_client -connect localhost:4443
```

This will show the certificate details and SSL/TLS connection information.

## Learning Objectives

After completing this lab, you should understand:

- How to create and use SSL certificates
- Basic HTTPS server setup
- How certificates are presented to browsers
- How to verify SSL/TLS connections

## Troubleshooting

1. **Certificate Issues**

   - Ensure the certificate's Common Name (CN) matches 'localhost'
   - Check file permissions on the certificate and key files

2. **Connection Refused**

   - Verify the server is running
   - Check if port 4443 is available
   - Ensure you're using HTTPS, not HTTP

3. **Python Issues**
   - Verify Python 3.x is installed: `python3 --version`
   - Check if SSL module is available: `python3 -c "import ssl"`

## Next Steps

- Try creating a certificate with different attributes
- Add more HTML pages and test serving multiple secure pages
- Experiment with different SSL/TLS configurations
- Set up client certificates for mutual TLS authentication
