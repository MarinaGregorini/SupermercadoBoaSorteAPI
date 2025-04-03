# Supermercado Boa Sorte - Deploy no Microsoft Azure

## Visão Geral
Este projeto envolve a configuração e implementação de uma aplicação no Microsoft Azure, incluindo a criação de uma rede virtual, máquina virtual (VM), instalação de dependências e configuração de uma API acessível via Postman.

---

## 🌐 Configuração da Rede Virtual no Azure

### 1️⃣ Criar a Rede Virtual (VNet)
Aceda ao portal do Azure e siga os passos:
- Caminho: **Recursos** > **Redes Virtuais** > **Criar**
- Na aba **Básico**, preencha todos os campos necessários.
- Selecionar **Rever + Criar** > **Criar**.

---

## 🚀 Configuração da VM no Azure

### 2️⃣ Criar a Máquina Virtual
Aceda ao portal do Azure e siga os passos:
- Caminho: **Página Inicial** > **Criar um recurso** > **Máquina Virtual** > **Criar**
- Na aba **Básico**, preencha com:
  - **Subscrição**: FCUL-UPSKILL
  - **Grupo de Recursos**: RG-UPSKILL-SysAdmin
  - **Região**: Spain Central (Zona 3)
  - **Imagem**: Linux (Ubuntu 24.04)
  - **Tamanho**: Standard B1ms (1 vCPU, 2 GiB memória)
- Na aba **Discos**, configure:
  - **Tipo de disco**: LRS HDD Standard
  - **Tamanho**: 32 GiB
- Na aba **Rede**, selecione a rede virtual criada anteriormente em **Rede Virtual**.

### 3️⃣ Conectar-se à VM via SSH
```bash
ssh grupo4@68.221.171.29
```

---

## 📦 Configuração do Ambiente

### 4️⃣ Atualizar pacotes do sistema e instalar dependências essenciais
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3.12-venv
```

### 5️⃣ Criar a estrutura do projeto
```bash
mkdir grupo4
cd grupo4
```

### 6️⃣ Clonar o repositório do projeto
```bash
git clone http://github.com/MarinaGregorini/SupermercadoBoaSorteAPI.git
cd SupermercadoBoaSorteAPI
```

### 7️⃣ Criar e ativar o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 8️⃣ Atualizar pip e instalar as dependências do projeto
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔗 Configuração do Armazenamento no Azure

### 9️⃣ Criar a pasta `db-supermercado` e a subpasta `db` no Azure Storage
Aceda à interface gráfica do Azure e:
- Criar a pasta **db-supermercado**
- Dentro dela, criar a subpasta **db**

### 🔟 Criar a pasta `db` localmente na VM
```bash
mkdir -p /home/grupo4/grupo4/SupermercadoBoaSorteAPI/db
```

### 1️⃣1️⃣ Criar credenciais para armazenamento no Azure
Crie o ficheiro `/etc/azurefiles.cred`:
```bash
sudo nano /etc/azurefiles.cred
```
Adicione as credenciais:
```
username=[NOME_DA_CONTA_DE_ARMAZENAMENTO]
password=[CHAVE_DA_CONTA_DE_ARMAZENAMENTO]
```

### 1️⃣2️⃣ Montar a pasta da WebApp
Edite o ficheiro `/etc/fstab`:
```bash
sudo nano /etc/fstab
```
Adicione a seguinte linha ao final:
```bash
//tiagosilva1.file.core.windows.net/db-supermercado /home/grupo4/grupo4/SupermercadoBoaSorteAPI/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```

### 1️⃣3️⃣ Aplicar as configurações e testar a montagem
```bash
sudo systemctl daemon-reload
sudo mount -a
```

---

## 🔥 Configuração de Rede

### 1️⃣4️⃣ Abrir a porta 5000 no Azure
1. Aceda ao portal do Azure.
2. Vá até **Rede** > **Configurações da Rede** > **Criar Regra de Portas**.
3. Adicione a porta **5000** para entrada e saída.

---

## 📡 Executar a Aplicação

### 1️⃣5️⃣ Criar e popular a base de dados
```bash
python app.py  # Criar a base de dados
python populate_db.py  # Popular a base de dados
```

### 1️⃣6️⃣ Iniciar a aplicação
```bash
python app.py
```

Agora a aplicação estará acessível em:
```
http://68.221.171.29:5000
```

---

## 🛠️ Testar a API via Postman

### 1️⃣7️⃣ Listar transportadoras, produtores e produtos
```http
GET http://68.221.171.29:5000/api/transportadoras/
GET http://68.221.171.29:5000/api/produtores/
GET http://68.221.171.29:5000/api/produtos/
```

### 1️⃣8️⃣ Criar um consumidor
```http
POST http://68.221.171.29:5000/api/consumidores/
```
**Body (JSON):**
```json
{
  "nome": "Nome do Consumidor"
}
```

### 1️⃣9️⃣ Listar consumidores
```http
GET http://68.221.171.29:5000/api/consumidores/
```

### 2️⃣0️⃣ Criar um pedido
```http
POST http://68.221.171.29:5000/api/consumidores/<int:consumidor_id>/produtos/
```
**Body (JSON):**
```json
{
  "produtos": [
    {"produto_id": int:ID, "quantidade": int:QUANTIDADE}
  ]
}
```

### 2️⃣1️⃣ Ver detalhes do pedido
```http
GET http://68.221.171.29:5000/api/consumidores/<id:consumidor>/resumo
```

---

## 👥 Equipa
- **Bruna Dutra**
- **Marina Gregorini**
- **Marta Martins**
- **Tiago Silva**
