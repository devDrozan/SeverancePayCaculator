# E9 Mate Myanmar — Feature Specification

## 1. Product and release scope

E9 Mate Myanmar is an everyday utility hub for Myanmar workers in South Korea. Its first released tool is the severance calculator; later employment, finance, and administrative tools will be independent mini-app modules inside the same installed application.

### Confirmed status and next target

| Area | Status |
| --- | --- |
| V1.0 severance calculation, guidance, and E-9 insurance content | Implemented in the active API, web/PWA, and mobile source. The Product Owner reports a production Android AAB built; Google Play publication remains pending. This specification does not certify the release artifact. |
| Mobile home dashboard and module shell | Implemented in the active local mobile source: compact E9 Mate header, mixed information/sample-ad carousel, service and Coming soon sections, Home/Services/Notices footer, local search, separate Severance and Insurance routes, and specific Coming soon pages. Profile is not present. Native device QA and release approval remain pending. The previously built AAB does not contain this change. |
| V1.1 Salary Estimate from Work Time | Combined manual calendar and user-rate salary feature is implemented in the active API, web/PWA, and mobile source under section 6A. The service opens directly in local mobile source; native release verification remains pending. Earlier unpublished tracker prototype work is not a released feature. |
| Expense calendar | Implemented in local web/mobile source under section 6B; native release verification remains pending, with separate local expense storage and no cloud sync. |
| V1.3 Currency Exchange | Available mobile service: CBM market-based Official Rate and unchanged user-entered Hundi Rate in both directions. Legacy web reference endpoints remain compatible. Hosting/native release verification remain separate; see section 6C. |
| V1.2, V1.4–V1.5, ads, and analytics | Planned only apart from the approved basic monthly expense calendar. No live modules, data collection, or monetization are implied by roadmap cards. |

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
- Keep severance inputs and results in session memory; persist only language and appearance preferences except the explicitly approved salary-module records/settings in section 6A and expense records in section 6B.
- The mobile app defaults to the system appearance, follows device theme changes until the user chooses Light or Dark, and remembers an explicit choice. Existing saved System preferences continue to follow the device; the appearance icon inside the header menu indicates the resolved appearance and toggles to the other mode. Changing appearance preserves the current calculation draft and step. Both themes cover navigation, forms, validation, results, guidance, and About in English and Burmese.
- The mobile header shows the compact E9 Mate brand and one 44dp hamburger Menu button. Tapping it opens a themed, scrollable popup containing the existing appearance, language, search, and About us actions with visible labels. Appearance switches Light/Dark immediately using existing preferences; Language reveals English/Burmese radio choices, and choosing a language closes the popup. Search dismisses the popup and opens the local service search. About us dismisses the popup and opens the About screen. Close, backdrop tap, and Android Back dismiss it; route changes reset popup state. Keep Home/module links in place and preserve calculation drafts, preference storage, accessible names/expanded/checked states, Burmese line height, and narrow/large-text layouts.
- Mobile About credits "Created by devrozan" and explains the hub's purpose: helping Myanmar workers in South Korea use practical employment, financial, and administrative tools. The current released scope remains severance and E-9 insurance information. Show a copyright notice with the current year and `devrozan` as the owner, without invented biography or profile links.
- Do not cache calculation requests or responses.
- Verify Burmese glyph rendering, line wrapping, and readable font sizes.
- Mobile hero headings preserve the translated wording and spaces without inserting forced line breaks. Use readable responsive typography, remaining on one line where it fits and wrapping naturally for longer wording or larger text instead of truncating or automatically shrinking it.
- Mobile About, guidance, and insurance prose must leave room for stacked Burmese marks using the font's natural iOS line metrics, wrap without truncation at narrow widths and larger text sizes, and separate explanatory paragraphs visibly. Informational cards use balanced top and bottom padding so text does not crowd the card edges.
- Use accessible labels, keyboard navigation, and touch-friendly controls.

### Privacy

