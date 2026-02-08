import axios, { AxiosError } from "axios";
import {
  Solicitud,
  SolicitudCreate,
  SolicitudListResponse,
  EstadoSolicitud,
  ErrorResponse,
} from "../types/solicitud";

const API_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Tipo para los parámetros de la query
interface ListarParams {
  pagina: number;
  por_pagina: number;
  estado?: EstadoSolicitud;
}

export const solicitudesAPI = {
  crear: async (datos: SolicitudCreate): Promise<Solicitud> => {
    try {
      const response = await api.post<Solicitud>("/casos/", datos);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw axiosError.response?.data || axiosError.message;
    }
  },

  listar: async (
    pagina: number = 1,
    porPagina: number = 10,
    estado: EstadoSolicitud | null = null,
  ): Promise<SolicitudListResponse> => {
    try {
      const params: ListarParams = {
        pagina,
        por_pagina: porPagina,
      };

      if (estado) {
        params.estado = estado;
      }

      const response = await api.get<SolicitudListResponse>("/casos/", {
        params,
      });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw axiosError.response?.data || axiosError.message;
    }
  },

  obtener: async (id: string): Promise<Solicitud> => {
    try {
      const response = await api.get<Solicitud>(`/casos/${id}`);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw axiosError.response?.data || axiosError.message;
    }
  },

  actualizarEstado: async (
    id: string,
    estado: EstadoSolicitud,
  ): Promise<Solicitud> => {
    try {
      const response = await api.patch<Solicitud>(`/casos/${id}`, { estado });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw axiosError.response?.data || axiosError.message;
    }
  },
};

export default api;
