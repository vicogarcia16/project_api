
# 📌 Project API – FastAPI con Autenticación, Tareas y Tests

Este proyecto es una API REST construida con **FastAPI**, **SQLAlchemy**, autenticación JWT (`access` y `refresh tokens`), y generación automática de descripciones con **IA** (OpenRouter). Incluye pruebas asincrónicas con `pytest` y `httpx`.

## 🚀 Características

- ✅ Registro y login de usuarios
- 🔐 Autenticación JWT con tokens de acceso y actualización
- 📋 CRUD de tareas por usuario autenticado
- 🧠 Generación automática de descripciones usando IA (OpenRouter API)
- 🧪 Pruebas automatizadas asincrónicas
- 🧰 Helpers reutilizables para lógica de negocio
- 🧼 Manejo centralizado de excepciones

---

## 📁 Estructura General

```
project_api/
│
├── app/
│   ├── core/           # Configuración, seguridad y excepciones
│   ├── db/             # Base de datos y conexión
│   ├── helpers/        # Lógica reutilizable (helpers)
│   ├── middleware/     # Middleware para JWT
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routes/         # Endpoints de la API (auth, tasks)
│   ├── schemas/        # Esquemas con Pydantic
│   ├── services/       # Integraciones externas (OpenRouter)
│   └── main.py         # Punto de entrada de la app
```

---

## ⚙️ Requisitos

- Python 3.11+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

---

## 🔐 Archivos `.env` necesarios

### `.env` (para desarrollo)

```env
DATABASE_URL=postgresql+asyncpg://usuario:contraseña@localhost:5432/mi_base
SECRET_KEY=tu_clave_secreta
BACKEND_CORS_ORIGINS=http://localhost:5173
OPENROUTER_API_KEY=tu_api_key_openrouter
OPENROUTER_MODEL=tu_model_seleccionado
```

### `.env.test` (para pruebas)

```env
DATABASE_URL=postgresql+asyncpg://usuario:contraseña@localhost:5432/mi_base_test
SECRET_KEY=clave_secreta_test
BACKEND_CORS_ORIGINS=http://localhost:5173
OPENROUTER_API_KEY=tu_api_key_openrouter
OPENROUTER_MODEL=tu_model_seleccionado
```

---

## 🧪 Instalación y Ejecución

### Instalar dependencias

```bash
pipenv install --dev
```

### Ejecutar servidor de desarrollo

```bash
pipenv run uvicorn app.main:app --reload
```

### Ejecutar tests

```bash
pipenv run test
```

---

## 📚 Endpoints principales

### 🔐 Autenticación

- `POST /auth/register` – Registro de usuario
- `POST /auth/login` – Login y obtención de tokens
- `POST /auth/refresh` – Generar nuevo token de acceso

### ✅ Tareas

Todas las rutas requieren autenticación:

- `POST /tasks/` – Crear nueva tarea (con descripción generada por IA)
- `GET /tasks/` – Obtener todas las tareas del usuario
- `GET /tasks/{task_id}/` – Obtener una tarea específica
- `POST /tasks/{task_id}/` – Regenerar descripción
- `DELETE /tasks/{task_id}/` – Eliminar tarea

---

## 🧭 Vista de la documentación Swagger

Aquí puedes ver una vista previa del panel Swagger generado automáticamente por FastAPI:

![Swagger Screenshot](https://github.com/vicogarcia16/project_api/blob/main/assets/swagger_preview.jpeg)

---

## 📎 Nota sobre IA

La API se conecta con **OpenRouter** para generar descripciones automáticas a partir del título de la tarea. Asegúrate de tener una `API key` válida en tus variables de entorno.

---

## ✒️ Autor

**Víctor García** – [@vicogarcia16](https://github.com/vicogarcia16)
