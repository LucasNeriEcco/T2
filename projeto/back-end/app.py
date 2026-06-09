"""
app.py – Ponto de entrada da aplicação Flask.
Inicializa extensões, registra blueprints e configura o Flask-Login.
"""

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, Usuario

# ─────────────────────────────────────────────
# Importa os blueprints
# ─────────────────────────────────────────────
from routes.auth import auth_bp
from routes.services import services_bp
from routes.users import users_bp


def create_app():
    """Factory function que cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o SQLAlchemy com a aplicação
    db.init_app(app)

    # ─────────────────────────────────────────────
    # Configura o Flask-Login
    # ─────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"          # redireciona para login quando não autenticado
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        """Carrega o usuário a partir do ID armazenado na sessão."""
        return Usuario.query.get(int(user_id))

    # ─────────────────────────────────────────────
    # Registra os blueprints com prefixos de URL
    # ─────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(users_bp)

    # Rota raiz redireciona para a listagem de serviços
    @app.route("/")
    def index():
        return redirect(url_for("services.listar_servicos"))

    # ─────────────────────────────────────────────
    # Cria as tabelas no banco se não existirem
    # ─────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _criar_admin_padrao()

    return app


def _criar_admin_padrao():
    """
    Cria um usuário administrador padrão caso não exista nenhum.
    Credenciais: admin@boosting.com / admin123
    IMPORTANTE: Altere a senha após o primeiro acesso!
    """
    if not Usuario.query.filter_by(tipo_usuario="administrador").first():
        admin = Usuario(
            nome="Administrador",
            email="admin@boosting.com",
            tipo_usuario="administrador"
        )
        admin.set_senha("admin123")
        db.session.add(admin)
        db.session.commit()
        print("[INFO] Admin padrão criado: admin@boosting.com / admin123")


# Executa diretamente
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
