# ထွယ်ဂျီဂွမ်Caculator

An English/Burmese severance calculator for E-9 workers in Korea. Normal statutory severance, DB baseline estimates, and DC required-contribution estimates use one stateless API.

## Projects

This public root repository contains workspace documentation and references three independent public projects as Git submodules. Each project's README provides its own setup, configuration, usage, and build instructions.

| Project | Repository | Purpose | Local address |
| --- | --- | --- | --- |
| [api](https://github.com/devDrozan/api/blob/main/README.md) | [devDrozan/api](https://github.com/devDrozan/api) | Fastify/TypeScript calculation service | `http://127.0.0.1:3001` |
| [app](https://github.com/devDrozan/app/blob/main/README.md) | [devDrozan/app](https://github.com/devDrozan/app) | React/Vite web app and installable PWA | `http://127.0.0.1:5173` |
| [mobile](https://github.com/devDrozan/mobile/blob/main/README.md) | [devDrozan/mobile](https://github.com/devDrozan/mobile) | Expo/React Native Android and iPhone client | Expo development server |

## Clone the workspace

```sh
git clone --recurse-submodules https://github.com/devDrozan/SeverancePayCaculator.git
cd SeverancePayCaculator
```

For an existing root clone, fetch its pinned projects with `git submodule update --init --recursive`. Each project can also be cloned and built independently using its repository URL above. To contribute inside a submodule, check out `main` or a feature branch first; a fresh submodule checkout starts at the root's pinned commit.

Publish project commits from the relevant project repository before committing updated submodule pointers in the root. Local design-reference files `UI.pdf` and `UX.pdf` are excluded from version control.

## Run the web calculator

Use Node.js 24. In one terminal:

```sh
cd api
npm ci
npm run dev
```

In another terminal:

```sh
cd app
npm ci
npm run dev
```

Open `http://127.0.0.1:5173`. The web development server proxies calculation requests to the API. **Try an example** loads the official MOEL worked example into the form; the API computes the result after review.

## Run the mobile app

For installation and API configuration, follow [mobile/README.md](https://github.com/devDrozan/mobile/blob/main/README.md). Run Expo commands inside `mobile`, which contains the Expo `package.json` and `app.json`. From this workspace's root, after setup:

```sh
cd mobile
npx expo-doctor
npm start
```

The workspace root contains documentation and submodule pointers, so running `npx expo-doctor` there cannot load the mobile app's configuration. A physical phone needs an API address reachable over your local network; its own `localhost` is not your computer.

## Scope and privacy

The calculator estimates gross KRW amounts before tax for one continuous employment period with one unchanged plan. It flags special histories for review. DB estimates cover the statutory baseline. DC contributions and reported investment balances remain separate.

There is no login or database. Salary inputs and results stay in client memory and are not logged or cached by the API. Only language and mobile appearance preferences are saved on the device.

Local implementation does not provision public hosting, publish remote repositories, or submit mobile apps to stores. Before public release, have a Korean labor specialist review the calculation assumptions, historical boundaries, and English/Burmese wording.

## Documentation

| Document | Purpose |
| --- | --- |
| [SPEC.md](SPEC.md) | Current feature requirements, calculation behavior, acceptance criteria, and future features |
| [AGENTS.md](AGENTS.md) | Stable architecture, technology choices, repository boundaries, and engineering guidance |
| [CLAUDE.md](CLAUDE.md) | Entry point that directs Claude to `AGENTS.md` |
| Project READMEs above | User-facing information for running and using each project |
