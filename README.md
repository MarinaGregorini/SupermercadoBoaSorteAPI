# 🛡️ Supermercado Boa Sorte API – Segurança e Monitorização

Projeto de segurança e monitorização contínua de uma aplicação Python Flask, containerizada com Docker e deployada no Azure Kubernetes Service (AKS). Utiliza ferramentas como **Trivy**, **OWASP ZAP**, **Prometheus** e **GitHub Actions** para garantir a segurança e resiliência da aplicação ao longo do ciclo de vida.

---

## 📦 Requisitos

- Python 3.10+
- Docker
- Azure CLI
- Kubectl
- Helm
- Trivy
- jq (para leitura do relatório JSON do ZAP)
- Conta Azure com permissões para ACR/AKS
- GitHub Actions ativado

---

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/MarinaGregorini/SupermercadoBoaSorteAPI.git
cd SupermercadoBoaSorteAPI
```

### 2. Ambiente Virtual e Dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Instalar Azure CLI, Kubectl e Helm

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
sudo snap install kubectl --classic
sudo snap install helm --classic
```

### 4. Autenticar e Conectar ao Cluster AKS

```bash
az login
az aks get-credentials --resource-group RGUPSKILL-SysAdmin --name sysadmin-cluster
az acr credential show -n acrgrupo4
```

### 5. Criar Secret no Kubernetes para o ACR

```bash
kubectl create secret docker-registry acrsecret \
--docker-server=acrgrupo4.azurecr.io \
--docker-username=acrgrupo4 \
--docker-password=<password> -n grupo4
```

---

## ⚙️ Deploy da Aplicação com Helm

### 1. Build e Push da Imagem Docker

```bash
docker build -t acrgrupo4.azurecr.io/py-prom:latest .
docker push acrgrupo4.azurecr.io/py-prom:latest
```

### 2. Instalar o Helm Chart

```bash
helm install supermercado-metrics ./helm/supermercado-metrics -n grupo4
```

### 3. Verificar Recursos no AKS

```bash
kubectl get all -n grupo4
```

---

## 📈 Monitorização com Prometheus

A aplicação expõe métricas usando `prometheus_client`.  
Endpoint de métricas: `http://<EXTERNAL-IP>/metrics`

### 🔍 Métricas Incluídas

- `http_requests_total`
- `http_requests_in_progress`

Exemplo de consulta Prometheus:

```
http_requests_total{endpoint="/", http_status="200|302"}
```

---

## 🔐 Segurança com Trivy

### Análise da Imagem Docker

```bash
trivy image acrgrupo4.azurecr.io/supermercadoboasorteapi:latest
```

### Filtro por Severidade

```bash
trivy image --severity HIGH,CRITICAL acrgrupo4.azurecr.io/supermercadoboasorteapi:latest
```

### Análise do Dockerfile

```bash
trivy config Dockerfile
```

### Análise do Helm Chart

```bash
trivy config helm/
```

### Análise do Sistema de Ficheiros

```bash
trivy fs .
```

---

## 🧪 Testes de Segurança Automatizados (CI/CD)

### 📄 Workflow: Docker Build and Load Test

Arquivo localizado em `.github/workflows/`

#### Etapas do Pipeline:

| Etapa | Descrição |
|-------|-----------|
| `trivy-scan` | Verifica vulnerabilidades no Dockerfile e Helm Chart |
| `build-and-run` | Build da imagem, execução local e verificação de saúde |
| `locust` | Teste de carga com Locust |
| `zap-security-test` | Scan de segurança com OWASP ZAP |

### 🔁 Disparo Automático

Esse pipeline é acionado a cada push para a branch `seguranca`.

---

## 🔍 OWASP ZAP – Scan de Segurança

O `zap-security-test` executa um **scan passivo** na API pública (sem autenticação) com geração de relatórios `.html` e `.json`.

#### Exemplo de vulnerabilidades detectadas:

- Injeção SQL
- Cross-Site Scripting (XSS)
- Cookies inseguros

---

## 📊 Relatórios

Os relatórios gerados pelo ZAP podem ser acessados nos artefatos do GitHub Actions:

- `zap-report.html` – visual amigável
- `zap-report.json` – útil para integração automatizada

---

## ✅ Boas Práticas Recomendadas

- Executar scans a cada push para branches críticas
- Utilizar `.trivyignore` para lidar com falsos positivos
- Definir limites de recursos nos containers no Kubernetes
- Utilizar cabeçalhos de segurança como `Content-Security-Policy`
- Automatizar alertas com Prometheus e ferramentas externas (Slack, SIEM)

---

## 📌 Conclusão

Este projeto demonstra a integração eficaz de práticas DevSecOps com ferramentas modernas de segurança e monitorização. Com o uso de **Trivy**, **OWASP ZAP** e **Prometheus**, é possível detectar e mitigar vulnerabilidades desde o desenvolvimento até a produção.
 
 ---

## 👨‍💻 Autores

- Bruna Dutra  
- Marina Gregorini  
- Marta Martins  
- Tiago Silva
