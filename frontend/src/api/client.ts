import axios from "axios";

const BASE_URL = "http://localhost:8000"; // Marked for backend dev to create endpoints

export const api = axios.create({
  baseURL: BASE_URL,
});

export const createUser = async (adminSecret: string) => {
  // TODO: backend endpoint might not exist yet
  return api.post("/admin/create_user", null, {
    params: { admin_secret: adminSecret }
  });
};

export const synthesizeText = async (text: string, engine: string, apiKey: string) => {
  return api.post("/synthesize", null, {
    params: { text, engine },
    headers: { Authorization: `Bearer ${apiKey}` }
  });
};
