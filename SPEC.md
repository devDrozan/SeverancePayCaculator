# E9 Mate Myanmar — Feature Specification

## 1. Product and release scope

E9 Mate Myanmar is an everyday utility hub for Myanmar workers in South Korea. Its first released tool is the severance calculator; later employment, finance, and administrative tools will be independent mini-app modules inside the same installed application.

### Confirmed status and next target

| Area | Status |
| --- | --- |
| V1.0 severance calculation, guidance, and E-9 insurance content | Implemented in the active API, web/PWA, and mobile source. The Product Owner reports a production Android AAB built; Google Play publication remains pending. This specification does not certify the release artifact. |
| Mobile home dashboard and module shell | Implemented in the active local mobile source: compact E9 Mate header, mixed information/sample-ad carousel, service and Coming soon sections, Home/Services/Notices footer, local search, separate Severance and Insurance routes, and specific Coming soon pages. Profile is not present. Native device QA and release approval remain pending. The previously built AAB does not contain this change. |
| V1.1 Salary Estimate from Work Time | Combined manual calendar and user-rate salary feature is implemented in the active API, web/PWA, and mobile source under section 6A. The service opens directly in local mobile source; native release verification remains pending. Earlier unpublished tracker prototype work is not a released feature. |
| V1.2–V1.5, ads, and analytics | Planned only. No live modules, data collection, or monetization are implied by roadmap cards. |

The hub is a mobile interface change first; the existing web/PWA calculator stays available. New calculation features still follow the workspace's API and web/PWA-first delivery boundary. The hub shell does not change severance financial rules or its existing `/v1` contract, Android package identity, or EAS project configuration. Section 6A adds a separate backward-compatible salary endpoint.

### First-release capabilities

- Normal statutory severance, DB baseline estimates, and DC contribution estimates.
- Standard employment cases with one continuous employment period and one unchanged retirement scheme.
- Employment eligibility checks and an explanation of the result.
- Detailed calculation breakdowns, assumptions, and official source links.
- **English and Burmese**, with English as the default and fallback language and a language switcher throughout the calculation flow.
- Optional manually reported DC account balances, without investment-return projections.
- An E-9 departure guarantee insurance explanation with official EPS links.
- Calculation without an account; no login or saved cloud history in the first release.
- Mobile Light and Dark appearance controls with a system-following default, plus an About screen with creator credit and the app's purpose.
- A mobile launch screen with the app name and existing logo, shown for three seconds before the initial screen appears.

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
- Display the reported balance separately from required contributions, preserving its accepted decimal amount on Review and Result.
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

- Back, Edit, consulting guidance and returning, and continuing with unchanged employment preserve the selected scheme, entered details, and calculation step in session memory. Employment edits retain wage rows only when the API-generated period boundaries still match; identify changed periods needing new amounts. Explicit sample and new-calculation actions may replace the draft; switching retirement scheme with a draft asks for confirmation before clearing it. The mobile calculator begins with the employment form; do not show a sample-data button or populate demo wages.
- Weekly hours preserve decimal text during editing and submit the intended numeric value; typing `14.5` must never become `145`.
- Invalid amounts and required statement dates show localized errors beside the affected fields. Reveal and focus the first invalid field, including issues returned by the API.
- Successful forward, Back, and Edit transitions reveal the new step and move keyboard/accessibility focus to its heading or result summary. Language changes alone preserve reading position; respect reduced-motion preferences. The step indicator announces the current step and marks a step complete only when the shown journey finished it, so an ineligible result does not mark wages or review as done.
- Review displays every accepted decimal input exactly, including fractional digits, without conversion through binary floating point. Final benefit estimates keep the API's whole-won rounding rule.
- Loading actions retain their localized accessible names and communicate progress. Result amounts remain readable as complete values in narrow layouts, without truncation or an isolated final digit.

### PWA and mobile behavior