- Do not request passport numbers, alien registration numbers, or bank details.
- Exclude salaries and calculation payloads from logs and analytics.
- The Android E9 Mate Myanmar privacy notice must distinguish local records/preferences from user-requested API submissions and Google Mobile Ads processing. The source-audited English draft and static, accessible website live in the root documentation repository under `privacy-site/`, with internal audit and Console/consent checklists in `compliance/`. No fourth application repository is introduced.
- The owner explicitly authorized interim publication on 9 November 2026 while additional information is pending. The live notice at `https://devdrozan.github.io/SeverancePayCaculator/` has effective date 9 November 2026 and privacy contact `rozannainghangu@gmail.com`; anonymous HTTPS HTML/CSS were verified against the approved source. Serve only three static files from the dedicated `codex/privacy-policy-pages` branch. Keep unresolved practices visible and retain separate app-release gates; interim publication is not compliance certification. Future content changes require authorization and an updated approved digest. Approval checks permit open items only for an explicitly authorized, visibly labelled interim notice with app release marked unready.
- Current Home source requests Google non-personalized test banners; do not infer no SDK collection from test IDs or NPA. Missing advertising-consent controls and an in-app privacy-policy link, production hosting/log-retention unknowns, and final native release verification remain release gaps documented in the audit. This policy-site task does not authorize changes to application features.

## 5. Mobile mini-app hub — implemented in local source, pending native QA

### Home dashboard

- After the existing branded launch screen, open **Home** as the normal entry point. Use a dark green, card-based visual style with a compact E9 Mate header, an illustrated hero carousel, an **Our Services** grid with colored feature icons, a smaller **Coming soon** section, and a fixed footer. Keep a legible Light variant as well. Home loads without the calculation API, an account, or personal information.
- The shared top bar shows the compact E9 Mate brand with clickable Light/Dark, Language, and Search icons. Appearance toggles immediately and follows the system until manually chosen. Language offers English/Burmese choices. Search filters the local module catalog by translated names and descriptions without sending queries to a server.
- Show **one** horizontally swipeable hero carousel with useful information and sample E9 Mate ads in a stable order. It automatically advances every **4 seconds** with smooth animation and continuous looping. The useful-information cards link to existing severance and E-9 insurance guidance. Sample-ad cards are visibly labelled **Sample ad · E9 Mate**, link only to existing E9 Mate services, and are preview content; they do not imply an advertiser, paid placement, live campaign, AdMob integration, or ad impressions. Show adjacent-card peeks, position dots, and accessible previous/next controls. Keep manual swiping and previous/next controls working, including wraparound in both directions. Use an adjacent-slide loop transition rather than an animated jump across the entire strip. Suspend the timer during manual interaction, while Home is unfocused, and while the app is inactive/backgrounded; restart a full four-second interval after interaction or returning to active Home. Respect reduced-motion preferences by using nonanimated transitions, and do not trap vertical scrolling.
- Under **Our Services**, show a responsive service grid ordered **Salary Estimate from Work Time**, **Expenses**, Severance Calculator, E-9 Insurance, and Currency Exchange. Salary is the priority feature by ordering; keep Home as the mobile entry screen and the severance calculator as the web entry screen. The combined salary card opens the implemented calendar and user-rate salary module directly; its scope is section 6A. Availability here describes local functionality, not native release certification. Currency Exchange opens the available converter with CBM Official Rate and the unchanged Hundi Rate. Available cards open their working service; planned cards open a specific Coming soon page without forms or permissions. Historical salary/work planned links redirect to the implemented salary module.
- Show a smaller **Coming soon** area for Finance & Reminders and Worker Information Center, each tappable with an honest planned destination. Keep About us reachable from the header menu.
- The footer shows **Home**, **Services**, and **Notices** only on hub pages. Home returns to the dashboard; Services shows the service catalog; Notices opens a clear empty state until real notices exist. **Do not show Profile** or a profile destination in this implementation. Footer navigation must not cover or interrupt the calculator or other module screens.

### Initial module catalog

