# Step 1: Use a secure, slim Python base
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# 1. Patch OS Vulnerabilities (Fixes libc6 / libc-bin)
# We update the package list and upgrade existing libraries
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 2. Patch Python Tooling (Fixes wheel / jaraco.context)
# Upgrading pip and wheel often resolves secondary dependency CVEs
RUN pip install --no-cache-dir --upgrade pip wheel bandit

# Step 3: Install Bandit directly
# This avoids needing a requirements.txt just for the scanner
# RUN pip install --no-cache-dir bandit

# Step 4: Copy only the necessary project files
# .dockerignore will handle the exclusions
COPY . .

# Step 5: Security Best Practice - Create and use a non-root user
# This prevents the container from having admin rights if breached
RUN useradd -m securesphere
USER securesphere

# Step 6: Define the entry point
# We run bandit directly to ensure it works in the container environment
CMD ["bandit", "-r", ".", "--exclude", "./venv,./.venv,./env"]