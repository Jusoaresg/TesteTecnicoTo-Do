# Um To-Do-List para um teste técnico

## Objetivo:

Desenvolver uma aplicação simples de gerenciamento de tarefas (To-Do List), utilizando Python como linguagem principal, integrando Back-end (API), Front-end, banco de dados, e funcionalidades de segurança. O objetivo é avaliar a capacidade técnica em Python, assim como habilidades com tecnologias complementares.

## Requisitos

- Back-end (Python):
- Utilize Flask ou FastAPI para criar uma API que permita:
- Adicionar uma nova tarefa.
- Atualizar o status de uma tarefa (pendente/completa).
- Remover uma tarefa.
- Listar todas as tarefas.
- Use Redis para cache de tarefas ou sessões, além de um banco de dados
relacional ou não de sua escolha (MySQL, PostgreSQL, MongoDB, etc.) para
armazenar as tarefas de maneira persistente.
- Implemente validação de dados para garantir que as informações das tarefas
estejam corretas e evitar erros (ex.: uma tarefa não pode ter título vazio).

## Configuração do ambiente

O projeto necessita do redis, postgres e uma dotenv na raiz do backend

Estrutura do dotenv:

```
HOST=*
PORT=*
DATABASE=*
USER=*
PASSWORD=*


SECRET_KEY=*
ALGORITHM=*
ACCESS_TOKEN_EXPIRE_MINUTES=*

REDIS_HOST=*
REDIS_PORT=*
```

## TO-DO-LIST
- [x] API com CRUD de usuarios e tarefas
- [x] Banco de dados relacional (Postgres)
- [x] JWT usuarios
- [x] JWT com cookies
- [x] Front-end ligado a API
- [x] Validação de dados no Front-end
- [x] Tarefas utilizando o cache do redis
- [ ] Deploy na nuvem (Infelizmente não consegui pegar nenhuma)
- [ ] Deslogar usuario quando o token expirar
