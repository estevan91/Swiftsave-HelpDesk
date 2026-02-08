import React, { useState } from "react";
import {
  TextField,
  Button,
  Box,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  InputAdornment,
} from "@mui/material";
import { solicitudesAPI } from "../Services/api";
import { SolicitudCreate, ErrorResponse } from "../types/solicitud";
import PersonIcon from "@mui/icons-material/Person";
import BadgeIcon from "@mui/icons-material/Badge";
import EmailIcon from "@mui/icons-material/Email";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import SaveIcon from "@mui/icons-material/Save";

interface FormularioSolicitudProps {
  onSuccess?: () => void;
}

interface FormErrors {
  cliente?: string;
  documento?: string;
  email?: string;
  monto_inicial?: string;
}

interface Mensaje {
  tipo: "success" | "error" | "info" | "warning";
  texto: string;
}

const FormularioSolicitud: React.FC<FormularioSolicitudProps> = ({
  onSuccess,
}) => {
  const [formData, setFormData] = useState<SolicitudCreate>({
    cliente: "",
    documento: "",
    email: "",
    monto_inicial: 0,
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [mensaje, setMensaje] = useState<Mensaje>({ tipo: "info", texto: "" });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]:
        name === "monto_inicial"
          ? value === ""
            ? 0
            : parseFloat(value)
          : value,
    });

    if (errors[name as keyof FormErrors]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validarFormulario = (): boolean => {
    const nuevosErrores: FormErrors = {};

    if (!formData.cliente.trim()) {
      nuevosErrores.cliente = "El nombre del cliente es requerido";
    } else if (formData.cliente.length < 3) {
      nuevosErrores.cliente = "El nombre debe tener al menos 3 caracteres";
    }

    if (!formData.documento.trim()) {
      nuevosErrores.documento = "El documento es requerido";
    } else if (formData.documento.length < 5) {
      nuevosErrores.documento = "El documento debe tener al menos 5 caracteres";
    } else if (!/^\d+$/.test(formData.documento)) {
      nuevosErrores.documento = "El documento debe contener solo números";
    }

    if (!formData.email.trim()) {
      nuevosErrores.email = "El correo electrónico es requerido";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      nuevosErrores.email = "El correo electrónico no es válido";
    }

    if (!formData.monto_inicial || formData.monto_inicial <= 0) {
      nuevosErrores.monto_inicial = "El monto debe ser mayor a 0";
    }

    setErrors(nuevosErrores);
    return Object.keys(nuevosErrores).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setMensaje({ tipo: "info", texto: "" });

    if (!validarFormulario()) {
      setMensaje({
        tipo: "error",
        texto: "Por favor, corrige los errores en el formulario",
      });
      return;
    }

    setLoading(true);

    try {
      await solicitudesAPI.crear(formData);

      setMensaje({
        tipo: "success",
        texto: "¡Solicitud creada exitosamente!",
      });

      setFormData({
        cliente: "",
        documento: "",
        email: "",
        monto_inicial: 0,
      });

      if (onSuccess) {
        setTimeout(() => {
          onSuccess();
        }, 1500);
      }
    } catch (error) {
      console.error("Error al crear solicitud:", error);
      const err = error as ErrorResponse;
      const mensajeError =
        err.detail?.mensaje || err.mensaje || "Error al crear la solicitud";
      setMensaje({
        tipo: "error",
        texto: mensajeError,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 600, mx: "auto" }}>
      <Typography variant="h5" component="h2" gutterBottom sx={{ mb: 3 }}>
        Registrar Nueva Solicitud
      </Typography>

      {mensaje.texto && (
        <Alert severity={mensaje.tipo} sx={{ mb: 3 }}>
          {mensaje.texto}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <TextField
          fullWidth
          label="Nombre del Cliente"
          name="cliente"
          value={formData.cliente}
          onChange={handleChange}
          error={!!errors.cliente}
          helperText={errors.cliente}
          margin="normal"
          required
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <PersonIcon />
              </InputAdornment>
            ),
          }}
        />

        <TextField
          fullWidth
          label="Número de Documento"
          name="documento"
          value={formData.documento}
          onChange={handleChange}
          error={!!errors.documento}
          helperText={errors.documento}
          margin="normal"
          required
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <BadgeIcon />
              </InputAdornment>
            ),
          }}
        />

        <TextField
          fullWidth
          label="Correo Electrónico"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={!!errors.email}
          helperText={errors.email}
          margin="normal"
          required
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <EmailIcon />
              </InputAdornment>
            ),
          }}
        />

        <TextField
          fullWidth
          label="Monto Inicial"
          name="monto_inicial"
          type="number"
          value={formData.monto_inicial || ""}
          onChange={handleChange}
          error={!!errors.monto_inicial}
          helperText={errors.monto_inicial}
          margin="normal"
          required
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <AttachMoneyIcon />
              </InputAdornment>
            ),
          }}
        />

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          size="large"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
          sx={{ mt: 3 }}
        >
          {loading ? "Guardando..." : "Registrar Solicitud"}
        </Button>
      </Box>
    </Paper>
  );
};

export default FormularioSolicitud;
