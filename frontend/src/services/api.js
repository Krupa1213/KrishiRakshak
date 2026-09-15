const API_BASE_URL = "http://192.168.1.109:8000";

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

export async function getFarmRisk(latitude, longitude) {
  const response = await fetch(
    `${API_BASE_URL}/farm/risk?latitude=${latitude}&longitude=${longitude}`
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || "Failed to get farm risk"
    );
  }

  return await response.json();
}

export async function detectDisease(imageFile) {
  const formData = new FormData();
  formData.append("file", imageFile);

  const response = await fetch(`${API_BASE_URL}/disease/predict`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to analyze crop health");
  }

  return data;
}

export async function getCropHistory() {
  const response = await fetch(`${API_BASE_URL}/crop/history`);

  if (!response.ok) {
    throw new Error("Failed to fetch crop history");
  }

  return await response.json();
}

export async function getAdvisory(advisoryData) {
  const response = await fetch(`${API_BASE_URL}/advisory/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(advisoryData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to get advisory");
  }

  return data;
}

export async function getMarketPrice() {
  const response = await fetch(`${API_BASE_URL}/market/price`);

  if (!response.ok) {
    throw new Error("Failed to fetch market price");
  }

  return await response.json();
}