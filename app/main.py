from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.macros import MacroRequest, MacroResponse
from app.logic.calculator import calcular_macros
from app.database import engine, get_db, Base
from app.models.macro_history import MacroHistory

from rich.console import Console
from rich.table import Table

# Instância do Console Rich para logs maravilhosos no terminal
console = Console()

# Inicializa o banco de dados (Cria a tabela se não existir)
Base.metadata.create_all(bind=engine)

description_md = """
# Modern Dark SaaS API 🚀
Bem-vindo à **Fitness API** do meu portfólio!

Esta aplicação demonstra minha proficiência em **Python & Backend**:
* **Linguagem:** Python (FastAPI)
* **Design Pattern:** Injeção de Dependências & Validação via Pydantic
* **Banco de Dados:** PostgreSQL via SQLAlchemy ORM
* **Deploy:** Preparado para Docker & Nuvem

---
### Como funciona?
Envie seus dados físicos no endpoint `/macros` e o sistema aplicará regras de negócio isoladas para sugerir a melhor distribuição de Proteínas, Carboidratos e Gorduras.
"""

app = FastAPI(
    title="Fitness API - Guilherme Rondon",
    description=description_md,
    version="1.0.0",
    # Configuração de tema escuro para os blocos de código do Swagger UI
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"}
)

# Configuração de CORS para permitir o frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """
    Imprime um log bonito no terminal assim que o servidor iniciar.
    """
    console.print("\n[bold blue]🚀 API Iniciada: Fitness API - Guilherme Rondon[/bold blue]")
    console.print("[bold cyan]✓[/bold cyan] [cyan]FastAPI rodando na porta 8000[/cyan]")
    console.print("[bold yellow]✓[/bold yellow] [yellow]Conexão com PostgreSQL estabelecida[/yellow]\n")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Fitness API with PostgreSQL is running!"}

@app.post("/macros", response_model=MacroResponse)
def calculate_macros(request: MacroRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal para cálculo de macros.
    
    - Recebe o payload validado pelo Pydantic.
    - Delega o cálculo para o módulo lógico (`calculator.py`).
    - Salva o registro completo na tabela `macro_history` do PostgreSQL.
    - Registra um log elegante no terminal usando a biblioteca 'rich'.
    """
    # 1. Calcula as macros usando a camada de regra de negócio
    resultado = calcular_macros(
        peso=request.peso,
        altura=request.altura,
        idade=request.idade,
        objetivo=request.objetivo
    )
    
    # 2. Mapeia para o Modelo ORM do banco de dados
    history_record = MacroHistory(
        peso=request.peso,
        altura=request.altura,
        idade=request.idade,
        objetivo=request.objetivo,
        proteina=resultado["proteinas"],
        carbo=resultado["carboidratos"],
        gordura=resultado["gorduras"],
        calorias_totais=resultado["calorias_totais"]
    )
    
    # 3. Salva a transação no banco (Persistência)
    db.add(history_record)
    db.commit()
    
    # Renderização da Tabela de Logs via Rich
    table = Table(title="[bold blue]Novo Cálculo Realizado[/bold blue]", show_header=True, header_style="bold magenta")
    table.add_column("Input / Output", style="cyan")
    table.add_column("Valor", style="yellow")
    
    table.add_row("Peso (kg)", str(request.peso))
    table.add_row("Objetivo", request.objetivo.upper())
    table.add_row("Calorias Calculadas", f"{resultado['calorias_totais']} kcal")
    table.add_row("Proteínas", f"{resultado['proteinas']} g")
    
    console.print(table)
    
    # 4. Retorna a resposta ao usuário baseada no Schema
    return MacroResponse(**resultado)
