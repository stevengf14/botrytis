import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import BotrytisHome from "./components/BotrytisDetection/BotrytisHome";
import BotrytisDetection from "./components/BotrytisDetection/BotrytisDetection";
import BotrytisInformation from "./components/BotrytisDetection/BotrytisInformation";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { LanguageProvider } from "./services/hooks/LanguageContext";

function App() {
  return (
    <LanguageProvider>
      <Router>
        <Header />
        <div className="container">
          <Routes>
            <Route path="/" element={<BotrytisHome />} />
            <Route path="/information" element={<BotrytisInformation />} />
            <Route path="/botrytis-detection" element={<BotrytisDetection />} />
          </Routes>
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
