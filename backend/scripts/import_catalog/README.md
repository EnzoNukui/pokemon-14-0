# Catálogo de Pokémon

O importador `import_pokemon.py` coordena a preparação e gravação do catálogo das gerações I a IX. As responsabilidades ficam separadas: `pokeapi_client.py` busca e armazena respostas da PokéAPI em cache local; `pokemon_normalizer.py` normaliza espécies e formas e cria builds candidatas determinísticas; `pokemon_repository.py` grava Pokémon e builds no PostgreSQL. A Pokédex Nacional tem 1025 espécies base até Pecharunt. O importador também traz formas alternativas que não sejam Mega, Primal, Gigantamax ou Totem, marcando-as como exclusivas dos times de treinadores para que não entrem no draft.

As builds usam até quatro golpes distintos e natureza/EVs com um perfil ofensivo genérico, sem item segurado. Os nomes são armazenados pelo nome canônico da espécie. O importador não ativa builds: grava cada uma como candidata (`is_default = false`) e com validação `PENDING`.

## Validar builds com Pokémon Showdown

O validador usa Pokémon Showdown e o formato Singles `gen9nationaldexag`. O National Dex permite times com espécies de qualquer geração, incluindo Pokémon que não aparecem nos jogos Scarlet/Violet, e Anything Goes remove banimentos competitivos de espécies. Builds antigas Gen VII continuam no histórico; as novas builds `gen9-generated-v1` passam a ser as únicas candidatas a build padrão depois de aprovadas.

Na raiz do projeto, instale a dependência da engine uma vez:

```powershell
cd battle-engine
npm ci
cd ..\backend
```

Com PostgreSQL ligado, migrações aplicadas e o ambiente Python configurado, valide sem gravar:

```powershell
python -m scripts.validate_builds.validate_pokemon_builds
```

Para gravar os resultados e marcar builds válidas como padrão:

```powershell
python -m scripts.validate_builds.validate_pokemon_builds --apply
```

Se uma combinação inicial falhar, o validador tenta uma combinação de golpes e habilidade do movepool da Gen IX exposto pelo Showdown. Somente o TeamValidator do Showdown aprova a build. A importação do catálogo redefine as validações para `PENDING`; após importar novamente, rode a validação outra vez. Ao aprovar uma build Gen IX, o script desativa a build anterior daquela espécie como padrão para preservar exatamente uma build padrão por Pokémon.

O importador não escolhe `draft_tier`; a classificação de tier é uma etapa separada. O draft só seleciona Pokémon que tenham uma build padrão e tier configurado; validar a build, por si só, não define o tier. As migrações do esquema continuam sob responsabilidade exclusiva de Alembic em `backend/alembic/`; os scripts de importação não criam nem alteram o esquema.

## Classificar tiers do draft

O script `scripts/classify_catalog/classify_pokemon_tiers.py` consulta os tiers Singles do Showdown para Gen IX, grava o tier competitivo original em `competitive_tier` e converte para os cinco tiers do projeto. Lendários e míticos mantêm `draft_tier` vazio porque entram na categoria separada com chance de 5%. Espécies sem tier padrão atual conservam o tier de projeto já salvo; para espécies novas nessa situação, o fallback inicial é Tier 1, que precisa de revisão de balanceamento.

Mapeamento inicial:

| Tier do Showdown | Tier do projeto |
| --- | ---: |
| Uber, AG, OU, (OU), UUBL | 5 |
| UU, RUBL | 4 |
| RU, NUBL | 3 |
| NU, PUBL | 2 |
| PU, ZUBL, ZU, LC, NFE | 1 |

Rode primeiro sem `--apply` para revisar a distribuição. Depois de aplicar a migração e instalar as dependências Showdown, grave a classificação:

```powershell
python -m alembic upgrade head
python -m scripts.classify_catalog.classify_pokemon_tiers
python -m scripts.classify_catalog.classify_pokemon_tiers --apply
```

O tier competitivo original fica guardado para que a conversão seja auditável e possa ser refeita caso o critério mude. A migração do catálogo não redefine os tiers já classificados.

Depois que o PostgreSQL estiver ativo e a migração aplicada, execute a partir de `backend/`:

```powershell
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m scripts.import_catalog.import_pokemon --apply
python -m scripts.validate_builds.validate_pokemon_builds --apply
python -m scripts.classify_catalog.classify_pokemon_tiers --apply
```

Sem `--apply`, o script apenas busca os dados e mostra quantos registros preparou. O comando de importação é idempotente: pode ser repetido para atualizar os dados sem duplicar Pokémon ou builds.
