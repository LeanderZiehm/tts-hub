
import { useState } from "react";
import { synthesizeText } from "../api/client";
import "./Synthesize.css";
import "./Synthesize.css";

export const Synthesize = () => {
  const [text, setText] = useState("");
  const [engine, setEngine] = useState("espeak");
  const [apiKey, setApiKey] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [status, setStatus] = useState("");

  const handleSynthesize = async () => {
    if (!apiKey) return setStatus("API Key required");
    if (!text) return setStatus("Text cannot be empty");
    setStatus("Processing...");
    try {
      const res = await synthesizeText(text, engine, apiKey);
      const blob = new Blob([res.data], { type: "audio/wav" });
      setAudioUrl(URL.createObjectURL(blob));
      setStatus("Success");
    } catch (e: any) {
      setStatus("Error: " + e.response?.data?.detail || e.message);
    }
  };

  return (
    <div className="synthesize-container">
      <h2>Synthesize Text</h2>
      <input type="password" placeholder="API Key" value={apiKey} onChange={e => setApiKey(e.target.value)} />
      <textarea placeholder="Enter text" value={text} onChange={e => setText(e.target.value)} />
      <select value={engine} onChange={e => setEngine(e.target.value)}>
        <option value="espeak">ESpeak</option>
        <option value="kokoro">Kokoro</option>
      </select>
      <button onClick={handleSynthesize}>Synthesize</button>
      {status && <div className="status-message">{status}</div>}
      {audioUrl && (
        <audio controls src={audioUrl} className="audio-player"></audio>
      )}
    </div>
  );
};

