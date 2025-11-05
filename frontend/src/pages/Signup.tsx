import { useState } from "react";
import { createUser } from "../api/client";

export const Signup = () => {
  const [adminSecret, setAdminSecret] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [credits, setCredits] = useState<number | null>(null);
  const [status, setStatus] = useState("");

  const handleSignup = async () => {
    setStatus("Creating user...");
    try {
      const res = await createUser(adminSecret);
      setApiKey(res.data.api_key);
      setCredits(res.data.credits);
      setStatus("User created successfully!");
    } catch (e: any) {
      setStatus("Error: " + e.response?.data?.detail || e.message);
    }
  };

  return (
    <div>
      <h2>Create API User</h2>
      <input
        type="text"
        placeholder="Admin Secret"
        value={adminSecret}
        onChange={e => setAdminSecret(e.target.value)}
      />
      <button onClick={handleSignup}>Create User</button>
      <div>{status}</div>
      {apiKey && <div>API Key: {apiKey}</div>}
      {credits !== null && <div>Credits: {credits}</div>}
    </div>
  );
};