- On each cold mobile launch, show the configured app name (currently `E9 Mate Myanmar`) and existing won logo centered on a full-screen launch view. Keep it visible for at least three seconds from its first layout; reveal the initial route once that duration and local font/language/theme initialization have completed. Font or preference failures must fall back without trapping the user. Do not wait for the calculation API. Ordinary navigation, appearance/language changes, and returning from the background must not replay it. Respect light/dark appearance, safe areas, large text, and reduced motion; use a static layout without a countdown, ads, or extra actions. Configure the native launch screen with matching branding/background and hand off to the timed app view without showing another screen in between. Native splash presentation must also be checked in a standalone build because Expo Go's launch UI differs.
- The PWA supports installation and cached explanatory content.
- Calculations require connectivity.
- Keep severance inputs and results in session memory; persist only language and appearance preferences except the explicitly approved salary-module records/settings in section 6A.
- The mobile app defaults to the system appearance, follows device theme changes until the user chooses Light or Dark, and remembers an explicit choice. Existing saved System preferences continue to follow the device; the header icon indicates the resolved appearance and toggles to the other mode. Changing appearance preserves the current calculation draft and step. Both themes cover navigation, forms, validation, results, guidance, and About in English and Burmese.
- The mobile header shows the compact E9 Mate brand and three 44dp icon actions: appearance, language, and search. The appearance icon switches between Light and Dark immediately; the language icon opens English/Burmese choices; search opens a local service search with empty and no-result states. About us remains available from Home. Each action has a localized accessible label and state where applicable. Switching language or appearance preserves the current calculation; route changes close the language chooser. Home and module navigation follow section 5.
- Mobile About credits "Created by devrozan" and explains the hub's purpose: helping Myanmar workers in South Korea use practical employment, financial, and administrative tools. The current released scope remains severance and E-9 insurance information. Show a copyright notice with the current year and `devrozan` as the owner, without invented biography or profile links.
- Do not cache calculation requests or responses.
- Verify Burmese glyph rendering, line wrapping, and readable font sizes.
- Mobile hero headings preserve the translated wording and spaces without inserting forced line breaks. Use readable responsive typography, remaining on one line where it fits and wrapping naturally for longer wording or larger text instead of truncating or automatically shrinking it.
- Mobile About, guidance, and insurance prose must leave room for stacked Burmese marks using the font's natural iOS line metrics, wrap without truncation at narrow widths and larger text sizes, and separate explanatory paragraphs visibly. Informational cards use balanced top and bottom padding so text does not crowd the card edges.
- Use accessible labels, keyboard navigation, and touch-friendly controls.

### Privacy

- Do not request passport numbers, alien registration numbers, or bank details.
- Exclude salaries and calculation payloads from logs and analytics.

## 5. Mobile mini-app hub — implemented in local source, pending native QA

### Home dashboard

- After the existing branded launch screen, open **Home** as the normal entry point. Use a dark green, card-based visual style with a compact E9 Mate header, an illustrated hero carousel, an **Our Services** grid with colored feature icons, a smaller **Coming soon** section, and a fixed footer. Keep a legible Light variant as well. Home loads without the calculation API, an account, or personal information.
- The shared top bar shows the compact E9 Mate brand with clickable Light/Dark, Language, and Search icons. Appearance toggles immediately and follows the system until manually chosen. Language offers English/Burmese choices. Search filters the local module catalog by translated names and descriptions without sending queries to a server.
- Show **one** manually controlled, horizontally swipeable hero carousel with useful information and sample E9 Mate ads in a stable order. The useful-information cards link to existing severance and E-9 insurance guidance. Sample-ad cards are visibly labelled **Sample ad · E9 Mate**, link only to existing E9 Mate services, and are preview content; they do not imply an advertiser, paid placement, live campaign, AdMob integration, or ad impressions. Show adjacent-card peeks, position dots, and accessible previous/next controls. Do not auto-advance or trap vertical scrolling.
- Under **Our Services**, show a responsive two-column flexbox grid of Severance Calculator, **Salary Estimate from Work Time**, E-9 Insurance, and Currency Exchange. The combined salary card opens the implemented calendar and user-rate salary module directly; its scope is section 6A. Availability here describes local functionality, not native release certification. Currency Exchange is also Coming soon. Available cards open their working service; planned cards open a specific Coming soon page without forms or permissions. Historical salary/work planned links redirect to the implemented salary module.
- Show a smaller **Coming soon** area for Finance & Reminders and Worker Information Center, each tappable with an honest planned destination. Keep About us reachable from Home.
- The footer shows **Home**, **Services**, and **Notices** only on hub pages. Home returns to the dashboard; Services shows the service catalog; Notices opens a clear empty state until real notices exist. **Do not show Profile** or a profile destination in this implementation. Footer navigation must not cover or interrupt the calculator or other module screens.

