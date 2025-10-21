from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from projectarkad import db
from projectarkad.models.renda_model import Renda
from datetime import datetime, date

# Cria o blueprint (controlador do módulo de rendas)
renda_bp = Blueprint("renda", __name__, url_prefix="/renda")


# ==========================================================
# ROTAS DE CRUD DE RENDA
# ==========================================================

@renda_bp.route("/nova", methods=["GET", "POST"])
def nova_renda():
    """
    Cadastra uma nova renda no sistema.
    """
    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        tipo = request.form.get("tipo", "").strip()
        valor = request.form.get("valor", 0)
        data_input = request.form.get("data")

        try:
            valor = float(valor)
        except ValueError:
            flash("Valor inválido. Digite um número.", "danger")
            return redirect(url_for("renda.nova_renda"))

        # Converte a string da data para objeto date
        data_obj = (
            datetime.strptime(data_input, "%Y-%m-%d").date()
            if data_input else date.today()
        )

        nova = Renda(descricao=descricao, tipo=tipo, valor=valor, data=data_obj)
        db.session.add(nova)
        db.session.commit()

        flash("Renda adicionada com sucesso!", "success")
        return redirect(url_for("renda.listar_rendas"))

    return render_template("renda/form.html")


@renda_bp.route("/listar", methods=["GET"])
def listar_rendas():
    """
    Lista as rendas cadastradas com filtros opcionais:
    - Por intervalo de datas
    - Por tipo de renda
    """
    tipos = ["Salário", "Presente", "Prêmio", "Extra", "Renda Passiva"]

    # Captura filtros (GET)
    tipo_filtro = request.args.get("tipo")
    data_inicio = request.args.get("inicio")
    data_fim = request.args.get("fim")

    # Query base
    query = Renda.query

    # Filtro por tipo
    if tipo_filtro and tipo_filtro != "Todos":
        query = query.filter(Renda.tipo == tipo_filtro)

    # Filtro por data
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            query = query.filter(Renda.data >= data_inicio_obj)
        except ValueError:
            flash("Data inicial inválida.", "warning")

    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
            query = query.filter(Renda.data <= data_fim_obj)
        except ValueError:
            flash("Data final inválida.", "warning")

    # Executa a query
    rendas = query.order_by(Renda.data.desc()).all()

    # Totais
    total_geral = sum([r.valor for r in rendas])
    total_hoje = sum([r.valor for r in rendas if r.data == date.today()])

    return render_template(
        "renda/list.html",
        rendas=rendas,
        total_geral=total_geral,
        total_hoje=total_hoje,
        tipos=tipos,
        tipo_filtro=tipo_filtro,
        data_inicio=data_inicio or "",
        data_fim=data_fim or ""
    )


@renda_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_renda(id: int):
    """
    Edita uma renda existente.
    """
    renda = Renda.query.get_or_404(id)

    if request.method == "POST":
        renda.descricao = request.form.get("descricao", "").strip()
        renda.tipo = request.form.get("tipo", "").strip()
        valor = request.form.get("valor", 0)
        data_input = request.form.get("data")

        try:
            renda.valor = float(valor)
        except ValueError:
            flash("Valor inválido.", "danger")
            return redirect(url_for("renda.editar_renda", id=id))

        if data_input:
            try:
                renda.data = datetime.strptime(data_input, "%Y-%m-%d").date()
            except ValueError:
                flash("Data inválida.", "danger")

        db.session.commit()
        flash("Renda atualizada com sucesso!", "info")
        return redirect(url_for("renda.listar_rendas"))

    return render_template("renda/form.html", renda=renda)


@renda_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_renda(id: int):
    """
    Exclui uma renda.
    """
    renda = Renda.query.get_or_404(id)
    db.session.delete(renda)
    db.session.commit()
    flash("Renda excluída com sucesso!", "danger")
    return redirect(url_for("renda.listar_rendas"))
