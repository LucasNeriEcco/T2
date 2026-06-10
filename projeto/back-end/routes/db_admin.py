from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import text
from models import db
from routes.users import admin_required
import traceback

db_admin_bp = Blueprint("db_admin", __name__)

@db_admin_bp.route("/admin/database", methods=["GET", "POST"])
@login_required
@admin_required
def query_panel():
    query = ""
    columns = []
    results = []
    error = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                result = db.session.execute(text(query))
                if query.lower().startswith("select") or query.lower().startswith("show") or query.lower().startswith("desc"):
                    columns = result.keys()
                    results = result.fetchall()
                else:
                    db.session.commit()
                    flash("Comando executado com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                error = str(e)
                flash("Erro ao executar query.", "danger")
        else:
            flash("A query não pode estar vazia.", "warning")

    return render_template("admin_db.html", query=query, columns=columns, results=results, error=error)
