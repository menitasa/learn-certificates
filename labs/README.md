# SSL/TLS Certificate Labs

This directory contains hands-on labs for learning about SSL/TLS certificates, secure communications, and authentication. The labs are designed to be completed in sequence, with each lab building upon concepts from the previous ones.

## Lab Structure

### Lab 1: Basic SSL/TLS Web Server

- Create and use self-signed certificates
- Set up a basic HTTPS web server
- Understand certificate warnings and validation
- Located in: `ssl-webserver-lab/`

### Lab 2: Mutual TLS (mTLS) Authentication

- Create a Certificate Authority (CA)
- Generate and sign server/client certificates
- Implement mutual TLS authentication
- Located in: `mtls-lab/`

## Prerequisites

Before starting the labs, ensure you have:

1. OpenSSL installed

   ```sh
   # Check OpenSSL version
   openssl version
   ```

2. Python 3.x installed

   ```sh
   # Check Python version
   python3 --version
   ```

3. Basic command line knowledge
4. A text editor
5. A modern web browser

## Getting Started

1. Start with Lab 1 (`ssl-webserver-lab/`)

   - Learn basic certificate creation
   - Understand HTTPS server setup
   - See how browsers handle certificates

2. Progress to Lab 2 (`mtls-lab/`)
   - Build upon Lab 1 knowledge
   - Learn about certificate authorities
   - Implement mutual authentication

## Lab Files Structure

Each lab contains:

- A detailed README/guide
- Source code files
- Configuration examples
- Sample web pages
- Certificate directories

## Tips for Success

1. **Read First, Type Later**

   - Read through each lab guide completely before starting
   - Understand the objectives and expected outcomes

2. **Follow Sequential Steps**

   - Don't skip steps
   - Complete prerequisites before starting

3. **Troubleshooting**

   - Each lab includes troubleshooting sections
   - Common issues and solutions are documented

4. **Experimentation**
   - After completing a lab, try modifying parameters
   - Experiment with different configurations
   - Break things and fix them to learn

## Learning Objectives

After completing these labs, you should understand:

1. How SSL/TLS certificates work
2. Certificate creation and signing
3. Server and client authentication
4. Security best practices
5. Real-world implementation scenarios

## Need Help?

- Check the troubleshooting sections in each lab
- Verify your OpenSSL and Python installations
- Ensure proper file permissions
- Double-check file paths and commands

## Next Steps

After completing these labs, consider:

1. Implementing in production environments
2. Exploring advanced certificate features
3. Setting up certificate rotation
4. Adding security headers
5. Implementing certificate revocation
