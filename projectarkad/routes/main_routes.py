from flask import Blueprint, render_template
from projectarkad.models.renda_model import Renda
from projectarkad.models.despesa_model import Despesa
from projectarkad.services.calculos_service import calcular_702010
from sqlalchemy import func
from projectarkad import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # Totais de receitas e despesas
    total_rendas = db.session.query(func.sum(Renda.valor)).scalar() or 0
    total_despesas = db.session.query(func.sum(Despesa.valor)).scalar() or 0
    saldo = total_rendas - total_despesas

    # Cálculo 70/20/10 apenas se houver rendas
    calc = calcular_702010(total_rendas) if total_rendas > 0 else None

    return render_template(
        "main/index.html",
        total_rendas=total_rendas,
        total_despesas=total_despesas,
        saldo=saldo,
        calc=calc
    )
