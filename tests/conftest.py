# tests/conftest.py
import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock
from app.db import Base
from app.dependencies import get_db, get_redis
from fastapi import FastAPI
from app.routers import pokemon


@pytest.fixture(scope="function")
def client():
    """
    Crée une app FastAPI isolée avec une base de données temporaire
    pour CHAQUE test, sans toucher à la vraie base de données.
    """
    # ✅ 1. Créer une base de données SQLite temporaire UNIQUE
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    test_db_url = f"sqlite:///{db_path}"

    # ✅ 2. Créer un moteur de test complètement isolé
    test_engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        echo=False  # Pas de logs SQL pendant les tests
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # ✅ 3. Créer les tables dans la DB de test SEULEMENT
    Base.metadata.create_all(bind=test_engine)

    # ✅ 4. Créer une NOUVELLE app FastAPI pour ce test (pas celle de main.py!)
    app = FastAPI(title="Test Pokedex API")
    app.include_router(pokemon.router)  # Ajouter seulement le router

    # ✅ 5. Override get_db pour utiliser notre DB de test
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # ✅ 6. Mock Redis pour éviter les appels réseau
    async def override_get_redis():
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        return mock_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    # ✅ 7. Créer le client de test
    with TestClient(app) as test_client:
        yield test_client

    # 🧹 8. NETTOYAGE COMPLET après chaque test
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    
    try:
        os.close(db_fd)
        os.unlink(db_path)
    except Exception:
        pass 