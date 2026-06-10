from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, Usuario
from routes.auth import auth_bp
from routes.services import services_bp
from routes.users import users_bp
from routes.contratacoes import contratacoes_bp
from routes.db_admin import db_admin_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"        
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    app.register_blueprint(auth_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(contratacoes_bp)
    app.register_blueprint(db_admin_bp)
    from flask_login import current_user
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for("users.dashboard"))
            return redirect(url_for("contratacoes.minhas_contratacoes"))
        return redirect(url_for("services.listar_servicos"))
    with app.app_context():
        db.create_all()
        _criar_admin_padrao()
    return app
def _criar_admin_padrao():
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
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
