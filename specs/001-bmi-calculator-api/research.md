# Research: BMI Calculator API

## Decisions

### Request validation and endpoint testing

- **Decision**: Define Pydantic request/response models, constrain weight and height to finite values greater than zero, and use FastAPI's `TestClient` with Pytest and HTTPX for endpoint tests.
- **Rationale**: This preserves the mandated schema validation and allows endpoint tests without starting a separate server. Unit tests remain focused on pure service behavior.
- **Alternatives considered**: Hand-written parsing in route handlers was rejected because it duplicates validation and weakens consistent error responses.
- **Sources**: [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) documents `TestClient`, HTTPX, and direct Pytest use.

### Email address validation

- **Decision**: Use Pydantic `EmailStr` and add its optional `email-validator` dependency.
- **Rationale**: Email validation is a stated requirement; relying on a hand-written regular expression would be an avoidable and fragile implementation. The extra package is narrowly justified by this requirement.
- **Alternatives considered**: A custom regex or superficial `@` check was rejected as less reliable; `pydantic-settings` is not needed for this small set of configuration values.
- **Sources**: [Pydantic network types](https://docs.pydantic.dev/2.10/api/networks/#pydantic.networks.EmailStr) states that `EmailStr` validates email addresses and requires the optional `email-validator` package.

### SMTP delivery, success semantics, and error handling

- **Decision**: Use Python's standard `smtplib` and `email.message` modules. Support explicit SMTP STARTTLS or SMTP-over-SSL modes, set a finite connection timeout, close clients via context management, and return generic delivery errors to callers. Report success only after the SMTP server accepts the message for delivery; do not claim that it reached the recipient's inbox.
- **Rationale**: SMTP acceptance is synchronous and testable with a mocked SMTP client, while inbox receipt cannot be guaranteed by this integration. The standard library satisfies the requested behavior without an email framework.
- **Alternatives considered**: Confirmed inbox delivery would require provider-specific tracking or delivery notifications beyond SMTP; plaintext SMTP, a mail framework, a background queue, and asynchronous mail infrastructure are unnecessary for this educational, stateless project. Missing configuration is reported as unavailable; connection or delivery failure is reported without exposing SMTP responses or secrets.
- **Sources**: [Python `smtplib`](https://docs.python.org/3.12/library/smtplib.html) documents `SMTP`, `SMTP_SSL`, `starttls()`, timeouts, and context-manager cleanup.

### Version 1 deployment scope

- **Decision**: Document and target local or classroom use only; public Internet exposure is out of scope for v1.
- **Rationale**: The project is didactic and explicitly excludes authentication. Restricting the intended deployment avoids implying that an unauthenticated SMTP-sending endpoint is ready for public use.
- **Alternatives considered**: A public service would require a separately designed abuse-prevention and operational-security scope, which is not part of this feature.

### Environment configuration

- **Decision**: Load `.env` for local development with python-dotenv and read settings from process environment variables. Keep `.env` out of version control and provide a placeholder-only `.env.example`.
- **Rationale**: This meets the constitution's requirement, works with ordinary deployment environments, and avoids adding a separate settings framework for a small configuration surface.
- **Alternatives considered**: Hard-coded defaults for credentials and a separate settings package were rejected. Missing mail settings do not prevent BMI calculations; they prevent only email delivery.
- **Sources**: [python-dotenv on PyPI](https://pypi.org/project/python-dotenv/) documents loading `.env` values into the process environment.

### Static interface hosting

- **Decision**: Serve the plain HTML/CSS/JavaScript interface from the same FastAPI application under `/ui/`; keep `/` for the explicitly requested API availability response.
- **Rationale**: A same-origin interface can call the API without CORS configuration, a separate frontend server, or a build system. A distinct path prevents the root availability operation from conflicting with the web page.
- **Alternatives considered**: Serving the UI at `/` would conflict with the required root response; a separate frontend process adds setup without user value.
- **Sources**: [FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/) documents mounting static files under a chosen path.
