
---
description: "Implementation tasks for the BMI Calculator API"
---
# Tasks: BMI Calculator API

**Input**: Design documents from `specs/001-bmi-calculator-api/`

**Prerequisites**: `plan.md` and `spec.md`; design references include `research.md`, `data-model.md`, `contracts/openapi.yaml`, and `quickstart.md`.

**Tests**: Tests are required by FR-014 and the project constitution. Write the listed tests before the corresponding implementation and verify they fail for the expected missing behavior.

**Organization**: Tasks are grouped by user story and ordered by priority. The BMI service and browser calculation are the MVP.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: The task can run in parallel with other marked tasks because it affects a separate file and has no dependency on unfinished work.
- **[Story]**: The user story addressed by the task, such as `[US1]`.
- Every task specifies the file or files to create, update, or validate.

## Phase 1: Setup

**Purpose**: Create the application skeleton and declare the mandated runtime and test dependencies.

- [ ] T001 Create Python package initializer files at `app/__init__.py`, `app/api/__init__.py`, `app/api/endpoints/__init__.py`, `app/schemas/__init__.py`, `app/services/__init__.py`, and `app/core/__init__.py`; create the `tests/` directory.
- [ ] T002 [P] Add FastAPI, Pydantic, Uvicorn, python-dotenv, email-validator, Pytest, and HTTPX dependencies to `requirements.txt`.
- [ ] T003 [P] Add `.env` and local Python/test artifacts to `.gitignore`; add placeholder-only SMTP variable names and values to `.env.example` for `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURITY`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SENDER`, and `SMTP_TIMEOUT_SECONDS`.

---

## Phase 2: Foundational

**Purpose**: Establish the importable FastAPI application and shared HTTP test setup required by the stories.

- [ ] T004 Create a reusable FastAPI `TestClient` fixture in `tests/conftest.py`.
- [ ] T005 Add an application bootstrap test that verifies `/docs` and the generated OpenAPI document are available in `tests/test_app.py`.
- [ ] T006 Create the FastAPI application with title, version, and `/docs` enabled in `app/main.py`.

**Checkpoint**: The app imports and its documentation endpoint can be tested before story-specific routes are added.

---

## Phase 3: User Story 1 - Calculate and view BMI (Priority: P1) 🎯 MVP

**Goal**: A person can calculate BMI and see an accurate, clearly labeled result in the web interface without configuring email.

**Independent Test**: Verify the `75` kg / `1.75` m example returns BMI `24.49` and `Peso normal`, verify all category boundaries and invalid measurements, then use `/ui/` to calculate without SMTP configuration.

### Tests for User Story 1

- [ ] T007 [P] [US1] Add service tests for the formula, two-decimal display value, unrounded category selection at 18.5, 25, and 30, and non-positive or non-finite inputs in `tests/test_bmi_service.py`.
- [ ] T008 [P] [US1] Add API tests for `POST /api/v1/bmi/calculate`, including the `75` / `1.75` response and HTTP 422 for missing, non-numeric, zero, negative, or non-finite measurements, in `tests/test_bmi_api.py`.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Define BMI request and result schemas in `app/schemas/bmi.py`; require weight and height to be “Finite and greater than 0” and return weight, height, rounded BMI, and one of the four adult category labels.
- [ ] T010 [P] [US1] Implement the framework-independent BMI formula and adult categories in `app/services/bmi_service.py`: below 18.5 `Bajo peso`, 18.5 to below 25 `Peso normal`, 25 to below 30 `Sobrepeso`, and 30 or above `Obesidad`; classify using unrounded BMI and round only the displayed result to two decimals.
- [ ] T011 [US1] Implement `POST /api/v1/bmi/calculate` in `app/api/endpoints/bmi.py`, validate with the BMI schemas, call the BMI service, and return clear HTTP 422 validation errors.
- [ ] T012 [US1] Create the Spanish-language calculation form, result area, email field, initially disabled email button, and informational-not-diagnosis note in `frontend/index.html`.
- [ ] T013 [P] [US1] Add simple responsive styling and visible focus/status states for the form and result in `frontend/styles.css`.
- [ ] T014 [P] [US1] Implement the calculation request and result/error rendering in `frontend/app.js`; do not duplicate BMI logic, enable email submission only after a valid calculation, and invalidate the displayed calculation and disable email submission whenever either measurement changes.
- [ ] T015 [US1] Register the BMI router and mount `frontend/` at `/ui/` in `app/main.py` without taking over `/`; add the root and health availability routes in US3.

**Checkpoint**: The calculation works through both the API and `/ui/`; a current result is required before the email button can be enabled.

---

## Phase 4: User Story 2 - Email a calculation (Priority: P2)

**Goal**: A person can request email delivery of a current BMI result and receives clear success or failure feedback.

**Independent Test**: With a current valid calculation and a mocked SMTP client, verify the request validates the address, the message has all six required elements, success follows SMTP acceptance without claiming inbox receipt, and missing configuration and SMTP failure are reported without a live mail server.

### Tests for User Story 2

- [ ] T016 [P] [US2] Add email service tests with mocked SMTP for SSL and STARTTLS modes, message greeting/measurements/BMI/category/informational note, SMTP acceptance as the success boundary, and delivery failure handling in `tests/test_email_service.py`.
- [ ] T017 [P] [US2] Add API tests for valid and invalid email input, an `accepted` response only after SMTP acceptance, missing configuration, SMTP failure status codes, and absence of credentials or inbox-delivery claims in responses in `tests/test_email_api.py`.

### Implementation for User Story 2

- [ ] T018 [P] [US2] Define the email request and response schemas in `app/schemas/email.py`; validate the recipient as an email address, keep weight and height “Finite and greater than 0”, and use response status `accepted` only after SMTP acceptance.
- [ ] T019 [P] [US2] Read SMTP settings from environment variables, load `.env` for local development, support only `starttls` or `ssl`, and allow missing mail settings without preventing app startup in `app/core/config.py`.
- [ ] T020 [US2] Implement `app/services/email_service.py` using the shared BMI service and Python's `email.message`/`smtplib`; include all required message elements, use a finite timeout and configured secure transport, and do not expose credentials or raw SMTP errors.
- [ ] T021 [US2] Add `POST /api/v1/bmi/send-email` to `app/api/endpoints/bmi.py`; return status `accepted` only after SMTP accepts the message, HTTP 503 for missing configuration, HTTP 502 for delivery failure, and safe validation errors without claiming inbox receipt.
- [ ] T022 [US2] Extend `frontend/app.js` to submit the recipient and current measurements, enable sending only for an unchanged valid calculation, show loading/success/failure states, preserve the calculation after email failure, and avoid claiming confirmed inbox receipt.

**Checkpoint**: Email requests work with configured SMTP, and automated email tests use mocks only.

---

## Phase 5: User Story 3 - Check service availability (Priority: P3)

**Goal**: An API consumer or operator can check root availability and application health.

**Independent Test**: Verify `GET /` reports the API as available and `GET /health` reports the application as healthy while it is running.

### Tests for User Story 3

- [ ] T023 [P] [US3] Add tests asserting HTTP 200 and `{"status":"available"}` for `GET /`, plus HTTP 200 and `{"status":"healthy"}` for `GET /health`, in `tests/test_health_api.py`.

### Implementation for User Story 3

- [ ] T024 [US3] Implement the root availability response and `/health` operational status in `app/api/endpoints/health.py`.
- [ ] T025 [US3] Register the health router in `app/main.py` without changing the `/ui/` static interface mount.

**Checkpoint**: Both availability operations return their documented successful responses when the application is running.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Document operation and verify the complete feature against its design artifacts.

- [ ] T026 Document local/classroom-only use and the prohibition on public Internet exposure, plus setup, startup, `/docs`, `/ui/`, API operations, SMTP environment variables, and tests, in `README.md`.
- [ ] T027 Run `pytest` and validate the calculation, email acceptance semantics, local-only scope, availability, and browser scenarios in `specs/001-bmi-calculator-api/quickstart.md`; correct any mismatch in the implementation or documentation.

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes package paths and dependencies.
- **Foundational (Phase 2)**: Depends on Setup; provides the app instance and test client.
- **US1 (Phase 3)**: Depends on Foundational; delivers the MVP calculation and UI.
- **US2 (Phase 4)**: Depends on US1 because email reuses its BMI service and is enabled from its current browser result; report `accepted` only at SMTP acceptance.
- **US3 (Phase 5)**: Depends only on Foundational for behavior. It is listed after US1/US2 by priority; integration changes to `app/main.py` should be serialized with the earlier router/UI registrations.
- **Polish (Phase 6)**: Depends on all three user stories.

### User Story Dependency Graph

```text
Setup -> Foundational -> US1 -> US2 -> Polish
                    \---------------> US3 ->/
