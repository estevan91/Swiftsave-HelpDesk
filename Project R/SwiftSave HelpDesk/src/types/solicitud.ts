export interface Solicitud {
  _id: string;
  cliente: string;
  documento: string;
  email: string;
  monto_inicial: number;
  estado: EstadoSolicitud;
  fecha_creacion: string;
}

export type EstadoSolicitud = "Pendiente" | "Procesando" | "Cerrado";

export interface SolicitudCreate {
  cliente: string;
  documento: string;
  email: string;
  monto_inicial: number;
}

export interface SolicitudListResponse {
  total: number;
  pagina: number;
  por_pagina: number;
  total_paginas: number;
  solicitudes: Solicitud[];
}

export interface ErrorResponse {
  mensaje?: string;
  detail?: {
    mensaje?: string;
    error_code?: string;
  };
}
