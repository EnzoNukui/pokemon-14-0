# Engine de batalhas

Este serviço Node.js mantém sessões temporárias de Pokémon Showdown. Uma IA tática escolhe movimentos por poder, precisão, STAB e efetividade de tipos, e troca apenas diante de uma desvantagem clara ou risco de nocaute. Após uma troca tática, ela evita voltar ao Pokémon anterior contra o mesmo adversário. O back-end Python equipa os times dos treinadores com Life Orb quando o conjunto não define outro item.

## Organização do código

- `src/server.cjs`: inicializa o servidor HTTP e trata falhas inesperadas.
- `src/http/`: roteamento, leitura/escrita JSON e validação das escolhas recebidas.
- `src/battles/`: casos de uso da batalha, armazenamento em memória, estado da sessão e snapshots.
- `src/showdown/`: criação dos streams do simulador e observação das respostas.
- `src/protocol/`: interpretação das linhas do protocolo em eventos e pedidos do jogador.
- `src/teams/`: serialização dos times para o formato aceito pelo Showdown.
- `src/ai/`: avaliação de movimentos e escolhas estratégicas dos dois lados da batalha.
- `scripts/`: validação de builds e exportação dos tiers Gen IX.

As batalhas e a validação de builds usam `gen9nationaldexag`, que aceita equipes com espécies das gerações I a IX. O catálogo base do backend cobre os 1025 números da Pokédex Nacional; formas alternativas necessárias aos times são armazenadas como entradas próprias.

As sessões e eventos vivem na memória do processo e podem ser perdidos se a engine reiniciar. O serviço Python devolve os eventos ao cliente durante a luta e persiste no PostgreSQL o estado, resultado, formato, versão da engine e horários da batalha.

O esquema e suas migrações pertencem ao back-end Python: SQLAlchemy mantém os modelos em `backend/app/db/models/` e Alembic é o único responsável pelas migrações em `backend/alembic/`. A engine Node não mantém migrações nem define o esquema do banco.

Inicie o serviço pela raiz do projeto com `docker compose up -d battle-engine`.
