# PokeAPI JWT

API desarrollada en **FastAPI** que permite autenticación mediante **JWT** y consulta de información de **Pokémons** a través de https://pokeapi.co/

## 1.Requisitos

- Python 3.10+
- pip
- Docker

## 2.Instalación y ejecución local

### 2.1 Clona el repositorio:

git clone https://github.com/Jefferson207/PokeApi-JWT.git
cd PokeApi-JWT 

### 2.2 Crea y activa un entorno virtual:

py -m venv venv
venv\Scripts\activate 

### 2.3 Instala las dependencias:

pip install -r requirements.txt

### 2.4 Ejecuta la API

uvicorn app.main:app --reload

### 2.5 Abre en tu navegador:

http://localhost:8000/docs


