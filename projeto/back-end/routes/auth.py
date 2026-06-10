from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario
from forms import FormCadastro, FormLogin
auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for("users.dashboard"))
        elif current_user.tipo_usuario == "booster":
            return redirect(url_for("services.gerenciar_servicos"))
        return redirect(url_for("contratacoes.minhas_contratacoes"))
    form = FormCadastro()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash("E-mail já cadastrado. Tente outro.", "danger")
            return render_template("cadastro.html", form=form)
        tipo_user = form.tipo_usuario.data
        novo_usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            tipo_usuario=tipo_user,
            status_booster="pendente" if tipo_user == "booster" else None,
            nickname=form.nickname.data if tipo_user == "booster" else None,
            jogos_atuacao=form.jogos_atuacao.data if tipo_user == "booster" else None,
            descricao_profissional=form.descricao_profissional.data if tipo_user == "booster" else None,
            discord=form.discord.data if tipo_user == "booster" else None
        )
        novo_usuario.set_senha(form.senha.data)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))
    return render_template("cadastro.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for("users.dashboard"))
        elif current_user.tipo_usuario == "booster":
            return redirect(url_for("services.gerenciar_servicos"))
        return redirect(url_for("contratacoes.minhas_contratacoes"))
    
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.checar_senha(form.senha.data):
            login_user(usuario)
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
                
            if usuario.is_admin():
                return redirect(url_for("users.dashboard"))
            elif usuario.tipo_usuario == "booster":
                return redirect(url_for("services.gerenciar_servicos"))
            return redirect(url_for("contratacoes.minhas_contratacoes"))
        
        flash("E-mail ou senha incorretos.", "danger")
    return render_template("login.html", form=form)
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
