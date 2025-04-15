# tests/test_api_script.py
import requests
import json
import os

# Define a URL base da sua API.
BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:5000")
CONSUMIDORES_ENDPOINT = f"{BASE_URL}/api/consumidores/"


def test_create_and_get_consumidor():
    """Testa a criação de um consumidor via POST e sua listagem via GET."""
    new_consumidor = {"nome": "Verbose Test Consumidor Script"}
    headers = {"Content-Type": "application/json"}

    print("\n--- Teste de Criação de Consumidor ---")
    print(f"Enviando POST para: {CONSUMIDORES_ENDPOINT}")
    print(f"Dados: {json.dumps(new_consumidor)}")

    # Criar o consumidor (POST)
    try:
        response_post = requests.post(
            CONSUMIDORES_ENDPOINT,
            headers=headers,
            json=new_consumidor
        )
        print(f"Status POST: {response_post.status_code}")
        print(f"Resposta POST: {response_post.text}")

        assert response_post.status_code == 201, (
            f"Erro ao criar consumidor: {response_post.status_code} - "
            f"{response_post.text}"
        )

        created_consumidor = response_post.json()
        assert "id" in created_consumidor, "Resposta sem 'id'"
        consumidor_id = created_consumidor["id"]
        assert created_consumidor["nome"] == new_consumidor["nome"], (
            f"Nome criado ({created_consumidor['nome']}) diferente do "
            f"enviado ({new_consumidor['nome']})"
        )
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão ao criar consumidor: {e}")
        return

    print("\n--- Teste de Listagem de Consumidores ---")
    print(f"Enviando GET para: {CONSUMIDORES_ENDPOINT}")

    # Listar todos os consumidores (GET)
    try:
        response_get = requests.get(CONSUMIDORES_ENDPOINT)
        print(f"Status GET: {response_get.status_code}")
        print(f"Resposta GET: {response_get.text}")
        assert response_get.status_code == 200, (
            f"Erro ao listar: {response_get.status_code} - "
            f"{response_get.text}"
        )

        all_consumidores = response_get.json()
        print(f"Lista de consumidores: {all_consumidores}")

        found = any(
            c["id"] == consumidor_id and c["nome"] == new_consumidor["nome"]
            for c in all_consumidores
        )

        assert found, (
            f"Consumidor ID {consumidor_id} com nome "
            f"'{new_consumidor['nome']}' não encontrado"
        )

        print(
            f"Consumidor ID {consumidor_id} com nome "
            f"'{new_consumidor['nome']}' encontrado"
        )
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão ao listar: {e}")


if __name__ == "__main__":
    test_create_and_get_consumidor()
