# BMI Calculator API

## Scope

This application is intended for local or classroom use only. Do not expose it to the public Internet.

## Setup

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

BMI calculations work without SMTP configuration.

## Run

```sh
uvicorn app.main:app --reload
```

- Browser interface: `http://127.0.0.1:8000/ui/`
- API documentation: `http://127.0.0.1:8000/docs`
- API availability: `GET http://127.0.0.1:8000/`
- Health check: `GET http://127.0.0.1:8000/health`

## API operations

### Calculate BMI

`POST /api/v1/bmi/calculate`

```json
{"weight":75,"height":1.75}
```

### Send BMI result

`POST /api/v1/bmi/send-email`

```json
{"email":"person@example.com","weight":75,"height":1.75}
```

Success means the SMTP server accepted the message for delivery. It does not confirm inbox receipt.

## SMTP configuration

Set the following variables in `.env`:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_SECURITY`: `starttls` or `ssl`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_SENDER`
- `SMTP_TIMEOUT_SECONDS`

Keep real credentials out of source control.

## Tests

```sh
.venv/bin/python -m pytest
```

The test suite mocks SMTP delivery and does not require a real mail server.
