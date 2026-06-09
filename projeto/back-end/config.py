"""
config.py – Configurações da aplicação Flask.
Define as variáveis de ambiente para banco de dados, segurança e sessão.
"""

import os


class Config:
    # Chave secreta usada para assinar sessões e tokens CSRF
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-boosting-2024")

    # URI de conexão com o MySQL via SQLAlchemy
    # Formato: mysql+pymysql://usuario:senha@host/banco
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:senha@localhost/boosting_db"
    )

    # Desabilita o rastreamento de modificações para economizar recursos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de sessão
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
