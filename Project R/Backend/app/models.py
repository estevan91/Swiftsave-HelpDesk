from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoEnum(str, Enum):
    """Estados posibles de una solicitud"""
    PENDIENTE = "Pendiente"
    PROCESANDO = "Procesando"
    CERRADO = "Cerrado"

class SolicitudBase(BaseModel):
    """Modelo base de solicitud"""
    cliente: str = Field(..., min_length=3, max_length=100, description="Nombre completo del cliente")
    documento: str = Field(..., min_length=5, max_length=20, description="Número de documento de identidad")
    email: EmailStr = Field(..., description="Correo electrónico del cliente")
    monto_inicial: float = Field(..., gt=0, description="Monto inicial de la cuenta (debe ser positivo)")
    
    @field_validator('cliente')
    @classmethod
    def validar_cliente(cls, v):
        """Validar que el nombre del cliente no esté vacío"""
        if not v or v.strip() == "":
            raise ValueError('El nombre del cliente no puede estar vacío')
        return v.strip()
    
    @field_validator('documento')
    @classmethod
    def validar_documento(cls, v):
        """Validar que el documento no esté vacío"""
        if not v or v.strip() == "":
            raise ValueError('El documento no puede estar vacío')
        return v.strip()

class SolicitudCreate(SolicitudBase):
    """Modelo para crear una solicitud"""
    pass

class SolicitudUpdate(BaseModel):
    """Modelo para actualizar el estado de una solicitud"""
    estado: EstadoEnum = Field(..., description="Nuevo estado de la solicitud")

class SolicitudResponse(SolicitudBase):
    """Modelo de respuesta de solicitud"""
    id: str = Field(..., alias="_id", description="ID único de la solicitud")
    estado: EstadoEnum = Field(default=EstadoEnum.PENDIENTE, description="Estado actual de la solicitud")
    fecha_creacion: datetime = Field(..., description="Fecha y hora de creación")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SolicitudListResponse(BaseModel):
    """Respuesta para lista de solicitudes con paginación"""
    total: int = Field(..., description="Total de solicitudes")
    pagina: int = Field(..., description="Página actual")
    por_pagina: int = Field(..., description="Solicitudes por página")
    total_paginas: int = Field(..., description="Total de páginas")
    solicitudes: list[SolicitudResponse] = Field(..., description="Lista de solicitudes")