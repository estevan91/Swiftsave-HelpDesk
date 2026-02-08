from fastapi import APIRouter, HTTPException, Query, status
from app.models import SolicitudCreate, SolicitudUpdate, SolicitudResponse, SolicitudListResponse, EstadoEnum
from app.dataBase import get_collection
from datetime import datetime
from bson import ObjectId
from typing import Optional
import math
from pydantic import ValidationError

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

@router.post("/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
async def crear_solicitud(solicitud: SolicitudCreate):
    """
    Crear una nueva solicitud de apertura de cuenta.
    
    **Validaciones:**
    - El cliente debe tener entre 3 y 100 caracteres
    - El documento debe tener entre 5 y 20 caracteres y ser único
    - El email debe ser válido
    - El monto inicial debe ser positivo
    
    **Errores posibles:**
    - 400: Documento duplicado
    - 422: Datos inválidos
    - 500: Error del servidor
    """
    try:
        collection = get_collection()
        
        # Verificar si ya existe una solicitud con el mismo documento
        solicitud_existente = collection.find_one({"documento": solicitud.documento})
        if solicitud_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "Ya existe una solicitud con este documento",
                    "documento": solicitud.documento,
                    "error_code": "DOCUMENTO_DUPLICADO"
                }
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
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "mensaje": "Error de validación en los datos proporcionados",
                "errores": ve.errors()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error interno del servidor al crear la solicitud",
                "error": str(e)
            }
        )

@router.get("/", response_model=SolicitudListResponse)
async def listar_solicitudes(
    pagina: int = Query(1, ge=1, description="Número de página (mínimo 1)"),
    por_pagina: int = Query(10, ge=1, le=100, description="Solicitudes por página (entre 1 y 100)"),
    estado: Optional[EstadoEnum] = Query(None, description="Filtrar por estado (Pendiente, Procesando, Cerrado)")
):
    """
    Obtener lista de solicitudes con paginación y filtros opcionales.
    
    **Parámetros:**
    - **pagina**: Número de página (por defecto 1)
    - **por_pagina**: Cantidad de resultados por página (por defecto 10, máximo 100)
    - **estado**: Filtro opcional por estado
    
    **Ejemplo de uso:**
    - Listar todas: GET /casos
    - Filtrar pendientes: GET /casos?estado=Pendiente
    - Paginación: GET /casos?pagina=2&por_pagina=5
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
        total_paginas = math.ceil(total / por_pagina) if total > 0 else 0
        
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error al obtener las solicitudes",
                "error": str(e)
            }
        )

@router.get("/{caso_id}", response_model=SolicitudResponse)
async def obtener_solicitud(caso_id: str):
    """
    Obtener una solicitud específica por ID.
    
    **Parámetros:**
    - **caso_id**: ID único de la solicitud (formato ObjectId de MongoDB)
    
    **Errores posibles:**
    - 400: ID inválido
    - 404: Solicitud no encontrada
    - 500: Error del servidor
    """
    try:
        collection = get_collection()
        
        # Validar formato de ObjectId
        if not ObjectId.is_valid(caso_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "El ID de solicitud proporcionado no tiene un formato válido",
                    "caso_id": caso_id,
                    "error_code": "ID_INVALIDO"
                }
            )
        
        # Buscar solicitud
        solicitud = collection.find_one({"_id": ObjectId(caso_id)})
        
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "mensaje": "No se encontró ninguna solicitud con el ID proporcionado",
                    "caso_id": caso_id,
                    "error_code": "SOLICITUD_NO_ENCONTRADA"
                }
            )
        
        return solicitud_helper(solicitud)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error al obtener la solicitud",
                "error": str(e)
            }
        )

@router.patch("/{caso_id}", response_model=SolicitudResponse)
async def actualizar_estado(caso_id: str, datos: SolicitudUpdate):
    """
    Actualizar el estado de una solicitud.
    
    **Parámetros:**
    - **caso_id**: ID único de la solicitud
    - **estado**: Nuevo estado (Pendiente, Procesando o Cerrado)
    
    **Validaciones:**
    - El ID debe ser válido
    - La solicitud debe existir
    - El estado debe ser uno de los valores permitidos
    
    **Errores posibles:**
    - 400: ID inválido
    - 404: Solicitud no encontrada
    - 422: Estado inválido
    - 500: Error del servidor
    """
    try:
        collection = get_collection()
        
        # Validar formato de ObjectId
        if not ObjectId.is_valid(caso_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "El ID de solicitud proporcionado no tiene un formato válido",
                    "caso_id": caso_id,
                    "error_code": "ID_INVALIDO"
                }
            )
        
        # Verificar que la solicitud existe
        solicitud_existente = collection.find_one({"_id": ObjectId(caso_id)})
        if not solicitud_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "mensaje": "No se encontró ninguna solicitud con el ID proporcionado",
                    "caso_id": caso_id,
                    "error_code": "SOLICITUD_NO_ENCONTRADA"
                }
            )
        
        # Verificar si el estado ya es el mismo
        if solicitud_existente["estado"] == datos.estado.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "La solicitud ya tiene el estado indicado",
                    "estado_actual": datos.estado.value,
                    "error_code": "ESTADO_SIN_CAMBIOS"
                }
            )
        
        # Actualizar estado
        resultado = collection.update_one(
            {"_id": ObjectId(caso_id)},
            {"$set": {"estado": datos.estado.value}}
        )
        
        # Obtener solicitud actualizada
        solicitud_actualizada = collection.find_one({"_id": ObjectId(caso_id)})
        
        return solicitud_helper(solicitud_actualizada)
        
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "mensaje": "Error de validación en los datos proporcionados",
                "errores": ve.errors()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error al actualizar el estado de la solicitud",
                "error": str(e)
            }
        )

@router.delete("/{caso_id}", status_code=status.HTTP_200_OK)
async def eliminar_solicitud(caso_id: str):
    """
    Eliminar una solicitud (endpoint adicional, opcional).
    
    **Parámetros:**
    - **caso_id**: ID único de la solicitud a eliminar
    
    **Errores posibles:**
    - 400: ID inválido
    - 404: Solicitud no encontrada
    - 500: Error del servidor
    """
    try:
        collection = get_collection()
        
        # Validar formato de ObjectId
        if not ObjectId.is_valid(caso_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "El ID de solicitud proporcionado no tiene un formato válido",
                    "caso_id": caso_id,
                    "error_code": "ID_INVALIDO"
                }
            )
        
        # Verificar que la solicitud existe
        solicitud_existente = collection.find_one({"_id": ObjectId(caso_id)})
        if not solicitud_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "mensaje": "No se encontró ninguna solicitud con el ID proporcionado",
                    "caso_id": caso_id,
                    "error_code": "SOLICITUD_NO_ENCONTRADA"
                }
            )
        
        # Eliminar solicitud
        collection.delete_one({"_id": ObjectId(caso_id)})
        
        return {
            "mensaje": "Solicitud eliminada exitosamente",
            "caso_id": caso_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error al eliminar la solicitud",
                "error": str(e)
            }
        )