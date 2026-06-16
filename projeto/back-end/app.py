from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models import db, Usuario
from routes.auth import auth_bp
from routes.services import services_bp
from routes.contratacoes import contratacoes_bp

import pymysql

def create_database_if_not_exists():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="963968"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS loja_boosting")
        conn.close()
    except Exception as e:
        pass

def create_app():
    create_database_if_not_exists()
    app = Flask(
        __name__,
        template_folder="../front-end/templates",
        static_folder="../front-end/static"
    )
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
    app.register_blueprint(contratacoes_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.is_vendedor():
                return redirect(url_for("services.meus_pedidos_vendedor"))
            return redirect(url_for("contratacoes.meus_pedidos"))
        return redirect(url_for("services.listar_vendedores"))

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
