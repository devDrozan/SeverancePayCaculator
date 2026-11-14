# AdMob privacy and consent checklist

Reviewed **9 November 2026** for **E9 Mate Myanmar / com.e9mate.myanmar**. No AdMob account access or live inventory settings were inspected. Current source requests Google test banners with `requestNonPersonalizedAdsOnly: true`. This is not evidence of a compliant production consent flow or absence of SDK processing.

## Privacy notice

- [x] Draft names Google AdMob/Mobile Ads and explains external processing separately from calculator/expense storage.
- [x] Includes Google’s [Privacy Policy](https://policies.google.com/privacy), [advertising information](https://policies.google.com/technologies/ads), [partner-app explanation](https://policies.google.com/technologies/partner-sites), and advertising controls.
- [x] Explains advertising identifiers/device storage and distinguishes NPA from consent.
- [ ] Obtain final policy approval; publish and verify the actual HTTPS URL. Do not use the proposed URL while unpublished.
- [ ] Configure the verified policy URL and appropriate messages in the AdMob account. Check the exact parties/mediation partners used; update policy/disclosures if additional vendors are enabled.

Google’s [EU user consent policy](https://www.google.com/about/company/user-consent-policy/) covers applicable users in the EEA, UK and Switzerland, including disclosures, required device-storage consent and revocation information. [NPA guidance](https://support.google.com/admob/answer/7676680?hl=en) does not make non-personalized ads a blanket consent exemption. Check applicable regions and actual configuration rather than assuming users remain in Myanmar/Korea.

## Consent lifecycle — current application gap

- [ ] Configure applicable regional Privacy & messaging messages and a Google-certified consent solution where required.
- [ ] Update consent information at launch and present required messages; handle expiry, prior choices and errors.
- [ ] Gate ad requests using the consent solution’s eligibility state; prevent requests racing ahead of required consent and prevent duplicate requests.
- [ ] Provide a visible privacy-options entry when required and verify changes/revocation.
- [ ] Test accept/refuse, fresh install, returning user, offline/error, regional test geography and withdrawn choices using test devices. Never force debug geography in release.
- [ ] Ensure refusing optional ad consent does not delete local records or silently repurpose salary/expense data. Storage acknowledgments are separate from ads.

Use the installed SDK’s supported integration and [Google UMP guidance](https://developers.google.com/admob/android/privacy). The reviewed code does not call the available consent library or implement these controls. A policy website does not repair this gap; app changes remain separate and were not performed.

## Release and disclosure checks

- [ ] Verify the resolved native Google Mobile Ads and UMP versions in the production build. Wrapper 17.4.0 defaults are not proof of final resolution.
- [ ] Reconcile Data Safety categories/purposes/sharing with [Google’s SDK disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure) and final ad options. Refer to the separate Play checklist; do not assert “no data collected.”
- [ ] Check Advertising ID/Ad Services permissions and device controls against the final manifest; do not assume the NPA flag removes identifiers.
- [ ] Confirm target audience and age-related treatment; review applicable regional privacy messages and account settings, including US-state settings where relevant.
- [ ] Test with test IDs/devices during development; only switch to production IDs in an authorized, verified release. Never click your own live ads.
- [ ] Verify ad placement/labels and policies using the release UI. Paid-inventory behavior and mediation were not inspected.
- [ ] Check any account-specific app-ads.txt requirement separately. No seller record was invented or published; obtain the exact authorized line from AdMob if needed.
- [ ] Retain records of the configuration and privacy review, then recheck after SDK/vendor changes. Consult [AdMob policies](https://support.google.com/admob/answer/6128543?hl=en) for the full scope; this checklist is not certification.
