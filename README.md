# SwiftSave HelpDesk - Sistema de Gestión de Solicitudes

Sistema web full-stack para gestionar solicitudes de apertura de cuentas de ahorro del banco SwiftSave.

## 🚀 Tecnologías Utilizadas

### Backend
- **Python** con **FastAPI**
- **MongoDB Atlas** (Base de datos en la nube)
- **Pydantic** para validaciones
- **Uvicorn** como servidor ASGI

### Frontend
- **React** con **TypeScript**
- **Vite** como bundler
- **Material UI** para componentes
- **Axios** para peticiones HTTP
- **React Router** para navegación

## 📋 Funcionalidades

- ✅ Registro de nuevas solicitudes de cuenta
- ✅ Dashboard con listado de solicitudes
- ✅ Paginación de resultados
- ✅ Filtrado por estado (Pendiente, Procesando, Cerrado)
- ✅ Actualización de estados en tiempo real
- ✅ Validaciones de datos en frontend y backend
- ✅ Diseño responsive con Material UI

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- Cuenta en MongoDB Atlas

### Backend

1. Navegar a la carpeta del backend:
```bash
cd Backend
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install fastapi uvicorn pymongo python-dotenv pydantic
```

5. Crear archivo `.env` con las siguientes variables:
```env
MONGODB_URL=tu_url_de_mongodb_atlas
DATABASE_NAME=SwiftSave
COLLECTION_NAME=Solicitudes
```

6. Ejecutar el servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

El backend estará disponible en: `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

### Frontend

1. Navegar a la carpeta del frontend:
```bash
cd "SwiftSave HelpDesk"
```

2. Instalar dependencias:
```bash
npm install
```

3. Ejecutar en modo desarrollo:
```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📡 API Endpoints

### Casos (Solicitudes)

- **POST** `/casos/` - Crear nueva solicitud
- **GET** `/casos/` - Listar solicitudes (con paginación y filtros)
- **GET** `/casos/{id}` - Obtener solicitud específica
- **PATCH** `/casos/{id}` - Actualizar estado de solicitud

### Ejemplo de Request (Crear Solicitud)
```json
{
  "cliente": "Juan Pérez González",
  "documento": "1234567890",
  "email": "juan.perez@email.com",
  "monto_inicial": 500000
}
```

## 📊 Estructura del Proyecto
```
Project R/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── casos.py
│   ├── .env (no incluido en repo)
│   ├── .gitignore
│   └── requirements.txt
│
└── SwiftSave HelpDesk/
    ├── src/
    │   ├── types/
    │   │   └── solicitud.ts
    │   ├── services/
    │   │   └── api.ts
    │   ├── components/
    │   │   ├── Navbar.tsx
    │   │   ├── FormularioSolicitud.tsx
    │   │   ├── TablaSolicitudes.tsx
    │   │   └── CambiarEstado.tsx
    │   ├── pages/
    │   │   ├── Dashboard.tsx
    │   │   └── NuevaSolicitud.tsx
    │   ├── App.tsx
    │   └── main.tsx
    └── package.json
```

## Seguridad

- Las credenciales de MongoDB están en archivo `.env` (no incluido en el repositorio)
- Validaciones tanto en frontend como backend
- CORS configurado para desarrollo local

## 👤 Autor

David Esteban Moreno Fernandez
- Prueba Técnica: ID 31007 Desarrollador Frameworks
- Banco de Bogotá

## 📝 Notas

- El proyecto fue desarrollado como parte de una prueba técnica
- Base de datos configurada en MongoDB Atlas
- Frontend y Backend deben ejecutarse simultáneamente
