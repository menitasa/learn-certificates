# Lab 1: Basic SSL/TLS Web Server

## Purpose

This lab teaches you how to create, configure, and use SSL/TLS certificates to secure a web server. You'll gain hands-on experience with certificate creation, HTTPS setup, and troubleshooting.

## Learning Outcomes

By the end of this lab, you will be able to:

- Generate private keys and self-signed certificates
- Understand the certificate creation process and its fields
- Set up a basic HTTPS server
- Recognize and resolve common certificate issues
- Test and inspect SSL/TLS connections
- Experiment with certificate and server configurations

## Time Required

- Setup: 10-15 minutes
- Lab completion: 20-30 minutes
- Optional exercises: 15-20 minutes

## Prerequisites

Before starting, verify you have:

1. OpenSSL installed:

   ```sh
   openssl version
   # Should show something like: OpenSSL 1.1.1 or higher
   ```

2. Python 3.x installed:

   ```sh
   python3 --version
   # Should show Python 3.7 or higher
   ```

3. A modern web browser (Chrome, Firefox, Safari, or Edge)

## Step-by-Step Instructions

### Step 1: Create Lab Environment

**Why?** Organizing your files makes the lab easier to follow and troubleshoot.

1. Create the lab directory structure:

   ```sh
   # Create main lab directory
   mkdir ssl-webserver-lab
   cd ssl-webserver-lab

   # Create subdirectories
   mkdir certs   # For certificates
   mkdir www     # For web files
   ```

2. Verify the structure:
   ```sh
   ls
   # Should show: certs/ www/
   ```

### Step 2: Generate SSL Certificate

**Why?** Certificates are the foundation of HTTPS. You'll create your own to understand the process.

1. Generate a private key:

   ```sh
   openssl genrsa -out certs/server.key 2048
   ```

   - This creates a 2048-bit RSA private key
   - **Keep this file secure** – it's your server's private key

2. Create a certificate signing request (CSR):

   ```sh
   openssl req -new -key certs/server.key -out certs/server.csr \
       -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
   ```

   **Explanation:**

   - `-subj` lets you fill in certificate fields non-interactively.
   - C: Country (2-letter code)
   - ST: State/Province
   - L: City/Locality
   - O: Organization
   - CN: Common Name (your domain – we use localhost for testing)

   > **What If?**
   > If you forget `-subj`, OpenSSL will prompt you interactively for each field.

3. Generate self-signed certificate:

   ```sh
   openssl x509 -req -days 365 -in certs/server.csr \
       -signkey certs/server.key -out certs/server.crt
   ```

   - Valid for 365 days
   - Signed with your private key
   - **Self-signed** (not recommended for production)

4. Verify the certificate:

   ```sh
   openssl x509 -in certs/server.crt -text -noout
   ```

   Look for:

   - Validity period
   - Subject information
   - Public key details

   > **What If?**
   > If you see errors, check that the file paths are correct and that you have permission to read the files.

### Step 3: Create Web Content

**Why?** You need a web page to serve over HTTPS.

1. Create a basic HTML file:
   ```sh
   cat > www/index.html << 'EOF'
   <!DOCTYPE html>
   <html>
   <head>
       <title>SSL Lab - Secure Website</title>
       <style>
           body {
               font-family: Arial;
               max-width: 800px;
               margin: 40px auto;
               padding: 20px;
           }
           .secure {
               background: #e8f5e9;
               padding: 20px;
               border-radius: 5px;
           }
       </style>
   </head>
   <body>
       <div class="secure">
           <h1>🔒 Secure Connection Established!</h1>
           <p>This page is being served over HTTPS using your self-signed certificate.</p>
       </div>
       <h2>What's Happening?</h2>
       <ul>
           <li>The connection is encrypted</li>
           <li>The certificate is self-signed</li>
           <li>Your browser shows a security warning (expected)</li>
       </ul>
   </body>
   </html>
   EOF
   ```

### Step 4: Create HTTPS Server

**Why?** This server will use your certificate to serve content securely.

