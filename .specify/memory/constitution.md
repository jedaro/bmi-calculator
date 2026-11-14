<!--
Sync Impact Report
Version change: unratified template -> 1.0.0
Modified principles: none (initial ratification)
Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
Removed sections: none
Follow-up TODOs: none
-->
# BMI Calculator API Constitution

## Core Principles

### I. Correct and Informative BMI Calculation
The BMI MUST be calculated as weight in kilograms divided by height in meters
squared. Weight and height MUST be numeric and positive; height MUST NOT be
zero. The result MUST be rounded to two decimal places for display. Adult
categories are informational: below 18.5 is Bajo peso, from 18.5 to below 25
is Peso normal, from 25 to below 30 is Sobrepeso, and 30 or above is Obesidad.
The application MUST state that the classification is not a medical diagnosis.
This keeps the calculation consistent and prevents the result from being
misrepresented as clinical advice.

### II. Simple, Modular Architecture
The application MUST keep HTTP endpoints, Pydantic schemas and validation,
business and email services, and shared configuration in the `api`, `schemas`,
`services`, and `core` areas respectively; automated tests belong in `tests`.
Business logic MUST remain separate from endpoint handlers. Functions MUST
have focused responsibilities and reusable behavior MUST NOT be duplicated.
This separation makes the educational codebase understandable and testable
without introducing unnecessary layers.

### III. Established Technology Stack
The project MUST use Python 3.12+, FastAPI, Pydantic, Uvicorn, Pytest, HTML,
CSS, JavaScript, SMTP, and python-dotenv for their stated purposes. Additional
technologies or dependencies MUST NOT be introduced without a clear,
documented justification and must preserve the project's simplicity.

### IV. Validated Interfaces and Safe Errors
All input MUST be validated, and API responses MUST use appropriate HTTP
status codes and clear, consistent error messages. Calculation, validation,
connection, and email-delivery errors MUST be handled explicitly. Responses
MUST NOT disclose sensitive information, and credentials MUST be provided
through environment variables rather than source code.

### V. Tested, Readable, Minimal Changes
Implemented functionality MUST have relevant automated tests. Python code
MUST follow PEP 8, use descriptive names and type hints, and keep complexity
proportional to the requirement. Changes MUST preserve the stated business
rules and project structure; unnecessary features and dependencies MUST NOT
be added. These practices support the project's didactic purpose and
maintainability.

## Additional Constraints

- The user interface MUST let users enter weight and height, view a valid
  calculation, enter an email address, and submit the result using a visible
  button.
- Email submission MUST be available only after a valid calculation exists.
- The result and category MUST be presented as informational and not as a
  diagnosis.
- Email delivery MUST use SMTP, with configuration and credentials supplied
  through environment variables.

## Development Workflow

- Before implementation, identify the affected responsibility areas and
  follow the existing modular structure.
- Add or update focused Pytest coverage for implemented behavior, including
  relevant validation and error cases.
- Keep user-facing and API errors clear and consistent while excluding
  sensitive details.
- Update documentation when behavior, configuration, or usage changes.
- Any proposed change to the architecture, technology stack, or business
  rules requires consultation before implementation.
- Explain relevant technical decisions briefly and favor the simplest
  implementation that fulfills the requirement.

## Governance

This constitution governs project decisions and implementation. Amendments
MUST be documented in this file, reviewed for consistency with the project’s
didactic purpose, and reflected in affected documentation and tests. Every
change and review MUST verify compliance with these principles. Any exception
to a MUST rule requires a documented justification and approval before the
exception is implemented.

The version follows Semantic Versioning: MAJOR for incompatible changes to
principles or governance, MINOR for new principles or materially expanded
requirements, and PATCH for clarifications and non-semantic refinements.
Contributors and reviewers MUST check the version and dates when amending this
constitution.

**Version**: 1.0.0 | **Ratified**: 2026-11-14 | **Last Amended**: 2026-11-14
