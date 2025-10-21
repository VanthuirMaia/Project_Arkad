import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Renda
from utils import calcular_702010
from datetime import date

# --- Caminho absoluto para o banco ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "arkad.db")

# --- Garante que a pasta 'database' exista ---
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)

# --- Flask app ---
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    rendas = Renda.query.all()
    total = sum([r.valor for r in rendas])
    calc = calcular_702010(total) if total > 0 else None
    return render_template("index.html", total=total, calc=calc, rendas=rendas)

@app.route("/add_renda", methods=["GET", "POST"])
def add_renda():
    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        nova = Renda(descricao=descricao, valor=valor, data=date.today())
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_renda.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print(f"✅ Banco criado em: {DB_PATH}")
    app.run(debug=True)
