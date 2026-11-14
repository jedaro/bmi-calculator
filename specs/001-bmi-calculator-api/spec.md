# Feature Specification: BMI Calculator API

**Feature Branch**: `Not specified`

**Created**: 2026-11-14

**Status**: Draft

**Input**: User description: "A BMI calculation service with a simple web interface, optional email delivery, availability checks, and automated verification."

## Clarifications

### Session 2026-11-14

- Q: ¿Cuándo debe la aplicación considerar que un correo se envió correctamente? → A: Éxito cuando SMTP acepta el mensaje para entrega; no se garantiza recepción en bandeja.
- Q: ¿Qué nivel de acceso debe asumir la versión 1 para el envío de correos? → A: Solo uso local/aula; no exponer públicamente en v1.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Calculate and view BMI (Priority: P1)

A person enters their weight and height and receives their BMI and an informational category so they can understand the result.

**Why this priority**: Calculation and clear presentation are the core value of the product.

**Independent Test**: Submit valid weight and height values and verify the displayed BMI and category without configuring email.

**Acceptance Scenarios**:

1. **Given** positive weight in kilograms and height in meters, **When** the person requests a calculation, **Then** the result shows BMI rounded to two decimal places and its corresponding adult category.
2. **Given** missing, non-numeric, zero, negative, or non-finite weight or height, **When** the person requests a calculation, **Then** no result is produced and a clear validation message is shown.
3. **Given** a displayed result, **When** the person changes either measurement, **Then** email submission is unavailable until a new valid calculation is completed.

---

### User Story 2 - Email a calculation (Priority: P2)

A person provides an email address after calculating BMI and requests that the result be sent to them.

**Why this priority**: Email is a useful follow-up to the primary calculation, but is not needed to obtain a result.

**Independent Test**: With a valid calculation and a working mail configuration, submit a valid address and verify SMTP acceptance and the required calculation details in the message.

**Acceptance Scenarios**:

1. **Given** a current valid calculation and a valid email address, **When** the person requests email delivery, **Then** a confirmation is shown after the SMTP server accepts the message for delivery; the message contains a greeting, weight, height, BMI, category, and an informational-not-diagnosis note. The confirmation does not claim that the message reached the recipient's inbox.
2. **Given** an invalid email address, **When** the person requests email delivery, **Then** delivery is rejected and a clear validation message is shown.
3. **Given** valid calculation details but unavailable or failing mail delivery, **When** the person requests email delivery, **Then** the person is told delivery failed without exposing credentials or sensitive configuration.

---

### User Story 3 - Check service availability (Priority: P3)

An API consumer or operator checks whether the application is available and receives a clear status.

**Why this priority**: Availability checks help distinguish a running service from an unavailable one without affecting the calculation flow.

**Independent Test**: Request the application's availability checks and verify that an operational application reports a healthy status.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** a consumer checks availability, **Then** the application returns a successful response with a clear operational status.
2. **Given** the application is not running, **When** a consumer attempts to check availability, **Then** no healthy response is reported.

### Edge Cases

- Values on category boundaries (18.5, 25, and 30) are assigned to the category whose lower bound they meet.
- A value close to a category boundary that rounds across it is categorized using the unrounded calculation; only the displayed BMI is rounded.
- Invalid or changed measurements must not leave an earlier result eligible for email submission.
- Email delivery may fail because configuration is missing, the mail service cannot be reached, or the recipient is rejected; the interface must report failure without claiming success.
- SMTP acceptance confirms that the message was accepted for delivery, not that it reached the recipient's inbox; user-facing success must not imply confirmed inbox delivery.
- A delivery failure must not discard the displayed calculation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The product MUST let a person submit weight in kilograms and height in meters for a BMI calculation.
- **FR-002**: The product MUST accept only finite numeric weight and height values greater than zero.
- **FR-003**: The product MUST calculate BMI as weight divided by height squared and display the result rounded to two decimal places.
- **FR-004**: The product MUST assign the adult informational category using these ranges: below 18.5, Bajo peso; 18.5 to below 25, Peso normal; 25 to below 30, Sobrepeso; and 30 or above, Obesidad.
- **FR-005**: The product MUST identify the result and category as informational and not a medical diagnosis.
- **FR-006**: The calculation capability MUST be available to API consumers and return the submitted measurements, calculated BMI, and category for valid input.
- **FR-007**: The product MUST reject invalid calculation input with an appropriate error and a clear message.
- **FR-008**: The web interface MUST provide weight and height fields, a calculation action, a result area, an email field, and an email submission action.
- **FR-009**: The email submission action MUST remain unavailable unless a valid current calculation exists; changing either measurement invalidates the current calculation for email submission.
- **FR-010**: The product MUST validate email addresses before attempting delivery and report success only after SMTP accepts the message for delivery; the success message MUST NOT claim confirmed inbox receipt.
- **FR-011**: When SMTP accepts the message for delivery, the email MUST include a greeting, the submitted weight and height, the BMI, its category, and a note that the result is informational.
- **FR-012**: The product MUST use configured mail delivery and MUST NOT expose mail credentials in source code or user-facing errors.
- **FR-013**: The product MUST provide availability checks that report a successful operational status while it is running.
- **FR-014**: Automated verification MUST cover BMI calculation and categories, measurement and email validation, primary API behavior, and email success and failure without requiring a live mail server.
- **FR-015**: Setup instructions MUST explain how to run the product and configure email delivery, and the API's available operations and inputs MUST be documented.
- **FR-016**: Version 1 MUST be scoped and documented for local or classroom use only; public Internet exposure is out of scope.

### Key Entities *(include if feature involves data)*

- **Calculation**: The submitted weight and height together with the derived BMI and informational category.
- **Email delivery request**: A valid recipient address and the calculation details requested for delivery; no calculation history or user profile is retained.
- **Availability status**: An indication of whether the application is operational.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All defined valid calculation examples produce the expected BMI to two decimal places and the expected category, including examples at 18.5, 25, and 30.
- **SC-002**: All defined invalid measurement examples are rejected with a clear error and do not produce a usable result.
- **SC-003**: In every tested primary web flow, a person can calculate and view a result without email configuration, and cannot submit an email until a current valid result exists.
- **SC-004**: Every email-delivery test that receives SMTP acceptance contains all six required message elements and reports acceptance without claiming inbox receipt; every failure test reports failure without revealing credentials.
- **SC-005**: All automated verification runs without a real mail server and covers the calculation, validation, API, and delivery outcomes described above.
- **SC-006**: A person following the setup instructions can start the product, find its API documentation, and configure email delivery without needing undocumented steps.
- **SC-007**: Setup documentation explicitly identifies version 1 as local/classroom use and states that public Internet exposure is out of scope.

## Assumptions

- The intended category ranges are for adults and are informational, not medical advice.
- Weight is entered in kilograms and height in meters; no unit conversion is in scope.
- Categories are selected from the unrounded calculated BMI; rounding applies only to the displayed BMI.
- The interface and user-facing messages are in Spanish.
- Email is sent only on an explicit user request. The product does not retain calculation history, email addresses, or user profiles.
- Mail delivery is configured outside the source code; the product reports a configuration or delivery problem without exposing secrets.
- The application has one simple web interface and API capabilities for local/classroom users; public Internet exposure, authentication, persistence, and administration are outside scope.
