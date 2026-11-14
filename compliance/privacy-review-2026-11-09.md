# E9 Mate Myanmar privacy evidence review

Reviewed: **9 November 2026 (Asia/Seoul)**. Current status: **interim policy published by subsequent explicit owner instruction; app/advertising release gaps remain**. Earlier draft-only findings below record the pre-publication review. This is an evidence review, not legal certification or a guarantee of Google approval.

## Scope and limits

Inspected the current dirty working trees, including untracked implementation files, dependency lockfile and installed native SDK configuration, mobile routes/source/configuration, calculation API handlers, storage adapters and deletion paths, and archived Android artifacts. Baseline commits: root `1926cbb940d7fb9f17fcf3b7fe0c539e04e9767f`, mobile `5c5a0d61f886963a5fb4745e4466ef995414e88b`, API `aa4d1c2559394c8f8e58a9832582aab878c852b4`. Findings describe current source, including changes after those commits.

No signed production APK/AAB, production runtime traffic capture, Play Console disclosure export, AdMob account configuration, hosting-provider configuration, or hosting logs were available. An archived debug artifact is not proof of release behavior. No app features, SDKs, permissions, or dependencies were modified for this task. No policy has been published.

The owner supplied privacy contact **rozannainghangu@gmail.com**. No different Play developer identity was supplied. Production API operator/location/log retention, support-email retention, target countries/ages and mediation settings remain owner confirmations.

## Findings

