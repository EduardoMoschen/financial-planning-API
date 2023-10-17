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