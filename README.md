# serv-dialogo-redes
Trabalho Final de disciplina de Fundamentos de Redes de Computadores

Requirementos:
- Python 3.10.*
- Docker-compose
- pip 23.3.1

Para Iniciar localmente:
- Crie uma [Crie uma virtualenv](https://docs.python.org/3/library/venv.html´virtualenv)
- Entre na virtualenv
- Instale os requirements: ``pip install -r requirements.txt``
- Inicie o serviço do postgres: ``docker-compose up -d``
- Inicie a API: 
    - ``cd serv-dialogo-redes``
    - ``uvicorn app.main:app --reload``

Swagger: /docs
