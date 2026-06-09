"""
routes/services.py – Blueprint de serviços de boosting.
Gerencia o CRUD completo de serviços (admin) e a listagem pública.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Servico
from forms import FormServico
from functools import wraps

services_bp = Blueprint("services", __name__)


def admin_required(f):
    """Decorador que restringe o acesso apenas a administradores."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


# ─────────────────────────────────────────────
# Rota pública – listagem de serviços
# ─────────────────────────────────────────────

@services_bp.route("/servicos")
def listar_servicos():
    """Exibe todos os serviços disponíveis para qualquer visitante."""
    servicos = Servico.query.all()
    return render_template("servicos.html", servicos=servicos)


# ─────────────────────────────────────────────
# Rotas de CRUD – apenas administradores
# ─────────────────────────────────────────────

@services_bp.route("/admin/servicos")
@login_required
@admin_required
def admin_servicos():
    """Lista todos os serviços no painel do administrador."""
    servicos = Servico.query.all()
    return render_template("admin_servicos.html", servicos=servicos)


@services_bp.route("/admin/servicos/novo", methods=["GET", "POST"])
@login_required
@admin_required
def novo_servico():
    """Cadastra um novo serviço de boosting."""
    form = FormServico()

    if form.validate_on_submit():
        servico = Servico(
            jogo=form.jogo.data,
            tipo_servico=form.tipo_servico.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            prazo_estimado=form.prazo_estimado.data
        )
        db.session.add(servico)
        db.session.commit()
        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for("services.admin_servicos"))

    return render_template("form_servico.html", form=form, titulo="Novo Serviço")


@services_bp.route("/admin/servicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_servico(id):
    """Edita um serviço existente."""
    servico = Servico.query.get_or_404(id)
    form = FormServico(obj=servico)

    if form.validate_on_submit():
        servico.jogo = form.jogo.data
        servico.tipo_servico = form.tipo_servico.data
        servico.descricao = form.descricao.data
        servico.preco = form.preco.data
        servico.prazo_estimado = form.prazo_estimado.data
        db.session.commit()
        flash("Serviço atualizado com sucesso!", "success")
        return redirect(url_for("services.admin_servicos"))

    return render_template("form_servico.html", form=form, titulo="Editar Serviço", servico=servico)


@services_bp.route("/admin/servicos/excluir/<int:id>", methods=["POST"])
@login_required
@admin_required
def excluir_servico(id):
    """Exclui um serviço pelo ID."""
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    flash("Serviço excluído com sucesso.", "warning")
    return redirect(url_for("services.admin_servicos"))
