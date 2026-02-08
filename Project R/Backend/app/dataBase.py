from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MongoDB
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "SwiftSave")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "solicitudes")

# Cliente de MongoDB
client = None
db = None
solicitudes_collection = None

def connect_to_mongo():
    """Conectar a MongoDB Atlas"""
    global client, db, solicitudes_collection
    
    try:
        client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
        # Verificar conexión
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB Atlas")
        
        db = client[DATABASE_NAME]
        solicitudes_collection = db[COLLECTION_NAME]
        
    except Exception as e:
        print(f" Error al conectar a MongoDB: {e}")
        raise e

def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    global client
    if client:
        client.close()
        print(" Conexión a MongoDB cerrada")

def get_database():
    """Obtener instancia de la base de datos"""
    return db

def get_collection():
    """Obtener colección de solicitudes"""
    return solicitudes_collection