### Initial module catalog

| Service label | Home placement | Current status | Destination and scope |
| --- | --- | --- | --- |
| Severance Calculator | Our Services | Available in local hub | Existing Normal, DB, and DC flows, in-module How it works guidance, results, assumptions, and official sources. No formula or API contract change. |
| Salary Estimate from Work Time | Our Services | Available in local source; native release QA pending | Opens `/work` directly for calendar records, monthly settings, and API salary estimates. `/salary` and historical planned salary/work links redirect to the same module. Scope is section 6A. |
| E-9 Insurance | Our Services | Available in local hub | Existing departure-guarantee explanation and official EPS links. It remains informational and is not added to severance totals. |
| Currency Exchange | Our Services | Coming soon | Specific planned-service page. V1.3 scope remains in section 6. |
| Finance & Reminders | Coming soon | Coming soon | Specific planned-service page. V1.4 scope remains in section 6. |
| Worker Information Center | Coming soon | Coming soon | Specific planned-service page. V1.5 scope remains in section 6. |

### Module and navigation boundaries

- A mini-app is an independently navigable **feature area inside one E9 Mate Myanmar installation**, not a separately installed application or remotely downloaded code package. The shared shell owns Home, Services, Notices, global navigation, language, appearance, search, About, and common accessibility/privacy behavior. Each module owns its screens, content, feature state, tests, and any feature-specific storage or service integration.
- Use a local module catalog with stable identifiers, localized metadata, availability, section, and destination routes. Retain old salary planned links as aliases to the combined Salary Estimate from Work Time destination. Adding a module must not require changing another module's calculation logic or stored data. Modules may share established shell services and intentional interfaces; they must not reach into another module's private state or database tables.
- Opening an available card enters that module. A visible Home action and Android/iOS back navigation return from its entry screen to Home; in-module Back continues to follow the feature's existing flow. Home and module switching must not reset a calculator draft. Closing the app still clears V1.0 financial inputs and results as required in section 4.
- Preserve working access to the existing calculator, guidance, insurance, and About destinations during migration. Existing external/deep links, if supported, must open or redirect to the corresponding module page. Guidance belongs inside the Severance module.
- Do not make Home or unrelated modules depend on the severance API's availability. A calculator outage shows a retry state within that module. Later offline work records remain local to their approved module. Cross-module reuse, such as salary estimates reading work logs, needs an explicit interface, user disclosure, and separate approval; all financial calculations continue to run in the API.

### Hub acceptance criteria

