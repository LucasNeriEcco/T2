from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Servico
from forms import FormServico
from functools import wraps

services_bp = Blueprint("services", __name__)

def booster_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.is_admin():
            return f(*args, **kwargs)
        if current_user.tipo_usuario == "booster":
            if current_user.status_booster != "aprovado":
                flash("Sua conta de Booster ainda está pendente de aprovação.", "warning")
                return redirect(url_for("services.listar_servicos"))
            return f(*args, **kwargs)
        
        flash("Acesso restrito a Boosters e Administradores.", "danger")
        return redirect(url_for("auth.login"))
    return decorated_function

@services_bp.route("/servicos")
def listar_servicos():
    servicos = Servico.query.filter_by(status="Ativo").all()
    return render_template("servicos.html", servicos=servicos)

@services_bp.route("/painel/servicos")
@login_required
@booster_or_admin_required
def gerenciar_servicos():
    if current_user.is_admin():
        servicos = Servico.query.all()
    else:
        servicos = Servico.query.filter_by(booster_id=current_user.id).all()
    return render_template("admin_servicos.html", servicos=servicos)

@services_bp.route("/painel/servicos/novo", methods=["GET", "POST"])
@login_required
@booster_or_admin_required
def novo_servico():
    form = FormServico()
    if form.validate_on_submit():
        servico = Servico(
            booster_id=current_user.id,
            nome=form.nome.data,
            jogo=form.jogo.data,
            categoria=form.categoria.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            prazo_dias=form.prazo_dias.data,
            max_pedidos_simultaneos=form.max_pedidos_simultaneos.data,
            status=form.status.data
        )
        db.session.add(servico)
        db.session.commit()
        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for("services.gerenciar_servicos"))
    return render_template("form_servico.html", form=form, titulo="Novo Serviço")

@services_bp.route("/painel/servicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@booster_or_admin_required
def editar_servico(id):
    servico = Servico.query.get_or_404(id)
    
    # Restrição de propriedade
    if not current_user.is_admin() and servico.booster_id != current_user.id:
        abort(403)
        
    form = FormServico(obj=servico)
    if form.validate_on_submit():
        servico.nome = form.nome.data
        servico.jogo = form.jogo.data
        servico.categoria = form.categoria.data
        servico.descricao = form.descricao.data
        servico.preco = form.preco.data
        servico.prazo_dias = form.prazo_dias.data
        servico.max_pedidos_simultaneos = form.max_pedidos_simultaneos.data
        servico.status = form.status.data
        db.session.commit()
        flash("Serviço atualizado com sucesso!", "success")
        return redirect(url_for("services.gerenciar_servicos"))
    return render_template("form_servico.html", form=form, titulo="Editar Serviço", servico=servico)

@services_bp.route("/painel/servicos/excluir/<int:id>", methods=["POST"])
@login_required
@booster_or_admin_required
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    
    if not current_user.is_admin() and servico.booster_id != current_user.id:
        abort(403)
        
    # Impedir exclusão se houver pedidos ativos
    pedidos_ativos = [c for c in servico.contratacoes if c.status in ('Pendente', 'Em andamento')]
    if pedidos_ativos:
        flash("Não é possível excluir um serviço que possui pedidos em andamento ou pendentes.", "danger")
        return redirect(url_for("services.gerenciar_servicos"))
        
    db.session.delete(servico)
    db.session.commit()
    flash("Serviço excluído com sucesso.", "warning")
    return redirect(url_for("services.gerenciar_servicos"))
