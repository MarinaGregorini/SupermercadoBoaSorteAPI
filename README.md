# Supermercado Boa Sorte - Deploy no Microsoft Azure

## Visão Geral
Este projeto envolve a configuração e implementação de uma aplicação no Microsoft Azure, incluindo a criação de uma máquina virtual (VM), instalação de dependências e configuração de uma API acessível via Postman.

---

## 🚀 Configuração da VM no Azure

### 1️⃣ Criar a Máquina Virtual
Aceda ao portal do Azure e siga os passos:
- Caminho: **Página Inicial** > **Criar um recurso** > **Máquina Virtual** > **Criar**
- Na aba **Básico**, preencha com:
  - **Subscrição**: FCUL-UPSKILL
  - **Grupo de Recursos**: RG-UPSKILL-SysAdmin
  - **Região**: Spain Central (Zona 3)
  - **Imagem**: Linux (Ubuntu 24.04)
  - **Tamanho**: Standard B1ms (1 vCPU, 2 GiB memória)

### 2️⃣ Conectar-se à VM via SSH
```bash
ssh grupo4@68.221.121.174
```

---

## 📦 Configuração do Ambiente

### 3️⃣ Atualizar pacotes do sistema e instalar dependências essenciais
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3.12-venv
```

### 4️⃣ Criar a estrutura do projeto
```bash
mkdir grupo4
cd grupo4
```

### 5️⃣ Clonar o repositório do projeto
```bash
git clone http://github.com/MarinaGregorini/SupermercadoBoaSorteAPI.git
cd SupermercadoBoaSorteAPI
```

### 6️⃣ Criar e ativar o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 7️⃣ Atualizar pip e instalar as dependências do projeto
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔗 Configuração do Armazenamento no Azure

### 8️⃣ Criar a pasta `db` no Azure Storage
Aceda à interface gráfica do Azure e, dentro da pasta `db-supermercado`, crie uma subpasta chamada `db`.

### 9️⃣ Criar credenciais para armazenamento no Azure
Crie o ficheiro `/etc/azurefiles.cred`:
```bash
sudo nano /etc/azurefiles.cred
```
Adicione as credenciais:
```
username=[NOME_DA_CONTA_DE_ARMAZENAMENTO]
password=[CHAVE_DA_CONTA_DE_ARMAZENAMENTO]
```

### 🔟 Montar a pasta da WebApp
Edite o ficheiro `/etc/fstab`:
```bash
sudo nano /etc/fstab
```
Adicione a seguinte linha ao final:
```
//tiagosilva1.file.core.windows.net/db-supermercado /home/grupo4/grupo4/SupermercadoBoaSorteAPI/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```

### 🔄 Aplicar as configurações e testar a montagem
```bash
sudo systemctl daemon-reload
sudo mount -a
ls /home/grupo4/grupo4/SupermercadoBoaSorteAPI/db  # Verificar se a montagem foi bem-sucedida
```

---

## 🔥 Configuração de Rede

### 1️⃣1️⃣ Abrir a porta 8000 no Azure
1. Aceda ao portal do Azure.
2. Vá até **Rede** > **Configurações da Rede** > **Criar Regra de Portas**.
3. Adicione a porta **8000** para entrada e saída.

---

## 📡 Executar a Aplicação

### 1️⃣2️⃣ Criar e popular a base de dados
```bash
python app.py  # Criar a base de dados
python populate_db.py  # Popular a base de dados
```

### 1️⃣3️⃣ Iniciar a aplicação em segundo plano
```bash
nohup python app.py &
```

Agora a aplicação estará acessível em:
```
http://68.221.121.174:8000
```

---

## 🛠️ Testar a API via Postman

### 1️⃣4️⃣ Listar transportadoras, produtores e produtos
```http
GET http://68.221.121.174:8000/api/transportadoras/
GET http://68.221.121.174:8000/api/produtores/
GET http://68.221.121.174:8000/api/produtos/
```

### 1️⃣5️⃣ Criar um consumidor
```http
POST http://68.221.121.174:8000/api/consumidores/
```
**Body (JSON):**
```json
{
  "nome": "Nome do Consumidor"
}
```

### 1️⃣6️⃣ Listar consumidores
```http
GET http://68.221.121.174:8000/api/consumidores/
```

### 1️⃣7️⃣ Criar um pedido
```http
POST http://68.221.121.174:8000/api/consumidores/<id:consumidor>/produtos
```
**Body (JSON):**
```json
{
  "produtos": [
    {"produto_id": ID, "quantidade": QUANTIDADE}
  ]
}
```

### 1️⃣8️⃣ Ver detalhes do pedido
```http
GET http://68.221.121.174:8000/api/consumidores/<id:consumidor>/resumo
```

---

## 👥 Equipa
- **Bruna Dutra**
- **Marina Gregorini**
- **Marta Martins**
- **Tiago Silva**
