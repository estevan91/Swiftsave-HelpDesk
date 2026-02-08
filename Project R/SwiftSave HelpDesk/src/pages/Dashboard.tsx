import React from "react";
import { Container } from "@mui/material";
import TablaSolicitudes from "../components/TablaSolicitudes";

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <TablaSolicitudes />
    </Container>
  );
};

export default Dashboard;
