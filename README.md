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

- **Python 3.8+** 🐍
- **Docker** 🐳
- **Azure DevOps** (com agente configurado) ☁️

## 🗂️ Estrutura de Diretórios

```plaintext
.
├── azure-pipelines.yml
├── Dockerfile
├── README.md
├── app.py
├── db/
│   └── db_supermercado.db
├── models.py
├── populate_db.py
├── requirements.txt
├── scriptVM.sh
├── static/
│   └── styles.css
├── templates/
│   ├── base.html
│   ├── cadastro.html
│   ├── escolher_produtos.html
│   └── resumo_compra.html
├── tests/
│   ├── locustfile.py
│   └── teste_api.py
```

## 👥 Equipa

- **Bruna Dutra** 
- **Marina Gregorini** 
- **Marta Martins** 
- **Tiago Silva**

