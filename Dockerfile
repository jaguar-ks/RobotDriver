FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

# Minimal Playwright-based image: copy app, install Python deps, run uvicorn
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY . /app

EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

