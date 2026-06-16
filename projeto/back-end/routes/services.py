from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db, Pedido, Vendedor, Usuario
from forms import FormPedido, FormStatusPedido, FormMensagem
from functools import wraps

services_bp = Blueprint("services", __name__)

def vendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.is_vendedor():
            return f(*args, **kwargs)
        flash("Acesso restrito a vendedores.", "danger")
        return redirect(url_for("auth.login"))
    return decorated_function

@services_bp.route("/vendedores")
def listar_vendedores():
    vendedores = Vendedor.query.all()
    return render_template("servicos.html", vendedores=vendedores)

@services_bp.route("/vendedor/<int:id>/contratar", methods=["GET", "POST"])
@login_required
def contratar_vendedor(id):
    if current_user.tipo_usuario != "comprador":
        flash("Apenas compradores podem contratar serviços.", "warning")
        return redirect(url_for("services.listar_vendedores"))

    vendedor_perfil = Vendedor.query.get_or_404(id)
    vendedor_usuario = vendedor_perfil.usuario

    form = FormPedido()
    if form.validate_on_submit():
        pedido = Pedido(
            id_comprador=current_user.id_usuario,
            id_vendedor=vendedor_perfil.id_vendedor,
            jogo=form.jogo.data,
            servico=form.servico.data,
            rank_atual=form.rank_atual.data,
            rank_desejado=form.rank_desejado.data,
            valor=form.valor.data
        )
        db.session.add(pedido)
        db.session.commit()
        flash("Pedido realizado com sucesso! Acompanhe o status no seu painel.", "success")
        return redirect(url_for("contratacoes.meus_pedidos"))

    return render_template("contratar.html", form=form, vendedor=vendedor_perfil, vendedor_usuario=vendedor_usuario)

@services_bp.route("/painel/pedidos-vendedor")
@login_required
@vendedor_required
def meus_pedidos_vendedor():
    vendedor_perfil = current_user.vendedor_perfil
    pedidos = Pedido.query.filter_by(id_vendedor=vendedor_perfil.id_vendedor).order_by(Pedido.id_pedido.desc()).all() if vendedor_perfil else []
    forms = {p.id_pedido: FormStatusPedido(status=p.status) for p in pedidos}
    return render_template("admin_pedidos.html", pedidos=pedidos, forms=forms)

@services_bp.route("/painel/pedidos-vendedor/<int:id>/status", methods=["POST"])
@login_required
@vendedor_required
def atualizar_status_vendedor(id):
    pedido = Pedido.query.get_or_404(id)
    vendedor_perfil = current_user.vendedor_perfil
    if not vendedor_perfil or pedido.id_vendedor != vendedor_perfil.id_vendedor:
        abort(403)

    form = FormStatusPedido()
    if form.validate_on_submit():
        pedido.status = form.status.data
        db.session.commit()
        flash("Status atualizado com sucesso!", "success")
    else:
        flash("Erro ao atualizar status.", "danger")
    return redirect(url_for("services.meus_pedidos_vendedor"))
