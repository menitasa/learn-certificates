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