- On 320–360dp Android layouts and iPhone sizes, the compact header, hero carousel, service cards, planned badges, and footer remain readable in English and Burmese, Light and Dark, and larger text. Service cards align icons, wrapping titles, status space, descriptions, and bottom actions consistently within each row. The grid may use one column at narrow width, in Burmese on phones, or with larger text. Cards grow with content; Burmese marks must not clip. Touch targets are at least 44dp and screens respect safe areas.
- Screen readers announce hero card labels and positions, service names, availability, and actions. Previous/next controls work without swipe gestures; focus moves predictably on opening a service and returning Home. Reduced-motion settings are respected.
- The carousel stays on the selected card while Home remains mounted, does not advance by itself, and cannot trap vertical scrolling. Every service is discoverable in the grid or Services page without swiping.
- Available services open the expected feature and return Home without losing permitted session state. Planned services open their own honest Coming soon pages and cannot be mistaken for released features. Native release verification remains a separate requirement for implemented local modules. Notices has an explicit empty state; no Profile item appears. Search handles an empty query and no results. A failed module load does not prevent Home or other modules from working.
- Existing V1.0 calculator examples, API errors, source links, language/theme preferences, privacy behavior, and insurance separation pass regression checks. No new native storage, backend hosting, analytics, or paid advertising is required for this hub shell; salary-module storage is separately authorized in section 6A.

## 6. Planned modules and future scope

| Milestone | Priority | Planned module, subject to separate implementation and release approval |
| --- | --- | --- |
| V1.1 | P0 | Combined Salary Estimate from Work Time: manual daily calendar hours, local monthly rate snapshots, and API gross estimates; see section 6A. API/web first, then mobile. Native verification gates mobile release approval. |
| V1.2 | P0 | Later tracker/payroll enhancements: clock-in/out, automatic shift interpretation, payslip comparison, backup/export. Separate specification and statutory-rule verification required. |
| V1.3 | P1 | Currency Exchange: KRW/MMK rate with source and update time, conversion, history, and remittance-fee estimate. Evaluate provider reliability, licensing, cost, rate staleness, and backend requirements before implementation. |
| V1.4 | P1 | Personal Finance & Reminders: savings, salary/expense and remittance records, payday and document-expiry reminders, and local notifications. Define local storage, notification privacy, and export/backup behavior first. |
| V1.5 | P2 | Worker Information Center: reviewed Myanmar tax, passport-renewal, and visa guidance with official references, verification dates, and an unofficial-app disclaimer. |

Login/cloud history, a verified-information assistant, additional languages, AdMob, and analytics remain optional later scope. Module cards do not authorize implementation of those features. The hub release label and whether it precedes the pending V1.0 Play publication remain Product Owner release decisions; the existing AAB is unchanged by this specification.

## 6A. Salary Estimate from Work Time — approved implementation scope

Status: implemented in local API/web/PWA and mobile source. Following web acceptance, mobile opens directly from Home, Services, and Search. Native verification is still required before release approval. Deliver API and web/PWA first, then mobile. This combined initial release supersedes the separate V1.1/V1.2 manual-record and estimate scopes; automatic clock-in/out, shift interpretation, payslip comparison, backup/export remain future work.

### Pay rules and contract

Gross monthly estimate (KRW) = full basic monthly salary + weekday overtime hours × overtime rate + Saturday worked hours × Saturday rate + Sunday worked hours × Sunday rate + night hours × extra night premium rate.

Collect the basic monthly salary plus normal, overtime, Saturday, Sunday, and night-premium hourly rates. Normal weekday hours are covered by the full base; the normal hourly rate is reference-only. Weekend rates are full payment, without another overtime component. Night premiums stack on weekday/weekend pay. Missing days add no hours and never deduct from the base. Exclude tax, insurance, absence deductions, partial-month proration, public-holiday rules, and automatic statutory rates. Clearly identify these as user-rate estimates rather than statutory payroll calculations.

`POST /v1/salary-estimates` accepts a selected `YYYY-MM` month, monthly settings, and unique dated work entries. Money and fractional hours use decimal strings. The stateless API owns categorization and all financial arithmetic, validates real dates/month membership, duplicates, money limits, and hour relationships, and returns categorized hours, pay components, raw and whole-won totals, formula version, assumptions, and rounding metadata. Preserve decimal precision and round down once for the displayed total. Existing severance contracts are unchanged; each client pins and regenerates its independent OpenAPI artifact.

