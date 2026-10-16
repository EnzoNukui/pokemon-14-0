"""PostgreSQL-backed account API integration test.

Set POKEMON_TEST_DATABASE_URL to an isolated database with Alembic migrations
applied before running this test. Requests are rolled back after each test.
"""

from __future__ import annotations

import os
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

os.environ["AUTH_SECRET_KEY"] = "test-only-signing-key-with-at-least-32-bytes"

import httpx
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import get_settings
from app.db.models.pokemon import Pokemon, PokemonBuild
from app.db.session import get_session
from app.db.models.trainer import Trainer, TrainerTeam, TrainerTeamPokemon
from app.main import app
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.presentation.dependencies import get_configured_draft_policy


TEST_DATABASE_URL = os.environ.get("POKEMON_TEST_DATABASE_URL")
get_settings.cache_clear()
DRAFT_POLICY = DraftProbabilityPolicy(
    tier_weights={
        1: Decimal("0.12"),
        2: Decimal("0.32"),
        3: Decimal("0.40"),
        4: Decimal("0.10"),
        5: Decimal("0.05"),
    }
)


@unittest.skipUnless(TEST_DATABASE_URL, "set POKEMON_TEST_DATABASE_URL for DB integration tests")
class AccountsApiIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        assert TEST_DATABASE_URL is not None
        self.engine = create_async_engine(TEST_DATABASE_URL)
        self.connection = await self.engine.connect()
        self.transaction = await self.connection.begin()

        async def override_get_session():
            async with AsyncSession(
                bind=self.connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            ) as session:
                yield session

        app.dependency_overrides[get_session] = override_get_session
        app.dependency_overrides[get_configured_draft_policy] = lambda: DRAFT_POLICY
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()
        app.dependency_overrides.pop(get_session, None)
        app.dependency_overrides.pop(get_configured_draft_policy, None)
        if self.transaction.is_active:
            await self.transaction.rollback()
        await self.connection.close()
        await self.engine.dispose()

    async def test_register_login_authenticated_profile_and_rejection_paths(self) -> None:
        email = "Pokemon13-Integration@example.com"
        password = "Integration-Test-Password-42"

        readiness = await self.client.get("/ready")
        self.assertEqual(readiness.status_code, 200, readiness.text)
        self.assertEqual(readiness.json(), {"status": "ready", "database": "ok"})

        registration = await self.client.post(
            "/accounts/register", json={"email": email, "password": password}
        )
        self.assertEqual(registration.status_code, 201, registration.text)
        registration_body = registration.json()
        self.assertEqual(registration_body["user"]["email"], email.lower())
        self.assertEqual(registration_body["token_type"], "bearer")
        self.assertGreater(registration_body["expires_in"], 0)

        duplicate = await self.client.post(
            "/accounts/register",
            json={"email": email.upper(), "password": password},
        )
        self.assertEqual(duplicate.status_code, 409, duplicate.text)

        login = await self.client.post(
            "/accounts/login",
            json={"email": email.upper(), "password": password},
        )
        self.assertEqual(login.status_code, 200, login.text)

        profile = await self.client.get(
            "/accounts/me",
            headers={"Authorization": f"Bearer {login.json()['access_token']}"},
        )
        self.assertEqual(profile.status_code, 200, profile.text)
        self.assertEqual(profile.json()["email"], email.lower())

        wrong_password = await self.client.post(
            "/accounts/login",
            json={"email": email, "password": "not-the-password"},
        )
        self.assertEqual(wrong_password.status_code, 401)

        unauthenticated = await self.client.get("/accounts/me")
        self.assertEqual(unauthenticated.status_code, 401)

    async def test_draft_battle_progression_and_champion_history(self) -> None:
        await self._seed_catalog_and_trainers()
        registration = await self.client.post(
            "/accounts/register",
            json={
                "email": "pokemon13-run-integration@example.com",
                "password": "Integration-Test-Password-42",
            },
        )
        self.assertEqual(registration.status_code, 201, registration.text)
        headers = {
            "Authorization": f"Bearer {registration.json()['access_token']}"
        }

        created_run = await self.client.post("/runs", headers=headers)
        self.assertEqual(created_run.status_code, 201, created_run.text)
        run_id = created_run.json()["id"]
        self.assertEqual(created_run.json()["stage"], "DRAFT")
        conflict = await self.client.post("/runs", headers=headers)
        self.assertEqual(conflict.status_code, 409)

        first_round = await self.client.get(f"/runs/{run_id}/draft", headers=headers)
        self.assertEqual(first_round.status_code, 200, first_round.text)
        self.assertEqual(len(first_round.json()["options"]), 6)
        first_offer_ids = {option["pokemon_id"] for option in first_round.json()["options"]}

        reroll = await self.client.post(
            f"/runs/{run_id}/draft/reroll", headers=headers
        )
        self.assertEqual(reroll.status_code, 200, reroll.text)
        self.assertEqual(reroll.json()["display_set"], 1)
        self.assertFalse(reroll.json()["reroll_available"])
        rerolled_ids = {option["pokemon_id"] for option in reroll.json()["options"]}
        self.assertEqual(len(rerolled_ids), 6)
        self.assertTrue(first_offer_ids.isdisjoint(rerolled_ids))

        second_reroll = await self.client.post(
            f"/runs/{run_id}/draft/reroll", headers=headers
        )
        self.assertEqual(second_reroll.status_code, 409)

        for round_number in range(1, 7):
            if round_number > 1:
                current_round = await self.client.get(
                    f"/runs/{run_id}/draft", headers=headers
                )
                self.assertEqual(current_round.status_code, 200, current_round.text)
                self.assertEqual(current_round.json()["round_number"], round_number)
            selected = await self.client.post(
                f"/runs/{run_id}/draft/selection",
                headers=headers,
                json={"option_number": 1},
            )
            self.assertEqual(selected.status_code, 200, selected.text)
            self.assertEqual(selected.json()["team_slot"], round_number)
            self.assertEqual(selected.json()["draft_complete"], round_number == 6)

        run_team = await self.client.get(f"/runs/{run_id}/team", headers=headers)
        self.assertEqual(run_team.status_code, 200, run_team.text)
        self.assertEqual(len(run_team.json()), 6)
        self.assertEqual(
            (await self.client.get("/runs/current", headers=headers)).json()["stage"],
            "GYM",
        )

        path = await self.client.get(f"/runs/{run_id}/battles", headers=headers)
        self.assertEqual(path.status_code, 200, path.text)
        battles = path.json()["battles"]
        self.assertEqual(len(battles), 13)
        self.assertEqual([battle["stage"] for battle in battles[:8]], ["GYM"] * 8)
        self.assertEqual([battle["stage"] for battle in battles[8:12]], ["ELITE_FOUR"] * 4)
        self.assertEqual(battles[12]["stage"], "CHAMPION")
        self.assertEqual(len({battle["trainer_id"] for battle in battles}), 13)
        self.assertEqual(len(battles[0]["opponent_team"]), 6)

        fake_showdown = SimpleNamespace(
            start_battle=AsyncMock(side_effect=self._fake_start_battle),
            submit_choice=AsyncMock(side_effect=self._fake_complete_battle),
            get_battle=AsyncMock(),
            abandon_battle=AsyncMock(),
        )
        with patch(
            "app.modules.battles.application.battle_service.ShowdownClient",
            return_value=fake_showdown,
        ):
            for battle_number in range(1, 14):
                started = await self.client.post(
                    f"/runs/{run_id}/battles/current/start", headers=headers
                )
                self.assertEqual(started.status_code, 200, started.text)
                self.assertEqual(started.json()["battle_number"], battle_number)
                self.assertEqual(started.json()["status"], "RUNNING")
                self.assertEqual(started.json()["events"][0]["event_type"], "start")

                completed = await self.client.post(
                    f"/runs/{run_id}/battles/{battle_number}/choices",
                    headers=headers,
                    json={"choice": "move 1"},
                )
                self.assertEqual(completed.status_code, 200, completed.text)
                self.assertEqual(completed.json()["simulator_result"], "WIN")
                self.assertEqual(completed.json()["progress_index"], battle_number)
                self.assertEqual(
                    completed.json()["run_status"],
                    "COMPLETED" if battle_number == 13 else "ACTIVE",
                )
                self.assertEqual(completed.json()["events"][0]["event_type"], "win")

        outcome = await self.client.get(f"/runs/{run_id}/result", headers=headers)
        self.assertEqual(outcome.status_code, 200, outcome.text)
        self.assertEqual(outcome.json()["run"]["status"], "COMPLETED")
        self.assertEqual(len(outcome.json()["hall_of_fame_snapshot"]["team"]), 6)
        self.assertEqual(len(outcome.json()["hall_of_fame_snapshot"]["battles"]), 13)
        self.assertIsNotNone(outcome.json()["champion_history"])

        current_champion = await self.client.get("/champions/current", headers=headers)
        self.assertEqual(current_champion.status_code, 200, current_champion.text)
        self.assertEqual(current_champion.json()["run_id"], run_id)
        champion_history = await self.client.get("/champions/history", headers=headers)
        self.assertEqual(champion_history.status_code, 200, champion_history.text)
        self.assertEqual(len(champion_history.json()), 1)
        self.assertEqual(fake_showdown.start_battle.await_count, 13)
        self.assertEqual(fake_showdown.submit_choice.await_count, 13)

        abandoned_run = await self.client.post("/runs", headers=headers)
        self.assertEqual(abandoned_run.status_code, 201, abandoned_run.text)
        abandoned_run_id = abandoned_run.json()["id"]
        for round_number in range(1, 7):
            draft_round = await self.client.get(
                f"/runs/{abandoned_run_id}/draft", headers=headers
            )
            self.assertEqual(draft_round.status_code, 200, draft_round.text)
            self.assertEqual(draft_round.json()["round_number"], round_number)
            selected = await self.client.post(
                f"/runs/{abandoned_run_id}/draft/selection",
                headers=headers,
                json={"option_number": 1},
            )
            self.assertEqual(selected.status_code, 200, selected.text)

        abandoned_path = await self.client.get(
            f"/runs/{abandoned_run_id}/battles", headers=headers
        )
        self.assertEqual(abandoned_path.status_code, 200, abandoned_path.text)
        fake_showdown.abandon_battle = AsyncMock()
        with patch(
            "app.modules.battles.application.battle_service.ShowdownClient",
            return_value=fake_showdown,
        ):
            active_battle = await self.client.post(
                f"/runs/{abandoned_run_id}/battles/current/start", headers=headers
            )
            self.assertEqual(active_battle.status_code, 200, active_battle.text)
            abandoned = await self.client.post(
                f"/runs/{abandoned_run_id}/abandon", headers=headers
            )
            self.assertEqual(abandoned.status_code, 200, abandoned.text)
        self.assertEqual(abandoned.json()["status"], "ABANDONED")
        fake_showdown.abandon_battle.assert_awaited_once()

        run_history = await self.client.get("/runs/history", headers=headers)
        self.assertEqual(run_history.status_code, 200, run_history.text)
        self.assertEqual(
            {run["status"] for run in run_history.json()}, {"COMPLETED", "ABANDONED"}
        )

    async def _seed_catalog_and_trainers(self) -> None:
        now = datetime.now(timezone.utc)
        pokemon_rows = []
        build_rows = []
        for index in range(48):
            pokemon = Pokemon(
                external_key=f"test:pokemon/{uuid4()}",
                name=f"Testmon{index:02d}",
                national_dex_number=10000 + index,
                generation=1,
                primary_type="normal",
                base_stats={"hp": 50, "attack": 50, "defense": 50},
                draft_tier=(index % 5) + 1,
                data_source="integration-test",
            )
            pokemon_rows.append(pokemon)
        async with AsyncSession(
            bind=self.connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        ) as session:
            session.add_all(pokemon_rows)
            await session.flush()
            for index, pokemon in enumerate(pokemon_rows):
                build_rows.append(
                    PokemonBuild(
                        pokemon_id=pokemon.id,
                        build_key="integration-test-build",
                        nature="Serious",
                        ability="Run Away",
                        moves=["Tackle", "Protect"],
                        evs={"hp": 4, "attack": 252, "speed": 252},
                        ivs={"hp": 31, "attack": 31, "speed": 31},
                        validation_status="VALID",
                        validated_format="gen9nationaldexag",
                        validated_at=now,
                        is_default=True,
                    )
                )

            trainer_rows = []
            for index in range(14):
                trainer = Trainer(name=f"Integration Trainer {index}", region="Kanto")
                trainer_rows.append((trainer, index))
            session.add_all(trainer for trainer, _ in trainer_rows)
            await session.flush()
            for trainer, index in trainer_rows:
                if index < 8:
                    category = "GYM_LEADER"
                elif index < 12:
                    category = "ELITE_FOUR"
                else:
                    category = "CHAMPION"
                team = TrainerTeam(
                    trainer_id=trainer.id,
                    team_key="integration-team",
                    category=category,
                    anime_period="Integration fixture",
                )
                session.add(team)
                await session.flush()
                for slot in range(1, 7):
                    member = pokemon_rows[(index + slot) % len(pokemon_rows)]
                    session.add(
                        TrainerTeamPokemon(
                            trainer_team_id=team.id,
                            pokemon_id=member.id,
                            slot_number=slot,
                            nature="Serious",
                            ability="Run Away",
                            moves=["Tackle", "Protect"],
                            evs={"hp": 4, "attack": 252, "speed": 252},
                            ivs={"hp": 31, "attack": 31, "speed": 31},
                        )
                    )
            session.add_all(build_rows)
            await session.commit()

    @staticmethod
    async def _fake_start_battle(**_kwargs):
        return {
            "status": "RUNNING",
            "request": {"active": [{"moves": [{"move": "Tackle", "pp": 35}]}]},
            "simulator_result": None,
            "engine_version": "test-showdown",
            "events": [
                {"event_type": "start", "payload": {"line": "|start|"}}
            ],
        }

    @staticmethod
    async def _fake_complete_battle(**_kwargs):
        return {
            "status": "COMPLETED",
            "request": None,
            "simulator_result": "WIN",
            "engine_version": "test-showdown",
            "events": [
                {"event_type": "win", "payload": {"line": "|win|Player"}}
            ],
        }


if __name__ == "__main__":
    unittest.main()
