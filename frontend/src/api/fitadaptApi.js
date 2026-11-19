// fitadaptApi.js — API client for FitAdapt ML backend

const BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Submit health profile for ML analysis
 * POST /api/predict
 */
export const analyzeHealth = async (data) => {
  const res = await fetch(`${BASE_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }
  return res.json();
};

/**
 * Fetch all workout templates
 * GET /api/workout-templates
 */
export const getTemplates = async () => {
  const res = await fetch(`${BASE_URL}/api/workout-templates`);
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
};

/**
 * Check backend health
 * GET /api/health
 */
export const checkHealth = async () => {
  const res = await fetch(`${BASE_URL}/api/health`);
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
};
