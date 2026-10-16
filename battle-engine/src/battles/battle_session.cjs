'use strict';

const { snapshot } = require('./battle_snapshot.cjs');
const { createBattleStreams } = require('../showdown/battle_stream.cjs');
const { serializeTeams } = require('../teams/team_serializer.cjs');

const BATTLE_TIMEOUT_MS = 60000;

class BattleSession {
  constructor(input) {
    this.teams = serializeTeams(input);
    this.playerName = String(input.player.name || 'Player').slice(0, 18);
    this.request = null;
    this.requestCount = 0;
    this.winner = null;
    this.activeSpecies = { p1: null, p2: null };
    this.pendingEvents = [];
    this.waiters = new Set();
    this.revision = 0;
    this.engineError = null;
    this.lastChoiceError = null;

    this.streams = createBattleStreams(input, this);
  }

  signal() {
    this.revision += 1;
    const waiters = [...this.waiters];
    this.waiters.clear();
    for (const wake of waiters) wake();
  }

  async waitFor(condition, timeoutMs = BATTLE_TIMEOUT_MS) {
    if (condition()) return;
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.waiters.delete(wake);
        reject(new Error('Timed out waiting for Showdown.'));
      }, timeoutMs);
      const wake = () => {
        clearTimeout(timeout);
        if (condition()) resolve();
        else this.waiters.add(wake);
      };
      this.waiters.add(wake);
    });
  }

  async waitUntilComplete() {
    await this.waitFor(() => this.winner !== null || this.engineError);
    if (this.engineError) throw new Error(this.engineError);
  }

  snapshot() {
    return snapshot(this);
  }

  async submitChoice(choice) {
    const previousRequestCount = this.requestCount;
    this.request = null;
    this.lastChoiceError = null;
    await this.streams.p1.write(choice);
    await this.waitFor(() =>
      this.requestCount > previousRequestCount || this.winner !== null ||
      this.engineError || this.lastChoiceError,
    );
    if (this.engineError) throw new Error(this.engineError);
    const payload = this.snapshot();
    if (this.lastChoiceError) payload.choice_error = this.lastChoiceError;
    return payload;
  }

  close() {
    void this.streams.omniscient.writeEnd();
  }
}

module.exports = { BattleSession };