```

US3 has no functional dependency on the calculation or email story; it can be developed independently after the app bootstrap. The sequential phase placement preserves the specified priority order.

### Parallel Opportunities

- **Setup**: T002 and T003 can run in parallel after T001 because they edit different files.
- **US1**: T007 and T008 are independent test files; T009 and T010 are independent schema/service files. After T012 fixes the HTML IDs/classes, T013 and T014 can proceed in parallel.
- **US2**: T016 and T017 are independent tests; T018 and T019 are independent schema/config files. After T020, endpoint work T021 and browser request work T022 can proceed in parallel against the documented contract, then validate together.
- **US3**: No implementation tasks are marked parallel: tests must be written first, then the health router and its registration are completed in order.
- **Polish**: T026 documentation must precede T027's final validation; these tasks are sequential.

## Parallel Examples

### User Story 1

```text
Parallel: T007 tests/test_bmi_service.py and T008 tests/test_bmi_api.py
Parallel: T009 app/schemas/bmi.py and T010 app/services/bmi_service.py
After T012: T013 frontend/styles.css and T014 frontend/app.js
```

### User Story 2

```text
Parallel: T016 tests/test_email_service.py and T017 tests/test_email_api.py
Parallel: T018 app/schemas/email.py and T019 app/core/config.py
After T020: T021 app/api/endpoints/bmi.py and T022 frontend/app.js
```

### User Story 3

```text
No parallel implementation is identified: write T023 tests/test_health_api.py first,
then implement T024 app/api/endpoints/health.py and register it in T025 app/main.py.
```

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup and Foundational phases.
2. Complete US1 tests and implementation.
3. Validate calculation, category boundaries, input errors, and browser flow without SMTP.
4. Stop at the US1 checkpoint if an MVP demonstration is needed; email and availability stories can follow.

### Incremental Delivery

1. Deliver Setup + Foundational, including a testable FastAPI app.
2. Deliver US1 for a usable BMI calculation and result view.
3. Deliver US2 for explicitly requested email delivery.
4. Deliver US3 availability checks.
5. Complete README and quickstart validation.

## Notes

- Every task uses the required checkbox, sequential ID, optional parallel marker, required story label for story phases, and explicit file path.
- Story tests are required by FR-014; SMTP is mocked and no SMTP server is required for automated tests.
- No database, authentication, user history, frontend framework, or mail framework is in scope.
