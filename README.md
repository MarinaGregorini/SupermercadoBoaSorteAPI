[![Python CI](https://github.com/MarinaGregorini/SupermercadoBoaSorteAPI/actions/workflows/testes-commit.yml/badge.svg?branch=teste&event=push)](https://github.com/MarinaGregorini/SupermercadoBoaSorteAPI/actions/workflows/testes-commit.yml)

# Supermercado API

Este projeto é uma API desenvolvida com **Flask** que simula um sistema de supermercado. A aplicação oferece endpoints REST, interface web com HTML e CSS, e está integrada a um sistema de CI/CD no **Azure DevOps** e no **GitHub Actions**. Conta ainda com testes funcionais e de performance.

## Pipelines CI/CD

Este projeto utiliza **duas abordagens de integração contínua**:

### GitHub Actions (CI/CD)

- **Localização:** `.github/workflows/`

#### Workflows definidos

1. **testes.yml**
   - **Gatilho:** `push` na branch `teste`.
   - **Etapas:**
     - Instalação de dependências.
     - Lint com `flake8`.
     - Testes funcionais com `python tests/teste_api.py`.

2. **build-and-loadtest.yml**
   - **Gatilho:** Pull Requests da branch `teste` para `main`.
   - **Etapas:**
     - Build da imagem Docker.
     - Verificação da aplicação via container (`curl`).
     - Teste de carga com `Locust`.

---

### Azure Pipelines

- **Localização:** `.azure/`

#### pipeline-commit.yml

- **Gatilho:** Commits na branch `teste`.

##### Etapas:

1. **LintTest**  
   - Verifica a formatação com `flake8`.

2. **TestAPI**  
   - Inicia o Flask localmente.
   - Executa `tests/teste_api.py`.

#### pipeline-pr.yml

- **Gatilho:** Pull Requests da branch `teste` para `main`.

##### Etapas:

1. **BuildAndRun**  
   - Constrói a imagem Docker.  
   - Executa container e valida com `curl`.

2. **Locust**  
   - Testes de performance com múltiplos utilizadores.

---

## Requisitos

- **Python 3.8+**  
- **Docker**  
- **Azure DevOps** (com agente configurado)

---

## Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/MarinaGregorini/SupermercadoBoaSorteAPI.git
cd SupermercadoBoaSorteAPI
```

### 2. Criar um Ambiente Virtual e Instalar Dependências

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Executar a Aplicação

```bash
python app.py
```

### 4. Aceder à Web App

Depois de iniciar a aplicação, abra o navegador e aceda a:

```bash
http://127.0.0.1:5000/
```

---

## Funcionalidades da Aplicação

- Identificação do utilizador  
- Escolha de produtos com sugestões ambientalmente sustentáveis  
- Cálculo do impacto ambiental dos produtos  
- Resumo dos produtos seleccionados  

---

## Tecnologias Utilizadas

- **Python (Flask)**  
- **HTML, CSS (Bootstrap)**  
- **SQLite**

---

## Estrutura de Diretórios

```plaintext
.
├── .azure/
│   ├── pipeline-commit.yml
│   └── pipeline-pr.yml
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

---

## Equipa

- **Bruna Dutra**  
- **Marina Gregorini**  
- **Marta Martins**  
- **Tiago Silva**
