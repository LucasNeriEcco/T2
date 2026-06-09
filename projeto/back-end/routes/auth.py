"""
routes/auth.py – Blueprint de autenticação.
Gerencia cadastro, login e logout de usuários.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario
from forms import FormCadastro, FormLogin

# Cria o blueprint de autenticação
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Página e lógica de cadastro de novo usuário."""
    # Redireciona se já estiver logado
    if current_user.is_authenticated:
        return redirect(url_for("services.listar_servicos"))

    form = FormCadastro()

    if form.validate_on_submit():
        # Verifica se e-mail já está em uso
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash("E-mail já cadastrado. Tente outro.", "danger")
            return render_template("cadastro.html", form=form)

        # Cria o novo usuário com senha hasheada
        novo_usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            tipo_usuario="cliente"
        )
        novo_usuario.set_senha(form.senha.data)

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Página e lógica de autenticação."""
    if current_user.is_authenticated:
        return redirect(url_for("services.listar_servicos"))

    form = FormLogin()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        # Verifica credenciais
        if usuario and usuario.checar_senha(form.senha.data):
            login_user(usuario)
            flash(f"Bem-vindo, {usuario.nome}!", "success")

            # Redireciona para a página que o usuário tentou acessar, se houver
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)

            # Redireciona admin para o dashboard
            if usuario.is_admin():
                return redirect(url_for("users.dashboard"))

            return redirect(url_for("services.listar_servicos"))

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Encerra a sessão do usuário."""
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
