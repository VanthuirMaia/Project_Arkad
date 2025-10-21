from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Renda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)
    data = db.Column(db.Date)

class Divida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credor = db.Column(db.String(100))
    valor_total = db.Column(db.Float)
    juros = db.Column(db.Float)
    parcelas = db.Column(db.Integer)
    status = db.Column(db.String(20))  # ativa, quitada, atrasada...

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50))
    valor = db.Column(db.Float)
    data = db.Column(db.Date)
    descricao = db.Column(db.String(150))
