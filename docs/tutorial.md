# Tutorial
O objetivo deste projeto é ajudar os usuários a gerenciar e monitoriar suas finanças pessoais de forma eficaz. A API oferece funcionalidades abrangentes, incluindo a criação de perfis de titulares, contas financeiras, categorias para as transações, estabelecimento de orçamentos e registro detalhado de transações financeiras. Com recursos para categorização precisa e acompanhamento contínuo, os usuários podem ter um controle mais sólido sobre suas despesas, receitas e metas financeiras.

{% include "templates/instalacao.md" %}


## Como usar?

### Operações

Temos operações que são fundamentais para garantir um gerenciamento eficaz e seguro de todas as informações financeiras e relacionadas aos titulares dentro do sistema, garantindo que as operações possam ser executadas de maneira eficiente e confiável.

* **Listagem de Recursos:** Permite listar todos os registros disponíveis para cada entidade, permitindo uma visão geral de todas as informações presentes no sistema. Isso é crucial para entender a situação atual das contas, transações e outros dados financeiros.

* **Criar Novos Registros:** É possível adicionar novos dados ao sistema para cada entidade. Isso permite a adição de novas contas, titulares, transações e outras informações relevenates, expandindo assim a base de dados com informações atualizadas.

* **Visualizar Detalhes Específicos:** Obtenção de detalhes específicos para cada registro, incluindo informações detalhadas sobre contas individuais, detalhes do titular, informações de transações e outros elementos importantes para a compreensão completa das atividades financeiras.

* **Atualizar Registros Existentes:** Existe a capacidade de modificar e atualizar informações específicas para cada entidade, garantindo que o saldo das contas, detalhes dos usuários e outras informações estejam sempre precisas e atualizadas conforme as necessidades do sistema.

* **Excluir Registros:** A remoção de registros específicos do sistema é possível quando necessário, mantendo a integridade e a organização dos dados financeiros em geral.

### Owner

Representa as operações relacionadas aos titulares de contas bancárias. Essa API oferece funcionalidades para gerenciar todos os dados dos titulares, desde a criação à remoção do titular, que são essenciais para a funcionalidade do sistema.

#### GET api/owners/

Retorna uma lista com todos os titulares cadastrados no banco de dados.

```json
[
	{
		"id": 1,
		"username": "moschen",
		"first_name": "Eduardo",
		"last_name": "Moschen",
		"email": "moschen@email.com"
	},
	{
		"id": 2,
		"username": "carlosalberto1",
		"first_name": "Carlos",
		"last_name": "Alberto",
		"email": "calberto@email.com"
	}
]
```

#### POST api/owners/

É usada para cadastrar um novo titular no banco de dados. Para realizar a operação com sucesso, os clientes devem fornecer o primeiro nome, último nome, nome de usuário, e-mail e senha.

```json
{
    "first_name": "Eduardo",
	"last_name": "Moschen",
	"username": "moschen",
	"email": "moschen@email.com",
    "password": "T3st@ndo"
}
```

Caso não informe um desses campos, retornará uma mensagem solicitando tal campo.

```json
{
	"first_name": "Eduardo",
	"last_name": "Moschen",
	"email": "moschen@email.com"
}
```

```json
{
	"username": [
		"Este campo é obrigatório."
	],
	"password": [
		"Este campo é obrigatório."
	]
}
```

Além disso, caso já tenha um e-mail ou usuário cadastrado e ocorra uma solicitação de cadastro com o mesmo nome, retornará uma mensagem informando.

```json
{
	"username": [
		"Um usuário com este nome de usuário já existe."
	],
	"email": [
		"Um usuário com este email já existe."
	],
	"password": [
		"Este campo é obrigatório."
	]
}
```

#### GET api/owner/pk/

Retorna uma lista com os detalhes de um titular específico. Necessita de passar o ID do titular como parâmetro.

```json
{
	"id": 1,
	"username": "moschen",
	"first_name": "Eduardo",
	"last_name": "Moschen",
	"email": "moschen@email.com"
}
```

#### PATCH api/owner/pk/

Atualiza um titular específico, mas de forma que não necessita atualizar todos os dados, apenas o que solicitar.

Neste caso, foi solicitado a alteração da senha.

```json
{
	"password": "sdmssssspd2"
}
```

#### DELETE api/owner/pk/

É usado para deletar o usuário cadastrado no banco de dados. Retorna apenas o método HTTP 204 No Content informando que foi deletado com sucesso.

Quando o titular é deletado, todos os dados relacionados à ele também serão deletados.


### Account

Representa as operações relacionadas à conta financeira de um titular específico. Essa API oferece funcionalidades essenciais para gerenciar informações relacionadas à conta e ao titular, permitindo interações fundamentais com o sistema

