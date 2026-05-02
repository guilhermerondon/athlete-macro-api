from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class MacroHistory(Base):
    __tablename__ = "macro_history"

    id = Column(Integer, primary_key=True, index=True)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    idade = Column(Integer, nullable=False)
    objetivo = Column(String, nullable=False)
    proteina = Column(Float, nullable=False)
    carbo = Column(Float, nullable=False)
    gordura = Column(Float, nullable=False)
    calorias_totais = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
