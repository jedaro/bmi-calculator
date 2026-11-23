# Quickstart: BMI Calculator API

## Prerequisites

- Python 3.12 or newer
- A shell with `python`/`python3.12` and `pip`
- SMTP account settings only if you want to exercise real email delivery

## Install and start

From the repository root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Version 1 is for local or classroom use only. **Do not expose this application to the public Internet.** Set the SMTP variables in `.env` only when testing email delivery. Keep real credentials out of source control. The application can calculate BMI when mail delivery is not configured.

Start the application:

```sh
uvicorn app.main:app --reload
```

Expected: the application starts at `http://127.0.0.1:8000`; API documentation is available at `/docs`, the browser interface at `/ui/`, and availability responses at `/` and `/health`.

## Validate calculation

```sh
curl -X POST http://127.0.0.1:8000/api/v1/bmi/calculate \
  -H 'Content-Type: application/json' \
  -d '{"weight":75,"height":1.75}'
```

Expected result includes `weight: 75`, `height: 1.75`, `bmi: 24.49`, and `category: "Peso normal"`.

## Validate email delivery

Configure a working SMTP host, port, security mode, sender, and any required credentials in `.env`, then submit:

```sh
curl -X POST http://127.0.0.1:8000/api/v1/bmi/send-email \
  -H 'Content-Type: application/json' \
  -d '{"email":"person@example.com","weight":75,"height":1.75}'
```

Expected: an `accepted` response only after the SMTP server accepts the message for delivery. This does not confirm inbox receipt. Invalid input returns a validation error; missing mail configuration or delivery failure is reported without revealing secrets.

## Run automated tests

With the virtual environment active:

```sh
pytest
```

Expected: calculation, category, validation, API, and email behavior are tested; the email tests use a mock and do not require a live SMTP server.

## Browser smoke check

Open `http://127.0.0.1:8000/ui/`. Calculate with `75` kg and `1.75` m and verify `24.49` / `Peso normal`. Change a measurement and verify email submission becomes unavailable until recalculation. With SMTP configured, send the result and verify the success or understandable failure message.
