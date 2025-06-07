# API FastAPI con Autenticación y Tests

Este proyecto es una API REST construida con **FastAPI**, **SQLAlchemy** y autenticación usando **JWT (access y refresh tokens)**. Incluye pruebas automáticas con `pytest` y `httpx`.

## Características

- Registro y login de usuarios
- Autenticación con tokens `access` y `refresh`
- Middleware y dependencias personalizadas
- Pruebas automatizadas asincrónicas

## Requisitos

- Python 3.11+
- Pipenv

## Archivos `.env` necesarios

Debes crear los siguientes archivos en la raíz del proyecto:

### `.env` (para desarrollo)
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/mi_base
SECRET_KEY=tu_clave_secreta
BACKEND_CORS_ORIGINS=http://localhost:5173
```
### `.env.test` (para pruebas)
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/mi_base_test
SECRET_KEY=clave_secreta_test
BACKEND_CORS_ORIGINS=http://localhost:5173
```
### Instalación
```
pipenv install --dev
```
### Ejecutar el servidor local
```
pipenv run uvicorn app.main:app --reload
```
### Ejecutar los tests
```
pipenv run test
```
### Autor ✒️
* **Víctor García** [vicogarcia16](https://github.com/vicogarcia16) 