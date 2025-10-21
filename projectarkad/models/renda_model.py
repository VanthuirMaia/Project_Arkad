from projectarkad import db
from datetime import date

class Renda(db.Model):
    __tablename__ = "renda"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, default=date.today, nullable=False)

    def __repr__(self):
        return f"<Renda {self.descricao} - R${self.valor}>"
