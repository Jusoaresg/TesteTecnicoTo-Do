from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import task_routes, user_routes
from cache import redis
from dotenv import dotenv_values
from cache import redis

origins = [
    "127.0.0.1:5000",
    "http://localhost:5000",
    "localhost:5000"
]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Pode ser alterado para um domínio específico
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

app.include_router(redis.router, prefix="/cache", tags=["Redis"])
app.include_router(task_routes.router, prefix="/task", tags=["Task"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
