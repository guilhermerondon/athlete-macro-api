from app.logic.calculator import calcular_macros

def test_calcular_macros_perda():
    # Arrange
    peso, altura, idade, objetivo = 80.0, 180.0, 30, 'perda'
    
    # Act
    resultado = calcular_macros(peso, altura, idade, objetivo)
    
    # Assert
    assert "proteinas" in resultado
    assert "calorias_totais" in resultado
    # TMB = (10*80) + (6.25*180) - (5*30) + 5 = 800 + 1125 - 150 + 5 = 1780
    # Gasto = 1780 * 1.55 = 2759
    # Perda = 2759 - 500 = 2259
    assert resultado["calorias_totais"] == 2259.0

def test_calcular_macros_ganho():
    # Arrange
    peso, altura, idade, objetivo = 80.0, 180.0, 30, 'ganho'
    
    # Act
    resultado = calcular_macros(peso, altura, idade, objetivo)
    
    # Assert
    # Ganho = 2759 + 500 = 3259
    assert resultado["calorias_totais"] == 3259.0

def test_calcular_macros_manutencao():
    # Arrange
    peso, altura, idade, objetivo = 80.0, 180.0, 30, 'manutencao'
    
    # Act
    resultado = calcular_macros(peso, altura, idade, objetivo)
    
    # Assert
    # Manutencao = 2759
    assert resultado["calorias_totais"] == 2759.0
