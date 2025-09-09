import React, { useEffect, useState } from "react";
import { Container, Typography, List, Card, CardContent, Button } from "@mui/material";
import { fetchWorks } from "../api/works";
import { useNavigate } from "react-router-dom";

const WorksList = () => {
    const [works, setWorks] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchWorks().then(setWorks);
    }, [])

    return (
        <Container>
            <Typography variant="h4">Available Works</Typography>
            <List>
                {works.map((w) => (
                    <Card key={w.id}>
                        <CardContent>
                            <Typography variant="h6">{w.title}</Typography>
                            <Typography color="text.secondary">{w.author || "Unknown"}</Typography>
                            <Button variant="contained" onClick={() => navigate(`/work/${w.slug}`)} >View</Button>
                        </CardContent>
                    </Card>
                ))}
            </List>
        </Container>
    );
}

export default WorksList;