import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.macros import MacroRequest, MacroResponse
from app.logic.calculator import calcular_macros
from app.database import engine, get_db, Base
from app.models.macro_history import MacroHistory

from rich.console import Console
from rich.table import Table

# Instância do Console Rich para logs de alta performance no terminal
console = Console()

# Inicializa o banco de dados (Cria as tabelas no PostgreSQL se não existirem)
Base.metadata.create_all(bind=engine)

description_md = """
# Modern Dark SaaS API 🚀
Bem-vindo à **Fitness API** do meu portfólio!

Esta aplicação demonstra proficiência em **Python & Backend**:
* **Linguagem:** Python (FastAPI)
* **Design Pattern:** Injeção de Dependências & Validação via Pydantic
* **Banco de Dados:** PostgreSQL via SQLAlchemy ORM
* **Deploy:** Infraestrutura Escalável em Nuvem
"""

app = FastAPI(
    title="Fitness API - Guilherme Rondon",
    description=description_md,
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
)

# --- CONFIGURAÇÃO DE SEGURANÇA E CONECTIVIDADE (CORS) ---
# Sincronizado com a variável 'URL_FRONTEND' do painel Railway
frontend_url = os.getenv("URL_FRONTEND", "http://localhost:4200").strip("/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        frontend_url,
        f"{frontend_url}/",  # Garante compatibilidade com barras extras
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """
    Log de inicialização para monitoramento de saúde do container.
    """
    console.print(
        "\n[bold blue]🚀 API Iniciada: Fitness API - Guilherme Rondon[/bold blue]"
    )
    console.print(
        f"[bold cyan]✓[/bold cyan] [cyan]CORS configurado para:[/cyan] {frontend_url}"
    )
    console.print(
        "[bold yellow]✓[/bold yellow] [yellow]Conexão com PostgreSQL estabelecida[/yellow]\n"
    )


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Fitness API with PostgreSQL is running!",
        "environment": "Production",
    }


@app.post("/macros", response_model=MacroResponse)
def calculate_macros(request: MacroRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal: Processa dados físicos e persiste o histórico no banco.
    """
    # 1. Camada de Regra de Negócio: Cálculo de macros isolado
    resultado = calcular_macros(
        peso=request.peso,
        altura=request.altura,
        idade=request.idade,
        objetivo=request.objetivo,
    )

    # 2. Persistência: Mapeamento para o Modelo ORM
    history_record = MacroHistory(
        peso=request.peso,
        altura=request.altura,
        idade=request.idade,
        objetivo=request.objetivo,
        proteina=resultado["proteinas"],
        carbo=resultado["carboidratos"],
        gordura=resultado["gorduras"],
        calorias_totais=resultado["calorias_totais"],
    )

    # 3. Transação Atômica no PostgreSQL
    db.add(history_record)
    db.commit()

    # Logs Visuais (Rich) para facilitar o Debugging na nuvem
    table = Table(
        title="[bold blue]Novo Cálculo Realizado[/bold blue]", show_header=True
    )
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="yellow")

    table.add_row("Peso Informado", f"{request.peso} kg")
    table.add_row("Calorias Totais", f"{resultado['calorias_totais']} kcal")
    table.add_row("Proteínas", f"{resultado['proteinas']} g")

    console.print(table)

    return MacroResponse(**resultado)
