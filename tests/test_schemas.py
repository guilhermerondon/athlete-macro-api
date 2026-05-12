import pytest
from pydantic import ValidationError
from app.schemas.macros import MacroRequest

def test_macro_request_invalid_peso():
    with pytest.raises(ValidationError) as excinfo:
        MacroRequest(peso=-10, altura=180, idade=30, objetivo='perda')
    assert "Input should be greater than 0" in str(excinfo.value)

def test_macro_request_invalid_altura():
    with pytest.raises(ValidationError) as excinfo:
        MacroRequest(peso=80, altura=0, idade=30, objetivo='perda')
    assert "Input should be greater than 0" in str(excinfo.value)

def test_macro_request_invalid_idade():
    with pytest.raises(ValidationError) as excinfo:
        MacroRequest(peso=80, altura=180, idade=-5, objetivo='perda')
    assert "Input should be greater than 0" in str(excinfo.value)

def test_macro_request_valid():
    request = MacroRequest(peso=80, altura=180, idade=30, objetivo='perda')
    assert request.peso == 80.0
    assert request.objetivo == 'perda'
