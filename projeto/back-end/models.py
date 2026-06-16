from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(
        db.Enum("comprador", "vendedor"),
        nullable=False,
        default="comprador"
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vendedor_perfil = db.relationship('Vendedor', backref='usuario', uselist=False, lazy=True, cascade="all, delete-orphan")
    pedidos_como_comprador = db.relationship('Pedido', foreign_keys='Pedido.id_comprador', backref='comprador', lazy=True)
    pedidos_como_vendedor = db.relationship('Pedido', foreign_keys='Pedido.id_vendedor', backref='vendedor', lazy=True)
    mensagens_enviadas = db.relationship('Mensagem', foreign_keys='Mensagem.remetente', backref='remetente_usuario', lazy=True)
    mensagens_recebidas = db.relationship('Mensagem', foreign_keys='Mensagem.destinatario', backref='destinatario_usuario', lazy=True)
    avaliacoes_como_comprador = db.relationship('Avaliacao', foreign_keys='Avaliacao.id_comprador', backref='comprador_avaliacao', lazy=True)
    avaliacoes_como_vendedor = db.relationship('Avaliacao', foreign_keys='Avaliacao.id_vendedor', backref='vendedor_avaliacao', lazy=True)

    def get_id(self):
        return str(self.id_usuario)

    def set_senha(self, senha_plana):
        self.senha = generate_password_hash(senha_plana)

    def checar_senha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)

    def is_admin(self):
        return False

    def is_vendedor(self):
        return self.tipo_usuario == "vendedor"

    def __repr__(self):
        return f"<Usuario {self.email} ({self.tipo_usuario})>"


class Vendedor(db.Model):
    __tablename__ = "vendedores"
    id_vendedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    especialidade = db.Column(db.String(100), nullable=True)
    nota_media = db.Column(db.Numeric(3, 2), nullable=True, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vendedor {self.id_vendedor} - Especialidade: {self.especialidade}>"


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comprador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    jogo = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    rank_atual = db.Column(db.String(50), nullable=True)
    rank_desejado = db.Column(db.String(50), nullable=True)
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(
        db.Enum('Pendente', 'Aceito', 'Em andamento', 'Concluido', 'Cancelado'),
        nullable=True,
        default='Pendente'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mensagens = db.relationship('Mensagem', backref='pedido', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido {self.id_pedido} - {self.status}>"


class Mensagem(db.Model):
    __tablename__ = "mensagens"
    id_mensagem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    remetente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    destinatario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Mensagem {self.id_mensagem}>"


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    id_avaliacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comprador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Avaliacao {self.id_avaliacao} - Nota: {self.nota}>"
