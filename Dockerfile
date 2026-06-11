# Quran Root Explorer — web build
# Designed for Hugging Face Spaces (Docker SDK) but runs on any host that
# can build and run a Linux container (Render, Fly.io, Railway, VPS, etc.).

FROM python:3.11-slim

# ─── System dependencies ────────────────────────────────────────────────
# chromium       — required by kaleido (Plotly) to render PNG/PDF
# fonts-noto-*   — Arabic + Persian + Urdu glyph coverage in exported PNGs
# libnss3 etc.   — chromium runtime libs that 'slim' images omit
RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium \
        fonts-noto \
        fonts-noto-core \
        fonts-noto-extra \
        fonts-noto-cjk \
        fonts-noto-color-emoji \
        libnss3 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libgbm1 \
        libpango-1.0-0 \
        libcairo2 \
        libasound2 \
        ca-certificates \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Tell kaleido where Chromium lives so it doesn't try to download its own
ENV KALEIDO_EXECUTABLE_PATH=/usr/bin/chromium
ENV CHROME_BIN=/usr/bin/chromium

# ─── App ────────────────────────────────────────────────────────────────
WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# HF Spaces requires the container to run as a non-root user (uid 1000).
# /data is where analytics.py writes its SQLite DB; create + chown so the
# non-root user can write to it.
RUN useradd -m -u 1000 user \
    && mkdir -p /data \
    && chown -R user:user /app /data
USER user

# HF Spaces routes external traffic to port 7860
EXPOSE 7860

# Headless flags so Streamlit doesn't try to open a browser inside the container
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV ANALYTICS_DATA_DIR=/data

CMD ["streamlit", "run", "app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
