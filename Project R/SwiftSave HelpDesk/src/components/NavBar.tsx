import React from "react";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AddCircleIcon from "@mui/icons-material/AddCircle";

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <AppBar position="static" sx={{ mb: 4 }}>
      <Toolbar>
        <AccountBalanceIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          SwiftSave HelpDesk
        </Typography>
        <Box>
          <Button
            color="inherit"
            startIcon={<DashboardIcon />}
            onClick={() => navigate("/")}
            sx={{
              fontWeight: location.pathname === "/" ? "bold" : "normal",
              textDecoration: location.pathname === "/" ? "underline" : "none",
            }}
          >
            Dashboard
          </Button>
          <Button
            color="inherit"
            startIcon={<AddCircleIcon />}
            onClick={() => navigate("/nueva-solicitud")}
            sx={{
              fontWeight:
                location.pathname === "/nueva-solicitud" ? "bold" : "normal",
              textDecoration:
                location.pathname === "/nueva-solicitud" ? "underline" : "none",
            }}
          >
            Nueva Solicitud
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
