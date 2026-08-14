## Collection of APIs for home automation

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Quickstart

### 1. Install dependencies with uv

From the project root:

```bash
uv sync
```

This installs all dependencies from `pyproject.toml` into a virtual environment. Use `uv run` to run commands in that environment.

### 2. Create an `.env` file

Create a file named `.env` in the project root (use .env.example as reference)

**Required variables:**

| Variable | Description |
|----------|-------------|
| `WA_PHONE_ID` | WhatsApp Business API phone number ID |
| `WA_TOKEN` | WhatsApp Business API access token |
| `PAPERLESS_WEBHOOK_TOKEN` | Webhook token expected from paperless ngx |
| `PAPERLESS_NOTIFICATION_NUMBERS` | List of WA Numbers to notify |

### 3. Run the project

Start the FastAPI app in development mode:

```bash
uv run fastapi dev
```

The server will start (default: http://127.0.0.1:7000).