#### GET api/accounts/

Retorna uma lista com todas as contas bancárias cadastradas no banco de dados.

```json
[
	{
		"id": 3,
		"name": "Conta Corrente",
		"balance": "1050.00",
		"created_at": "2023-08-16T15:44:33.227307-03:00",
		"owner": 1
	},
	{
		"id": 5,
		"name": "Conta Corrente",
		"balance": "750.00",
		"created_at": "2023-08-19T19:58:43.550259-03:00",
		"owner": 2
	}
]
```

#### POST api/accounts/

É usada para cadastrar uma nova conta bancária no banco de dados. Para realizar essa operação com sucesso, deve-se informar o ID do titular para poder atribuir a conta ao titular, o nome da conta (Corrente, Poupança ou outra que quiser) e o saldo inicial da conta. 

```json
{
	"name": "Conta Corrente",
	"balance": 1050,
	"owner": 1
}
```

Aqui todos os camos são obrigatórios. Caso não seja inserido, retornará uma mensagem informando a ausência do campo.

```json
{
	"name": "Conta Corrente",
	"balance": 1520
}
```

```json
{
	"owner": [
		"Este campo é obrigatório."
	]
}
```

Outro ponto é quando for inserir o saldo inicial e este for negativo. Será retornado uma mensagem informando que não é permitido.

```json
{
	"name": "Conta Corrente",
	"balance": -1520,
	"owner": 1
}
```

```json
{
	"balance": [
		"The balance must not be negative."
	]
}
```

#### GET api/account/pk/

Retorna uma lista com os detalhes de uma conta específica. Necessita de passar o ID da conta como parâmetro.

Dentre os detalhes da conta estão todas as transações realizadas e os orçamentos, ambas de acordo com a categoria escolhida.

```json
{
	"owner": {
		"id": 1,
		"username": "moschen",
		"first_name": "Eduardo",
		"last_name": "Moschen",
		"email": "moschen@email.com"
	},
	"transactions": [
		{
			"id": 4,
			"amount": "210.00",
			"description": "Compra em supermercado",
			"account": 3,
			"category": 1
		}
	],
	"budgets": [
		{
			"id": 1,
			"amount": "500.00",
			"start_date": "2023-08-01",
			"end_date": "2023-08-31",
			"spent": "210.00",
			"account": 3,
			"category": 1
		}
	]
}
```

#### PATCH api/account/pk/

Atualiza os dados da conta bancária de forma parcial, onde não precisa inserir todos os dados para atualização, apenas o ID do titular.

Neste exemplo, atualizamos o nome da conta.

```json
{
	"name": "Current Account",
	"owner": 1
}
```

```json
{
	"id": 3,
	"name": "Current Account",
	"balance": "850.00",
	"created_at": "2023-08-16T15:44:33.227307-03:00",
	"owner": 1
}
```

#### DELETE api/account/pk/

É usado para deletar a conta bancária cadastrada no banco de dados. Retorna apenas o método HTTP 204 No Content informado que foi deletado com sucesso.


### Category

Representa as operações relacionadas as categorias. A partir dessa API que é possível fazer as relações entre transação e orçamento, onde ambas dependem da categoria que foi selecionada pelo usuário.

#### GET api/categories/

Retorna uma lista com todas as categorias cadastradas no banco de dados.

```json
[
	{
		"id": 1,
		"name": "Alimentação"
	},
	{
		"id": 3,
		"name": "Aluguel"
	},
	{
		"id": 4,
		"name": "Academia"
	}
]
```

#### POST api/categories/

É usada para cadastrar uma nova categoria no banco de dados. Para realizar a operação com sucesso, os clientes devem fornecer apenas um campo, que é o nome da categoria desejada.

```json
{
	"name": "Remédios"
}
```

#### GET api/category/pk/

Retorna uma lista com os detalhes de uma categoria específica. Necessita de passar o ID da categoria como parâmetro.

```json
{
	"id": 1,
	"name": "Alimentação"
}
```

#### PUT api/category/pk/

Atualiza a categoria específica. Como a categoria só tem apenas um campo, que é o nome, a atualização é feita de forma completa.

Neste exemplo, a alteração ocorreu de `Remédios` para `Medicamentos`

```json
{
	"name": "Medicamentos"
}
```

#### DELETE api/category/pk/

É usado para deletar a categoria cadastrada no banco de dados. Retorna apenas o método HTTP 204 No Content informando que foi deletado com sucesso.

Quando a categoria é deletada, as transações e orçamentos também são deletados, pois dependem de categoria.


### Transaction

Representa as operações relacionadas às transações financeiras de uma conta bancária. Essa API oferece funcionalidades essenciais para gerenciar informações de acordo com a relação entre a categoria definida pelo titular. 

