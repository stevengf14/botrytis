import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Home from "./components/Home";
import BotrytisDetection from "./components/BotrytisDetection/BotrytisDetection";
import "@fortawesome/fontawesome-free/css/all.min.css";

function App() {
  return (
    <Router>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/botrytis-detection" element={<BotrytisDetection />} />
          {/* Add more routes here for future functionalities */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
