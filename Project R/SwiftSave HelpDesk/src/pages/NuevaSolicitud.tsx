import React from "react";
import { Container } from "@mui/material";
import { useNavigate } from "react-router-dom";
import FormularioSolicitud from "../components/FormularioSolicitud";

const NuevaSolicitud: React.FC = () => {
  const navigate = useNavigate();

  const handleSuccess = () => {
    navigate("/");
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <FormularioSolicitud onSuccess={handleSuccess} />
    </Container>
  );
};

export default NuevaSolicitud;