#### GET api/transactions/

Retorna uma lista com todas as transações cadastradas no banco de dados.

```json
[
	{
		"id": 5,
		"amount": "200.00",
		"description": "Pagamento de aluguel",
		"account": 3,
		"category": 3
	}
]
```

#### POST api/transactions/

É usada para cadastrar uma nova transaçao no banco de dados. Para realizar a operação com sucesso, os clientes devem fornecer o ID da conta bancária, o ID da categoria, o valor e a descrição da transação.

```json
{
	"amount": 100.00,
	"description": "Reajuste do valor",
	"account": 8,
	"category": 4
}
```

Aqui todos os campos são obrigatórios. Caso não seja inserido, retornará uma mensagem informando a ausência do campo.

```json
{
	"amount": 100.00,
	"account": 8,
	"category": 4
}
```

```json
{
	"description": [
		"Este campo é obrigatório."
	]
}
```

#### GET api/transaction/pk/

Retorna uma lista com os detalhes de uma transação específica. Necessita de passar o ID da transação como parâmetro.

```json
[
    {
		"id": 9,
		"amount": "100.00",
		"description": "Reajuste do valor",
		"account": 8,
		"category": 4
	}
]
```

#### PATCH api/transaction/pk/

Atualiza os dados da transação de forma parcial, onde não precisa inserir todos os dados para atualização.

Neste exemplo, atualizamos o valor da transação.

```json
{
	"amount": "120.00",
	"description": "Reajuste do valor",
	"account": 8,
	"category": 4
}
```

```json
{
	"id": 9,
	"amount": "120.00",
	"description": "Reajuste do valor",
	"account": 8,
	"category": 4
}
```

#### DELETE api/transaction/pk/

É usado para deletar a transação cadastrada no banco de dados. Retorna apenas o método HTTP 204 No Content informando que foi deletado com sucesso.

Além disso, caso a transação esteja assciada a um orçamento, ao excluí-la será atualizado o valor gasto no orçamento; diminuindo o valor da transação excluída.

### Budget

Representa as operações relacionadas aos orçamentos de uma conta bancária. Essa API oferece funcionalidades essenciais para gerenciar informações de acordo com as transações realizadas pelo titular.

#### GET api/budgets/

Retorna uma lista com todos os orçamentos cadastrados no banco de dados.

```json
[
	{
		"id": 1,
		"amount": "-250.00",
		"start_date": "2023-08-01",
		"end_date": "2023-08-31",
		"spent": "0.00",
		"account": 8,
		"category": 4
	},
	{
		"id": 4,
		"amount": "150.00",
		"start_date": "2023-08-01",
		"end_date": "2023-08-31",
		"spent": "0.00",
		"account": 8,
		"category": 4
	}
]
```

#### POST api/budgets/

É usado para cadastrar um novo orçamento no banco de dados. Para realizar a operação com sucesso, os clientes devem fornecer o ID da conta bancária, o ID da categoria, o valor do orçamento, a data de início e término do orçamento e, por fim, o valor gasto.

```json
{
	"amount": "150.00",
	"start_date": "2023-08-01",
	"end_date": "2023-08-31",
	"account": 8,
	"category": 4
}
```

Aqui todos os campos são obrigatórios, menos o `spent`. Caso não seja inserido, retornará uma mensagem informando a ausência do campo.

```json
{
	"amount": "150.00",
	"start_date": "2023-08-01",
	"end_date": "2023-08-31",
	"account": 8
}
```

```json
{
	"category": [
		"Este campo é obrigatório."
	]
}
```

#### GET api/budget/pk/

Retorna uma lista com os detalhes de um orçamento específico. Necessita de passar o ID do orçamento como parâmetro.

```json
{
	"id": 1,
	"account": 3,
	"category": 1,
	"amount": "500.00",
	"start_date": "2023-08-01",
	"end_date": "2023-08-31"
}
```

#### PUT api/budget/pk/

Atualiza o orçamento específico. Necessita de inserir todos os dados para concluir a atualização das informações.

Neste exemplo, foi atualizado o valor do orçamento.

```json
{
	"amount": 250.00,
	"start_date": "2023-08-01",
	"end_date": "2023-08-31",
	"account": 8,
	"category": 4
}
```

```json
{
	"id": 1,
	"amount": "250.00",
	"start_date": "2023-08-01",
	"end_date": "2023-08-31",
	"spent": "0.00",
	"account": 8,
	"category": 4
}
```

#### DELETE api/budget/pk/

É usado para deletar o orçamento cadastrado no banco de dados. Retorna apenas o método HTTP 204 No Content informando que foi deletado com sucesso.