from fastapi import APIRouter, HTTPException, Query
from app.models import SolicitudCreate, SolicitudUpdate, SolicitudResponse, SolicitudListResponse, EstadoEnum
from app.dataBase import get_collection
from datetime import datetime
from bson import ObjectId
from typing import Optional
import math

router = APIRouter(prefix="/casos", tags=["Casos"])

def solicitud_helper(solicitud) -> dict:
    """Convertir documento de MongoDB a diccionario"""
    return {
        "_id": str(solicitud["_id"]),
        "cliente": solicitud["cliente"],
        "documento": solicitud["documento"],
        "email": solicitud["email"],
        "monto_inicial": solicitud["monto_inicial"],
        "estado": solicitud["estado"],
        "fecha_creacion": solicitud["fecha_creacion"]
    }

@router.post("/", response_model=SolicitudResponse, status_code=201)
async def crear_solicitud(solicitud: SolicitudCreate):
    """
    Crear una nueva solicitud de apertura de cuenta.
    
    - **cliente**: Nombre completo del cliente (3-100 caracteres)
    - **documento**: Número de identificación (5-20 caracteres)
    - **email**: Correo electrónico válido
    - **monto_inicial**: Monto inicial positivo
    """
    try:
        collection = get_collection()
        
        # Verificar si ya existe una solicitud con el mismo documento
        solicitud_existente = collection.find_one({"documento": solicitud.documento})
        if solicitud_existente:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una solicitud con el documento {solicitud.documento}"
            )
        
        # Crear nuevo documento
        nuevo_caso = {
            "cliente": solicitud.cliente,
            "documento": solicitud.documento,
            "email": solicitud.email,
            "monto_inicial": solicitud.monto_inicial,
            "estado": EstadoEnum.PENDIENTE.value,
            "fecha_creacion": datetime.utcnow()
        }
        
        # Insertar en MongoDB
        resultado = collection.insert_one(nuevo_caso)
        
        # Obtener el documento insertado
        caso_creado = collection.find_one({"_id": resultado.inserted_id})
        
        return solicitud_helper(caso_creado)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la solicitud: {str(e)}")

@router.get("/", response_model=SolicitudListResponse)
async def listar_solicitudes(
    pagina: int = Query(1, ge=1, description="Número de página"),
    por_pagina: int = Query(10, ge=1, le=100, description="Solicitudes por página"),
    estado: Optional[EstadoEnum] = Query(None, description="Filtrar por estado")
):
    """
    Obtener lista de solicitudes con paginación.
    
    - **pagina**: Número de página (por defecto 1)
    - **por_pagina**: Cantidad de resultados por página (por defecto 10, máximo 100)
    - **estado**: Filtro opcional por estado (Pendiente, Procesando, Cerrado)
    """
    try:
        collection = get_collection()
        
        # Filtro de búsqueda
        filtro = {}
        if estado:
            filtro["estado"] = estado.value
        
        # Contar total de documentos
        total = collection.count_documents(filtro)
        
        # Calcular paginación
        skip = (pagina - 1) * por_pagina
        total_paginas = math.ceil(total / por_pagina)
        
        # Obtener solicitudes ordenadas por fecha (más recientes primero)
        solicitudes = list(
            collection.find(filtro)
            .sort("fecha_creacion", -1)
            .skip(skip)
            .limit(por_pagina)
        )
        
        # Convertir a formato de respuesta
        solicitudes_formateadas = [solicitud_helper(s) for s in solicitudes]
        
        return {
            "total": total,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total_paginas": total_paginas,
            "solicitudes": solicitudes_formateadas
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes: {str(e)}")

@router.get("/{caso_id}", response_model=SolicitudResponse)
async def obtener_solicitud(caso_id: str):
    """
    Obtener una solicitud específica por ID.
    
    - **caso_id**: ID único de la solicitud
    """
    try:
        collection = get_collection()
        
        # Validar formato de ObjectId
        if not ObjectId.is_valid(caso_id):
            raise HTTPException(status_code=400, detail="ID de solicitud inválido")
        
        # Buscar solicitud
        solicitud = collection.find_one({"_id": ObjectId(caso_id)})
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        return solicitud_helper(solicitud)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la solicitud: {str(e)}")

@router.patch("/{caso_id}", response_model=SolicitudResponse)
async def actualizar_estado(caso_id: str, datos: SolicitudUpdate):
    """
    Actualizar el estado de una solicitud.
    
    - **caso_id**: ID único de la solicitud
    - **estado**: Nuevo estado (Pendiente, Procesando, Cerrado)
    """
    try:
        collection = get_collection()
        
        # Validar formato de ObjectId
        if not ObjectId.is_valid(caso_id):
            raise HTTPException(status_code=400, detail="ID de solicitud inválido")
        
        # Verificar que la solicitud existe
        solicitud_existente = collection.find_one({"_id": ObjectId(caso_id)})
        if not solicitud_existente:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        # Actualizar estado
        resultado = collection.update_one(
            {"_id": ObjectId(caso_id)},
            {"$set": {"estado": datos.estado.value}}
        )
        
        if resultado.modified_count == 0:
            # Si no se modificó, podría ser que ya tenía ese estado
            pass
        
        # Obtener solicitud actualizada
        solicitud_actualizada = collection.find_one({"_id": ObjectId(caso_id)})
        
        return solicitud_helper(solicitud_actualizada)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la solicitud: {str(e)}")