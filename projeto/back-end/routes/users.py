from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Usuario, Servico
from forms import FormEditarUsuario, FormCadastro
from functools import wraps
users_bp = Blueprint("users", __name__)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
@users_bp.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():
    total_usuarios = Usuario.query.count()
    total_clientes = Usuario.query.filter_by(tipo_usuario="cliente").count()
    total_boosters = Usuario.query.filter_by(tipo_usuario="booster").count()
    boosters_pendentes = Usuario.query.filter_by(tipo_usuario="booster", status_booster="pendente").count()
    total_servicos = Servico.query.count()
    stats = {
        "total_usuarios": total_usuarios,
        "total_clientes": total_clientes,
        "total_boosters": total_boosters,
        "boosters_pendentes": boosters_pendentes,
        "total_servicos": total_servicos,
    }
    ultimos_usuarios = Usuario.query.order_by(Usuario.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", stats=stats, ultimos_usuarios=ultimos_usuarios)

@users_bp.route("/admin/boosters/pendentes")
@login_required
@admin_required
def listar_boosters_pendentes():
    boosters = Usuario.query.filter_by(tipo_usuario="booster", status_booster="pendente").all()
    return render_template("admin_boosters.html", boosters=boosters)

@users_bp.route("/admin/boosters/aprovar/<int:id>", methods=["POST"])
@login_required
@admin_required
def aprovar_booster(id):
    booster = Usuario.query.get_or_404(id)
    if booster.tipo_usuario == "booster":
        booster.status_booster = "aprovado"
        db.session.commit()
        flash(f"Booster {booster.nome} aprovado com sucesso!", "success")
    return redirect(url_for("users.listar_boosters_pendentes"))
@users_bp.route("/admin/usuarios")
@login_required
@admin_required
def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.created_at.desc()).all()
    return render_template("admin_usuarios.html", usuarios=usuarios)
@users_bp.route("/admin/usuarios/novo", methods=["GET", "POST"])
@login_required
@admin_required
def novo_usuario():
    form = FormCadastro()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("E-mail já está em uso.", "danger")
            return render_template("form_usuario.html", form=form, titulo="Novo Usuário")
        usuario = Usuario(nome=form.nome.data, email=form.email.data)
        usuario.set_senha(form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("users.listar_usuarios"))
    return render_template("form_usuario.html", form=form, titulo="Novo Usuário")
@users_bp.route("/admin/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = FormEditarUsuario(obj=usuario)
    if form.validate_on_submit():
        email_existente = Usuario.query.filter_by(email=form.email.data).first()
        if email_existente and email_existente.id != usuario.id:
            flash("E-mail já está em uso por outro usuário.", "danger")
            return render_template("form_usuario.html", form=form, titulo="Editar Usuário", usuario=usuario)
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.tipo_usuario = form.tipo_usuario.data
        if form.nova_senha.data:
            usuario.set_senha(form.nova_senha.data)
        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("users.listar_usuarios"))
    return render_template("form_usuario.html", form=form, titulo="Editar Usuário", usuario=usuario)
@users_bp.route("/admin/usuarios/excluir/<int:id>", methods=["POST"])
@login_required
@admin_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash("Você não pode excluir sua própria conta.", "danger")
        return redirect(url_for("users.listar_usuarios"))
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso.", "warning")
    return redirect(url_for("users.listar_usuarios"))
