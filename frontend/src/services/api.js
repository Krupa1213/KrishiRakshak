const API_BASE_URL = "http://127.0.0.1:8000";

export async function getFarmers() {
  const response = await fetch(`${API_BASE_URL}/farmers/`);

  if (!response.ok) {
    throw new Error("Failed to fetch farmers");
  }

  return response.json();
}

export async function recommendCrop(cropData) {
  const response = await fetch(`${API_BASE_URL}/crop/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cropData),
  });

  if (!response.ok) {
    throw new Error("Failed to get crop recommendation");
  }

  return await response.json();
}
