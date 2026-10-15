# Banco de dados local

O PostgreSQL roda pelo serviço `postgres` definido em `compose.yaml`. Os dados ficam em um volume nomeado do Docker, então reiniciar ou recriar o contêiner não apaga o banco.

## Preparar as credenciais locais

Na raiz do projeto, copie `.env.example` para `.env` e troque `POSTGRES_PASSWORD` por uma senha local sua. O arquivo `.env` é ignorado pelo Git.

```powershell
Copy-Item .env.example .env
```

## Iniciar e parar

Na raiz do projeto:

```powershell
docker compose up -d postgres
docker compose ps
docker compose down
```

`docker compose down` mantém o volume com os dados. `docker compose down --volumes` também remove o volume e apaga os dados locais do banco.

O PostgreSQL fica disponível somente na própria máquina, na porta definida por `POSTGRES_PORT` (5432 por padrão).

## Estrutura inicial

Esta pasta raiz guarda documentação e arquivos de entrada mantidos pelo projeto, como a seleção aprovada de treinadores. Ela não contém o código ORM nem as migrações: os modelos SQLAlchemy ficam em `backend/app/db/models/`, a conexão fica em `backend/app/db/`, e Alembic é o único responsável pelas revisões em `backend/alembic/versions/`. As importações de dados e atualizações de catálogo ficam em `backend/scripts/`; não se duplicam aqui. O esquema inicial contém estas tabelas:

- `users`
- `pokemon` e `pokemon_builds`
- `trainers`, `trainer_teams` e `trainer_team_pokemon`
- `runs` e `run_draft_options`
- `teams` e `team_pokemon`
- `battles`
- `hall_of_fame`, `champion_history` e `current_champion`

A estrutura define chaves estrangeiras, unicidade, intervalos válidos e índices para impedir mais de uma run ativa por conta. Regras que dependem de várias linhas — por exemplo, exigir exatamente seis Pokémon em cada time de treinador — também precisarão ser validadas pela lógica da aplicação/importação de dados.

## Elenco de treinadores

O seed em `seeds/trainers/elenco_aprovado.json` é a fonte usada para importar os **100 treinadores** e suas versões de time. Ele preserva times parciais do Kaggle como inativos e registra separadamente escalações completas encontradas em jogos ou batalhas específicas. A importação não mistura Pokémon de ocasiões diferentes para completar uma equipe.

`trainer_team_pokemon` permite a mesma espécie em mais de um slot do mesmo time, pois alguns times oficiais repetem Pokémon. Cada slot continua único e numerado de 1 a 6; o preenchimento automático deve evitar acrescentar uma espécie que já esteja naquele time.

Para validar o seed sem gravar, execute em `backend/`:

```powershell
python -m scripts.import_trainers.import_trainer_roster
```

Para aplicar ao PostgreSQL local:

```powershell
python -m scripts.import_trainers.import_trainer_roster --apply
```

A carga contém 182 versões de time, das quais 111 estão ativas. Há 91 treinadores com ao menos um time ativo; todos os times ativos têm seis Pokémon com builds válidas em `gen9nationaldexag`. Os 71 registros parciais do Kaggle continuam inativos como histórico. Dez equipes aprovadas pelo usuário foram completadas com uma mistura explicitamente documentada de Pokémon usados em outras aparições e escolhas temáticas; esses acréscimos não são apresentados como um sexteto oficial de uma única batalha. Variantes oficiais completas foram registradas separadamente a partir de escalações de jogos; isso inclui equipes encontradas anteriormente para os 12 treinadores que estavam pendentes na checagem fora de Kalos/Alola/Galar/Paldea.

Nove treinadores seguem sem variante ativa: Allister, Bea, Gordie, Kabu, Melony, Nessa, Opal, Piers e Raihan. Seus registros selecionados continuam parciais, e não foi encontrada uma escalação canônica de seis adequada no levantamento atual.

Há 99 URLs de sprites preenchidas. Os arquivos vêm do diretório de sprites de treinadores do Pokémon Showdown; o crédito aponta para o índice de artistas da fonte. Gary usa o sprite de Blue, sua contraparte nos jogos; Paul permanece sem URL porque não há sprite correspondente no diretório consultado.

A lista completa dos registros ainda inativos, com a indicação de quais treinadores já têm uma variante jogável, está em [`relatorio_times_inativos.md`](seeds/trainers/relatorio_times_inativos.md).

## Catálogo e batalhas

O catálogo do jogo cobre as gerações I a IX. As batalhas usam o formato Singles `gen9nationaldexag`, permitindo Pokémon de qualquer região sem restringir os times aos jogos Scarlet/Violet. O catálogo contém 1025 espécies base, além de formas alternativas usadas pelos treinadores. Os tiers já definidos para o draft permanecem 5%, 10%, 15%, 35% e 30%; lendários e míticos continuam no pool separado de 5%.
