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