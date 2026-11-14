# Privacy configuration verification — 9 November 2026

Current working-tree review; no application changes, remote configuration changes, Console submissions or publication. This supplements the [six-area source audit](privacy-review-2026-11-09.md). Local environment files were inspected with secret values redacted; private network addresses are not reproduced here.

## What the files establish

| Topic | Verified locally | What this means / what remains unknown |
| --- | --- | --- |
| API address | The current mobile `.env` points to a private-network HTTP server on port 3001. Examples use localhost/emulator addresses. [client.ts:5](../mobile/src/api/client.ts#L5) reads EXPO_PUBLIC_API_BASE_URL; [eas.json:14](../mobile/eas.json#L14) supplies no production URL in the checked-in production profile. | The files describe development on a computer/local network. They do not identify a public host. Expo online build environment values or a separate deployment may exist; neither was inspected. Do not state “there is no deployed API.” |
| Server binding | [Dockerfile:10](../api/Dockerfile#L10) listens on all container interfaces at port 3001. [index.ts:5](../api/src/index.ts#L5) reads HOST/PORT. No provider-specific deployment, reverse-proxy or regional config was found. | `0.0.0.0` is a listening setting, not a company, country, or public URL. A Dockerfile is a way to run the service, not proof of where it runs. |
| Request logging | [server.ts:15](../api/src/server.ts#L15) sets Fastify logger=false. No calculator request/body/result logging or persistent request store was found in API source. | Supported policy claim: the API application does not log calculator inputs/results. It cannot establish a hosting provider’s access/security logs. |
| Startup logs | [index.ts:6](../api/src/index.ts#L6) prints the listening address; line 8 prints startup error messages. | Corrected the earlier overbroad “application logging is disabled” wording. Operational startup logs do exist; no financial body is supplied to those messages. Host log retention remains unknown. |
| Financial retention | Calculation handlers process requests without an application database or saved history. [server.ts:21](../api/src/server.ts#L21) sends no-store responses. | No application-level saved financial history was found. This is not proof of immediate memory erasure, no device/network caches, or no hosting-layer retention. |
| Technical memory | The rate limiter uses request identity/IP and counts in process memory with a one-minute rate window; its local store is in-memory. Currency metadata is eligible for cache reuse for 15 minutes. | Neither is a saved salary/expense history. A rate-window or freshness limit is not a guarantee that the underlying object is erased at that exact time. Do not invent a precise IP-erasure period. |
| Device retention | Work records/pay settings and expenses use local SQLite; language/theme use preferences. Deletion actions exist; no app-operated cloud sync. Unsaved drafts/results are session state. | Local records remain until user deletion/app-data removal. Do not describe all financial inputs as session-only. Existing deletion/backup qualifications remain valid. |
| Advertising | [HomeBannerAd.tsx:13](../mobile/src/components/HomeBannerAd.tsx#L13) uses Google test banners and NPA. The only advertising wrapper in the lockfile is react-native-google-mobile-ads 17.4.0; no added mediation adapter was found. | Google AdMob is verified. Complete account-side demand/bidding/mediation partners are not verified by absence of extra SDKs. Do not claim Google is the sole possible recipient. |
| Advertising consent | No app-level consent update/form, request-eligibility gate or privacy-options implementation was found. | This is a known app-side release gap, not something the owner needs to confirm from memory. UMP being present as a dependency does not implement the flow. |

## Current Google requirements checked

Official pages rechecked **9 November 2026**:

- **Policy access and content:** provide policy access in Play Console and within the app; identify app/developer and contact, explain data handling, recipients, retention/deletion and security. The policy URL must be public HTML without geographic/login barriers. The known missing in-app link remains a release task. [Google Play User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en)
- **Data Safety:** account for SDKs and online financial processing. In-memory request processing still needs evaluation in the form; only select ephemeral treatment after checking actual operations. A no-store response does not prove host logs are absent. No submitted form was available. [Data Safety guidance](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en)
- **Permissions:** compare actual release permissions with implemented functions and disclosures. Do not treat obsolete debug permissions as production evidence. Changes announced for 2027 are not effective requirements for this November 2026 review. [Sensitive permissions](https://support.google.com/googleplay/android-developer/answer/16558241?hl=en)
- **AdMob data:** Google’s SDK disclosure covers technical/device data separately from local records. Match final resolved SDK/options to declarations; no “no collection” claim. [Google SDK disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure)
- **Consent:** NPA does not automatically remove applicable consent obligations. Verify consent state/messages before eligible ad requests and privacy-options access when required; local storage acknowledgments do not satisfy advertising consent. [NPA guidance](https://support.google.com/admob/answer/7676680?hl=en), [UMP guidance](https://developers.google.com/admob/android/privacy)

## Owner response received — 9 November 2026

1. **API not deployed yet.** This resolves deployment status; there is no current production provider/region/retention to name. The source table above records what local inspection alone established. Future hosting must be reviewed before public calculation release.
2. **Default Google AdMob setup.** This is the owner’s account-status confirmation, not a live account audit. No separate ad-network adapter was found in code. Do not infer that Google has no default advertising partners.
3. **Support-email retention not decided.** This is the only remaining inbox-policy decision; no duration has been invented. It can be supplied when the owner is ready, before publication.

The contact email is already confirmed. SDK versions, code behavior, consent implementation, manifests and hosting log configuration are verification tasks, not questions asking the owner to guess technical answers. Distribution/audience choices remain relevant for release setup, but no verified child/teen or regional configuration is claimed in the policy.

## Outcome

The HTML and full Markdown policy distinguish startup logging from request logging, document the confirmed lack of a deployed API and default AdMob setup, and leave the undecided email-retention period explicit. The owner subsequently authorized interim publication with updates to follow. The policy is now public at <https://devdrozan.github.io/SeverancePayCaculator/>, while future hosting/retention and final advertising configuration remain release verification tasks. App release readiness remains false. Final content and Console answers cannot be certified from repository source alone.
