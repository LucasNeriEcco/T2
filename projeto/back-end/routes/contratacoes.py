from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Servico, Contratacao
from forms import FormContratacao, FormStatusPedido
from functools import wraps

contratacoes_bp = Blueprint("contratacoes", __name__)

def booster_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.is_admin() or current_user.tipo_usuario == "booster":
            return f(*args, **kwargs)
        flash("Acesso restrito.", "danger")
        return redirect(url_for("auth.login"))
    return decorated_function

                         

@contratacoes_bp.route("/servico/<int:id>/contratar", methods=["GET", "POST"])
@login_required
def contratar(id):
    if current_user.tipo_usuario != "cliente":
        flash("Apenas clientes podem contratar serviços.", "warning")
        return redirect(url_for("services.listar_servicos"))
        
    servico = Servico.query.get_or_404(id)
    if servico.status != "Ativo":
        flash("Este serviço não está mais ativo.", "danger")
        return redirect(url_for("services.listar_servicos"))

                                         
    pedidos_ativos = Contratacao.query.filter_by(servico_id=servico.id).filter(Contratacao.status.in_(['Pendente', 'Em andamento'])).count()
    if pedidos_ativos >= servico.max_pedidos_simultaneos:
        flash("Este serviço já atingiu o limite de pedidos simultâneos no momento.", "warning")
        return redirect(url_for("services.listar_servicos"))

    form = FormContratacao()
    if form.validate_on_submit():
        contratacao = Contratacao(
            cliente_id=current_user.id,
            booster_id=servico.booster_id,
            servico_id=servico.id,
            nick_jogador=form.nick_jogador.data,
            rank_atual=form.rank_atual.data,
            rank_desejado=form.rank_desejado.data,
            observacoes=form.observacoes.data
        )
        db.session.add(contratacao)
        db.session.commit()
        flash("Contratação realizada com sucesso! Acompanhe o status no seu painel.", "success")
        return redirect(url_for("contratacoes.minhas_contratacoes"))

    return render_template("contratar.html", form=form, servico=servico)


@contratacoes_bp.route("/minhas-contratacoes")
@login_required
def minhas_contratacoes():
    if current_user.tipo_usuario != "cliente":
        if current_user.is_admin():
            return redirect(url_for("users.dashboard"))
        return redirect(url_for("services.gerenciar_servicos"))
        
    contratacoes = Contratacao.query.filter_by(cliente_id=current_user.id).order_by(Contratacao.created_at.desc()).all()
    return render_template("minhas_contratacoes.html", contratacoes=contratacoes)


                                 

@contratacoes_bp.route("/painel/pedidos")
@login_required
@booster_or_admin_required
def gerenciar_pedidos():
    if current_user.is_admin():
        contratacoes = Contratacao.query.order_by(Contratacao.created_at.desc()).all()
    else:
        contratacoes = Contratacao.query.filter_by(booster_id=current_user.id).order_by(Contratacao.created_at.desc()).all()
        
    forms = {c.id: FormStatusPedido(status=c.status) for c in contratacoes}
    return render_template("admin_pedidos.html", contratacoes=contratacoes, forms=forms)


@contratacoes_bp.route("/painel/pedidos/<int:id>/status", methods=["POST"])
@login_required
@booster_or_admin_required
def atualizar_status(id):
    contratacao = Contratacao.query.get_or_404(id)
    
                                                    
    if not current_user.is_admin() and contratacao.booster_id != current_user.id:
        abort(403)
        
    form = FormStatusPedido()
    if form.validate_on_submit():
        contratacao.status = form.status.data
        db.session.commit()
        flash("Status atualizado com sucesso!", "success")
    else:
        flash("Erro ao atualizar status.", "danger")
    return redirect(url_for("contratacoes.gerenciar_pedidos"))
