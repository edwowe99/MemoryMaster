import React from "react";
import { Container, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Home = () => {
    const navigate = useNavigate()

    const handleGetStarted = () => {
        navigate("/works")
    }

    return (
        <Container maxWidth="sm" style={{ textAlign: "center", marginTop: "4rem" }}>
        <Typography variant="h3" gutterBottom>
            MemoryMaster
        </Typography>
        <Typography variant="body1" gutterBottom>
            Welcome! This is the frontend for your poem memorisation app.
        </Typography>
        <Button variant="contained" color="primary" onClick={handleGetStarted}>
            Get Started
        </Button>
        </Container>
    );
}

export default Home;