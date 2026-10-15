# Back-end tests

Run unit tests from `backend/` with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The unit tests cover run progression, draft probability rules, authentication helpers, catalog normalization, Showdown team mapping, and SQLAlchemy schema metadata. They use the standard-library `unittest` runner and do not require a database.

The API integration tests require an isolated PostgreSQL database with the current Alembic migrations applied. They cover account registration/login, the complete six-round draft and reroll, the 13-opponent path, transient battle event responses, result persistence, champion history, and abandonment. Showdown protocol events are returned to the client during a live battle and are not archived in PostgreSQL. The separate engine suite runs an actual battle against the installed Pokémon Showdown package.

Set `POKEMON_TEST_DATABASE_URL` to the isolated database's `postgresql+asyncpg` URL before running the suite. API requests use a transaction that is rolled back after each test. The battle engine integration is run from `battle-engine/` with `npm test`. Never point these tests at a production database.
