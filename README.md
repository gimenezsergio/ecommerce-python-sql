# 🎓 Catálogo de E-commerce Interactivo - Propuesta Educativa Fullstack

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Este proyecto es una evolución del e-commerce educativo original. Se **desacopló y eliminó por completo la dependencia con el servidor de prueba externo (`FakeStoreAPI`)** para construir nuestro **Backend propio, robusto y profesional en Python (Flask)** alimentado por una **Base de Datos SQL real (SQLite con ORM SQLAlchemy)**.

---

## 🎯 Objetivos de Aprendizaje

A través de la exploración, análisis y extensión de esta base de código, los estudiantes dominarán los siguientes conceptos técnicos:

*   **🐍 Servidor Backend Propio en Python (Flask)**: Creación de un servidor API RESTful nativo para administrar los recursos del sistema y servir tanto los endpoints como los archivos estáticos.
*   **🗄️ Persistencia de Datos con SQL & SQLAlchemy**: Modelado de datos en una base de datos relacional (SQLite), consultas `SELECT DISTINCT`, filtrados y ORM orientado a objetos.
*   **⚙️ Variables de Entorno (`.env`) & Arquitectura Limpia**: Configuración defensiva mediante `python-dotenv` expuesta al cliente a través del endpoint `/api/config` sin hardcodear `localhost` en el código.
*   **🌐 Consumo de APIs REST**: Consumo asíncrono y estructurado de endpoints propios usando `fetch`, `async/await` y control de manejo de errores HTTP.
*   **🧩 ES Modules Nativos (Modularización)**: Estructuración de código desacoplado mediante ES Modules (`<script type="module">` e `import/export`) aplicando el **Principio de Responsabilidad Única (SRP)**.
*   **🎨 Diseño UI Avanzado (Glassmorphism & Modos de Tema)**: Creación de sistemas de diseño modernos con Vanilla CSS, variables CSS dinámicas, desenfoque de fondo (`backdrop-filter`) y alternancia de **Modo Día / Modo Noche** persistente en `localStorage`.
*   **🛒 Estado del Carrito & Seguridad de Tipos**: Gestión de estado global en cliente para el carrito de compras, manipulación defensiva de tipos (`Number(productId)`), persistencia local y sincronización del badge contador.
*   **👤 Perfil de Usuario Integrado**: Consumo y renderizado defensivo de endpoints de usuario con desplegables Glassmorphism y tolerancia a fallos.
*   **↕️ Ordenamiento Avanzado y Paginación en Cliente**: Algoritmos de ordenamiento local por **Precio (Menor/Mayor)** y **Nombre (A-Z/Z-A)** combinados con rebanado dinámico (*slice*) y renderizado de una botonera de paginación interactiva.
*   **🔗 Sincronización de URL (URLSearchParams & History API)**: Estado bidireccional reflejado en la barra de navegación (`window.location.search`) mediante `URLSearchParams` e `history.pushState()`, permitiendo enlaces compartibles y soporte nativo para los botones **Atrás / Adelante** (`popstate`).
*   **🎤 Web APIs Avanzadas**: Integración del reconocimiento de voz nativo (`SpeechRecognition` API) con mapa de traducción local (español a inglés) para filtrado por voz.
*   **🧪 Testing Unitario con Vitest**: Cobertura de pruebas unitarias probando funciones puras, manipulaciones del DOM simuladas (*mocking*) y peticiones de red asíncronas.

---

## 📁 Estructura del Proyecto

```text
ecommerce-python-sql/
├── index.html              # Frontend: Interfaz principal del cliente
├── style.css               # Frontend: Sistema de estilos Glassmorphism y temas
├── js/                     # Frontend: Módulos JavaScript (consiste en llamadas a la API propia)
│   └── api.js              # Cliente HTTP configurado dinámicamente mediante /api/config
└── backend/                # 🐍 SERVIDOR PYTHON & BASE DE DATOS SQL
    ├── app.py              # Aplicación principal Flask, rutas API REST y servicio de estáticos
    ├── models.py           # Modelos de tablas SQL (SQLAlchemy) con comentarios pedagógicos
    ├── seed.py             # Script de inicialización y siembra de datos semilla en SQL
    ├── requirements.txt    # Dependencias de Python (Flask, Flask-CORS, Flask-SQLAlchemy, python-dotenv)
    ├── .env.example        # Plantilla pública de variables de entorno
    └── ecommerce.db        # Base de datos SQLite local
```

---

## 🛠️ Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/gimenezsergio/ecommerce-python-sql.git
cd ecommerce-python-sql
```

### 2. Iniciar el Backend (Python + Flask + SQL)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Linux/macOS
# En Windows: venv\Scripts\activate

pip install -r requirements.txt
python seed.py  # Inicializa la base de datos SQL con los datos de prueba
python app.py   # Inicia el servidor Flask en http://localhost:5000
```

### 3. Abrir la Aplicación
Abrí `http://localhost:5000` en tu navegador. El backend de Flask servirá automáticamente el frontend y la API REST en la misma instancia.
