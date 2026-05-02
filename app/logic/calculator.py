# Constantes Nutricionais (Suplementos)
SUPLEMENTOS = {
    "Whey Protein": {
        "porcao_g": 30,
        "proteinas_g": 24.0,
        "carboidratos_g": 2.0,
        "gorduras_g": 1.5,
        "descricao": "~24g de Proteína por scoop (30g), com baixo teor de gordura e carboidratos."
    }
}

def calcular_macros(peso: float, altura: float, idade: int, objetivo: str) -> dict:
    """
    Calcula os macronutrientes ideais diários baseando-se na fórmula de Mifflin-St Jeor.
    
    A lógica engloba o cálculo do Metabolismo Basal (TMB), ajuste pelo nível de atividade 
    e o déficit/superávit calórico de acordo com o objetivo selecionado.
    """
    tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
    
    gasto_diario = tmb * 1.55
    
    if objetivo == 'perda':
        calorias_alvo = gasto_diario - 500
    elif objetivo == 'ganho':
        calorias_alvo = gasto_diario + 500
    else:
        calorias_alvo = gasto_diario

    proteina_g = (calorias_alvo * 0.30) / 4
    carbo_g = (calorias_alvo * 0.40) / 4
    gordura_g = (calorias_alvo * 0.30) / 9

    sugestao_suplemento = f"Recomendação: Whey Protein - {SUPLEMENTOS['Whey Protein']['descricao']}"

    return {
        "proteinas": round(proteina_g, 1),
        "carboidratos": round(carbo_g, 1),
        "gorduras": round(gordura_g, 1),
        "calorias_totais": round(calorias_alvo, 1),
        "sugestao_suplemento": sugestao_suplemento
    }
