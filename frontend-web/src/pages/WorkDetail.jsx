import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchWorkBySlug } from "../api/works";
import { Container, FormControl, Typography, MenuItem, Button, InputLabel, Select } from "@mui/material";

export default function WorkDetail() {
    const { slug } = useParams();
    const [work, setWork] = useState(null);
    const [selectedSection, setSelectedSection] = useState("full");
    const navigate = useNavigate();

    useEffect(() => {
        fetchWorkBySlug(slug).then(setWork);
    }, [slug]);

    if (!work) return <p>Loading...</p>;

    const handleViewWork = () => {
        if (selectedSection === "full") {
            alert(`Viewing full work: ${work.title}`);
        } else {
            alert(`Viewing section ${selectedSection} of work: ${work.title}`);
        }
    };

    return (
        <Container>
            <Typography variant="h4">{work.title}</Typography>
            <Typography colour="text.secondary">By: {work.author || "Unknown"}</Typography>
            <FormControl fullWidth>
                <InputLabel id="section-select-label">Select Section</InputLabel>
                    <Select
                    labelId="section-select-label"
                    value={selectedSection}
                    onChange={(e) => setSelectedSection(e.target.value)}
                    >
                    <MenuItem value="full">Full Work</MenuItem>
                    {work.sections.map((section, index) => (
                        <MenuItem key={section.id} value={index + 1}>
                        Section {index + 1}
                        </MenuItem>
                    ))}
                    </Select>
            </FormControl>
            <Button variant="contained" onClick={handleViewWork}>View Work</Button>
        </Container>
    )
}