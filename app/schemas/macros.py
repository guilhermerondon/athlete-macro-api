from pydantic import BaseModel, Field
from typing import Literal

class MacroRequest(BaseModel):
    peso: float = Field(..., gt=0, description="Peso em kg")
    altura: float = Field(..., gt=0, description="Altura em cm")
    idade: int = Field(..., gt=0, description="Idade em anos")
    objetivo: Literal['perda', 'manutencao', 'ganho'] = Field(..., description="Objetivo do usuário")

class MacroResponse(BaseModel):
    proteinas: float = Field(..., description="Proteínas diárias (g)")
    carboidratos: float = Field(..., description="Carboidratos diários (g)")
    gorduras: float = Field(..., description="Gorduras diárias (g)")
    calorias_totais: float = Field(..., description="Calorias diárias totais (kcal)")
    sugestao_suplemento: str | None = Field(None, description="Sugestão de suplementação recomendada")
