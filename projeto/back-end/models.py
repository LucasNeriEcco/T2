from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(
        db.Enum("cliente", "booster", "administrador"),
        nullable=False,
        default="cliente"
    )
    
                                    
    status_booster = db.Column(db.Enum('pendente', 'aprovado'), nullable=True)
    nickname = db.Column(db.String(100), nullable=True)
    jogos_atuacao = db.Column(db.String(255), nullable=True)
    descricao_profissional = db.Column(db.Text, nullable=True)
    discord = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

                     
    servicos = db.relationship('Servico', backref='booster', lazy=True, cascade="all, delete-orphan")
    contratacoes_como_cliente = db.relationship('Contratacao', foreign_keys='Contratacao.cliente_id', backref='cliente', lazy=True)
    contratacoes_como_booster = db.relationship('Contratacao', foreign_keys='Contratacao.booster_id', backref='booster_contratado', lazy=True)

    def set_senha(self, senha_plana):
        self.senha = generate_password_hash(senha_plana)

    def checar_senha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)

    def is_admin(self):
        return self.tipo_usuario == "administrador"
        
    def is_booster_aprovado(self):
        return self.tipo_usuario == "booster" and self.status_booster == "aprovado"

    def __repr__(self):
        return f"<Usuario {self.email} ({self.tipo_usuario})>"


class Servico(db.Model):
    __tablename__ = "servicos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booster_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    jogo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    prazo_dias = db.Column(db.Integer, nullable=False)
    max_pedidos_simultaneos = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Enum('Ativo', 'Inativo'), nullable=False, default='Ativo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

                     
    contratacoes = db.relationship('Contratacao', foreign_keys='Contratacao.servico_id', backref='servico_obj', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Servico {self.nome} - Booster ID {self.booster_id}>"


class Contratacao(db.Model):
    __tablename__ = "contratacoes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    booster_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    
    nick_jogador = db.Column(db.String(100), nullable=False)
    rank_atual = db.Column(db.String(50), nullable=True)
    rank_desejado = db.Column(db.String(50), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    status = db.Column(
        db.Enum('Pendente', 'Em andamento', 'Concluído', 'Cancelado'),
        nullable=False,
        default='Pendente'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Contratacao {self.id} - {self.status}>"
