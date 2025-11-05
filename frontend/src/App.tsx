import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Tabs } from "./components/Tabs";
import { Signup } from "./pages/Signup";
import { Dashboard } from "./pages/Dashboard";
import { Synthesize } from "./pages/Synthesize";

function App() {
  return (
    <Router>
      <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "Arial, sans-serif" }}>
        <h1>MindSnap TTS Client</h1>
        <Tabs />
        <Routes>
          <Route path="/" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/synthesize" element={<Synthesize />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
