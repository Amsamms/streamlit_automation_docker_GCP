# ── Dockerfile ───────
# 1. Base image
FROM python:3.11-slim

# 2. Install system deps for Chrome / Selenium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget gnupg ca-certificates \
        fonts-liberation libasound2 libglib2.0-0 libnss3 \
        libx11-6 libxext6 libxdamage1 libxcomposite1 libxrandr2 \
        libxfixes3 libxcursor1 libxinerama1 libpango-1.0-0 && \
    # Google Chrome stable
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
        gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] \
        http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy code
COPY streamlit_app_monitor.py .

# 5. Default command – container exits when script finishes
ENTRYPOINT ["python", "streamlit_app_monitor.py"]
