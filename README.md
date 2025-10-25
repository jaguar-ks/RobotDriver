# RobotDriver — SauceDemo Automation API

Small FastAPI service that uses Playwright to log into [suacedemo](https://www.saucedemo.com/) and return product prices.

## Navigation table

1. [Contents](#contents)
1. [Prerequisites](#prerequisites)
1. [Setup](#setup)
1. [Run the API](#run-the-api)
1. [Endpoint](#endpoint)

## Contents

```bash
RobotDriver
├── README.md
├── SauceDemo.py #Automation script using Playwright
├── main.py #FastAPI app exposing '/run' endpoint
└── requirements.txt #Python dependencies
```

## Prerequisites

- Python 3.9+
- Linux environment (commands shown use POSIX shell)
- Network access to `https://www.saucedemo.com/`

## Setup

1. Clone or copy project to your machine:

    ```bash
    git clone https://github:jagur-ks/RobotDriver.git
    ```

1. Create and activate virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

1. Install Python dependencies:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

1. Install Playwright browsers:

    ```bash
    playwright install
    ```

## Run the API

Start the FastAPI server (development mode):

```bash
uvicorn main:app --reload --port 8000
```

The service will be available at `http://localhost:8000`.

## Endpoint

`GET /run`

Query parameter:

- `product` (required) — exact product name (example: `Sauce Labs Backpack`)

Example:

```bash
curl "http://localhost:8000/run?product=Sauce%20Labs%20Backpack"
```

Successful response (HTTP 200):

```json
{
  "status": "success",
  "details": "✅ Product (Sauce Labs Backpack) found! with price: $29.99"
}
```

Product not found (HTTP 404):

```json
{
  "status": "Error",
  "details": "❌ Failed!: product (Sauce Labs Bac) not found."
}
```

Server error (HTTP 500) includes exception class and message.