| Service label | Home placement | Current status | Destination and scope |
| --- | --- | --- | --- |
| Salary Estimate from Work Time | Our Services, first | Available in local source; native release QA pending | Opens `/work` directly for calendar records, monthly settings, and API salary estimates. `/salary` and historical planned salary/work links redirect to the same module. Scope is section 6A. |
| Expenses | Our Services, immediately after salary | Available in local source; native release QA pending | Separate monthly local expense calendar; see section 6B. |
| Severance Calculator | Our Services | Available in local hub | Existing Normal, DB, and DC flows, in-module How it works guidance, results, assumptions, and official sources. No formula or API contract change. |
| E-9 Insurance | Our Services | Available in local hub | Existing departure-guarantee explanation and official EPS links. It remains informational and is not added to severance totals. |
| Currency Exchange | Our Services | Available | Opens `/exchange` directly with CBM market-based Official Rate and unchanged Hundi Rate, both directions with instant API recalculation. Older planned links redirect. See section 6C. |
| Finance & Reminders | Coming soon | Coming soon | Specific planned-service page. V1.4 scope remains in section 6. |
| Worker Information Center | Coming soon | Coming soon | Specific planned-service page. V1.5 scope remains in section 6. |

### Module and navigation boundaries

- A mini-app is an independently navigable **feature area inside one E9 Mate Myanmar installation**, not a separately installed application or remotely downloaded code package. The shared shell owns Home, Services, Notices, global navigation, language, appearance, search, About, and common accessibility/privacy behavior. Each module owns its screens, content, feature state, tests, and any feature-specific storage or service integration.
- Use a local module catalog with stable identifiers, localized metadata, availability, section, and destination routes. Retain old salary planned links as aliases to the combined Salary Estimate from Work Time destination. Adding a module must not require changing another module's calculation logic or stored data. Modules may share established shell services and intentional interfaces; they must not reach into another module's private state or database tables.
- Opening an available card enters that module. A visible Home action and Android/iOS back navigation return from its entry screen to Home; in-module Back continues to follow the feature's existing flow. Home and module switching must not reset a calculator draft. Closing the app still clears V1.0 financial inputs and results as required in section 4.
- Preserve working access to the existing calculator, guidance, insurance, and About destinations during migration. Existing external/deep links, if supported, must open or redirect to the corresponding module page. Guidance belongs inside the Severance module.
- Do not make Home or unrelated modules depend on the severance API's availability. A calculator outage shows a retry state within that module. Later offline work records remain local to their approved module. Cross-module reuse, such as salary estimates reading work logs, needs an explicit interface, user disclosure, and separate approval; salary/severance calculations continue to run in the API, with only local expense-record aggregation permitted by section 6B.

### Hub acceptance criteria

- On 320–360dp Android layouts and iPhone sizes, the compact header, hero carousel, service cards, planned badges, and footer remain readable in English and Burmese, Light and Dark, and larger text. Service-card headers place the existing icon and wrapping title on the same row, vertically centered with consistent spacing; preserve icon size, title styling, colors, and actions. Available-service cards use content-driven height with a tighter header and no empty planned-status spacer, reducing excess vertical space. Planned/Coming soon cards retain their existing spacing, size, and badge layout. The grid may use one column at narrow width, in Burmese on phones, or with larger text. Cards grow with content; Burmese marks must not clip. Touch targets are at least 44dp and screens respect safe areas.
- Screen readers announce hero card labels and positions, service names, availability, and actions. Previous/next controls work without swipe gestures; focus moves predictably on opening a service and returning Home. Reduced-motion settings are respected.
- The carousel advances once per four seconds on active Home and loops smoothly from the last card to the first and back with manual navigation. Manual dragging pauses autoplay and resets its countdown after settling; backgrounding, leaving Home, and unmounting stop its timer. Resize and language/theme changes keep its logical selected card. Reduced-motion transitions are static. It cannot trap vertical scrolling. Every service is discoverable in the grid or Services page without swiping.
- Available services open the expected feature and return Home without losing permitted session state. Planned services open their own honest Coming soon pages and cannot be mistaken for released features. Native release verification remains a separate requirement for implemented local modules. Notices has an explicit empty state; no Profile item appears. Search handles an empty query and no results. A failed module load does not prevent Home or other modules from working.
- Existing V1.0 calculator examples, API errors, source links, language/theme preferences, privacy behavior, and insurance separation pass regression checks. No new native storage, backend hosting, analytics, or paid advertising is required for this hub shell; salary-module storage is separately authorized in section 6A.

