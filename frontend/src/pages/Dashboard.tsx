
import { useEffect, useState } from "react";
import { api } from "../api/client";
import "./Dashboard.css";
import "./Dashboard.css";

export const Dashboard = () => {
  const [apiKey, setApiKey] = useState(localStorage.getItem("apiKey") || "");
  const [credits, setCredits] = useState<number | null>(null);
  const [showKey, setShowKey] = useState(false);
  const [status, setStatus] = useState("");

  const fetchCredits = async () => {
    if (!apiKey) return setStatus("API key required to fetch credits.");
    setStatus("Fetching credits...");
    try {
      const res = await api.get("/credits", {
        headers: { Authorization: `Bearer ${apiKey}` }
      });
      setCredits(res.data.credits ?? 0);
      setStatus("");
    } catch (e: any) {
      setStatus("Error fetching credits: " + (e.response?.data?.detail || e.message));
    }
  };

  useEffect(() => {
    if (apiKey) fetchCredits();
  }, [apiKey]);

  return (
    <div className="dashboard-container">
      <h2>Dashboard</h2>

      <div className="dashboard-section api-key-section">
        <strong>API Key:</strong>
        {showKey ? apiKey : apiKey ? apiKey.slice(0, 4) + "..." + apiKey.slice(-4) : "Not set"}
        <button onClick={() => setShowKey(prev => !prev)}>
          {showKey ? "Hide" : "Show"}
        </button>
      </div>

      <div className="dashboard-section credits-section">
        <strong>Credits:</strong> {credits !== null ? credits : "Loading..."}
        <button onClick={fetchCredits}>
          Refresh
        </button>
      </div>

      <div>
        <a href="/synthesize">Go to Synthesize Page</a>
      </div>

      {status && <div className="status-message">{status}</div>}
    </div>
  );
};

