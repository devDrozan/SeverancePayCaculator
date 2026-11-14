# E9 Mate Myanmar — Privacy Policy

> **Approved interim notice.** Open items remain disclosed; this is not app-release approval.

**Effective date:** 2026-11-09  
**Android package:** `com.e9mate.myanmar`  
**Privacy contact:** rozannainghangu@gmail.com

This is the full readable export of [the canonical policy website](privacy-site/index.html). Generated with `python3 tools/export-privacy-policy.py`; edit the HTML rather than this copy.

## 01. About this policy

This policy explains how the developer of **E9 Mate Myanmar** (“we”, “us”, or “our”) handles information in the Android application with package name `com.e9mate.myanmar`. The app provides severance calculations, an expense tracker, work-time salary estimates, and E-9 worker information and utilities. It also includes a currency-conversion preview whose live rates are currently unavailable until an approved source is configured.

The app does not require an account. It does not ask you to connect a bank account or provide a passport number, alien registration number, or payment-card details. Please avoid putting identifying or sensitive information in expense descriptions or support emails unless needed for your request.

## 02. Information we handle

| Information | How it is used | Storage or transmission |
| --- | --- | --- |
| Severance calculator inputs | Employment dates, working hours, pension/calculation choice, a yes/no flag indicating whether special employment adjustments apply, wages, allowances, bonuses, leave pay, and any pension balance/date you enter are used to prepare your estimate. The adjustment flag does not request detailed leave or settlement records. | Held in the app session; employment details, including the adjustment flag, are sent when you continue to request calculation context. The relevant financial inputs and employment details are sent when calculating an estimate. |
| Work records & monthly pay settings | Monthly base salary, hourly rates, dated normal/overtime/night hours, and the saved storage-notice acknowledgment support the work calendar. | Saved in a local SQLite database. Requesting a salary estimate sends only the selected month’s settings and work entries to the API. |
| Expense records | Record ID, date, category, description, amount, and a saved storage-notice acknowledgment support your expense calendar and totals. | Saved in a local SQLite database. The expense feature does not upload these records to our API. |
| Currency preview input | The entered amount and KRW/MMK direction are used for the conversion you request when a valid rate is available. | Held in session memory and sent to our API on Convert; the app does not send that amount to the rate institution. |
| Language & appearance | Remember your interface choices. | Saved in local app preferences. |
| Advertising & technical data | Ad delivery, measurement, diagnostics, security, and fraud prevention. | Processed externally through Google Mobile Ads; see the advertising section. |
| Privacy or support messages | Respond to questions you choose to email us. | Your email address and message pass through your and our email providers. Do not include financial records unless necessary. |

Estimates and unsaved drafts remain in session memory rather than being saved as a calculation history. Local expense and work records can be recorded and edited offline; API calculations and ads require a network connection.

## 03. Processing & sharing

**Calculation service.** The app sends the information described above to the configured calculation API for the requested functionality. The API application processes financial inputs for the request and has no database or application-level history of those inputs or results. API request logging is disabled, and the reviewed code does not write calculator inputs or results to logs. Server startup messages and startup errors may be logged. Responses use a no-store instruction. This does not establish that every hosting or network layer has no logs.

**Network and hosting information.** As of the effective date, the developer has not deployed a public production calculation API; the reviewed configuration points to a development server. Connecting to a configured API exposes technical information such as your IP address to the endpoint and its infrastructure. The service uses in-memory request rate limiting. Before public online calculations are released, the production provider, processing locations, and any hosting connection/security logs and retention must be verified and reflected in this policy. No production hosting provider or retention period has been selected.

**Advertising.** Google processes advertising data separately as described below. Our app code does not pass your salary, severance inputs, work entries, or expense descriptions to AdMob as advertising parameters. No separate app analytics or crash-reporting service is integrated in the reviewed application code; the advertising SDK has its own measurement and diagnostic processing.

