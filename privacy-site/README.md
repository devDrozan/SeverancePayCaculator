# E9 Mate Myanmar Privacy Policy website

The owner authorized **interim publication on 9 November 2026** with the instruction “now publish and i will provide update informations later”. This authorizes the policy page, not app release or a claim of Google approval. The page visibly discloses the undeployed API, undecided support-email retention, and incomplete consent/release checks.

Public address: <https://devDrozan.github.io/SeverancePayCaculator/>. Check `../compliance/privacy-publication.json` for the recorded deployment verification.

## Current GitHub Pages setup

- Repository: `devDrozan/SeverancePayCaculator`.
- Source: **Deploy from a branch**, branch `codex/privacy-policy-pages`, folder `/ (root)`.
- The dedicated publishing branch contains only `index.html`, `styles.css`, and `.nojekyll`; it has its own static-only history. Main and the application submodules are unchanged.
- GitHub’s generated **pages build and deployment** workflow publishes this branch automatically when it changes. HTTPS is required for the default github.io domain.
- Source HTML/CSS remain in this workspace’s `privacy-site/`. This is a root documentation website, not a fourth application repository.

The site has no JavaScript, account, forms, analytics, advertisements, remote fonts, tracking pixels or client storage. GitHub still processes connection information to host it, as disclosed. Internal compliance reports, environment files and application code are not uploaded in the policy branch.

## Preview and validate updates

From the workspace root:

```sh
python3 tools/export-privacy-policy.py
python3 tools/check-privacy-site.py
python3 -m http.server 8088 --bind 127.0.0.1 --directory privacy-site
```

Open `http://127.0.0.1:8088/`. Check phone/desktop, light/dark, keyboard navigation, table scrolling, date, contact and truthful descriptions. The Markdown export is a readable copy; HTML is canonical.

## Future publication updates

1. Update HTML to verified practices and revise the effective date when appropriate. Keep undecided facts explicit rather than inventing them.
2. Obtain authorization for the changed content. Record the approval, date and content SHA-256 in `../compliance/privacy-publication.json`. `openItems` stays visible in internal records until actually resolved.
3. Run `python3 tools/check-privacy-site.py --release`. An interim version requires explicit interim authorization, a visible interim marker and `appReleaseReady: false`; a complete release requires no open items. Both require the approved content digest. The interim exception records the owner’s specific instruction; it is not a general bypass of approval.
4. Publish only the three static files to the existing `codex/privacy-policy-pages` branch, preserving the branch parent commit and pushing normally. Never force-push or include unrelated working-tree files. A change to that branch automatically deploys; authorization must precede the push.
5. Check GitHub’s deployment result, anonymous HTTPS access and rendered page; record the verified URL/commit. Do not mark the app compliant merely because the website works.

The local `.github/workflows/privacy-pages.yml` is an **optional custom-workflow alternative**, not the active deployment. Do not run it unless intentionally switching Pages Source to GitHub Actions; the current branch-based source already supplies deployment. It was not uploaded with the website.

References: [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).

## Outstanding application release work

Ad-consent eligibility and privacy options, an accessible in-app policy link, production hosting/log-retention review, final signed manifest/SDK/transport checks, target audience/country settings and accurate Play disclosures remain separate release work. No application features were changed while publishing this notice.
