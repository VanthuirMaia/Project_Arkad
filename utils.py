def calcular_702010(valor):
    """Divide a renda conforme o método 70-20-10."""
    return {
        "reserva": round(valor * 0.10, 2),
        "dividas": round(valor * 0.20, 2),
        "despesas": round(valor * 0.70, 2)
    }