| Priority / status | Area and evidence | Consequence / required action |
| --- | --- | --- |
| P1 · Observed gap | **Consent:** [HomeBannerAd.tsx:13](../mobile/src/components/HomeBannerAd.tsx#L13) renders a Google test banner with NPA at line 17; [HomeScreen.tsx:22](../mobile/src/modules/hub/HomeScreen.tsx#L22) mounts it on Home. No app calls to AdsConsent/UMP update, consent-form presentation, canRequestAds gating, or privacy-options UI were found. | Test IDs/NPA do not replace required consent. Implement and verify the appropriate flow before advertising release; the policy describes the current gap. Storage acknowledgments are unrelated. No fix was made because app changes are excluded. |
| P1 · Observed gap | **Policy access:** no in-app privacy-policy link was found in routes, About, header/footer or source. | Add a permanent accessible link in a later authorized app change. A website and Play Console link alone do not provide in-app access. |
| P1 · Unverified | **Production service:** [mobile client:6](../mobile/src/api/client.ts#L6) guards production requests with HTTPS; [API server:15](../api/src/server.ts#L15) disables request logging. [index.ts:6](../api/src/index.ts#L6) still emits startup messages/errors. Host, reverse-proxy/CDN logs, processing region, subprocessors and retention are unknown. | Confirm those operational facts before finalizing publication or selecting ephemeral processing / encryption declarations. Do not claim all server layers retain nothing or all application logging is disabled. |
| P1 · Unverified | **Release permission/backup facts:** [app.json:21](../mobile/app.json#L21) sets allowBackup=false. Archived debug native files contain permissions/metadata inconsistent with the current package, including obsolete SecureStore traces and cleartext debug configuration. | Inspect the final release merged manifest, resolved Gradle dependencies and signed artifact; test backup/migration. Do not infer release access from archived/debug files. |
| P2 · Supported limitation | **Local encryption:** [app.json:42](../mobile/app.json#L42) enables SQLCipher capability, but [work storage:6](../mobile/src/modules/work/storage.native.ts#L6) and [expense storage:7](../mobile/src/modules/expenses/storage.native.ts#L7) have no key setup. | No evidence supports an encrypted-database claim. Secure deletion pragmas are not a forensic-erasure guarantee. Draft avoids both claims. |
| P2 · Observed documentation mismatch | **Advertising:** mobile README’s “no paid ads run yet” describes monetization, while current Home source actually requests Google test ads. | Do not convert that statement into “no advertising network requests” or “no SDK collection.” Reconcile release copy with final ad behavior. |
| P2 · Unverified owner practice | **Retention:** API infrastructure and support-mail retention are not established. | Confirm actual practices and replace the corresponding visible draft limitations; do not invent durations. |

Google’s [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en) requires a public policy with developer/app identity, contact, data handling and retention/deletion information, accessible from the app and Console. A public policy does not by itself establish consent or accurate declarations. Official requirements reviewed on 9 November 2026.

## Six audit areas

### 1. File permission

No app JavaScript runtime requests were found for camera, microphone, contacts, personal files, photos, precise location or biometric use. This is a source-level finding, not proof that every merged permission is absent. The installed advertising wrapper manifest requests Internet, network state and wake lock. Advertising-ID and Ad Services permissions may be merged from Google dependencies; check the exact release manifest and declaration.

The archived `mobile/android-backup` tree includes external-storage/overlay and other development-related permissions. Its debug artifact and SecureStore/Updates traces differ from current source and do not establish production needs. Review/remove unnecessary permissions in a separate app-release task. No broad file-access workflow was found that would justify all-files access. Reference: [Google Play sensitive permissions](https://support.google.com/googleplay/android-developer/answer/16558241).

### 2. Data collection

The app receives user-entered employment dates/hours, wage and pension details, pay settings, work records and expense records. There is no implemented login/account, bank connection, identity-document field or payment flow. Preference values and disclosure flags are also stored. Ads have an independent technical data flow; absence of names or accounts does not make financial inputs or SDK data irrelevant to privacy disclosures.

### 3. Server upload

| Flow | Trigger and data | Recipient / supported retention |
| --- | --- | --- |
| Employment context | Continue/prepare: calculation method, start/last-work dates, weekly hours, adjustment flag | Configured API; application processes in memory |
| Severance / pension estimate | Calculate: employment context, wage periods, base/allowances, bonuses/leave pay/ordinary wage, or yearly DC wages and optional balance/date | Configured API; no application database or saved result history |
| Work-time salary estimate | Calculate/Retry: selected month, monthly pay settings, dated normal/overtime/night hours | Configured API; selected month only |
| Currency preview | Public metadata GET; Convert POST contains amount and pair only | API; rate-source request is server-only and excludes user amount; live source is currently gated/unconfigured |
| Expenses | Save/edit/delete and exact daily totals | Local SQLite; no expense API call found |

Evidence: [client.ts:54](../mobile/src/api/client.ts#L54), [client.ts:65](../mobile/src/api/client.ts#L65), [exchange API:20](../mobile/src/modules/exchange/api.ts#L20), [API server](../api/src/server.ts), [rate adapter](../api/src/exchange.ts). Requests expose network metadata to the endpoint. API request limiting keeps request identity in memory. No body logging or financial result cache was found; responses use no-store. Infrastructure behavior remains outside this source guarantee.

### 4. Third-party SDKs

| Locked dependency / installed configuration | Privacy-relevant role |
| --- | --- |
| Expo 58.0.21 / React Native 0.88.1 | App/native runtime; final binary must be checked |
| react-native-google-mobile-ads 17.4.0 | AdMob wrapper; installed package defaults to Android classic GMA 25.5.0 and UMP 4.0.0, not proof of final Gradle resolution |
| expo-sqlite 58.0.14 / AsyncStorage 2.2.0 | Local financial records and preferences |
| expo-router 58.0.28 / expo-linking 58.0.15 | Navigation and external links |
| expo-font 58.0.11 / Noto Sans Myanmar 0.4.2 | Bundled font assets; no runtime remote font integration found |
| expo-splash-screen 58.0.12 / expo-dev-client 58.0.18 | Launch/development capabilities; debug is not a release artifact |
| openapi-fetch 0.14.1 | Typed API transport |
| React/form/translation/validation libraries | UI/state/input handling; no independent telemetry integration identified |

No separate Firebase Analytics, Sentry, account SDK, Expo Updates or SecureStore integration was found in current application dependencies. UMP is present through the ad package but unused by app source. Package presence/absence cannot establish all native runtime traffic. Use the installed version’s [Google SDK disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure) and the final native dependency tree for Console declarations. The policy lists SDK data categories; NPA remains distinct from consent under [Google’s NPA guidance](https://support.google.com/admob/answer/7676680?hl=en).

### 5. Data storage

- Work data: `e9-work-time.db`; monthly payload and disclosure flag. [Native adapter:12](../mobile/src/modules/work/storage.native.ts#L12), delete-month/all at lines 36–40. Prior settings may be copied into a new month; editing remains isolated.
- Expense data: `e9-expenses.db`; record ID/date/category/description/decimal amount and disclosure flag. [Native adapter:13](../mobile/src/modules/expenses/storage.native.ts#L13), deletion at lines 48–65.
- Preferences: [theme.tsx](../mobile/src/theme.tsx), [i18n.ts](../mobile/src/i18n.ts) use AsyncStorage for appearance/language.
- Severance drafts and calculation outputs: session state; no persistent history found. Currency preview values/results are session-only. Process lifetime can outlast a foreground visit.
- No app-managed cloud sync or export/backup exists. Android backup is disabled in configuration, but [Android’s backup documentation](https://developer.android.com/identity/data/autobackup) qualifies manufacturer device-to-device behavior. OS migration and app-switcher snapshots were not tested.
- `secure_delete` and a work delete-all WAL checkpoint do not justify guaranteed erasure. Enabling SQLCipher support alone does not key a database; see [Expo SDK 58 SQLite](https://docs.expo.dev/versions/v58.0.0/sdk/sqlite/).

### 6. Privacy policy

The new draft separates local/off-device flows, financial/API retention from advertising retention, and website hosting from app behavior. It identifies the app, package, proposed date and owner-supplied email. It includes Google policy/ads links, consent limits, deletion controls, backup/security qualifications and contact. It intentionally remains visibly draft while operational facts are unknown.

The static site has no client tracking or external assets. GitHub hosting still receives connection metadata; the draft links [GitHub’s statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). It does not falsely promise zero website data processing.

## Data Safety cross-check and inconsistencies

No submitted Console or AdMob account disclosures were available, so this is a source-to-disclosure comparison, not a claim to have inspected those dashboards.

- “No data collected” would conflict with API submissions and advertising.
- “All calculations are offline” would conflict with context/estimate requests.
- “All salary information is session-only” would conflict with saved work-module settings; existing severance-only “no saved salary history” copy must not be generalized.
- “NPA means no identifiers/consent necessary” is unsupported.
- “Encrypted local database” is unsupported by current key handling.
- “No data ever leaves the device / zero retention at every layer” is unsupported by SDK, API and unknown infrastructure behavior.
- An app-wide saved-expense upload or purchase-history declaration is not supported solely by the local expense feature. Free-text descriptions remain user-controlled local data.

Use [the Play checklist](google-play-checklist.md) for a qualified per-type mapping, including ephemeral processing and service-provider exceptions. Use [the AdMob checklist](admob-checklist.md) for consent and release checks. Publication approval and app release approval are separate decisions.

## Verification record

### Owner-authorized interim publication — 9 November 2026

The owner explicitly requested publication now with updated information to follow. Published only `index.html`, `styles.css` and `.nojekyll` on `codex/privacy-policy-pages`, commit `693ba4ead5ae741ff1dab611454bdfbabba5cce1`; main and application submodules were not changed. GitHub Pages was previously disabled, then configured to that branch root with HTTPS enforced. [Deployment](https://github.com/devDrozan/SeverancePayCaculator/actions/runs/42627769135) succeeded. [Public policy](https://devdrozan.github.io/SeverancePayCaculator/) and stylesheet both returned 200 anonymously over HTTPS with bytes matching the reviewed files. The rendered page visibly identifies its interim status, current date/app, contact and unresolved practices. Approval applies to interim publication only, with `appReleaseReady: false` and open items preserved. No Play/AdMob declaration was submitted or app behavior changed. The GitHub connector could not write; normal Git authentication published the isolated branch and the signed-in browser configured Pages.

### Focused configuration follow-up — 9 November 2026

Inspected local environment files with values redacted, the production EAS profile, Docker startup and request handlers, installed in-memory rate-limit store, rate cache, dependency/ad configuration and current Google guidance. Corrected “application logging is disabled” to distinguish disabled request logging from actual startup/error console output. No production host can be identified from local files; online EAS settings were not verified. No extra ad SDK/adapter was found, which does not establish all account-side partners. [Configuration findings and plain-language explanations](configuration-verification.md) record the evidence and reduce owner questions to deployment status/service, AdMob account additions and email retention. No app changes or publication were performed.

### Second policy review and corrections — 9 November 2026

- **P2 · Fixed policy omission:** the severance input inventory now explicitly includes the yes/no `hasSpecialCircumstances` flag submitted in context and estimate requests. It does not imply that detailed leave or settlement records are collected. Evidence: [API schema:16](../api/src/schemas.ts#L16), [mobile contract:277](../mobile/src/api/schema.d.ts#L277).
- **P3 · Fixed ambiguous acknowledgment wording:** salary requires explicit acceptance before saving/calculating, whereas expense Save automatically stores the acknowledgment. The revised policy distinguishes both from advertising consent. Evidence: [work guard:155](../mobile/src/modules/work/WorkSalaryScreen.tsx#L155), [work checkbox:235](../mobile/src/modules/work/WorkSalaryScreen.tsx#L235), [expense Save:97](../mobile/src/modules/expenses/ExpensesScreen.tsx#L97).
- Clarified the summary that employment context can be transmitted on Continue, before the final estimate action. Added that opening Home can initiate banner requests, and explicitly identified Google processing for the owner-supplied Gmail contact.
- Rechecked storage/deletion and HTTPS guards, including the currency preview. Local acknowledgment flags are not part of salary API payloads. No additional data-sharing integration or supported local-encryption claim was found.
- Generated the full readable Markdown policy from the canonical HTML for approval, rather than leaving only an overview/link. All remaining owner inputs are consolidated in [owner-inputs.md](owner-inputs.md).
- Fixed the release guard’s broad `draft` substring match, which incorrectly matched legitimate references to unsaved **drafts**. Explicit draft markers, unresolved review phrases, an open-items list, owner approval and content digest still block publication. No approval or publication was performed.
- Re-ran draft validation and the desktop/light, 320px/light and 390px/dark browser checks after the corrections: all passed with only local HTML/CSS requests and no cookies or browser storage. Verified Markdown export consistency and that the release guard still rejects the unapproved policy and open items.
- Rechecked the current official Google pages linked above. Sensitive-permission changes announced for 2027 were not treated as already effective on this review date. No live Play Console or AdMob settings were inspected.

Static source/configuration/dependency inspection and official documentation review completed. Website draft validation and workflow YAML parsing passed. The release validator correctly rejected the unapproved draft and absent approval digest. Chromium checks passed at 1440px/light, 320px/light and 390px/dark: no document-wide horizontal overflow; exactly two resource requests (local HTML/CSS); no cookies or local/session storage; no page errors; keyboard skip-link and contact navigation worked. Light desktop/mobile and dark mobile screenshots were inspected. This is bounded browser verification, not accessibility certification or an Android runtime audit.

Release traffic, consent lifecycle, signed manifest, backup/migration, console settings and production infrastructure remain unverified. App checks were not rerun because this task did not change application code. No existing app features were changed, and no remote publication or console submission was performed.
