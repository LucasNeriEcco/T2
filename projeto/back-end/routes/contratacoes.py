from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Pedido, Avaliacao, Mensagem
from forms import FormMensagem, FormAvaliacao

contratacoes_bp = Blueprint("contratacoes", __name__)

@contratacoes_bp.route("/meus-pedidos")
@login_required
def meus_pedidos():
    if current_user.tipo_usuario != "comprador":
        return redirect(url_for("services.meus_pedidos_vendedor"))

    pedidos = Pedido.query.filter_by(id_comprador=current_user.id_usuario).order_by(Pedido.id_pedido.desc()).all()
    return render_template("minhas_contratacoes.html", pedidos=pedidos)

@contratacoes_bp.route("/pedido/<int:id>/mensagens", methods=["GET", "POST"])
@login_required
def mensagens_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    vendedor_perfil = current_user.vendedor_perfil
    is_vendedor_do_pedido = vendedor_perfil and pedido.id_vendedor == vendedor_perfil.id_vendedor
    if pedido.id_comprador != current_user.id_usuario and not is_vendedor_do_pedido:
        flash("Acesso negado.", "danger")
        return redirect(url_for("contratacoes.meus_pedidos"))

    form = FormMensagem()
    if form.validate_on_submit():
        if pedido.id_comprador == current_user.id_usuario:
            dest = pedido.vendedor.id_usuario
        else:
            dest = pedido.id_comprador

        msg = Mensagem(
            id_pedido=pedido.id_pedido,
            remetente=current_user.id_usuario,
            destinatario=dest,
            mensagem=form.mensagem.data
        )
        db.session.add(msg)
        db.session.commit()
        flash("Mensagem enviada!", "success")
        return redirect(url_for("contratacoes.mensagens_pedido", id=id))

    mensagens = Mensagem.query.filter_by(id_pedido=pedido.id_pedido).order_by(Mensagem.data_envio.asc()).all()
    return render_template("mensagens.html", pedido=pedido, mensagens=mensagens, form=form)

@contratacoes_bp.route("/pedido/<int:id>/avaliar", methods=["GET", "POST"])
@login_required
def avaliar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    if pedido.id_comprador != current_user.id_usuario:
        flash("Apenas o comprador pode avaliar.", "danger")
        return redirect(url_for("contratacoes.meus_pedidos"))
    if pedido.status != "Concluido":
        flash("Só é possível avaliar pedidos concluídos.", "warning")
        return redirect(url_for("contratacoes.meus_pedidos"))

    ja_avaliou = Avaliacao.query.filter_by(id_comprador=current_user.id_usuario, id_vendedor=pedido.id_vendedor).first()
    if ja_avaliou:
        flash("Você já avaliou este vendedor.", "info")
        return redirect(url_for("contratacoes.meus_pedidos"))

    form = FormAvaliacao()
    if form.validate_on_submit():
        avaliacao = Avaliacao(
            id_comprador=current_user.id_usuario,
            id_vendedor=pedido.id_vendedor,
            nota=form.nota.data,
            comentario=form.comentario.data
        )
        db.session.add(avaliacao)
        db.session.commit()
        flash("Avaliação enviada com sucesso!", "success")
        return redirect(url_for("contratacoes.meus_pedidos"))

    return render_template("avaliar.html", pedido=pedido, form=form)
