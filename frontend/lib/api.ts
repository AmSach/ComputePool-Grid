const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://e65440d9-cfb0-47fa-b11a-d2070bf13013.up.railway.app";

const getStatus = async () => {
  const r = await fetch(`${API_BASE}/status`);
  return r.json();
};

const getNodes = async () => {
  const r = await fetch(`${API_BASE}/nodes`);
  return r.json();
};

const getJobs = async (params?: string) => {
  const r = await fetch(`${API_BASE}/jobs${params ? `?${params}` : ""}`);
  return r.json();
};

const getCredits = async (userId: string) => {
  const r = await fetch(`${API_BASE}/credits/${userId}`);
  return r.json();
};

const register = async (userId: string, name: string, region: string) => {
  const r = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, name, region }),
  });
  return r.json();
};

const registerNode = async (payload: any) => {
  const r = await fetch(`${API_BASE}/nodes/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return r.json();
};

const submitJob = async (payload: any) => {
  const r = await fetch(`${API_BASE}/jobs/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return r.json();
};

const getLeaderboard = async () => {
  const r = await fetch(`${API_BASE}/credits/leaderboard`);
  return r.json();
};

export { getStatus, getNodes, getJobs, getCredits, register, registerNode, submitJob, getLeaderboard };