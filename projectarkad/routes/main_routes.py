from flask import Blueprint, render_template
from projectarkad.models.renda_model import Renda
from projectarkad.services.calculos_service import calcular_702010

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    rendas = Renda.query.all()
    total = sum([r.valor for r in rendas])
    calc = calcular_702010(total) if total > 0 else None
    return render_template("main/index.html", total=total, calc=calc, rendas=rendas)
