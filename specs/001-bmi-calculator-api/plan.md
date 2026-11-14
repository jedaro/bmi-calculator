# Implementation Plan: BMI Calculator API

**Branch**: `spec-feature` | **Date**: 2026-11-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-bmi-calculator-api/spec.md` and the supplied technical plan.

## Summary

Build a small, stateless BMI web service for local or classroom use, with a Spanish-language browser interface. A pure BMI service supplies the calculation and adult category; Pydantic schemas validate API input; a separate SMTP service sends the result only after an explicit request. Email success means the SMTP server accepted the message for delivery, not that it reached the recipient's inbox. FastAPI provides the calculation API, availability checks, static interface at `/ui/`, and API documentation at `/docs`. Automated tests cover service and HTTP behavior, with SMTP mocked.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: FastAPI, Pydantic, Uvicorn, python-dotenv, pytest, HTTPX, and `email-validator` for Pydantic `EmailStr`. SMTP and email message construction use Python's standard library.

**Storage**: None; calculations and email addresses are not retained.

**Testing**: Pytest; FastAPI `TestClient` backed by HTTPX; unit tests for calculation and email composition; endpoint tests with SMTP mocked.

**Target Platform**: Local development or a classroom demonstration; public Internet exposure is out of scope for version 1.

**Project Type**: Web service with a static browser interface.

**Performance Goals**: No throughput, concurrency, or latency target is specified; scope is an educational, interactive application.

**Constraints**: Preserve the constitution's modular `api`, `schemas`, `services`, `core`, and `tests` areas; require finite positive measurements; keep secrets in environment configuration; use secure SMTP transport; no authentication, database, or history. Version 1 is for local/classroom use only and MUST NOT be exposed to the public Internet. Keep `/` available as the requested API availability response; serve the browser interface at `/ui/` to avoid a route collision.

**Scale/Scope**: One BMI form, four API operations, one SMTP delivery flow, and no persistent data; local/classroom use only, without a public deployment or multi-user scale target.

## Constitution Check

### Before Phase 0

- **I. Correct and Informative BMI Calculation — PASS**: The specified formula, positive finite inputs, two-decimal display, adult category boundaries, and non-diagnostic notice are included.
- **II. Simple, Modular Architecture — PASS**: The proposed source layout separates API, schemas, business/email services, configuration, and tests; the calculation remains independent of HTTP handlers.
- **III. Established Technology Stack — PASS**: The design uses the mandated Python, FastAPI, Pydantic, Uvicorn, Pytest, HTML/CSS/JavaScript, SMTP, and python-dotenv stack. The additional `email-validator` package is justified by Pydantic's `EmailStr` support for the required email validation. `pydantic-settings` is omitted because a small environment configuration module does not need another settings dependency.
- **IV. Validated Interfaces and Safe Errors — PASS**: Requests are schema-validated; errors use explicit HTTP outcomes; SMTP credentials stay in environment variables and raw transport details are not returned to users.
- **V. Tested, Readable, Minimal Changes — PASS**: Tests cover required behavior and failures; no database, frontend framework, mail library, or unrelated dependency is introduced.
- **Additional Constraints — PASS**: Email is gated on a current valid result in the UI; calculation and email content are informational; SMTP settings and credentials are external to source.
- **Local-only v1 — PASS**: The specification explicitly excludes public Internet exposure; setup documentation will repeat this limit.

### Post-Design Gate

- The selected design retains the required project boundaries and avoids new infrastructure.
- The only added package beyond the supplied stack is `email-validator`, needed for robust address validation with `EmailStr`.
- The root availability response and UI path are separate to preserve both the requested `GET /` behavior and browser access.
- Email success is defined as SMTP acceptance; no inbox-delivery confirmation is promised.
- Version 1 is local/classroom-only; no public endpoint protections or deployment infrastructure are in scope.
- **Result: PASS.** No constitution exception or unresolved technical clarification remains.

## Project Structure

### Documentation (this feature)

```text
specs/001-bmi-calculator-api/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
app/
├── main.py
├── api/
│   └── endpoints/
│       ├── bmi.py
│       └── health.py
├── schemas/
│   ├── bmi.py
│   └── email.py
├── services/
│   ├── bmi_service.py
│   └── email_service.py
└── core/
    └── config.py

