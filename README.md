
# 🧠 Pokedex API — FastAPI + Docker + Redis + Weather

Une API REST complète construite avec **FastAPI**, **SQLAlchemy**, et **Redis**, permettant de gérer des Pokémon tout en adaptant leur puissance selon la météo ! 🌦️

---

## 🚀 Fonctionnalités

- **CRUD complet** sur les Pokémon : `GET`, `POST`, `PATCH`, `DELETE`
- **Météo en temps réel** via OpenWeather API
- **Cache** Redis (pour éviter de trop solliciter l’API météo)
- **Base SQLite**
- **Conteneurisation complète** avec Docker & Docker Compose
- Documentation automatique Swagger → [`/docs`](http://localhost:8000/docs)

---

## ⚙️ Installation locale (sans Docker)

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/pokedex-api.git
cd pokedex-api
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv .venv
.\.venv\Scriptsctivate
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer le serveur
```bash
uvicorn app.main:app --reload
```
👉 Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Installation avec Docker

### 1️⃣ Construire et lancer les conteneurs
```bash
docker-compose build
docker-compose up
```

### 2️⃣ Accéder à l’API
- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- Redis → [localhost:6379](http://localhost:6379)

---

## 🧩 Structure du projet

```
app/
 ┣ config.py          # Configuration de la DB et de l'API météo
 ┣ crud.py            # Opérations CRUD sur les Pokémon
 ┣ db.py              # Connexion et création des tables
 ┣ dependencies.py    # Dépendances FastAPI (DB, Redis)
 ┣ logic.py           # Calculs d’ajustement de puissance
 ┣ models.py          # Modèles SQLAlchemy
 ┣ schemas.py         # Schémas Pydantic
 ┣ weather.py         # Gestion de la météo et du cache
 ┗ routers/
    ┗ pokemon.py      # Routes principales
Dockerfile
docker-compose.yml
requirements.txt
```

---

## ☁️ Variables d’environnement

| Nom | Description | Exemple |
|-----|--------------|----------|
| `DATABASE_URL` | URL de la base de données | `sqlite:///./pokedex.db` |
| `WEATHER_API_URL` | Endpoint API météo | `https://api.openweathermap.org/data/2.5/weather` |
| `WEATHER_API_KEY` | Clé API OpenWeather | `xxxxxx` |
| `DEFAULT_CITY` | Ville par défaut | `Paris,FR` |
| `REDIS_HOST` | Nom du service Redis | `redis` |
| `REDIS_PORT` | Port de Redis | `6379` |

---

## 🧪 Tests unitaires

```bash
pytest -v
```

Les tests couvrent :
- Les opérations CRUD (`test_crud.py`)
- La logique météo et d’ajustement de puissance (`test_weather_logic.py`)

---

## 🧰 Dépannage

### ⚠️ Erreur WSL : `wsl needs updating`
Ouvre PowerShell (Admin) et lance :
```bash
wsl --update
```
Si erreur `0x803fb015` → exécute :
```bash
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Puis relance Docker Desktop.

---

## 👨‍💻 Auteur

Développé par **Lily** — Étudiante ingénieure en Réseaux & Télécoms 🌐  
📧 Contact : *votre_email@example.com*
