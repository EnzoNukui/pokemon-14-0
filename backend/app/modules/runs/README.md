# Runs module

`application/draft_service.py` implements the first draft use cases:

- Generate the next six-option round only when requested.
- Reroll the current round once per run; old options remain recorded and cannot appear again.
- Select one option per round, save its default build snapshot to the player's team, and advance to Gym stage after round six.
- Enforce the single Legendary/Mythical selection limit.

The service locks the run row during writes so simultaneous selections or rerolls for the same run are serialized. Each use case owns a database transaction and raises a `DraftError` subtype for expected rule or catalog problems; HTTP status mapping belongs in the presentation layer.

`DraftProbabilityPolicy` requires explicit Decimal weights for tiers 1–5 that total 99%. The current distribution is Tier 1: 36%, Tier 2: 39%, Tier 3: 20%, Tier 4: 3%, and Tier 5: 1%. The remaining 1% is reserved for Legendary/Mythical offers. To keep strong species from appearing in common pools when their competitive tier was missing or stale, pseudo-legendaries have a Tier 5 floor; competitive tiers AG/Uber/OU/UUBL, UU/RUBL, and RU/NUBL have minimum tiers 5, 4, and 3 respectively; other species have minimum tiers of 3 at 500 BST, 4 at 550 BST, and 5 at 600 BST. The API reads `DRAFT_TIER_1_PERCENT` through `DRAFT_TIER_5_PERCENT` from the repository root `.env`; missing or invalid values return HTTP 503 before a run is created or draft options are generated. Values are percentages, such as `15` for 15. If a tier has no remaining candidates, the available category weights are normalized for the current selection; options are never repeated within a run, including options that were rejected or rerolled.

Eligible catalog entries must have a default `PokemonBuild`; selection requires exactly one such build and stores a snapshot in `team_pokemon`.

## HTTP endpoints

Gameplay is available without an account. `POST /runs` creates a guest-owned run when no Bearer token is sent and returns `guest_session_token` in its response. The client must keep that token and send it as `X-Guest-Session` on subsequent run, draft, and battle requests. A guest session can have one active run and expires after 30 days. When a Bearer token is sent to `POST /runs`, the run belongs to that account and no guest token is returned.

Run ownership is required for private run operations, using either the account Bearer token or `X-Guest-Session`:

- `POST /runs` starts a run in the draft stage. It returns 409 if that player already has an active run.
- `GET /runs/current` returns that player's active run.
- `GET /runs/history` returns the account's completed, failed, and abandoned runs, including their end timestamps.
- `GET /runs/{run_id}/result` returns the final run state, Hall of Fame snapshot when completed, and champion entry when the run made a new champion.
- `GET /runs/{run_id}/team` returns the selected team and saved build snapshots.
- `POST /runs/{run_id}/abandon` ends the active run and frees the account to start another.
- `GET /runs/{run_id}/draft` creates and returns the current six options when needed.
- `POST /runs/{run_id}/draft/reroll` replaces the current six options, once per run.
- `POST /runs/{run_id}/draft/selection` with `{"option_number": 1}` selects one option and advances the round.
- `GET /runs/{run_id}/battles` creates (once) and returns the run's persisted path of 13 opponents.
- `GET /runs/{run_id}/battles/current` returns the next opponent after the six-Pokémon draft is complete.
- `POST /runs/{run_id}/battles/current/start` starts the current battle in Showdown and returns the player's current legal request plus new battle events.
- `POST /runs/{run_id}/battles/{battle_number}/choices` with `{"choice": "move 1"}` submits a Showdown choice. The response contains the next request/events and, when complete, applies the result to the run.
- `POST /runs/{run_id}/ranking` requires an account Bearer token and the owning guest session in `X-Guest-Session`. It associates a completed guest win with the account and publishes its Hall of Fame and champion history snapshots. Only a completed run can be submitted.

The battle path follows this order: battles 1–8 are Gym Leaders; battles 9–11 are Elite Four; battle 12 is the final Elite Four slot and may use either an Elite Four trainer or one of the approved 15 Champion trainers; battle 13 is a Champion. A trainer cannot appear twice in the same run. The selected path is stored against the run and stays fixed, including after the run ends. The account must have enough active, categorized trainer teams to fill all 13 unique slots.

The player submits Showdown choices; the opponent uses the engine's strategic battle AI. Trainer Pokémon receive Life Orb when their curated set has no held item. Protocol events are returned in each live battle response for the client to render, but are not archived in PostgreSQL. PostgreSQL retains the battle state, teams, simulator result, run result, format, engine version, and timestamps. Only the engine can produce the result applied to the run: a `LOSS` or `DRAW` ends it as `FAILED`, and winning battle 13 ends it as `COMPLETED` with stage `FINISHED`. Choices must be submitted for the current battle in sequence. A complete player team and a complete six-Pokémon opponent team are required.

A completed 13-win account-owned run is recorded in `hall_of_fame` with a snapshot of its team and all 13 results. The same transaction promotes that team in `current_champion`, appends `champion_history`, and timestamps the previous champion's reign as ended. A completed guest run stays private until the player signs in and submits it through `/ranking`. Abandoned runs are marked `ABANDONED`; an active Showdown battle is closed. Failed runs are retained with the battle result that ended them.

- `GET /champions/current` is public and returns the current champion history entry, or `null` before a player has completed a run.
- `GET /champions/history` is public and returns the global champion succession history.

Run PostgreSQL and Showdown with `docker compose up -d postgres battle-engine`. The backend connects to `BATTLE_ENGINE_URL` (default `http://127.0.0.1:3001`). Showdown sessions and protocol events live in the engine process memory; battle and run outcomes are persisted in PostgreSQL.

Run ownership is checked for every private operation. Database partial unique indexes enforce one active run per account and one per guest session. `GET /runs/history` remains account-only; guest runs can be resumed with their session token and can be submitted to the account history/ranking after sign-in.
