<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=8b5cf6&height=110&section=header&animation=fadeIn"/>

# Athlete Macro Analytics (Python)

Microsserviço assíncrono de alta performance especializado no processamento matemático, análise e distribuição de macronutrientes com base em variáveis biométricas e objetivos metabólicos. O sistema opera como uma engine pura de computação de dados (*headless engine*), perfeitamente integrada ao ecossistema distribuído por meio de uma arquitetura baseada em rotas otimizadas e segurança estrita.

---

## 🚀 Tecnologias e Arquitetura

* **Python & FastAPI**: Framework assíncrono moderno e de altíssima velocidade baseado em ASGI (Uvicorn), ideal para garantir concorrência eficiente e processamento de requisições em milissegundos.
* **Pydantic**: Validação estrita de esquemas de dados e tipagem em tempo de execução. Garante que os payloads recebidos do cliente Angular estejam perfeitamente formatados antes de disparar os algoritmos de cálculo.
* **SQLAlchemy & PostgreSQL**: Camada de persistência robusta utilizando mapeamento objeto-relacional (ORM) assíncrono para o armazenamento e auditoria do histórico de simulações nutricionais.
* **Rich Console**: Engine avançada de logging estruturado no terminal para monitoramento de rotas, formatação de payloads em tempo de execução e otimização da Experiência do Desenvolvedor (DX).

---

## ⚙️ Arquitetura do Engine (Cálculo e Processamento)

Diferente de monolitos tradicionais, esta API foi estruturada de forma modular para atuar estritamente como um processador matemático isolado. O fluxo de dados consiste em:
1. Recebimento do payload JSON contendo as chaves biométricas (Peso, Altura, Idade e Objetivo).
2. Sanitização automática dos dados de entrada através dos modelos do Pydantic.
3. Execução dos algoritmos de cálculo de taxa metabólica basal e divisão de macros.
4. Retorno do mapa de dados formatado diretamente para a interface pública do ecossistema.

---

## 🛠️ Execução Local

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Ambiente virtual ativo (`venv`).

### Instalação e Inicialização
```bash
# Instalar todas as dependências do projeto
pip install -r requirements.txt

# Inicializar o servidor ASGI Uvicorn com hot-reload ativo
uvicorn app.main:app --reload
