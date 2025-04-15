# Supermercado API 🛒

Este projeto é uma API desenvolvida com **Flask** que simula um sistema de supermercado. A aplicação oferece endpoints REST, interface web com HTML e CSS, e está integrada a uma pipeline de CI/CD no **Azure DevOps**. Conta ainda com testes funcionais e de performance.

## 🚀 Pipeline CI/CD - Azure DevOps

Este projeto utiliza **Azure Pipelines** para executar uma série de validações automatizadas a cada push na branch `main`.

### 🔥 Gatilho

A pipeline é acionada automaticamente com cada commit na branch `main`.

### 🛠️ Etapas do Pipeline

1. **LintTest**  
   - Instala as dependências.  
   - Executa o `flake8` para verificar o estilo de código nos principais arquivos `.py`.

2. **TestAPI**  
   - Sobe o servidor Flask localmente.  
   - Executa `tests/teste_api.py` para validar os endpoints de criação e listagem de consumidores.

3. **BuildAndRun**  
   - Constrói a imagem Docker da aplicação (`supermercado-api:latest`).  
   - Sobe um container para garantir que a aplicação responde na porta 8080.  
   - Verifica a saúde da aplicação via `curl`.

4. **Locust**  
   - Executa testes de performance simulando múltiplos usuários acessando a API.  
   - Usa o arquivo `tests/locustfile.py` para simular requisições GET e POST para `/api/consumidores/`.

## 📋 Requisitos

- **Python 3.8+**
- **Docker**
- **Azure DevOps** (com agente configurado)

## 🗂️ Estrutura de Diretórios

.
├── azure-pipelines.yml      # Arquivo de configuração da pipeline do Azure DevOps
├── Dockerfile               # Arquivo para criação da imagem Docker
├── README.md                # Este arquivo
├── app.py                   # Arquivo principal da aplicação Flask
├── db/
│   └── db_supermercado.db   # Banco de dados SQLite
├── models.py                # Definição dos modelos de dados
├── populate_db.py           # Script para popular o banco de dados
├── requirements.txt         # Dependências do projeto
├── scriptVM.sh              # Script para inicialização de máquina virtual
├── static/
│   └── styles.css           # Arquivo de estilos CSS
├── templates/
│   ├── base.html            # Template base da aplicação
│   ├── cadastro.html        # Template de cadastro de consumidores
│   ├── escolher_produtos.html # Template para escolha de produtos
│   └── resumo_compra.html   # Template de resumo da compra
├── tests/
│   ├── locustfile.py        # Arquivo de testes de performance com Locust
│   └── teste_api.py         # Testes dos endpoints da API


## 👥 Equipa

- **Bruna Dutra** 
- **Marina Gregorini** 
- **Marta Martins** 
- **Tiago Silva**

