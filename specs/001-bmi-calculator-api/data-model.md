# Data Model: BMI Calculator API

The application is stateless. These models represent request/response data and transient browser state; no data is stored after a request.

## BMI Calculation Request

| Field | Type | Validation | Meaning |
|---|---|---|---|
| `weight` | Number | Finite and greater than 0 | Weight in kilograms |
| `height` | Number | Finite and greater than 0 | Height in meters |

## BMI Calculation Result

| Field | Type | Validation / derivation | Meaning |
|---|---|---|---|
| `weight` | Number | Echo of accepted request | Submitted kilograms |
| `height` | Number | Echo of accepted request | Submitted meters |
| `bmi` | Number | `weight / (height * height)`, rounded to two decimal places for display | Calculated body mass index |
| `category` | String | Derived from the unrounded BMI | `Bajo peso`, `Peso normal`, `Sobrepeso`, or `Obesidad` |

Adult category ranges: below 18.5 is `Bajo peso`; 18.5 to below 25 is `Peso normal`; 25 to below 30 is `Sobrepeso`; 30 or above is `Obesidad`. The result is informational, not a medical diagnosis.

## Email Delivery Request

| Field | Type | Validation | Meaning |
|---|---|---|---|
| `email` | Email address | Must pass email-address validation | Explicit recipient for this delivery |
| `weight` | Number | Same finite-positive rule as BMI request | Weight to calculate and include |
| `height` | Number | Same finite-positive rule as BMI request | Height to calculate and include |

The email service obtains the result from the shared BMI service and includes greeting, measurements, BMI, category, and the informational notice. Credentials are configuration, not request data. Neither request nor recipient is retained.

## Email Delivery Response

| Field | Type | Meaning |
|---|---|---|
| `status` | String | `accepted` only when the SMTP server accepts the message for delivery |
| `message` | String | User-facing confirmation that does not imply inbox receipt |

SMTP acceptance is not confirmation that the message reached the recipient's inbox. Failures are HTTP errors, not success-shaped delivery responses. Missing configuration and transport failure are distinct operational outcomes; sensitive details are not returned.

Version 1 is intended for local or classroom use only; public Internet exposure is out of scope.

## Availability Responses

- Root status: `status` indicates that the API is available.
- Health status: `status` indicates that the application is operational.

## Browser Calculation State

The interface holds either no current result or a result associated with the exact current weight and height values. Editing either value invalidates the association and disables email submission. A new valid calculation establishes a current result; a mail failure does not invalidate it.