frontend/
├── index.html
├── styles.css
└── app.js

tests/
├── test_bmi_service.py
├── test_bmi_api.py
├── test_email_service.py
└── test_email_api.py

.env.example
.gitignore
README.md
requirements.txt
```

**Structure Decision**: Use the single-project web-service structure from the supplied plan, aligned with the constitution's responsibility areas. The calculation service is a pure, reusable module. `main.py` assembles the routers and mounts the static frontend at `/ui/`; `GET /` and `GET /health` remain API availability responses. Configuration is read in `core/config.py` using environment variables and python-dotenv for local development. No persistence or frontend build system is needed.

## Implementation Phases

1. **Setup and foundation**: Establish the source layout, dependencies, environment example, ignore rules, FastAPI application, test client, and `/docs`. Do not add availability routes or mount the browser interface in this phase.
2. **US1 — BMI calculation and result view**: Define validated input/output schemas, implement the independent formula and category service, expose `POST /api/v1/bmi/calculate`, build the calculation UI, and mount it at `/ui/`. Test boundaries and invalid values; email submission remains disabled until a current result exists.
3. **US2 — Email delivery**: Define the email request and response, compose the Spanish message from the shared BMI service, implement SMTP configuration and secure transport, and connect the UI. Report success only when SMTP accepts the message; do not imply inbox receipt. Test with SMTP mocks.
4. **US3 — Availability checks**: Add `GET /` and `GET /health` after the calculation and email stories, matching the P3 user-story priority.
5. **Integration and documentation**: Run all tests, verify the documented API flows and browser interaction, review error handling and secrets hygiene, and provide local/classroom setup and SMTP instructions in `README.md`.

## Interface and Error Decisions

- `GET /` returns an API availability response; `GET /health` reports operational status; the browser application is available at `/ui/`. These operations are for the local/classroom deployment only in v1.
- `POST /api/v1/bmi/calculate` returns the input weight and height, BMI rounded to two decimals, and the Spanish adult category.
- `POST /api/v1/bmi/send-email` accepts the recipient, weight, and height, recalculates through the shared BMI service, and reports `accepted` only after SMTP accepts the message for delivery. Neither the API nor UI claims confirmed inbox receipt.
- Invalid request data returns HTTP 422. Missing or incomplete mail configuration returns HTTP 503. SMTP connection or delivery failure returns HTTP 502 with a generic user-facing message; transport details and credentials are not included.
- Email is sent synchronously for this low-volume educational application with a finite connection timeout. The SMTP operation is kept out of the asynchronous event loop. SMTP-over-SSL or STARTTLS is selected explicitly in configuration; plaintext delivery is not supported.
- The API accepts a valid email request independently of prior browser state. The browser's send-button gate is UX state, not server-side history or persistence.
- Version 1 is not intended for public Internet exposure; the README and quickstart must state this limitation.

## Dependencies and Configuration

- Runtime: FastAPI, Uvicorn, python-dotenv, and `email-validator`; Pydantic is used through FastAPI's request model support.
- Development/test: Pytest and HTTPX for `TestClient`.
- Standard library: `smtplib`, `ssl`, and `email.message`.
- Do not add `pydantic-settings`; read the small, explicit SMTP configuration from the process environment after loading `.env` in development.
- `.env.example` documents `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURITY` (`starttls` or `ssl`), `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SENDER`, and `SMTP_TIMEOUT_SECONDS`. `.env` is ignored by Git; the example contains placeholders only.

## Test Strategy

- Unit: formula, two-decimal display value, all category boundaries, invalid/non-finite values, and email content.
- API: root and health responses; calculation success and invalid input; email validation, successful delivery, missing configuration, and SMTP failure.
- Email tests replace the SMTP client with a mock; no real SMTP account or network is needed for the test suite.
- Frontend: quickstart manual checks cover calculation, stale-result invalidation, disabled/enabled send behavior, and clear messages. No browser automation dependency is added.
