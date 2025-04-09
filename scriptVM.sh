#!/bin/bash

# Variáveis
VM_NAME="vm-grupo4"
RESOURCE_GROUP="RG-UPSKILL-SysAdmin"
VNET_NAME="redegrupo4"
SUBNET_NAME="subnetgrupo4"
PORT="5000"
LOCATION="spaincentral"
IMAGE="Ubuntu2404"
SIZE="Standard_B1ms"
OS_DISK_SIZE="32"
USER_NAME="grupo4"

# Solicita a senha
read -s -p "Digite a senha da VM para o usuário '$USER_NAME': " VM_PASSWORD
echo

# Função para verificar se o comando foi bem-sucedido
check_success() {
    if [ $? -ne 0 ]; then
        echo "Erro: O comando '$1' falhou."
        exit 1
    fi
}

# 1. Criar a rede virtual e sub-rede
echo "Criando rede virtual e sub-rede..."
az network vnet create \
  --resource-group $RESOURCE_GROUP \
  --name $VNET_NAME \
  --address-prefix 10.0.0.0/16 \
  --subnet-name $SUBNET_NAME \
  --subnet-prefix 10.0.1.0/24 \
  --location $LOCATION
check_success "az network vnet create"

# 2. Criar NSG com regras personalizadas
echo "Criando Network Security Group com regras personalizadas..."
az network nsg create \
  --resource-group $RESOURCE_GROUP \
  --name "${VM_NAME}-nsg" \
  --location $LOCATION

# Regra para SSH (porta 22)
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name "${VM_NAME}-nsg" \
  --name "allow-ssh" \
  --protocol tcp \
  --priority 1000 \
  --destination-port-range 22 \
  --access allow

# Regra para aplicação (porta 5000 entrada)
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name "${VM_NAME}-nsg" \
  --name "allow-app-in" \
  --protocol tcp \
  --priority 1001 \
  --destination-port-range $PORT \
  --access allow

# 3. Criar a máquina virtual associada ao NSG
echo "Criando máquina virtual com regras de segurança..."
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --image $IMAGE \
  --size $SIZE \
  --admin-username $USER_NAME \
  --admin-password "$VM_PASSWORD" \
  --authentication-type password \
  --os-disk-size-gb $OS_DISK_SIZE \
  --storage-sku Standard_LRS \
  --vnet-name $VNET_NAME \
  --subnet $SUBNET_NAME \
  --location $LOCATION \
  --public-ip-address-allocation static \
  --nsg "${VM_NAME}-nsg"
check_success "az vm create"

# 4. Configurar regra de saída para porta 5000
echo "Configurando regra de saída para porta $PORT..."
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name "${VM_NAME}-nsg" \
  --name "allow-app-out" \
  --protocol tcp \
  --priority 1002 \
  --destination-port-range $PORT \
  --access allow \
  --direction Outbound


# 5. Instalar dependências DENTRO DA VM
echo "Instalando Docker, Git e Azure CLI..."
az vm run-command invoke \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --command-id RunShellScript \
  --scripts '
    # Atualizar pacotes
    sudo apt-get update -y
    
    # Instalar utilitários básicos
    sudo apt-get install -y python3 python3-pip git curl wget

    # Instalar Docker (agora 100% dentro da VM)
    sudo mkdir -p /etc/apt/keyrings
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Configurar Docker
    sudo usermod -aG docker '"$USER_NAME"'
    sudo systemctl enable docker
    sudo systemctl start docker
    
    # Instalar Azure CLI
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  '
check_success "az vm run-command invoke (instalação)"

az vm run-command invoke \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --command-id RunShellScript \
  --scripts 'uname -a && lsb_release -a && docker --version'
# 6. Configurar aplicação
echo "Configurando aplicação..."
az vm run-command invoke \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --command-id RunShellScript \
  --scripts "
    cd /home/$USER_NAME
    git clone https://github.com/marinagregorini/supermercadoboasorteapi.git
    cd supermercadoboasorteapi
    sudo docker build -t supermercado-api .
    sudo docker run -d -p $PORT:$PORT supermercado-api
  "
check_success "az vm run-command invoke (aplicação)"

# 7. Obter IP público
VM_PUBLIC_IP=$(az vm list-ip-addresses --resource-group $RESOURCE_GROUP --name $VM_NAME --query "[0].virtualMachine.network.publicIpAddresses[0].ipAddress" -o tsv)
check_success "az vm list-ip-addresses"

echo -e "\n\033[1;32mConfiguração concluída!\033[0m"
echo "Acesse a aplicação em: http://$VM_PUBLIC_IP:$PORT"
echo "Conectar via SSH:"
echo "ssh $USER_NAME@$VM_PUBLIC_IP"