## 6. Planned modules and future scope

| Milestone | Priority | Planned module, subject to separate implementation and release approval |
| --- | --- | --- |
| V1.1 | P0 | Combined Salary Estimate from Work Time: manual daily calendar hours, local monthly rate snapshots, and API gross estimates; see section 6A. API/web first, then mobile. Native verification gates mobile release approval. |
| V1.2 | P0 | Later tracker/payroll enhancements: clock-in/out, automatic shift interpretation, payslip comparison, backup/export. Separate specification and statutory-rule verification required. |
| V1.3 | P1 | Available mobile Currency Exchange: CBM market-based Official Rate and unchanged Hundi Rate, both directions. Legacy web reference endpoints remain compatible; source freshness, caching and native release checks are defined in section 6C. |
| V1.4 | P1 | Personal Finance & Reminders: savings, extended salary/remittance records, payday and document-expiry reminders, and local notifications. The basic local expense calendar is now approved separately in section 6B. Define local storage, notification privacy, and export/backup behavior first. |
| V1.5 | P2 | Worker Information Center: reviewed Myanmar tax, passport-renewal, and visa guidance with official references, verification dates, and an unofficial-app disclaimer. |

Login/cloud history, a verified-information assistant, additional languages, AdMob, and analytics remain optional later scope. Module cards do not authorize implementation of those features. The hub release label and whether it precedes the pending V1.0 Play publication remain Product Owner release decisions; the existing AAB is unchanged by this specification.

## 6A. Salary Estimate from Work Time — approved implementation scope

Status: implemented in local API/web/PWA and mobile source. Following web acceptance, mobile opens directly from Home, Services, and Search. Native verification is still required before release approval. Deliver API and web/PWA first, then mobile. This combined initial release supersedes the separate V1.1/V1.2 manual-record and estimate scopes; automatic clock-in/out, shift interpretation, payslip comparison, backup/export remain future work.

### Pay rules and contract

Gross monthly estimate (KRW) = full basic monthly salary + weekday overtime hours × overtime rate + Saturday worked hours × Saturday rate + Sunday worked hours × Sunday rate + night hours × extra night premium rate.

Collect the basic monthly salary plus normal, overtime, Saturday, Sunday, and night-premium hourly rates. Normal weekday hours are covered by the full base; the normal hourly rate is reference-only. Weekend rates are full payment, without another overtime component. Night premiums stack on weekday/weekend pay. Missing days add no hours and never deduct from the base. Exclude tax, insurance, absence deductions, partial-month proration, public-holiday rules, and automatic statutory rates. Clearly identify these as user-rate estimates rather than statutory payroll calculations.

`POST /v1/salary-estimates` accepts a selected `YYYY-MM` month, monthly settings, and unique dated work entries. Money and fractional hours use decimal strings. The stateless API owns categorization and all financial arithmetic, validates real dates/month membership, duplicates, money limits, and hour relationships, and returns categorized hours, pay components, raw and whole-won totals, formula version, assumptions, and rounding metadata. Preserve decimal precision and round down once for the displayed total. Existing severance contracts are unchanged; each client pins and regenerates its independent OpenAPI artifact.

### Calendar and local records

- Both salary and expense calendars use a compact, responsive Monday–Sunday grid with aligned weekday columns and week rows, rounded date cells, subtle theme borders, and a clear selected-date highlight. Use centered month/year headers with previous/next arrows, avoid fixed-width horizontal calendar overflow, and retain salary’s accessible date-list alternative. Expense dates retain their small record indicator and daily total; selected-date records, exact total, and an Add Expense action appear below the calendar. Preserve all existing storage, calculation, acknowledgement, and editing behavior.

