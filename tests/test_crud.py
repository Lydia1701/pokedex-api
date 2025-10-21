def test_create_and_get(client):
    payload = {"name":"Charmander","type":"fire","power":100}
    r = client.post("/pokemons/", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["name"] == "Charmander"
    assert "power_current" in created 

    pid = created["id"]
    r2 = client.get(f"/pokemons/{pid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == pid

def test_update(client):
    r = client.post("/pokemons/", json={"name":"Squirtle","type":"water","power":90})
    pid = r.json()["id"]
    r2 = client.patch(f"/pokemons/{pid}", json={"power":120})
    assert r2.status_code == 200
    assert r2.json()["power"] == 120

def test_delete(client):
    r = client.post("/pokemons/", json={"name":"Bulbasaur","type":"grass","power":80})
    pid = r.json()["id"]
    rd = client.delete(f"/pokemons/{pid}")
    assert rd.status_code == 204
    r2 = client.get(f"/pokemons/{pid}")
    assert r2.status_code == 404
