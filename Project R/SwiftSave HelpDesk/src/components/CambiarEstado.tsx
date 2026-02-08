import React, { useState } from "react";
import { Menu, MenuItem, CircularProgress, Chip } from "@mui/material";
import ChangeCircleIcon from "@mui/icons-material/ChangeCircle";
import { solicitudesAPI } from "../Services/api";
import { Solicitud, EstadoSolicitud } from "../types/solicitud";

interface CambiarEstadoProps {
  solicitud: Solicitud;
  onEstadoActualizado?: () => void;
}

interface EstadoConfig {
  color:
    | "default"
    | "primary"
    | "secondary"
    | "error"
    | "info"
    | "success"
    | "warning";
  label: string;
}

const ESTADOS: Record<EstadoSolicitud, EstadoConfig> = {
  Pendiente: { color: "warning", label: "Pendiente" },
  Procesando: { color: "info", label: "Procesando" },
  Cerrado: { color: "success", label: "Cerrado" },
};

const CambiarEstado: React.FC<CambiarEstadoProps> = ({
  solicitud,
  onEstadoActualizado,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleCambiarEstado = async (nuevoEstado: EstadoSolicitud) => {
    setLoading(true);
    handleClose();

    try {
      await solicitudesAPI.actualizarEstado(solicitud._id, nuevoEstado);
      if (onEstadoActualizado) {
        onEstadoActualizado();
      }
    } catch (error) {
      console.error("Error al actualizar estado:", error);
      alert("Error al actualizar el estado");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Chip
        label={solicitud.estado}
        color={ESTADOS[solicitud.estado]?.color || "default"}
        onClick={handleClick}
        icon={loading ? <CircularProgress size={16} /> : <ChangeCircleIcon />}
        clickable
        disabled={loading}
      />
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        {(Object.keys(ESTADOS) as EstadoSolicitud[]).map((estado) => (
          <MenuItem
            key={estado}
            onClick={() => handleCambiarEstado(estado)}
            disabled={solicitud.estado === estado}
          >
            {estado}
          </MenuItem>
        ))}
      </Menu>
    </>
  );
};

export default CambiarEstado;