1. Create the Python server script:

   ```sh
   cat > server.py << 'EOF'
   import http.server
   import ssl

   # Server configuration
   server_address = ('localhost', 4443)
   httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

   # SSL/TLS configuration
   ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
   ssl_context.load_cert_chain('certs/server.crt', 'certs/server.key')
   httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

   print(f'Starting HTTPS server on https://localhost:4443')
   print('Press Ctrl+C to stop the server')
   httpd.serve_forever()
   EOF
   ```

### Step 5: Run the Server

1. Change to the www directory:

   ```sh
   cd www
   ```

2. Start the HTTPS server:

   ```sh
   python3 ../server.py
   ```

   You should see:

   ```
   Starting HTTPS server on https://localhost:4443
   Press Ctrl+C to stop the server
   ```

   > **What If?**
   > If you get a permission error, make sure you're not trying to use a privileged port (below 1024) without sudo.

### Step 6: Test the Connection

1. Open your web browser and navigate to:

   ```
   https://localhost:4443
   ```

2. Handle the security warning:

   - You'll see a warning because the certificate is self-signed
   - Click "Advanced" or "More Information"
   - Click "Proceed" or "Accept the Risk"

3. Examine the certificate:

   - Click the padlock icon in your browser
   - View certificate details
   - Verify the information matches what you entered

   > **What If?**
   > If you can't connect, check that the server is running and you're using https (not http).

### Step 7: Test with OpenSSL and curl

1. In a new terminal, test the SSL/TLS connection:

   ```sh
   openssl s_client -connect localhost:4443
   ```

   Look for:

   - Certificate chain
   - Server certificate details
   - SSL/TLS protocol version

2. Test with curl (ignore certificate validation):
   ```sh
   curl -k https://localhost:4443
   ```
   The `-k` flag tells curl to ignore certificate warnings (since it's self-signed).

## Understanding What Happened

1. **Certificate Creation**

   - Generated private key (server.key)
   - Created certificate request (server.csr)
   - Self-signed the certificate (server.crt)

2. **Server Setup**

   - Python server using SSL/TLS
   - Certificate and private key loaded
   - HTTPS enabled on port 4443

3. **Browser Interaction**
   - Warning due to self-signed certificate
   - Encrypted connection established
   - Certificate information available

## Common Issues and Solutions

1. **Certificate Problems**

   - Check file permissions
   - Verify certificate paths in server.py
   - Ensure CN=localhost in certificate
   - If browser says "Not Secure," check the certificate details

2. **Connection Refused**

   - Verify server is running
   - Check port 4443 is available
   - Confirm using https:// not http://
   - Try a different browser

3. **Python Issues**

   - Verify Python version
   - Check SSL module: `python3 -c "import ssl"`
   - Ensure proper working directory

4. **Browser Caching**
   - Try a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
   - Clear browser cache if you see old content

## Optional Exercises

1. **Create Different Certificates**

   - Try different subject fields (e.g., change CN, O, L)
   - Use different validity periods (e.g., 30 days, 730 days)
   - Generate multiple certificates and swap them in server.py

2. **Test Different Ports**

   - Modify the server port in server.py
   - Try standard HTTPS port (443) – requires sudo
   - Use random high ports (e.g., 8443, 10443)

3. **Add More Web Pages**

   - Create additional HTML files in www/
   - Add images or styles
   - Test different content types (e.g., .txt, .json)

4. **Test with Different Browsers and Devices**

   - Try accessing from another device on your network (update CN and use your IP)
   - Test with Chrome, Firefox, Safari, Edge

5. **Serve Multiple Files**

   - Add more files to www/ and access them via browser

## Suggested Variations

- Use a different key type (e.g., `openssl ecparam -genkey -name prime256v1 -out certs/server.key` for EC keys)
- Add Subject Alternative Names (SAN) to your certificate (requires a config file)
- Try using a different web server (e.g., Node.js, Nginx)
- Add HTTP headers for security (e.g., HSTS, Content-Security-Policy)

## Next Steps

After completing this lab:

1. Review certificate best practices
2. Learn about certificate authorities
3. Progress to Lab 2 (mTLS)
4. Explore production configurations

## Security Notes

Remember:

- Self-signed certificates are for testing only
- Production systems need trusted certificates
- Keep private keys secure
- Use appropriate key lengths
- Implement proper certificate management