- Selecting a salary calendar date (or its date-list alternative) opens an accessible popup. New dates open normal, overtime, and overlapping night-hour inputs; existing recorded dates show their hours with Edit working hours. Stage edits separately; Save working hours validates and saves the current monthly snapshot locally, then updates the calendar, invalidates any estimate, and closes. Cancel/Close discards staged changes. Preserve the existing storage disclosure/acknowledgement, include it within the popup when needed, and explain that Save stores settings and all current monthly work records. Failed validation/storage keeps the popup and staged values; block dismissal and duplicate submissions while saving. Preserve themes, bilingual labels, keyboard/Back handling, focus, and a scrollable narrow-screen layout.
- Navigate months; edit/save monthly settings; add, edit, or delete one daily record containing normal, overtime, and overlapping night hours. Show a calendar and accessible date-list alternative.
- Hours accept the ways users type time: a whole number through 24 is hours; a whole number above 24 is minutes; decimal values are hours; `H:MM` is clock hours and minutes. Examples: `8` = 8 hours, `1.5` and `1:30` = 90 minutes, `30` = 30 minutes. Normalize accepted input to at most two decimal hours before validation, local storage, and API submission. Normal plus overtime must be at most 24 per date; night hours cannot exceed their sum. Split overnight work onto actual dates. Use Korean calendar dates and timezone-independent weekdays. Saturday/Sunday pay uses normal plus overtime hours.
- Provide optional annual-leave tracking per calendar year, stored locally with the salary module and never included in the salary API payload. Ask whether the employer provides paid annual leave: **Yes**, **No**, or **Not sure**. Yes reveals an available-days field (0–365, up to two decimals), used and remaining days across all months of the selected year, and a non-working-date paid-leave toggle in the day popup. No hides the leave inputs and shows a notice that Korean labor law may still provide annual leave and unused-leave pay. Not sure shows a brief Labor Standards Act eligibility guide. Saving a leave-marked day clears its work hours and records the date as used leave. Do not add unused leave pay to the monthly salary estimate. Leave records are cleared by delete-all; deleting one salary month does not erase annual-leave marks.
- Monthly Pay Settings opens as an editable section with a Save pay settings action. Use the existing monthly local-save validation and storage disclosure. Only after a successful settings Save, collapse all six inputs into a compact saved-state heading and Edit pay settings button; Edit reopens the same values. Retain expanded/collapsed state per month during the session, reopen for settings validation/API errors, and keep fields expanded on failed saves. New months start expanded. General Save Month retains its existing behavior.
- Store one settings snapshot per month; new months may copy the latest earlier month's settings. Changes never modify another month. Initial fields use zero and remain editable.
- Persist this module's records/settings locally in IndexedDB (web) and SQLite (mobile). Disclose storage and selected-month API submission before the first save. No login/cloud sync. Provide confirmed delete-month and delete-all actions.
- This is an explicit exception to the financial session-memory policy for salary-module inputs only. Severance inputs/results remain session-only. Salary results also remain session-only; do not log, analyze, or service-worker-cache financial requests/responses.
- Recording/editing works offline. Calculating requires connectivity and explicit submission of the selected month only. Preserve drafts on request/storage failures, display each action's status and failure beside the button that produced it, scroll the finished estimate into view, and invalidate estimates whenever settings or records change. Ignore responses for outdated drafts. Mobile requests have a 15-second deadline covering response-body reading and parsing; timeouts preserve inputs and allow retry. On a valid calculation, dismiss the keyboard and reveal the measured estimate block once native layout is ready; layout arriving after the response must still reveal the result. Reduced-motion preference failures use static scrolling.
- Support English/Burmese, Light/Dark, accessible labels/focus and touch targets, narrow screens, and persistence across restart. Local service navigation is enabled; native Android/iOS storage and behavior verification remains required before release approval.

### Acceptance

- Base 2000000 + weekday overtime 10 × 15000 + Saturday 8 × 20000 + Sunday 4 × 25000 + night 6 × 5000 = **2440000 KRW**.
- Cover normal weekday exclusion, weekend single payment, overlapping night premiums, zero/fractional inputs, clock-time and minute-only hour entry, rounding, leap days/month boundaries, invalid/duplicate dates, excess hours, month-isolated settings, annual-leave policy/entitlement/used/remaining tracking across months and years, storage failures/deletion/restart, stale results, offline/retry, localized accessibility, independent contract checks, cache exclusions, and severance regressions.

## 6B. Priority salary navigation and expense calendar

