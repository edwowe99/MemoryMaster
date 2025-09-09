  import React, { useState, useRef, useEffect } from "react";
  import { useParams } from "react-router-dom";
  import { fetchWorkBySlug, postPracticeResults } from "../api/works";
  import {
    Box,
    Typography,
    Slider,
    Button,
    Card,
    CardContent,
    LinearProgress,
  } from "@mui/material";



  export default function PracticeWork() {
    const { slug } = useParams();
    const [work, setWork] = useState(null);
    const [blankPercent, setBlankPercent] = useState(30);
    const [practiceStarted, setPracticeStarted] = useState(false);
    const [words, setWords] = useState([]);
    const [blanks, setBlanks] = useState([]);
    const [currentBlankIndex, setCurrentBlankIndex] = useState(0);
    const inputRef = useRef(null);

    // Load work
    useEffect(() => {
      fetchWorkBySlug(slug).then(setWork);
    }, [slug]);

    useEffect(() => {
      if (practiceStarted && inputRef.current) {
        inputRef.current.focus();
      }
    }, [practiceStarted, currentBlankIndex]);

    const startPractice = () => {
      const newBlanks = [];
      const newWords = [];

      work.sections.forEach((section, sectionIdx) => {
        section.units.forEach((unit, unitIdx) => {
          const unitWords = unit.text.split(" ");
          const numToBlank = Math.ceil((blankPercent / 100) * unitWords.length);
          const blankIndices = new Set();

          while (blankIndices.size < numToBlank) {
            const randomIndex = Math.floor(Math.random() * unitWords.length);
            blankIndices.add(randomIndex);
          }

          unitWords.forEach((word, i) => {
            if (blankIndices.has(i)) {
              newBlanks.push({
                sectionId: section.id,
                unitId: unit.id,
                indexInFullText: newWords.length,
                original: word,
                guess: "",
                correct: null,
              });
              newWords.push("___");
            } else {
              newWords.push(word);
            }
          });

          // Add a single line break after each unit
          newWords.push("\n");

          // If last unit in section, add another line break
          if (unitIdx === section.units.length - 1) {
            newWords.push("\n");
          }
        });
      });

      setWords(newWords);
      setBlanks(newBlanks);
      setCurrentBlankIndex(0);
      setPracticeStarted(true);
    };

    const clean = (str) => str.replace(/[.,!?;:]/g, "").toLowerCase();

    const advanceBlank = (isCorrect) => {
      const updatedBlanks = [...blanks];
      updatedBlanks[currentBlankIndex].correct = isCorrect;
      setBlanks(updatedBlanks);

      const updatedWords = [...words];
      updatedWords[updatedBlanks[currentBlankIndex].indexInFullText] =
        updatedBlanks[currentBlankIndex].guess ||
        updatedBlanks[currentBlankIndex].original;

      setWords(updatedWords);
      setCurrentBlankIndex((prev) => prev + 1);
    };

    const handleInputChange = (value) => {
      const updatedBlanks = [...blanks];
      updatedBlanks[currentBlankIndex].guess = value;

      const updatedWords = [...words];
      updatedWords[updatedBlanks[currentBlankIndex].indexInFullText] =
        value || "___";

      setBlanks(updatedBlanks);
      setWords(updatedWords);
    };

    const handleKeyDown = (e) => {
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        const current = blanks[currentBlankIndex];
        const isCorrect = clean(current.guess) === clean(current.original);
        advanceBlank(isCorrect);
      }
    };

    const handlePracticeComplete = async () => {
      if (!work) return;

      const groupedResults = {};

      blanks.forEach((b) => {
        if (!groupedResults[b.unitId]) {
          groupedResults[b.unitId] = [];
        }
        groupedResults[b.unitId].push({
          word: b.original,
          guess: b.guess,
          correct: !!b.correct,
        });
      });

      // Precompute a quick lookup for unit word counts from `work`
      const unitWordCounts = {};
      work.sections.forEach((section) => {
        section.units.forEach((u) => {
          // robust split: remove extra whitespace, count real tokens
          unitWordCounts[u.id] = u.text
            .split(/\s+/)
            .filter(Boolean).length;
        });
      });

      // Build units payload
      const units = Object.entries(groupedResults).map(([unitId, entries]) => {
        const totalBlanks = entries.length;
        const totalCorrect = entries.filter((e) => e.correct).length;
        const score = totalBlanks > 0 ? totalCorrect / totalBlanks : 0;

        const totalWords = unitWordCounts[unitId] || 0;
        const cap = totalWords > 0 ? totalBlanks / totalWords : 0;

        return {
          unit_id: unitId,
          score,
          cap,
        };
      });

      // debug: inspect what we'll send
      console.log("practice payload", { work_id: work.id, mode: "practice", units });

      try {
        await postPracticeResults(work.id, units);
        alert("Practice complete! Results submitted.");
      } catch (err) {
        console.error("Failed to submit practice results:", err);
        alert("Failed to submit results; check console for details.");
      }
    };

    const progress = blanks.length
      ? (currentBlankIndex / blanks.length) * 100
      : 0;

    if (!work) {
      return <Typography>Loading...</Typography>;
    }

    return (
      <Box sx={{ p: 4, maxWidth: 800, mx: "auto" }}>
        <Typography variant="h4" gutterBottom>
          Practice Work: {work.title}
        </Typography>

        {!practiceStarted && (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography gutterBottom>
                Sections: {work.sections.length}
              </Typography>
              <Slider
                value={blankPercent}
                onChange={(e, val) => setBlankPercent(val)}
                valueLabelDisplay="auto"
                step={5}
                min={0}
                max={100}
              />
              <Button
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
                onClick={startPractice}
              >
                Start Practice
              </Button>
            </CardContent>
          </Card>
        )}

        {practiceStarted && (
          <Box>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{ mb: 3, height: 8, borderRadius: 4 }}
            />

            <Typography variant="body1" sx={{ mb: 3, lineHeight: 2 }}>
              {words.map((word, idx) => {
                  if (word === "\n") {
                    return <br key={`br-${idx}`} />;
                  }
                const isCurrent =
                  currentBlankIndex < blanks.length &&
                  idx === blanks[currentBlankIndex].indexInFullText;
                const blankData = blanks.find(
                  (b) => b.indexInFullText === idx
                );
                let color = "inherit";
                if (blankData?.correct === true) color = "green";
                if (blankData?.correct === false) color = "red";

                if (isCurrent) {
                  return (
                    <input
                      key={idx}
                      ref={inputRef}
                      value={blanks[currentBlankIndex].guess}
                      onChange={(e) => handleInputChange(e.target.value)}
                      onKeyDown={handleKeyDown}
                      style={{
                        display: "inline-block",
                        minWidth: "40px",
                        border: "2px solid #fbc02d",
                        borderRadius: "4px",
                        backgroundColor: "#fff9c4",
                        padding: "2px 4px",
                        fontWeight: "bold",
                        animation: "pulse 1s infinite",
                      }}
                    />
                  );
                }
                return (
                  <span key={idx} style={{ color }}>
                    {word}{" "}
                  </span>
                );
              })}
            </Typography>

            {currentBlankIndex >= blanks.length && (
              <Button
                variant="contained"
                color="success"
                onClick={handlePracticeComplete}
              >
                Complete Practice
              </Button>
            )}
          </Box>
        )}

        <style>
          {`
            @keyframes pulse {
              0% { box-shadow: 0 0 0 0 rgba(251,192,45, 0.7); }
              70% { box-shadow: 0 0 0 8px rgba(251,192,45, 0); }
              100% { box-shadow: 0 0 0 0 rgba(251,192,45, 0); }
            }
          `}
        </style>
      </Box>
    );
  }