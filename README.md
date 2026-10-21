<div align="center">



# 🔴 Pokémon 14-0

### Monte seu time. Vença 13 batalhas. Torne-se o campeão.

Jogo web de **draft aleatório** de 6 Pokémon seguido de **13 batalhas automáticas** contra Líderes de Ginásio, Elite dos Quatro e o Campeão, simuladas pelo motor do **Pokémon Showdown**.

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white&style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white&style=for-the-badge)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white&style=for-the-badge)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge)
<br>
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white&style=for-the-badge)
![Node.js](https://img.shields.io/badge/Node.js-22-5FA04E?logo=nodedotjs&logoColor=white&style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)

[Sobre](#-sobre-o-projeto) •
[Telas](#-telas) •
[Como jogar](#-como-jogar) •
[Instalação](#-instalação-e-execução) •
[Arquitetura](#-arquitetura) •
[API](#-api) •
[Testes](#-testes)

</div>

---

## 📖 Sobre o projeto

**Pokémon 14-0** é um desafio de treinador: você recebe opções aleatórias, monta um time de **6 Pokémon** e enfrenta uma sequência fixa de **13 treinadores**. Perdeu ou empatou uma única batalha? A run acaba. Venceu as 13? Você entra no **Hall da Fama** e pode se tornar o **campeão atual**.

### O que o jogo oferece

- 🎲 **Draft em 6 rodadas** com 6 opções por rodada, 1 reroll por run e no máximo **1 Lendário/Mítico** no time.
- ⚔️ **13 batalhas seguidas**: 8 Líderes de Ginásio → 4 da Elite dos Quatro → Campeão.
- 🤖 **Batalhas automáticas** com replay animado, controle de velocidade do texto e pausa.
- 🏆 **Hall da Fama** e histórico de campeões, com revanche contra o último campeão.
- 👤 **Jogue sem conta** (sessão de visitante) e publique sua vitória no ranking depois, ao entrar.
- 🌍 **Todas as gerações**: catálogo com as 1025 espécies da Pokédex Nacional (Gen I–IX), no formato `gen9nationaldexag` do Showdown.
- 🧑‍🎤 **Elenco de 100 treinadores** do universo Pokémon (jogos e anime), com times validados pelo simulador.

### Regras da run

| Etapa | Regra |
| --- | --- |
| **Draft** | 6 rodadas; em cada uma, 6 opções. Escolha 1. Opções recusadas ou roladas **nunca reaparecem** na mesma run. |
| **Reroll** | 1 por run, troca as 6 opções da rodada atual. |
| **Lendários/Míticos** | Aparecem com 1% de chance por oferta e só **1** pode entrar no time. |
| **Caminho** | Batalhas 1–8: Ginásios · 9–11: Elite dos Quatro · 12: vaga final da Elite (pode ser um dos 15 treinadores de Campeão aprovados) · 13: Campeão. |
| **Adversários** | Nenhum treinador se repete na mesma run. O caminho é sorteado uma vez e fica salvo. |
| **Derrota/Empate** | Encerra a run como falha. Empate **não** conta como vitória. |
| **Vitória na 13ª** | Run concluída. Com conta, entra no Hall da Fama e assume o título de campeão. |
| **Mega Evolução** | Desativada para os dois lados. |
| **Itens** | Líderes de Ginásio não ganham item de dano automático; os demais treinadores recebem *Life Orb* quando não têm item definido. |

<details>
<summary><b>🎲 Probabilidades do draft por tier</b></summary>

<br>

Os pesos são configuráveis no `.env` (`DRAFT_TIER_1_PERCENT` … `DRAFT_TIER_5_PERCENT`) e precisam somar **99%**; o 1% restante é reservado aos Lendários/Míticos.

| Tier do projeto | Chance padrão | Equivale no Showdown a |
| :---: | :---: | --- |
| 1 | 35% | PU, ZUBL, ZU, LC, NFE |
| 2 | 13% | NU, PUBL |
| 3 | 20% | RU, NUBL |
| 4 | 18% | UU, RUBL |
| 5 | 13% | Uber, AG, OU, (OU), UUBL |
| Lendário/Mítico | 1% | categoria separada |

Para evitar espécies fortes em pools comuns, existem pisos de tier por classificação competitiva e por BST (ex.: pseudo-lendários ficam no mínimo no Tier 5). Se um tier ficar sem candidatos, os pesos restantes são normalizados.

</details>

---

## 📸 Telas

> **Como preencher:** salve seus prints em `docs/screenshots/` **com exatamente os nomes abaixo** (formato PNG, ideal 1280×720). O README já aponta para eles, então não é preciso editar nada aqui. Os arquivos atuais são apenas placeholders.

### 🏠 Home
![Tela inicial](docs/screenshots/tela_inicial_pokemon.png)
<sub>📌 Página inicial com a chamada "Monte seu time. Vença 13 batalhas.", as 3 etapas da run (Draft → Desafio → Conquista) e o último campeão.</sub>


### 🎲 Escolhendo o time com a Run!
![Run de Pokémon](docs/screenshots/run_pokemon.png)
<sub>📌 Rodada com 6 opções, os 6 espaços do time, contador de rodadas (ex.: 3 / 6) e botões **Selecionar** e **Rolar de novo**.</sub>

### ⚔️ Batalha
![Arena de batalha](docs/screenshots/batalha_pokemon.png)
<sub>📌 Arena com barras de vida, caixa de diálogo com golpes coloridos por tipo, progresso das 13 lutas e controles de velocidade e pausa.</sub>

### 🏁 Tela de campeão
![Resultado da run](docs/screenshots/campiao_pokemon.png)
<sub>📌 Tela "Campeão!" com o time vitorioso, botão **Publicar no ranking** e **Enfrentar o último campeão**.</sub>

### 🏆 Ranking de campeões
![Hall da Fama](docs/screenshots/ranking_pokemon.png)
<sub>📌 Ranking com posição, treinador e equipe dos campeões.</sub>


---

## 🎮 Como jogar

> Com o projeto rodando (veja [Instalação](#-instalação-e-execução)), abra **http://localhost:5173**.

### Passo 1: Entre (ou não)

Você pode jogar **como visitante**: clique em **Começar run** e pronto. Sua sessão de visitante fica salva no navegador por **30 dias**.

Para guardar histórico e publicar no ranking, clique em **Visitante** no cabeçalho e crie uma conta em **Cadastro**:

| Campo | Regra |
| --- | --- |
| Nome de treinador | mínimo de 2 caracteres |
| E-mail | único (sem diferenciar maiúsculas/minúsculas) |
| Senha | mínimo de 8 caracteres |

### Passo 2: Faça o draft

1. Clique em **Começar run** na Home.
2. Você verá **6 opções** de Pokémon. Clique na que quiser.
3. Confirme em **Selecionar**. A rodada avança (`1 / 6`, `2 / 6`, …).
4. Não gostou das opções? Use **Rolar de novo**. Só funciona **uma vez por run**.
5. Apareceu um Lendário ou Mítico? Você só pode levar **um**; depois disso, os demais ficam bloqueados.
6. Se quiser recomeçar, use **Sair deste time e começar do zero**. A run atual é abandonada.

### Passo 3: Enfrente os 13 treinadores

1. Com os 6 espaços preenchidos, clique em **Iniciar desafio**.
2. A batalha é **simulada automaticamente**. Acompanhe o replay na arena.
3. Use o **controle de velocidade do texto** (1×, 2× e 3×) e o botão de **pausa** na caixa de diálogo para seguir o ritmo que preferir.
4. Vitória? Clique em **Próximo treinador** para avançar.
5. Derrota ou empate? A run termina em **Fim da run**. Volte à Home e comece outra.

A barra de progresso mostra onde você está: **Ginásios → Elite dos Quatro → Campeão**.

### Passo 4: Vire campeão

Vencendo a **13ª batalha** você vê a tela **Campeão!** e pode:

- **Publicar no ranking**: obrigatório para quem jogou como visitante (entre na conta primeiro). Quem já jogava logado é registrado automaticamente.
- **Enfrentar o último campeão**: simula uma revanche contra o time campeão anterior.
- Conferir sua posição no **Hall da Fama**, pelo item **Ranking** do cabeçalho.

### Dicas rápidas

- 💡 **Cobertura de tipos** vale mais do que força bruta: a IA adversária escolhe sempre o golpe de maior pontuação (poder, precisão, STAB e efetividade).
- 💡 Evite um time com fraquezas em comum: um único adversário bem escolhido pode derrubar vários Pokémon.
- 💡 Guarde o reroll para uma rodada em que *nenhuma* opção encaixe.
- 💡 Fechou a aba no meio da run? Volte em **Começar run**: a run ativa é **retomada** (1 run ativa por jogador).

---

## 🚀 Instalação e execução

### Pré-requisitos

| Ferramenta | Versão sugerida |
| --- | --- |
| [Git](https://git-scm.com/) | qualquer recente |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) + Compose | recente |
| [Python](https://www.python.org/) | 3.12 ou superior |
| [Node.js](https://nodejs.org/) | 22 LTS ou superior |

### 1. Clonar e configurar o ambiente

```bash
git clone <url-do-repositorio>
cd pokemon-14-0
```

Copie o arquivo de exemplo:

```powershell
# Windows (PowerShell)
Copy-Item .env.example .env
```
```bash
# Linux / macOS
cp .env.example .env
```

Abra o `.env` e ajuste **obrigatoriamente**:

- `POSTGRES_PASSWORD`: uma senha local sua.
- `AUTH_SECRET_KEY`: uma chave aleatória. Gere uma com:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

> ⚠️ O `.env` é ignorado pelo Git. **Nunca** faça commit dele.

<details>
<summary><b>📋 Variáveis do <code>.env</code></b></summary>

<br>

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `POSTGRES_DB` | `pokemon13` | Nome do banco |
| `POSTGRES_USER` | `pokemon13_local` | Usuário do banco |
| `POSTGRES_PASSWORD` | *(defina)* | Senha do banco |
| `POSTGRES_PORT` / `DATABASE_PORT` | `5432` | Porta do PostgreSQL |
| `DATABASE_HOST` | `127.0.0.1` | Host do banco para o backend |
| `BATTLE_ENGINE_URL` | `http://127.0.0.1:3001` | URL do motor de batalha |
| `BATTLE_ENGINE_PORT` | `3001` | Porta do motor de batalha |
| `BATTLE_ENGINE_TIMEOUT_SECONDS` | `15` | Timeout das chamadas ao motor |
| `AUTH_SECRET_KEY` | *(defina)* | Chave de assinatura dos tokens JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Validade do token de acesso |
| `DRAFT_TIER_1_PERCENT` … `_5_` | `35 / 13 / 20 / 18 / 13` | Pesos do draft (somam 99; 1% vai para lendários) |

Sem os pesos do draft, a API responde **503** ao criar uma run.

</details>

### 2. Subir o banco e o motor de batalha

```bash
docker compose up -d postgres battle-engine
docker compose ps
```

O PostgreSQL e o Showdown ficam acessíveis **apenas na sua máquina** (`127.0.0.1`).

### 3. Preparar o backend

```bash
cd backend
python -m venv .venv
```
```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```
```bash
# Linux / macOS
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
python -m alembic upgrade head
```

### 4. Popular o banco *(somente na primeira vez)*

Os scripts de validação usam o Showdown instalado na pasta `battle-engine`:

```bash
cd ../battle-engine && npm ci && cd ../backend
```

Depois, rode **na ordem** (sem `--apply` o script apenas simula e mostra o que faria):

```bash
# 1) Importa as 1025 espécies e formas (busca na PokéAPI; a 1ª execução é demorada, depois usa cache)
python -m scripts.import_catalog.import_pokemon --apply

# 2) Valida as builds no Showdown (gen9nationaldexag)
python -m scripts.validate_builds.validate_pokemon_builds --apply

# 3) Classifica os Pokémon nos 5 tiers do draft
python -m scripts.classify_catalog.classify_pokemon_tiers --apply

# 4) Importa os 100 treinadores e seus times
python -m scripts.import_trainers.import_trainer_roster --apply
```

> 🧠 Sem os passos 1–4 o draft não tem o que sortear e a run não consegue montar os 13 adversários.

### 5. Iniciar a API

```bash
python -m uvicorn app.main:app --reload
```

| Endereço | O que é |
| --- | --- |
| http://127.0.0.1:8000/health | O processo está de pé |
| http://127.0.0.1:8000/ready | Também confere a conexão com o PostgreSQL |
| http://127.0.0.1:8000/docs | Documentação interativa (Swagger) |

### 6. Iniciar o frontend

Em **outro terminal**:

```bash
cd frontend
npm install
npm run dev
```

Abra **http://localhost:5173** 🎉

O Vite faz proxy de `/api` para `http://127.0.0.1:8000`, então não há configuração extra em desenvolvimento. Para apontar para outra API, defina `VITE_API_BASE_URL`.

### Parar tudo

```bash
docker compose down              # mantém os dados do banco
docker compose down --volumes    # ⚠️ apaga também os dados do banco
```

<details>
<summary><b>🛠️ Problemas comuns</b></summary>

<br>

| Sintoma | Causa provável e solução |
| --- | --- |
| `POSTGRES_PASSWORD` obrigatório ao subir o Compose | Falta preencher o `.env` na **raiz** do projeto. |
| API retorna **503** ao iniciar a run | Pesos `DRAFT_TIER_*` ausentes ou inválidos no `.env`. |
| Draft vazio ou erro ao montar os adversários | O banco não foi populado (veja o passo 4). |
| "O motor de batalha está indisponível" | O container `battle-engine` não está rodando: `docker compose up -d battle-engine`. |
| Batalha travou depois de reiniciar o motor | As sessões vivem na memória do motor e se perdem ao reiniciar. Recarregue a página. |
| **409** ao criar uma run | Você já tem uma run ativa; retome-a ou abandone-a. |
| "A sessão desta run expirou" | Sessão de visitante vencida (30 dias) ou token inválido. Inicie uma nova run. |
| Porta 5432, 3001, 8000 ou 5173 em uso | Feche o programa que a usa ou mude a porta no `.env`. |

</details>

---

## 🧱 Arquitetura

```
┌──────────────────┐   /api    ┌───────────────────────┐   HTTP   ┌─────────────────────┐
│   Frontend       │ ────────► │   Backend (FastAPI)   │ ───────► │   Battle Engine     │
│ React + Vite     │ ◄──────── │   monólito modular    │ ◄─────── │ Node + Showdown     │
│ localhost:5173   │   JSON    │   localhost:8000      │  eventos │ localhost:3001      │
└──────────────────┘           └───────────┬───────────┘          └─────────────────────┘
                                           │ SQLAlchemy (async)
                                           ▼
                                ┌───────────────────────┐
                                │   PostgreSQL 18       │
                                │   localhost:5432      │
                                └───────────────────────┘
```

- O **backend** é dono das regras da run, do draft e da persistência. O **motor de batalha** só simula.
- O resultado de cada batalha e da run vai para o PostgreSQL. Os **eventos do protocolo** são transitórios: voltam ao cliente durante a luta e **não** são arquivados.
- O esquema do banco pertence ao backend: modelos em SQLAlchemy e migrações **somente** via Alembic.

### Módulos do backend

O backend segue um monólito modular, com camadas `domain` (regras puras), `application` (casos de uso), `presentation` (rotas e schemas) e `infrastructure` (integrações).

| Módulo | Responsabilidade |
| --- | --- |
| `accounts` | Cadastro, login e usuário autenticado |
| `runs` | Ciclo de vida da run, draft, caminho dos 13 adversários e progressão |
| `battles` | Inicia e avança uma batalha no Showdown, converte times e devolve eventos |
| `championship` | Hall da Fama, histórico de campeões e revanche |

### Estrutura de pastas

```
pokemon-14-0/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/             # roteador e health checks
│   │   ├── core/            # configurações e segurança (Argon2, JWT)
│   │   ├── db/              # modelos ORM e sessão
│   │   └── modules/         # accounts · runs · battles · championship
│   ├── alembic/             # migrações do banco
│   ├── scripts/             # importação de catálogo, validação de builds, tiers e treinadores
│   └── tests/               # testes unitários e de integração
├── battle-engine/           # serviço Node.js com Pokémon Showdown
│   ├── src/                 # http, battles, showdown, protocol, teams, ai
│   └── test/
├── database/                # documentação e seeds (elenco de treinadores)
├── frontend/                # React + TypeScript + Vite + Tailwind
│   └── src/                 # pages, components, service, types, routes
├── docs/screenshots/        # prints usados neste README
├── compose.yaml             # PostgreSQL + battle-engine
└── .env.example
```

### Tecnologias

| Camada | Stack |
| --- | --- |
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS 4, React Router, React Icons, oxlint |
| **Backend** | Python, FastAPI, Uvicorn, SQLAlchemy (async) + asyncpg, Alembic, Pydantic Settings, httpx |
| **Segurança** | Senhas com Argon2 (pwdlib), tokens JWT HS256 (PyJWT), e-mail normalizado e único sem diferenciar caixa |
| **Banco** | PostgreSQL 18 |
| **Batalhas** | Node.js 22, Pokémon Showdown 0.11.11, formato `gen9nationaldexag` |
| **Infra** | Docker Compose |
| **Dados** | PokéAPI (catálogo), sprites do Pokémon Showdown |

### Banco de dados

| Domínio | Tabelas |
| --- | --- |
| Contas | `users`, sessões de visitante |
| Catálogo | `pokemon`, `pokemon_builds` |
| Treinadores | `trainers`, `trainer_teams`, `trainer_team_pokemon` |
| Run | `runs`, `run_draft_options`, `teams`, `team_pokemon`, `battles` |
| Campeonato | `hall_of_fame`, `champion_history`, `current_champion` |

Índices parciais únicos garantem **uma run ativa por conta** e **uma por sessão de visitante**.

---

## 🔌 API

Rotas sem prefixo de versão. Documentação interativa em `/docs`.

**Autenticação:** `Authorization: Bearer <token>`. Para visitantes: `X-Guest-Session: <token>`, devolvido no `POST /runs` quando não há login.

### Saúde e contas

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/health` | Processo ativo |
| `GET` | `/ready` | Processo + banco |
| `POST` | `/accounts/register` | Cria a conta e devolve o token |
| `POST` | `/accounts/login` | Autentica e devolve o token |
| `GET` | `/accounts/me` | Conta do token enviado |

### Runs e draft

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/runs` | Inicia uma run (409 se já houver uma ativa) |
| `GET` | `/runs/current` | Run ativa do jogador |
| `GET` | `/runs/history` | Histórico da conta |
| `GET` | `/runs/{run_id}/team` | Time e builds escolhidas |
| `GET` | `/runs/{run_id}/result` | Resultado final e snapshot |
| `POST` | `/runs/{run_id}/abandon` | Abandona a run |
| `GET` | `/runs/{run_id}/draft` | Opções da rodada atual |
| `POST` | `/runs/{run_id}/draft/reroll` | Rola de novo (1 vez por run) |
| `POST` | `/runs/{run_id}/draft/selection` | Escolhe `{"option_number": 1}` |

### Batalhas e campeonato

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/runs/{run_id}/battles` | Os 13 adversários da run |
| `GET` | `/runs/{run_id}/battles/current` | Próximo adversário |
| `POST` | `/runs/{run_id}/battles/current/start` | Inicia/avança a batalha atual |
| `POST` | `/runs/{run_id}/battles/{n}/choices` | Envia uma escolha (`{"choice": "move 1"}`) |
| `POST` | `/runs/{run_id}/champion-challenge` | Revanche contra o último campeão |
| `POST` | `/runs/{run_id}/ranking` | Publica a vitória de visitante na conta |
| `GET` | `/champions/ranking` | Ranking público |
| `GET` | `/champions/current` | Campeão atual |
| `GET` | `/champions/history` | Sucessão de campeões |

---

## 🧪 Testes

**Backend**, testes unitários (não precisam de banco), a partir de `backend/`:

```bash
python -m unittest discover -s tests -v
```

**Testes de integração da API** exigem um PostgreSQL **isolado** com as migrações aplicadas:

```bash
export POKEMON_TEST_DATABASE_URL="postgresql+asyncpg://usuario:senha@127.0.0.1:5432/banco_de_teste"
python -m unittest discover -s tests -v
```

> ⚠️ Nunca aponte os testes para um banco que você usa para jogar.

**Motor de batalha** (executa uma batalha real no Showdown):

```bash
cd battle-engine
npm test
```

**Frontend:**

```bash
cd frontend
npm run lint
npm run build
```

---

## 🧑‍💻 Autores

| | |
| --- | --- |
| **Diego Soares Trujillo** | [GitHub](https://github.com/diegotrujillo011) · [LinkedIn](https://www.linkedin.com/in/diego-trujillo-3441b9380) |
| **Enzo Nukui da Silva** | [GitHub](https://github.com/EnzoNukui) · [LinkedIn](https://www.linkedin.com/in/enzo-nukui/) |



## ⚖️ Créditos e aviso legal

Projeto **não oficial**, feito por fãs e sem fins lucrativos. Pokémon e seus nomes são marcas registradas de **Nintendo**, **Game Freak** e **Creatures Inc.**; este projeto não é afiliado a nenhuma delas.

- Simulação de batalhas: [Pokémon Showdown](https://github.com/smogon/pokemon-showdown)
- Dados do catálogo: [PokéAPI](https://pokeapi.co/)
- Sprites de Pokémon e treinadores: diretório de sprites do Pokémon Showdown e artistas creditados no índice da fonte

<div align="center">

Feito e pensado para aqueles são fãs de Pokémon como a gente! Boa sorte na jornada, treinador! 

</div>