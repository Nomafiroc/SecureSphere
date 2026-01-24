# SecureSphere

SecureSphere is a "Shift Left" security tool designed to automate vulnerability detection within the development workflow. By integrating security gates into both the local environment and the CI/CD pipeline, it ensures that security is an automated requirement rather than a manual bottleneck.

# SecureSphere Technology Stack

Languages: Python

DevOps: Docker

Security: Bandit (SAST)

CI/CD: GitHub Actions

Version Control: Git & GitHub (with Branch Protection)

# Implemented Features

1. Automated Security Gates

  - Local Enforcement: Implemented pre-commit hooks to run security checks locally before code is even committed to the repository.

  - CI/CD Pipeline: Developed a GitHub Actions workflow (post_update.yml) that triggers automatically on pushes and pull requests to the main branch.

  - Mandatory Branch Protection: Configured GitHub Branch Protection rules to block any merge that fails the security audit.

2. Security Scanning

  - Static Analysis (SAST): Integrated a containerized Bandit engine to perform deep scans of Python source code for security risks like insecure functions (eval()) or hardcoded secrets.

4. Hardened Infrastructure

  - Dockerized Environment: Shifted the scanning engine from a local Python environment to an isolated non-root Docker container (python:3.11-slim) to ensure environment parity and security.

# Local Usage

  To build and run the security scanner locally using the hardened Docker image:

```
# Build the scanner image
docker build -t securesphere-scanner .

# Execute the scan
docker run securesphere-scanner
```

# Final Project Status
SAST: Active and Gated.

Environment: Fully Containerized.

CI/CD: Fully Automated with Branch Protection.
