from flask import Blueprint, render_template, request, redirect, url_for, flash
from projectarkad import db
from projectarkad.models.despesa_model import Despesa
from datetime import datetime, date
from sqlalchemy import func

# Blueprint
despesa_bp = Blueprint("despesa", __name__, url_prefix="/despesas")


# ==============================
# LISTAR DESPESAS + FILTROS
# ==============================
@despesa_bp.route("/")
def listar_despesas():
    categoria = request.args.get("categoria")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    query = Despesa.query

    # Filtros opcionais
    if categoria and categoria != "Todas":
        query = query.filter(Despesa.categoria == categoria)

    if data_inicio:
        query = query.filter(Despesa.data >= datetime.strptime(data_inicio, "%Y-%m-%d").date())

    if data_fim:
        query = query.filter(Despesa.data <= datetime.strptime(data_fim, "%Y-%m-%d").date())

    despesas = query.order_by(Despesa.data.desc()).all()

    # Totais gerais e filtrados
    total_geral = db.session.query(func.sum(Despesa.valor)).scalar() or 0
    total_hoje = db.session.query(func.sum(Despesa.valor)).filter(Despesa.data == date.today()).scalar() or 0
    total_filtrado = sum([d.valor for d in despesas])

    # Gera lista de categorias distintas
    categorias = [c[0] for c in db.session.query(Despesa.categoria).distinct().order_by(Despesa.categoria).all()]
    categorias.sort()
    categorias.insert(0, "Todas")

    return render_template(
        "despesa/list.html",
        despesas=despesas,
        total_geral=total_geral,
        total_hoje=total_hoje,
        total_filtrado=total_filtrado,
        categorias=categorias,
        categoria_selecionada=categoria,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


# ==============================
# NOVA DESPESA
# ==============================
@despesa_bp.route("/nova", methods=["GET", "POST"])
def nova_despesa():
    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        valor = float(request.form.get("valor", 0))
        categoria = request.form.get("categoria", "").strip()
        data_input = request.form.get("data")

        # Usa a data informada, ou a atual se vazia
        data_obj = datetime.strptime(data_input, "%Y-%m-%d").date() if data_input else date.today()

        despesa = Despesa(descricao=descricao, valor=valor, categoria=categoria, data=data_obj)
        db.session.add(despesa)
        db.session.commit()

        total_hoje = db.session.query(func.sum(Despesa.valor)).filter(Despesa.data == date.today()).scalar() or 0
        flash(f"Despesa de R$ {valor:.2f} adicionada ({categoria}) — total do dia: R$ {total_hoje:.2f}", "success")
        return redirect(url_for("despesa.listar_despesas"))

    # 🔧 Corrigido: precisamos passar despesa=None e date=date
    return render_template("despesa/form.html", despesa=None, date=date)


# ==============================
# EDITAR DESPESA
# ==============================
@despesa_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_despesa(id):
    despesa = Despesa.query.get_or_404(id)

    if request.method == "POST":
        despesa.descricao = request.form.get("descricao", "").strip()
        despesa.valor = float(request.form.get("valor", 0))
        despesa.categoria = request.form.get("categoria", "").strip()
        data_str = request.form.get("data")

        if data_str:
            despesa.data = datetime.strptime(data_str, "%Y-%m-%d").date()

        db.session.commit()
        flash("Despesa atualizada com sucesso!", "success")
        return redirect(url_for("despesa.listar_despesas"))

    # 🔧 Também enviamos `date` pro form para evitar erro no campo padrão
    return render_template("despesa/form.html", despesa=despesa, date=date)


# ==============================
# EXCLUIR DESPESA
# ==============================
@despesa_bp.route("/excluir/<int:id>")
def excluir_despesa(id):
    despesa = Despesa.query.get_or_404(id)
    db.session.delete(despesa)
    db.session.commit()
    flash("Despesa excluída com sucesso!", "danger")
    return redirect(url_for("despesa.listar_despesas"))
