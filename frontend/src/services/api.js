const API_BASE_URL = "http://127.0.0.1:8000";

export async function getFarmers() {
  const response = await fetch(`${API_BASE_URL}/farmers/`);

  if (!response.ok) {
    throw new Error("Failed to fetch farmers");
  }

  return response.json();
}