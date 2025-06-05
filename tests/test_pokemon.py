from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    response = client.post("/login", data={
        "username": "usuario1",
        "password": "password1"
    })
    return response.json()["access_token"]

def test_pokemon_requires_auth():
    response = client.post("/pokemon", json={"pokemons": ["pikachu"]})
    assert response.status_code in [401, 403]

def test_pokemon_with_auth():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/pokemon", json={"pokemons": ["pikachu"]}, headers=headers)
    assert response.status_code == 200
    assert "pikachu" in response.text.lower()
