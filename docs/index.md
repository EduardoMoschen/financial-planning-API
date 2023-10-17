![logo](assets/logo.png){ width="280" .center }

# Expense Control

O projeto `Expense Control` é uma API baseada em Django REST Framework (DRF) que capacita os usuários a gerenciar suas finanças pessoais com eficiência. Oferece recursos abrangentes, incluindo criação de perfis, contas, categorias e orçamentos, juntamente com um registro detalhado de transações financeiras. Ao permitir uma categorização precisa e monitoramento contínuo, os usuários podem ter um controle sólido sobre suas despesas, receitas e metas financeiras.
{% include "templates/cards.html" %}


{% include "templates/instalacao.md" %}

## Como usar?

### Operações Fundamentais

- **Listagem de Recursos:** Visualizar todos os registros disponíveis para cada entidade.
- **Criação de Registros:** Adicionar novos dados ao sistema para cada entidade.
- **Visualizar Detalhes Específicos:** Obter detalhes específicos para cada registro.
- **Atualizar Registros Existentes:** Modificar informações específicas para cada entidade.
- **Excluir Registros:** Remover registros específicos do sistema.

Aqui estão as principais entidades e suas operações:

* **Owner:**
    - Gerencie os titulares de contas bancárias.
    - Operações incluem listagem, criação, visualização detalhada, atualização e exclusão.

* **Account:**
    - Gerencie contas bancárias.
    - Operações incluem listagem, criação, visualização detalhada, atualização e exclusão.

* **Category:**
    - Gerencie categorias.
    - Operações incluem listagem, criação, visualização detalhada, atualização e exclusão.

* **Transaction:**
    - Gerencie transações financeiras.
    - Operações incluem listagem, criação, visualização detalhada, atualização e exclusão.

* **Budget:**
    - Gerencie orçamentos relacionados a transações.
    - Operações incluem listagem, criação, visualização detalhada, atualização e exclusão.

A documentação fornecida oferece exemplos claros e ilustrativos de como usar cada operação e o formato das solicitações e respostas esperadas. 