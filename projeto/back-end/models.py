"""
models.py – Definição dos modelos do banco de dados com SQLAlchemy.
Contém as classes Usuario e Servico que mapeiam as tabelas do MySQL.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Instância do SQLAlchemy compartilhada entre os módulos
db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    """
    Modelo de Usuário.
    Herda UserMixin para integração com Flask-Login.
    """
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)  # armazenada com hash
    tipo_usuario = db.Column(
        db.Enum("cliente", "administrador"),
        nullable=False,
        default="cliente"
    )
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha_plana):
        """Gera o hash da senha e armazena no campo senha."""
        self.senha = generate_password_hash(senha_plana)

    def checar_senha(self, senha_plana):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha, senha_plana)

    def is_admin(self):
        """Retorna True se o usuário for administrador."""
        return self.tipo_usuario == "administrador"

    def __repr__(self):
        return f"<Usuario {self.email}>"


class Servico(db.Model):
    """
    Modelo de Serviço de Boosting.
    Representa os serviços de rank boosting e account leveling disponíveis.
    """
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jogo = db.Column(db.String(100), nullable=False)
    tipo_servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    prazo_estimado = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Servico {self.jogo} - {self.tipo_servico}>"