### Calendar and local records

- Navigate months; edit/save monthly settings; add, edit, or delete one daily record containing normal, overtime, and overlapping night hours. Show a calendar and accessible date-list alternative.
- Hours are nonnegative decimal strings with at most two fractional digits. Normal plus overtime must be at most 24 per date; night hours cannot exceed their sum. Split overnight work onto actual dates. Use Korean calendar dates and timezone-independent weekdays. Saturday/Sunday pay uses normal plus overtime hours.
- Store one settings snapshot per month; new months may copy the latest earlier month's settings. Changes never modify another month. Initial fields use zero and remain editable.
- Persist this module's records/settings locally in IndexedDB (web) and SQLite (mobile). Disclose storage and selected-month API submission before the first save. No login/cloud sync. Provide confirmed delete-month and delete-all actions.
- This is an explicit exception to the financial session-memory policy for salary-module inputs only. Severance inputs/results remain session-only. Salary results also remain session-only; do not log, analyze, or service-worker-cache financial requests/responses.
- Recording/editing works offline. Calculating requires connectivity and explicit submission of the selected month only. Preserve drafts on request/storage failures, display retry/save status, and invalidate estimates whenever settings or records change. Ignore responses for outdated drafts.
- Support English/Burmese, Light/Dark, accessible labels/focus and touch targets, narrow screens, and persistence across restart. Local service navigation is enabled; native Android/iOS storage and behavior verification remains required before release approval.

### Acceptance

- Base 2000000 + weekday overtime 10 × 15000 + Saturday 8 × 20000 + Sunday 4 × 25000 + night 6 × 5000 = **2440000 KRW**.
- Cover normal weekday exclusion, weekend single payment, overlapping night premiums, zero/fractional inputs, rounding, leap days/month boundaries, invalid/duplicate dates, excess hours, month-isolated settings, storage failures/deletion/restart, stale results, offline/retry, localized accessibility, independent contract checks, cache exclusions, and severance regressions.

## 7. Feature acceptance criteria

- Match published MOEL calculation examples.
- Test eligibility boundaries, partial years, leap years, month ends, and final-working-day conversion.
- Test allowances, bonus inclusion, unused-leave-pay inclusion, and ordinary-wage comparison.
- Test DC yearly totals, partial-year wages, and separation of contributions from reported balances.
- Reject invalid dates, negative amounts, overlapping wage periods, and malformed requests.
- Confirm complex cases return review-required outcomes without misleading totals.
- Verify complete English/Burmese flows, including errors and result explanations.
- Test mobile layouts, accessibility, connectivity failures, retry behavior, and PWA cache exclusions.
- Verify the mixed Home carousel, sample-ad labels, combined Salary Estimate from Work Time card, service grid, footer without Profile, planned destinations, header actions, search, and module boundaries against section 5 on Android and iOS before releasing this local implementation.
- Verify the mobile launch logo/name, three-second minimum, readiness/fallback behavior, and that navigation or foregrounding does not replay the launch screen; check light/dark appearance and large text at narrow widths.
- Review implemented calculation rules against official sources before public release.

## 8. Product Owner release and design decisions

1. Confirm the combined Salary Estimate from Work Time dashboard label and its planned scope before release. The combined manual tracker/user-rate estimate scope is approved in section 6A; later automatic/statutory enhancements need separate approval.
2. Review the service order, English/Burmese copy, sample-ad previews, and Home visual direction before release. Actual advertiser content, an ad provider, consent design, placement, and impression tracking require separate approval and implementation.
3. Decide when Notices should contain real content and whether Profile should be added in a later milestone. Neither is a user account or notification system in this implementation.
4. Choose the hub's release milestone and whether it replaces the pending V1.0 Play submission or follows it in a later binary. Neither option changes the existing AAB automatically.
