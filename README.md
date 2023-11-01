# Expense Control

[![Documentation Status](https://readthedocs.org/projects/financial-planning-api/badge/?version=latest)](https://financial-planning-api.readthedocs.io/en/latest/?badge=latest) 
![CI](https://github.com/EduardoMoschen/financial-planning-API/actions/workflows/pipeline.yaml/badge.svg) 
[![codecov](https://codecov.io/gh/EduardoMoschen/financial-planning-API/graph/badge.svg?token=LZXNMFQYO8)](https://codecov.io/gh/EduardoMoschen/financial-planning-API)

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

## Como instalar o projeto

Certifique-se de ter o Python 3.10, ou uma versãos mais recente, instalada.

Clone o repositório do projeto do GitHub usando o seguinte comando

```bash
git clone https://github.com/EduardoMoschen/financial-planning-API.git
```

Crie um ambiente virtual usando o seguinte comando

```python
python -m venv nome-do-ambiente
```

Ative o ambiente virtual de acordo com o seu sistema operacional

Para a instalação dos requisitos, recomendamos que use o pip

```bash
pip install -r requirements.txt
```

Execute as migrações do Djando com o comando
    
```python
python manage.py migrate
```

Inicie o servidor de desenvolvimento com o seguinte comando

```python
python manage.py runserver
```

## Dica!

Para um melhor proveito de como usar os endpoints e métodos, além de visualizar como está sendo o retorno e criação de dados, indico a instalação do programa `Insomnia`.

Acesse para realizar o download: <https://insomnia.rest/download>