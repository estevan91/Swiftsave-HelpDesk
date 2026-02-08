from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.dataBase import connect_to_mongo, close_mongo_connection
from app.routes import casos
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    print(" Iniciando SwiftSave HelpDesk API")
    connect_to_mongo()
    yield
    # Shutdown
    print(" Cerrando SwiftSave HelpDesk API")
    close_mongo_connection()

# Crear aplicación FastAPI
app = FastAPI(
    title="SwiftSave HelpDesk API",
    description="API para gestión de solicitudes de apertura de cuentas de ahorro",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # URLs de Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(casos.router)

# Ruta raíz
@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "mensaje": "Bienvenido a SwiftSave HelpDesk API",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "servicio": "SwiftSave HelpDesk API"
    }