Implemented in local web/PWA and mobile source; native release verification remains pending. Keep existing entry screens: web opens Severance Calculator and mobile opens Home. Move Salary Estimate from Work Time first in web navigation and mobile catalog/service/search ordering. Expenses follows salary, then the remaining existing services. Do not reset drafts when switching tools; priority is ordering, not a changed start screen or extra featured banner.

### Expense records and behavior

- Provide a separate Expenses screen centered on an interactive monthly calendar. Use a localized month heading, previous/next month controls, weekday headings, real dated cells, and a visible selected date. Tapping a date reveals its saved expenses and Add Expense action. Add Expense opens a popup with Category, Description, and Amount for that date; Edit uses the same popup with existing values. Save closes only after successful local persistence and immediately updates the date's list/total. Invalid inputs or write errors retain the open popup for correction/retry. Close keeps the per-date draft in session memory without saving, and dismissal is blocked while saving. Preserve accessible focus, keyboard/Android Back handling, scrolling, bilingual themes, and the local-storage notice before Save. Saved records are ordered by stable identifier. Show an initial select-date prompt until a date is chosen; retain the selected date during tool switches. Each record has a unique local identifier, a real Korean calendar date (`YYYY-MM-DD`, years 1900–2099), required description (1–120 trimmed characters), category, and positive KRW decimal-string amount (up to 15 integer digits and 6 fractional digits). Preserve the entered decimal text for display; do not convert money through binary floating point.
- Categories are Food, Housing, Transport, Utilities, Health, Remittance, and Other, with stable machine identifiers and English/Burmese labels. Category names do not imply bank connections or transfers.
- Add, edit, and save individual records; delete a record, selected month, or all expense records only after explicit confirmation. Save/delete failures retain the prior list and entered form, report the error near the action, and allow retry. New and edited expenses belong to the selected calendar date. The date is displayed as a heading rather than an editable form field. Keep separate unsaved forms per date while switching dates/months/tools; returning to a date restores its draft. Editing or deleting one record must not replace another date's draft.
- Save only on explicit user action, with a visible disclosure stating that Save confirms storage on this device. Do not require manually checking the acknowledgement. Display the local-storage acknowledgement as a read-only checkbox/status; successful Save automatically checks it and persists acknowledgement together with the record where acknowledgement metadata is stored. Validation or write failures must not newly check it. Previously acknowledged storage restores its checked state; delete-all clears it. Persist records locally in an independently versioned IndexedDB database on web and SQLite database on mobile. Explain that records stay on this device/browser, browser-data clearing or uninstalling removes them, and there is no cloud sync. Do not request identity numbers, bank details, or financial attachments.
- Expense records, including descriptions, are never sent to the API, logs, or analytics. This is a scoped exception to the financial-input session-only policy. Severance and salary calculation results remain session-only. Expense deletion must not alter salary records or preferences.
- Calendar browsing, daily totals, validation, adding/editing, saving, and deleting work offline. Group saved records by their Korean calendar date and sum their decimal-string amounts exactly on the device; this is a narrowly approved exception for expense-record aggregation only. Never use binary floating-point money arithmetic. Totals are derived from saved entries and immediately reflect successful saves, edits, and deletions; failed writes leave totals unchanged. Individual amounts retain their accepted decimal text, and totals normalize trailing fractional zeros without rounding away precision. Display each populated date's expense marker/count and daily total in its calendar cell; if space requires a compact/approximate cell label, label it clearly, announce the exact total accessibly, and show the complete exact daily total above the selected date's list. Do not add salary deductions, budgets, conversion, recurring entries, or notifications.
- Show clear empty/loading/saved/unsaved/error states, localized field errors, accessible focus and touch targets, complete amounts, and narrow-screen English/Burmese layouts. Reuse each client's established appearance; mobile follows global Light/Dark and web expense appearance supports Light/Dark preferences.

### Acceptance

- Salary appears first and Expenses second in both clients, while their initial screen remains unchanged and existing calculator drafts survive navigation.
- Existing records remain available after this update and after restart, including exact decimal amounts and categories. Dates with multiple records show an exact combined daily total; test 0.1 + 0.2 = 0.3 and sums beyond binary-number precision. Selecting an empty date shows an honest empty state and an add form. Edits and deletion affect only intended records/dates/months.
- Reject missing/overlong descriptions, invalid/leap-day dates, unsupported categories, zero/negative/malformed/excessive amounts, corrupt storage, and duplicate identifiers without overwriting saved data.
- Cover calendar month/leap-year boundaries, per-date draft retention, selected-date CRUD and total updates, automatic acknowledgement only after successful Save, deletion cancellation, storage read/write failures and retry, offline use, bilingual accessibility, and separation from salary/severance storage. Verify expense data never enters API requests or caches as a network payload.

