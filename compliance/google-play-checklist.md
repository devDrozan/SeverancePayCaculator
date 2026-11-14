# Google Play Console privacy disclosure checklist

App: **E9 Mate Myanmar**, `com.e9mate.myanmar`. Reviewed **9 November 2026**. Working guidance only: no Console submission/export was available. Complete against the actual release build and operations, not this source snapshot alone.

## Policy field and access

- [x] Draft English HTML identifies the app, package, proposed date and owner-supplied contact: `rozannainghangu@gmail.com`.
- [x] Storage, submissions, advertising, retention/deletion and security limitations are explained without unsupported encryption/compliance claims.
- [ ] Resolve hosting and email-retention facts; approve final content/date; remove resolved draft notes and record content digest.
- [ ] Publish only after explicit owner approval. Planned URL: `https://devDrozan.github.io/SeverancePayCaculator/`. It is **not yet a verified public policy URL**.
- [ ] Verify anonymous HTTPS HTML access on phone/desktop; no login, PDF-only document, geographic restriction, or download requirement.
- [ ] Enter the verified final URL in the Privacy Policy field and keep it stable.
- [ ] Add/test an accessible in-app policy link in a separately authorized app update. No application change was made here.

These access and policy-content requirements are grounded in [Google Play User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en). Naming the app does not verify the developer’s listing identity; confirm the final listing and contact match.

## Proposed Data Safety mapping — verify before selecting answers

| Data / flow | Proposed treatment | Purpose and open decisions |
| --- | --- | --- |
| Wages, rates, bonuses, pension balances and conversion amount sent to API | Other financial info: collected off-device | App functionality; user-triggered. Decide optionality from the final flow. Confirm whether retention is ephemeral across infrastructure. |
| Employment dates, hours and yes/no special-employment-adjustment flag sent to API | Review Personal info → Other info using the current form taxonomy | App functionality; no detailed leave/settlement records are requested. Avoid omitting contextual personal data merely because no name is asked. |
| Expense records | No off-device collection through this local feature was found | Local-only expense recording is not an automatic off-device purchase-history declaration. Recheck if export/sync is added. |
| Approximate location / identifiers | Assess collected and shared for the Google ad SDK | Use actual SDK/settings and [Google’s SDK disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure). |
| App interactions / crash logs or diagnostics | Assess collected and shared for the Google ad SDK | Verify precise subtypes, purposes and required/optional treatment for the release SDK; no separate app analytics integration found. |
| Email address and messages sent voluntarily to support | Document in policy; assess form scope from the actual support flow | No in-app email collection/contact form exists. Do not mechanically claim an in-app collection flow solely because a public contact email exists. |

Do not choose “no collection.” Include SDK behavior and off-device requests. Ephemeral handling still needs to be considered in the form; verify its conditions before marking it. A service-provider sharing exception for the API depends on its real contracts and purposes, while ads require a separate sharing assessment. These are qualified instructions from [Google’s Data Safety guidance](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en), not prefilled final Console answers.

## Security, deletion and release declarations

- [ ] Verify **all** transmitted user data paths in the signed build use secure transport, including API redirects/proxies and SDKs, before answering the transit-encryption question. A client HTTPS guard alone is insufficient runtime proof.
- [ ] Confirm backend provider, region, subprocessors and logs/retention. Do not assert ephemeral processing from application code alone.
- [ ] Describe local deletion accurately; verify expense individual/month/all deletion, work month/all deletion, clear storage and uninstall. Do not promise forensic erasure or remote local-record deletion.
- [ ] Account creation is absent; account-deletion requirements are not automatically applicable. Reevaluate if accounts are added.
- [ ] Declare ads accurately; verify Advertising ID answers against the final manifest/SDK. NPA does not establish identifier absence.
- [ ] Review final merged permissions: AD_ID/Ad Services, network, storage, overlays, location, biometric/debug-only permissions. Remove unjustified access in separate release work. See [sensitive-permission guidance](https://support.google.com/googleplay/android-developer/answer/16558241).
- [ ] Confirm target audience/age and country availability, including applicable child/teen ad settings. Do not infer them from this worker-focused app name alone.
- [ ] Compare final policy, listing, in-app notices, Data Safety answers, SDK disclosures and actual traffic. Save dated screenshots/export and signed artifact hash.
- [ ] Re-review when ads, mediation, analytics, hosting, storage, accounts or features change. No Google approval is guaranteed by this checklist.
