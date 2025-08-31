FROM python:3.11-slim-bookworm

# System deps (optional but helps with some wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \ 
    && PIP_REQUIRE_HASHES=0 pip install --no-cache-dir -r requirements.txt


COPY app ./app

EXPOSE 8000
# Start the API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]