**Other recipients.** Messages sent to our Gmail contact address are also processed by Google under its [Privacy Policy](https://policies.google.com/privacy), as well as by your chosen email provider. If you open an official reference or an advertisement, the destination service handles your visit under its own policy. Information may also be disclosed where legally required. Google and other service providers may process information outside your country according to their own terms and applicable arrangements; this notice does not promise a particular data-residency location.

## 04. Google AdMob advertising

The app integrates **Google AdMob through the Google Mobile Ads SDK**. Opening the Home screen can initiate a banner-ad request. The reviewed implementation uses Google test banner IDs and requests non-personalized ads. Test ads are not evidence that no network data is processed, and non-personalized ads do not mean no data collection.

The developer has confirmed use of the default Google AdMob account setup, without separately added ad networks. No additional advertising-network SDK or mediation adapter was identified in the reviewed app code. Google’s advertising services may still involve advertising partners under Google’s policies and account configuration; this does not mean Google is the only possible advertising recipient. The final release configuration must be checked if the setup changes.

Google’s [Mobile Ads SDK data disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure) describes collection and sharing of IP addresses, which can indicate approximate location; product interactions such as launches, taps, and ad views; performance and diagnostic information; and device or account identifiers, including the Android advertising ID and app set ID when available. Google uses these data for advertising, measurement, and fraud prevention. Availability of identifiers depends on the device, settings, SDK, and ad-serving mode.

Advertising technology can access or store information on the device, including identifiers or similar technologies. Requesting non-personalized ads does not itself obtain consent for such access.

- [Google Privacy Policy](https://policies.google.com/privacy)
- [Google advertising information](https://policies.google.com/technologies/ads)
- [How Google uses information from partner apps](https://policies.google.com/technologies/partner-sites)
- [Google advertising privacy controls](https://myadcenter.google.com/)

## 05. Consent & your choices

The work-time module asks you to explicitly accept its local-storage and selected-month API-submission notice before saving or calculating. Saving an expense automatically records acknowledgment of its local-storage notice. Neither action is consent to advertising, tracking, or unrelated processing. You choose whether to request online calculations; expense recording does not require submitting expenses to the API.

**Advertising controls in the reviewed build:** an in-app advertising-consent form and advertising privacy-options entry are not currently implemented. Where consent is required, that flow must be implemented and verified before advertising release. Reading or accepting this policy is not a substitute for that consent.

You can manage or delete the Android advertising ID through your device’s advertising privacy settings, where available. Menu names vary by Android version. These settings do not necessarily prevent all technical processing or remove information already held by Google. Google’s controls and policy explain its available choices.

You may contact us about privacy questions or requests, including access, correction, or deletion where applicable. The response available depends on what information we hold and applicable requirements. We cannot access or remotely delete records that exist only in your app’s local storage.

## 06. Retention & deletion

- **Saved work records and pay settings:** remain locally until you use the work module’s delete-month or delete-all action, or the operating system removes the app’s data.
- **Saved expenses:** remain locally until you delete an expense, delete the selected month, delete all expenses, or remove the app’s data. Work and expense deletion controls operate separately.
- **Preferences:** remain locally until overwritten or the app’s data is cleared.
- **Unsaved drafts and calculation results:** are held for the app session and may remain while the app process is in memory; they are not a persistent server history.
- **Calculation requests:** are not saved by the API application. There is no deployed production API yet. Any production infrastructure log retention must be reviewed when hosting is selected, before public online calculations are released.
- **Google advertising data:** is retained according to Google’s policies and applicable controls. Clearing local app data does not automatically delete Google-held data.
- **Email correspondence:** is handled in the developer’s email account to answer your request. A fixed retention/deletion period has not yet been adopted for these messages. You can contact the privacy address below with a deletion request; this notice will be updated when a retention schedule is established.

You can use Android’s app settings to clear app storage, or uninstall the app, to remove its local records and preferences from that installation. Deletion through the app is not a guarantee of forensic erasure from every storage layer.

We do not provide app-operated cloud backup or synchronization. Android backup is disabled in the current app configuration; operating-system or manufacturer migration behavior can vary and is not guaranteed by this policy. Any copies made outside the app may need to be removed separately. There is no app account to delete.

## 07. Security & device access

The production API client is configured to require HTTPS. Google documents TLS for the Mobile Ads SDK’s data transmission. The final production endpoint and release build still need verification; development builds may use a local HTTP server. No system can guarantee absolute security.

Saved records use app-local storage. We do not claim that the app implements additional database encryption, end-to-end encryption, or guaranteed secure erasure. Protect your device with its available access controls and keep the operating system up to date.

The implemented calculator and expense flows do not request access to your camera, microphone, contacts, precise device location, photos, or personal files. Network access supports API requests and ads; advertising SDKs can use advertising-related identifiers as described above. Permissions added by native dependencies must still be checked in the final release build.

## 08. Children’s privacy

E9 Mate Myanmar is designed for E-9 workers and related personal planning, rather than for children. We do not intentionally seek children’s personal information. If you believe a child has provided information to us, contact the privacy email below. Audience settings and applicable advertising protections must be verified before distribution.

## 09. This website & external links

This policy website contains no advertising SDK, analytics, forms, embedded third-party content, tracking scripts, or cookies set by our site code. Its stylesheet is served with the page; there is no login or font-service request.

When hosted on GitHub Pages, GitHub processes visitor connection information, including IP addresses, to serve and protect the website. That hosting processing is governed by the [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). We do not claim the hosting provider records no information. Following an external link, or emailing us, sends information to the service you choose.

## 10. Changes to this policy

We will update this page when the app’s data practices change and revise the effective date. Material changes may require additional notice or consent as applicable. This interim version states the current implementation and identifies details that are still being finalized. Publishing this notice does not mean the app’s consent or release verification is complete.

Questions about your privacy?

## 11. Contact the developer

For privacy questions or requests about E9 Mate Myanmar, contact:

**E9 Mate Myanmar developer**  
[rozannainghangu@gmail.com](mailto:rozannainghangu@gmail.com)

Please identify the app and describe your request. Avoid sending identity documents, bank details, or full financial records.

---

**Approval notes (not part of the policy):** [Owner confirmations](compliance/owner-inputs.md) · [Source review](compliance/privacy-review-2026-11-09.md) · [Google Play checklist](compliance/google-play-checklist.md) · [AdMob checklist](compliance/admob-checklist.md) · [Deployment setup](privacy-site/README.md). Publication authorization is recorded separately in the publication metadata; generating this copy does not authorize future changes.
