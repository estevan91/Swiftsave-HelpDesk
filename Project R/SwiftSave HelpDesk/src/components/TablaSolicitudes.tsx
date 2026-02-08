import React, { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  Box,
  Typography,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from "@mui/material";
import { solicitudesAPI } from "../Services/api";
import { Solicitud, EstadoSolicitud } from "../types/solicitud";
import CambiarEstado from "./CambiarEstado";

const TablaSolicitudes: React.FC = () => {
  const [solicitudes, setSolicitudes] = useState<Solicitud[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");
  const [pagina, setPagina] = useState<number>(0);
  const [porPagina, setPorPagina] = useState<number>(10);
  const [total, setTotal] = useState<number>(0);
  const [filtroEstado, setFiltroEstado] = useState<EstadoSolicitud | "">("");

  const cargarSolicitudes = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await solicitudesAPI.listar(
        pagina + 1,
        porPagina,
        filtroEstado || null,
      );

      setSolicitudes(response.solicitudes);
      setTotal(response.total);
    } catch (err) {
      console.error("Error al cargar solicitudes:", err);
      setError("Error al cargar las solicitudes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarSolicitudes();
  }, [pagina, porPagina, filtroEstado]);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPagina(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setPorPagina(parseInt(event.target.value, 10));
    setPagina(0);
  };

  const handleChangeFiltro = (
    event: SelectChangeEvent<EstadoSolicitud | "">,
  ) => {
    setFiltroEstado(event.target.value as EstadoSolicitud | "");
    setPagina(0);
  };

  const formatearFecha = (fecha: string): string => {
    return new Date(fecha).toLocaleString("es-CO", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatearMonto = (monto: number): string => {
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      minimumFractionDigits: 0,
    }).format(monto);
  };

  if (loading && solicitudes.length === 0) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box
        sx={{
          mb: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h5" component="h2">
          Solicitudes de Apertura de Cuenta
        </Typography>

        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Filtrar por Estado</InputLabel>
          <Select
            value={filtroEstado}
            label="Filtrar por Estado"
            onChange={handleChangeFiltro}
          >
            <MenuItem value="">Todos</MenuItem>
            <MenuItem value="Pendiente">Pendiente</MenuItem>
            <MenuItem value="Procesando">Procesando</MenuItem>
            <MenuItem value="Cerrado">Cerrado</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <strong>Cliente</strong>
              </TableCell>
              <TableCell>
                <strong>Documento</strong>
              </TableCell>
              <TableCell>
                <strong>Email</strong>
              </TableCell>
              <TableCell align="right">
                <strong>Monto Inicial</strong>
              </TableCell>
              <TableCell align="center">
                <strong>Estado</strong>
              </TableCell>
              <TableCell>
                <strong>Fecha Creación</strong>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {solicitudes.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{ py: 3 }}
                  >
                    No hay solicitudes registradas
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              solicitudes.map((solicitud) => (
                <TableRow key={solicitud._id} hover>
                  <TableCell>{solicitud.cliente}</TableCell>
                  <TableCell>{solicitud.documento}</TableCell>
                  <TableCell>{solicitud.email}</TableCell>
                  <TableCell align="right">
                    {formatearMonto(solicitud.monto_inicial)}
                  </TableCell>
                  <TableCell align="center">
                    <CambiarEstado
                      solicitud={solicitud}
                      onEstadoActualizado={cargarSolicitudes}
                    />
                  </TableCell>
                  <TableCell>
                    {formatearFecha(solicitud.fecha_creacion)}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        component="div"
        count={total}
        page={pagina}
        onPageChange={handleChangePage}
        rowsPerPage={porPagina}
        onRowsPerPageChange={handleChangeRowsPerPage}
        rowsPerPageOptions={[5, 10, 25, 50]}
        labelRowsPerPage="Filas por página:"
        labelDisplayedRows={({ from, to, count }) =>
          `${from}-${to} de ${count}`
        }
      />
    </Paper>
  );
};

export default TablaSolicitudes;
