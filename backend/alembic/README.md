# Migrações do banco

Este ambiente do Alembic usa a configuração SQLAlchemy do aplicativo e `Base.metadata`. Todos os modelos são importados em `env.py` para registrar suas tabelas.

A revisão `20261014_0001` cria o esquema inicial. Ela é a revisão de bootstrap e usa o metadata completo; depois de aplicada a um banco compartilhado, mantenha-a imutável. Alterações futuras devem ser registradas em novas revisões Alembic.

Os comandos serão executados a partir de `backend/`, com o PostgreSQL disponível e o `.env` da raiz preenchido:

```powershell
python -m alembic revision --autogenerate -m "descricao da mudanca"
python -m alembic upgrade head
```

As migrações aplicadas são parte do histórico compartilhado e devem permanecer intactas. Para novas revisões, use o identificador único gerado pelo Alembic e uma descrição legível no nome do arquivo; não é necessário incluir a data no nome.

A revisão `20261015_0006` acrescenta `ABANDONED` aos estados de batalha para que uma partida em andamento seja encerrada junto com a run. Aplique `python -m alembic upgrade head` antes de usar a nova regra de abandono.
