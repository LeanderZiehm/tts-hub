import { useEffect, useState } from "react";
import { api } from "../api/client";

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
      // Assume backend returns { credits: number }
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
    <div>
      <h2>Dashboard</h2>

      <div style={{ marginBottom: 20 }}>
        <strong>API Key:</strong>{" "}
        {showKey ? apiKey : apiKey ? apiKey.slice(0, 4) + "..." + apiKey.slice(-4) : "Not set"}
        <button
          style={{ marginLeft: 10 }}
          onClick={() => setShowKey(prev => !prev)}
        >
          {showKey ? "Hide" : "Show"}
        </button>
      </div>

      <div style={{ marginBottom: 20 }}>
        <strong>Credits:</strong> {credits !== null ? credits : "Loading..."}
        <button style={{ marginLeft: 10 }} onClick={fetchCredits}>
          Refresh
        </button>
      </div>

      <div>
        <a href="/synthesize">Go to Synthesize Page</a>
      </div>

      {status && <div style={{ marginTop: 20, color: "red" }}>{status}</div>}
    </div>
  );
};
