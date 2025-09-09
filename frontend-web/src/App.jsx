import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from "./pages/Home";
import WorksList from "./pages/WorksList";
import WorkDetail from "./pages/WorkDetail";
import PracticeWork from "./pages/PracticeWork";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/works" element={<WorksList />} />
        <Route path="/work/:slug" element={<WorkDetail />} />
        <Route path="/work/:slug/practice" element={<PracticeWork />} />
      </Routes>
    </Router>
  )
}

export default App;