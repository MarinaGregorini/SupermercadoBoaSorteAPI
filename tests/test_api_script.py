# tests/test_api_script.py
import requests
import json
import os

# Define a URL base da sua API.
BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:5000")
CONSUMIDORES_ENDPOINT = f"{BASE_URL}/api/consumidores/"

def test_create_and_get_consumidor():
    """
    Testa a criação de um novo consumidor via POST e a sua listagem via GET, com mais output.
    """
    new_consumidor = {"nome": "Verbose Test Consumidor Script"}
    headers = {"Content-Type": "application/json"}

    print(f"\n--- Teste de Criação de Consumidor ---")
    print(f"Enviando requisição POST para: {CONSUMIDORES_ENDPOINT}")
    print(f"Dados da requisição: {json.dumps(new_consumidor)}")

    # Criar o consumidor (POST)
    try:
        response_post = requests.post(CONSUMIDORES_ENDPOINT, headers=headers, json=new_consumidor)
        print(f"Status Code da resposta POST: {response_post.status_code}")
        print(f"Texto da resposta POST: {response_post.text}")
        assert response_post.status_code == 201, f"Erro ao criar consumidor: {response_post.status_code} - {response_post.text}"
        created_consumidor = response_post.json()
        print(f"Consumidor criado (JSON): {created_consumidor}")
        assert "id" in created_consumidor, "A resposta de criação não contém um 'id'."
        consumidor_id = created_consumidor["id"]
        assert created_consumidor["nome"] == new_consumidor["nome"], f"Nome do consumidor criado ({created_consumidor['nome']}) diferente do enviado ({new_consumidor['nome']})."
        print(f"Consumidor criado com ID: {consumidor_id} e nome '{created_consumidor['nome']}'.")
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão ao criar consumidor: {e}")
        return

    print(f"\n--- Teste de Listagem de Consumidores ---")
    print(f"Enviando requisição GET para: {CONSUMIDORES_ENDPOINT}")

    # Listar todos os consumidores (GET) e verificar se o criado está lá
    try:
        response_get = requests.get(CONSUMIDORES_ENDPOINT)
        print(f"Status Code da resposta GET: {response_get.status_code}")
        print(f"Texto da resposta GET: {response_get.text}")
        assert response_get.status_code == 200, f"Erro ao listar consumidores: {response_get.status_code} - {response_get.text}"
        all_consumidores = response_get.json()
        print(f"Lista de consumidores (JSON): {all_consumidores}")
        found = False
        for consumidor in all_consumidores:
            if consumidor["id"] == consumidor_id and consumidor["nome"] == new_consumidor["nome"]:
                found = True
                break
        assert found, f"Consumidor criado com ID {consumidor_id} e nome '{new_consumidor['nome']}' não encontrado na lista."
        print(f"Consumidor com ID {consumidor_id} e nome '{new_consumidor['nome']}' encontrado na lista.")
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão ao listar consumidores: {e}")

if _name_ == "_main_":
    test_create_and_get_consumidor()
