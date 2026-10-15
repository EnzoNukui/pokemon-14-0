# Organização dos módulos

O back-end é um monólito modular. Cada pasta dentro de `modules/` representa uma área funcional e usa nomes de camadas consistentes quando aquela camada contém código:

- `domain/`: regras puras e tipos do domínio, sem HTTP, banco ou serviços externos.
- `application/`: casos de uso e coordenação das operações.
- `presentation/`: rotas HTTP, dependências e schemas da API.
- `infrastructure/`: integrações externas e adaptadores técnicos.

Nem todo módulo precisa das quatro camadas. Uma pasta de camada só deve existir quando houver uma responsabilidade concreta para colocar nela; não criamos camadas vazias para completar um molde.

## Limites atuais

- `accounts`: cadastro, login e identificação do usuário autenticado.
- `runs`: ciclo de vida, draft, escolha da sequência de adversários e avanço pelas 13 lutas.
- `battles`: início e avanço de uma batalha no Showdown, conversão dos times e envio dos eventos transitórios ao cliente.
- `championship`: snapshot das runs concluídas, Hall da Fama e sucessão do campeão.

O módulo `battles` não decide a progressão da run. Ele devolve o resultado produzido pelo simulador; `runs` aplica as regras da sequência. Ao vencer a última batalha, `runs` chama o caso de uso de `championship` dentro da mesma transação.

Os modelos ORM e a sessão ficam centralizados em `app/db`; as migrações ficam em `alembic`. Rotinas de importação e manutenção do catálogo continuam em `scripts`, e seus arquivos de entrada e documentação ficam em `database/` na raiz do projeto.

Os caminhos HTTP atuais permanecem sem o prefixo `/api/v1`. A versão da API será definida quando houver necessidade concreta de compatibilidade entre clientes.
