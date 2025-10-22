from projectarkad import db
from datetime import date

class Despesa(db.Model):
    __tablename__ = "despesas"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<Despesa {self.descricao} - R$ {self.valor:.2f}>"