## 6C. Currency Exchange — available mobile service with CBM Official Rate

Status: approved for available mobile navigation on **14 November 2026**. Home, Services and local search open `/exchange` directly; historical `/coming-soon?id=exchange` links redirect there. Remove the mobile Preview/Coming soon status without changing the Home entry screen or service order. Availability describes the implemented feature; backend hosting, signed native release checks and store publication remain separate.

### Official Rate source and arithmetic

- Mobile Official Rate uses CBM's published KRW indicative cross rate corresponding to the **Market Trading Rate** column from <https://forex.cbm.gov.mm/index.php/fxrate>. Attribute Central Bank of Myanmar and link the original page. It is an indicative published rate, not a guaranteed cash/remittance payout or transaction offer.
- CBM quotes MMK per **100 KRW**. Preserve that original decimal as `mmkPer100Krw`; calculate `mmkPerKrw = mmkPer100Krw / 100` exactly on the API. Never derive the market rate from a rounded reciprocal or the reference column.
- Fetch <https://forex.cbm.gov.mm/api/latest> separately to validate the website's **Reference Rate** and publication date. The JSON KRW unit comes from the matching website row, not an API units field. Keep reference and market rates distinct; the Reference Rate is never an automatic fallback for Official Rate calculations.
- With R = MMK per 100 KRW, compute **KRW → MMK = amount × R / 100** and **MMK → KRW = amount × 100 / R**, using decimal.js at 80 significant digits. Floor only once for the displayed result: 2 decimal MMK or whole KRW. Return a below-display-precision flag when appropriate.
- Dated acceptance fixture (CBM publication 13 November 2026, not a future live guarantee): R = `273.88` gives `2.7388` MMK per KRW; `100000` KRW → `273880.00` MMK; `273880` MMK → `100000` KRW. Reference `157.14` per 100 KRW → `1.5714`; it must not replace R.

### Existing Hundi Rate — unchanged

- Retain the existing mode, user MMK/USD input, editable USD/KRW input and default `1350`, reset action, bounds and field errors.
- Retain **KRW → MMK = amount × MMK/USD ÷ USD/KRW**, and **MMK → KRW = amount × USD/KRW ÷ MMK/USD**, with existing API-only precision, rounding and result metadata.
- Hundi requires no upstream rate provider and continues working through the calculation API when the CBM source is unavailable. Do not modify its endpoint, validation, calculation version, privacy or behavior as part of CBM integration.

### API and compatibility

- Add `GET /v1/exchange-rates/krw-mmk/cbm` with optional `refresh=true`, and `POST /v1/currency-conversions/cbm` with the existing `from`, `to`, decimal-string `amount` input bounds (up to 15 integer digits and 2 fractional digits).
- The API selects/validates the snapshot; clients cannot supply a CBM rate. Return provider `cbm`, type `MARKET_TRADING`, source link/name, original and normalized market/reference values, publication date, date-only precision, source timezone `Asia/Yangon`, retrieval/expiry times, freshness, quote ID, calculation version `krw-mmk-cbm-market-1`, precision and rounding.
- Preserve legacy Korean reference endpoints and their contracts for existing web/older clients. Keep `/v1/currency-conversions/hundi` unchanged. CBM integration is additive, not a silent new interpretation of an old reference quote.
- Promote the backend-only CBM experiment's validated parsing/fetch/cache implementation into API source; keep the experimental runner working against the promoted code instead of maintaining two production parsers. Mobile owns a separately copied OpenAPI artifact and regenerated types. No cross-repository imports.

### Fetch, cache and failure behavior

