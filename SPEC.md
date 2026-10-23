# ထွယ်ဂျီဂွမ်Caculator — Feature Specification

## 1. Product and release scope

Build a severance calculator for E-9 workers in South Korea, with a foundation for a broader worker-support platform.

### First-release capabilities

- Normal statutory severance, DB baseline estimates, and DC contribution estimates.
- Standard employment cases with one continuous employment period and one unchanged retirement scheme.
- Employment eligibility checks and an explanation of the result.
- Detailed calculation breakdowns, assumptions, and official source links.
- **English and Burmese**, with English as the default and fallback language and a language switcher throughout the calculation flow.
- Optional manually reported DC account balances, without investment-return projections.
- An E-9 departure guarantee insurance explanation with official EPS links.
- Calculation without an account; no login or saved cloud history in the first release.

Results are estimates **before tax, in KRW**. Insurance reconciliation, tax calculations, employer-specific enhanced benefits, and complex employment histories are outside the first release.

## 2. Calculation behavior

### Supported employment cases

Support one continuous employment period with one employer and one unchanged retirement scheme.

Collect employment dates, scheduled weekly hours, and confirmation that the history has no special calculation adjustments.

Leave requiring special treatment, previous severance settlements, scheme changes, and variable-hours histories requiring detailed eligibility analysis return **review required**, without a benefit total.

Employment beginning before 2013 and zero-reference-wage cases also require review, without a benefit total. Historical rule variants are outside the initial calculator.

Eligibility checks cover the statutory continuous-service and scheduled-hours requirements. [MOEL eligibility guidance](https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=202302031324407911000)

### Normal statutory severance

"Normal" means **퇴직금**.

- Ask for the final working day; the API derives the retirement date as the following calendar day.
- Derive the preceding three-calendar-month wage period on the server.
- Collect actual wages for the displayed periods, including relevant allowances, plus eligible annual bonus and unused-leave-pay components.
- Calculate daily average wage using actual calendar days.
- Use daily ordinary wage when it is higher.
- If daily ordinary wage is supplied, it must be positive; leave it blank when unknown.
- Calculate the baseline as `applicable daily wage × 30 × service days ÷ 365`.

If daily ordinary wage is unknown, label the result provisional and identify the missing comparison. Show input guidance for eligible wage components. [MOEL calculator and worked example](https://moel.go.kr/retirementpayCal.do)

### DB

Use the same wage-and-service baseline calculation while identifying the result as a **DB statutory baseline estimate**. Employer-specific plan enhancements require a future extension.

### DC

Collect wage totals for each year or partial year within the employment period. Partial-year inputs represent actual wages earned during that period.

- Calculate the minimum contribution estimate from eligible wages divided by 12.
- Show yearly calculations and their total.
- Optionally accept an account balance and its statement date.
- Display the reported balance separately from required contributions.
- Do not infer missing employer contributions by comparing the investment balance with the contribution estimate.

DC account value depends on contributions and investment performance. [MOEL pension guidance](https://moel.go.kr/retirementpay.do)

### E-9 insurance

Explain departure guarantee insurance separately from the selected retirement scheme. Do not automatically add insurance proceeds to benefits or subtract them from DB/DC results. First-release insurance support consists of explanatory content and official links. [EPS insurance guidance](https://www.eps.go.kr/eo/EmployPerSystem.eo?tabGb=06)

## 3. API features

### HTTP interface

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Service health |
| `GET /v1/rules` | Supported methods, rule version, verification date, and official sources |
| `POST /v1/calculations/context` | Derive employment duration, wage-entry periods, and required inputs |
| `POST /v1/calculations` | Validate inputs and calculate the selected method |

The calculation request uses a method discriminator: `normal`, `db`, or `dc`, with method-specific wage inputs.

Responses include:

- Method, rule version, and source metadata.
- Eligibility outcome and machine-readable reason codes.
- Derived dates and service duration.
- Calculation breakdown and relevant assumptions.
- Normal/DB benefit estimate, or DC required contributions and optional reported balance.

### Input and result behavior

- Dates use `YYYY-MM-DD` and Korean calendar-date semantics.
- Money crosses the API as decimal strings.
- Preserve intermediate precision and round down once for the displayed whole-won estimate.
- Keep display rounding explicit in result metadata.
- Distinguish eligible, ineligible, and review-required outcomes. Review-required results omit the benefit total.
- Return structured field errors for invalid input. Clients translate error codes into English or Burmese.

## 4. Client experience and privacy

### Calculation flow

1. Choose language and retirement scheme; show a short explanation of each scheme.
2. Enter employment details and answer special-case screening questions.
3. Enter wages using API-generated period labels.
4. Review inputs and submit.
5. Display the estimate, breakdown, assumptions, rule version, and sources.

Both clients must support clear loading, validation, unavailable-service, and review-required states. Failed requests retain entered information and offer an explicit retry.

- Back, Edit, and continuing with unchanged employment preserve all entered wage details in session memory. Employment edits retain rows only when the API-generated period boundaries still match; identify changed periods needing new amounts. Explicit sample and new-calculation actions may replace the draft.
- Invalid amounts and required statement dates show localized errors beside the affected fields. Reveal and focus the first invalid field, including issues returned by the API.
- Successful forward, Back, and Edit transitions reveal the new step and move keyboard/accessibility focus to its heading or result summary. Language changes alone preserve reading position; respect reduced-motion preferences.
- Review displays every accepted decimal input exactly, including fractional digits, without conversion through binary floating point. Final benefit estimates keep the API's whole-won rounding rule.

### PWA and mobile behavior

- The PWA supports installation and cached explanatory content.
- Calculations require connectivity.
- Keep financial inputs and results in session memory; persist only language preferences initially.
- Do not cache calculation requests or responses.
- Verify Burmese glyph rendering, line wrapping, and readable font sizes.
- Use accessible labels, keyboard navigation, and touch-friendly controls.

### Privacy

- Do not request passport numbers, alien registration numbers, or bank details.
- Exclude salaries and calculation payloads from logs and analytics.

## 5. Future features

- Login and saved history: workers can access their own saved calculations.
- Currency conversion: show converted amounts with the exchange-rate source and update timestamp.
- Worker information: reviewed multilingual content with official references and review dates.
- Assistant: answers grounded in verified worker information and the same calculation results.
- Additional languages: extend translation resources when demand is established.

These features are outside the first release.

## 6. Feature acceptance criteria

- Match published MOEL calculation examples.
- Test eligibility boundaries, partial years, leap years, month ends, and final-working-day conversion.
- Test allowances, bonus inclusion, unused-leave-pay inclusion, and ordinary-wage comparison.
- Test DC yearly totals, partial-year wages, and separation of contributions from reported balances.
- Reject invalid dates, negative amounts, overlapping wage periods, and malformed requests.
- Confirm complex cases return review-required outcomes without misleading totals.
- Verify complete English/Burmese flows, including errors and result explanations.
- Test mobile layouts, accessibility, connectivity failures, retry behavior, and PWA cache exclusions.
- Review implemented calculation rules against official sources before public release.
