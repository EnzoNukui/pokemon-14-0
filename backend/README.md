# Backend

FastAPI application for Pokémon 13-0.

## Run locally

Copy `.env.example` to `.env` at the repository root and set a local database password. Start PostgreSQL with Docker Compose, then install `requirements.txt` from this directory and start the development server:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The process health endpoint is available at `http://127.0.0.1:8000/health`.
The readiness endpoint at `http://127.0.0.1:8000/ready` also checks the PostgreSQL connection.

## Accounts and authentication

The account module provides email/password registration, login, and the authenticated account endpoint:

- `POST /accounts/register` — creates an account and returns a Bearer access token.
- `POST /accounts/login` — checks credentials and returns a Bearer access token.
- `GET /accounts/me` — returns the account for the supplied Bearer token.

The run and draft routes also require that token. See `app/modules/runs/README.md` for endpoints and probability configuration.

Feature ownership and the layer convention are documented in `app/modules/README.md`. The current API paths stay unversioned; no `/api/v1` prefix is used.

Passwords are stored as Argon2 hashes. Emails are trimmed and normalized to lowercase, with a database unique index enforcing case-insensitive uniqueness. Access tokens use HS256 and expire after 30 minutes by default.

Set `AUTH_SECRET_KEY` in the repository root `.env` before using the account endpoints. Generate a local value with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value into `.env`; do not commit it. The example configuration includes a placeholder only.

## Domain rules currently centralized

The first pure domain rules are in `app/modules/runs/domain/` and `app/modules/battles/domain/`. They record the agreed draft size, reroll and legendary limits, the 13-battle path (8 Gym Leaders, 4 Elite Four members, then the Champion), and the conversion of a simulator draw into a run loss. Run progression is modeled independently from HTTP and database code so the API and persistence layers can call the same rules later.

The draft weights are configured in the repository root `.env`: Tier 1: 35%, Tier 2: 38%, Tier 3: 20%, Tier 4: 4%, Tier 5: 2%, and Legendary/Mythical offers: 1%.

## Showdown battle engine

The root Compose file provides the local Showdown battle service. Start it with PostgreSQL using `docker compose up -d postgres battle-engine`; the FastAPI backend calls `BATTLE_ENGINE_URL` (default `http://127.0.0.1:3001`). The player controls their turns and the trainer is controlled by Showdown's random player AI. Battle requests and rules use Gen 9 National Dex Anything Goes, so teams can include Pokémon from any region through Gen IX. The Node service is divided into HTTP routing, session storage, individual battle sessions, stream observers, and event serialization; see `../battle-engine/README.md`. The Python `battles` module owns one battle and returns transient events to the client, `runs` applies the 13-battle progression, and `championship` records a completed run. PostgreSQL stores battle results and metadata, not the full protocol event stream or a duplicate raw log. See `app/modules/runs/README.md` for the authenticated battle endpoints.

## Importar catálogo e treinadores locais

O catálogo cobre as espécies base até a geração IX e suas formas suportadas. As builds usadas no draft e nas batalhas passam pela validação da engine Showdown em `gen9nationaldexag`. O importador do catálogo e suas limitações estão descritos em `scripts/import_catalog/README.md`.

O seed do elenco aprovado importa os 100 treinadores, versões de time, Pokémon, formações e builds validadas já armazenadas no catálogo. Rode primeiro sem `--apply` para validar os dados; use `--apply` para gravar no PostgreSQL local. Veja `../database/README.md` para os comandos e o estado atual do seed.