- Fetch only fixed official HTTPS URLs server-side, without user financial inputs, credentials, browser scraping on the client, redirects or background polling. Validate expected HTML/JSON content types and cap bodies at 256 KiB / 64 KiB. Bound each whole request, including body, to 10 seconds.
- Reject changed headers/units, missing/duplicate KRW rows, zero/negative/malformed rates, missing/invalid/future dates and website/API date or reference-value mismatches. Return structured translated failures; never fabricate or substitute a rate.
- Cache only validated public snapshots in process memory for 15 minutes; share concurrent retrievals and space attempts by at least 60 seconds. Honor a longer numeric upstream Retry-After up to one hour. Refresh bypasses a valid cache only when the minimum interval permits. Cache hits preserve retrieval time; failures never make old data newer. Do not return an expired cached snapshot after a failed retrieval.
- Determine publication freshness in **Asia/Yangon (MMT, UTC+06:30)**: today is Published today, ages 1–3 calendar days are Previous published rate, and older publications expire at Myanmar midnight. Reject future publications. This is a conservative product freshness limit, not a CBM update guarantee. Distinguish date-only publication from retrieval time; do not invent a publication instant from the API timestamp.

### Mobile flow and privacy

- Preserve English/Burmese, Light/Dark, accessible inputs/source links, both directions, exact input text and 400ms debounced API calculation. Keep the amount when swapping or switching modes; ignore late responses for changed inputs and retain input after offline/server failures.
- Replace the Preview eyebrow and Korean-reference copy with available currency-service wording. Show the original `100 KRW = R MMK`, normalized `1 KRW = r MMK`, CBM market-based label, source, MMT publication date, and MMT retrieval time. Show the API-validated reference value separately and explicitly mark it as comparison-only.
- Existing local preferences/records remain unchanged. Currency amounts/rates/results stay in session memory and financial requests/results are no-store and excluded from logs/analytics. Only requests to our calculation API include financial inputs; upstream CBM requests never include them.
- Reuse the existing Hundi layout/functionality; retain readable narrow/large-text layouts, field validation, error/retry and unavailable-source states. Removing Coming soon does not claim guaranteed network availability.

### Verification

- Test both CBM directions, precise fractional/max/tiny inputs, rounding and no reference-rate substitution; date/quote integrity, Myanmar midnight, cache expiry/shared requests/refresh/backoff, body timeout/size/status failures and source mismatches.
- Keep the existing Hundi tests passing unchanged and verify its request shape/version/default behavior. Verify legacy reference and severance/salary contracts and regressions.
- Verify available service-card/search navigation, legacy redirect, English/Burmese labels, MMT metadata, offline/error retention and late-response handling. Run API tests/type checks and mobile tests/lint/type checks independently. No build, push or deployment is requested by this change; report native runtime checks separately.

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

## Mobile calendar defaults, banners and shared storage acknowledgment (2026-11-15)

- On the initial visit to a calendar feature, select today using the Asia/Seoul calendar date without automatically opening an editor. Preserve deliberate session selections and drafts. In other browsed months select day 1 when no session selection exists; returning to the current month defaults to today. Applies to work/salary, annual leave within that calendar, and expenses.
- Mobile feature routes (salary/work, expenses, severance and guide, insurance, currency exchange) have one adaptive AdMob test banner in reserved normal layout space below their content and above the footer, within the safe area. Home retains its existing banner. Do not overlay controls or add refresh timers. Collapse failed ad slots; ad failure never blocks a feature. Production ad-unit setup and advertising consent remain separate release work.
- Mobile uses one versioned app-wide local-storage acknowledgment preference. Explain local work/pay/leave/expense storage and API submission of calculation inputs before acknowledgment; this is not advertising consent. Hide the notice in every feature after acceptance. Salary accepts explicitly; a successful expense Save automatically accepts, while invalid or failed expense saves do not. Preserve legacy acknowledgments from either module, migrating metadata only. Deleting records/months does not reset acceptance. Clearing app data/uninstalling resets it. Preference-write failure retains financial records and offers retry. This supersedes mobile-only per-module checkbox/reset behavior above; web is unchanged.
- Verify Korean-date boundaries, retained session drafts, shared acceptance across feature switches/restart, legacy migration, deletion, preference failures, and banner routing/layout/test units. No build or publication is part of this change.
