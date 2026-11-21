# ArcReel on Railway

Railway template for [ArcReel](https://github.com/ArcReel/ArcReel), an open-source, self-hosted AI video workspace. It turns novels and scripts into characters, scenes, props, storyboards, videos and CapCut/JianYing drafts, with an AI agent, many model providers and cost tracking.

## What it deploys

| Service | Source | Data |
|---|---|---|
| **ArcReel** (public) | This repo's `Dockerfile`: `arcreel/arcreel:0.37.0@sha256:9c15544e…1d158d`, the official image pinned by version and digest | Volume at `/data`: projects, generated media, logs, keys (`/data/arcreel`) and the agent runtime data (`/data/claude`) |
| **Postgres** | Railway's PostgreSQL | Its own volume |

ArcReel listens on `PORT` (1241) behind Railway's HTTPS domain. Railway checks `GET /health`, which needs no login.

## Variables

| Variable | Default | What it does |
|---|---|---|
| `AUTH_USERNAME` | `admin` | Login name |
| `AUTH_PASSWORD` | generated (24 characters) | Login password. Read it in the ArcReel service's **Variables** tab after the deploy |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres over the private network. The start script switches it to the `asyncpg` driver |
| `PORT` | `1241` | Port ArcReel listens on |

No other prompts. AI provider keys (Anthropic, Gemini, Ark, OpenAI and others) go in ArcReel's **Settings** page after you sign in, never in variables: ArcReel refuses to start when a provider key is in its environment.

Optional settings you can add later, all from ArcReel's [deployment docs](https://docs.arc-reel.com/en/ops/deployment): `AUTH_TOKEN_SECRET` (else a secret is generated and kept on the volume), `TZ` (default `UTC` here), `LOG_LEVEL`, `CORS_ORIGINS`.

## Differences from the upstream Docker Compose setup

- **Agent Bash sandbox.** Upstream Compose runs the container with `seccomp:unconfined`, `apparmor:unconfined` and `NET_ADMIN` so that bubblewrap can isolate the agent's Bash tool. Railway containers can't get those, and ArcReel refuses to start when bubblewrap can't create namespaces. `railway_launch.py` probes bubblewrap at start. If it fails, ArcReel uses its own fail-closed fallback (the one it uses on Windows): the agent's Bash tool may only run ArcReel's bundled skill scripts, and everything else is denied. Generation, editing and export work through ArcReel's built-in tools as usual. A log line at start says which mode is on.
- **One volume.** Railway gives a service one volume, so the data root and `~/.claude` both live under `/data`.
- **Postgres** instead of the default SQLite, as in upstream's `deploy/production`.

## Updates

This template builds from this repo. When the pinned ArcReel version changes here, Railway shows an "update available" notice to everyone who deployed it, and they choose when to apply it. Read `CHANGELOG.md` first. ArcReel runs its own database migrations at start. Back up the volume and the database before large upgrades.

## Local test

`docker compose -f docker-compose.test.yml up --build` starts the same setup on <http://localhost:8080> (test password `local-test-password-123`). Railway doesn't use this file.

## License

ArcReel is AGPL-3.0 ([upstream license](https://github.com/ArcReel/ArcReel/blob/main/LICENSE)). The wrapper files in this repo are MIT.
