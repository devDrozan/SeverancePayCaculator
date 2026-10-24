# Workspace guidance

This file contains the durable architecture, technology choices, and implementation boundaries for ထွယ်ဂျီဂွမ်Caculator. It applies to the entire workspace; project-local `AGENTS.md` files add guidance for their own directories.

## Documentation ownership

- `AGENTS.md`: stable engineering decisions and boundaries. Update when an architectural decision changes.
- `SPEC.md`: current feature requirements, calculation behavior, acceptance criteria, and future product scope. Update as features change.
- `CLAUDE.md`: references this file so Claude follows the same guidance; do not duplicate these rules there.
- Root `README.md`: user-facing project overview and workspace setup.
- Each project's `README.md`: user-facing capabilities, installation, configuration, commands, and operation for that project. Keep each usable after an independent clone.

Keep feature details in `SPEC.md` and setup instructions in the relevant README instead of copying them into agent guidance. Read the current specification before changing product behavior.

## Repository boundaries

```text
SeverancePayCaculator/        # Root documentation and submodule repository
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── SPEC.md
├── .gitmodules
├── api/                     # Independent repository, referenced as a submodule
├── app/                     # Independent repository, referenced as a submodule
└── mobile/                  # Independent repository, referenced as a submodule
```

- Maintain exactly three sibling projects: `api`, `app`, and `mobile`.
- The public root repository is `devDrozan/SeverancePayCaculator`; it owns workspace documentation and pins `api`, `app`, and `mobile` as Git submodules pointing to the public repositories `devDrozan/api`, `devDrozan/app`, and `devDrozan/mobile`.
- Keep project source and release history in those independent repositories. Use no cross-repository source imports, parent workspace package, or fourth shared-code repository.
- Each repository owns its dependencies, lockfile, environment example, README, checks, and release history. Each must build independently after cloning.
- Run project Git commands from the relevant project directory. Commit submodule pointer updates and workspace documentation from the root repository after the referenced project commits are published.
- Delivery is API and web/PWA first, followed by the mobile application against the same API.

## Technology choices

Use Node.js 24 and npm with each project's committed `package-lock.json`. Keep runtime and dependency versions compatible; the package manifests, lockfiles, and `.nvmrc` files record the selected versions.

| Project | Owns | Stack |
| --- | --- | --- |
| `api` | Calculation engine, authoritative validation, versioned rules, HTTP contract | TypeScript, [Fastify](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/), TypeBox/JSON Schema, OpenAPI, decimal.js, Vitest; Docker-compatible Node.js service |
| `app` | Responsive web interface and installable PWA | React, TypeScript, Vite, Tailwind CSS, React Hook Form, Zod, i18next/react-i18next, vite-plugin-pwa, Vitest, Playwright |
| `mobile` | Dedicated Android and iPhone interface | [Expo](https://docs.expo.dev/), React Native, TypeScript, Expo Router, React Hook Form, Zod, i18next/react-i18next, Jest, React Native Testing Library |

Both clients use [openapi-typescript](https://openapi-ts.dev/) to generate types and `openapi-fetch` to call the API. Clients own separate UI components and translation resources; do not create a shared source package between repositories.

## Calculation and contract boundaries

- All financial calculations run in `api`. Clients collect inputs, provide feedback, and display API results; do not duplicate calculation formulas in either client.
- Separate pure calculation functions and versioned rules from HTTP handling. Official sources, verification dates, and calculation-rule versions belong to API rules metadata.
- Client validation improves input feedback; server validation remains authoritative.
- Use decimal arithmetic for money and preserve intermediate precision. Follow `SPEC.md` for dates, monetary wire values, and displayed rounding.
- The API owns the OpenAPI contract. Copy an intentionally selected, versioned schema artifact into each client's `contract/openapi.json`, then regenerate that client's types. Client builds must not require a sibling checkout or running API.
- Keep `/v1` backward compatible. Breaking contracts require a new major API version; calculation-rule revisions have a separate `rulesVersion`.
- Return structured field errors with machine-readable codes. Clients translate the codes into the supported languages.
- Validate request sizes and amounts, apply rate limiting, and configure allowed web origins.

## Privacy and deployment boundaries

- Keep the initial system stateless, without login, cloud history, or a database. Authentication and persistence are future extensions, not dependencies of the calculator.
- Do not request passport numbers, alien registration numbers, or bank details.
- Keep financial inputs and results in client session memory. Persist only language and appearance preferences; do not cache financial requests or responses.
- Exclude salaries and calculation payloads from logs and analytics.
- Use HTTPS outside local development and keep API base URLs environment-configurable. Client-exposed environment variables must contain no secrets.
- Deliver `api` as a Docker-compatible HTTP service and `app` as static build assets. Mobile uses Expo's build and release workflow.
- Hosting provisioning, remote repository creation, and app-store publication are separate release work. Implementation and local repository creation are authorized; this guidance does not authorize those external release actions.

## Planned integration choices

These are reserved architectural extension points. Their feature scope belongs in `SPEC.md`; do not implement them as part of the initial release.

- Login and saved history: Supabase Auth and PostgreSQL, with per-user access controls.
- Currency conversion: backend exchange-rate integration carrying source and update timestamps.
- Worker information: reviewed multilingual content with official references and review dates.
- Assistant: backend language-model integration grounded in verified information; numerical answers call the calculation API.
- Additional languages: extend each client's translation resources.

## Verification and maintenance

- Use the relevant project's README for setup and check commands, and `SPEC.md` for feature acceptance criteria.
- Verify affected repositories independently, including compatibility with each client's pinned API contract.
- For calculation changes, cover official worked examples, calendar and eligibility boundaries, wage components, DC contributions, and structured error handling. Review implemented rules against official sources before public release.
- For client changes, verify English and Burmese, glyph rendering, accessibility, narrow layouts, failure/retry behavior, and financial-data cache exclusions.
- Preserve mobile's local `AGENTS.md` requirements, including version-matched Expo documentation and mobile checks.
- The web app owns its SVG won mark and generated PNG icons. Its `tools/generate-icons.py` uses Python's standard library to regenerate the PNG assets.
