def calcular_702010(valor):
    """Aplica o método 70/20/10 a uma receita"""
    return {
        "despesas": round(valor * 0.70, 2),
        "dividas": round(valor * 0.20, 2),
        "reserva": round(valor * 0.10, 2)
    }
