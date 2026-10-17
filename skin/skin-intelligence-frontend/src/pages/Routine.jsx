import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = "http://127.0.0.1:8000";
const Section = ({ title, value }) => <section className="routine-item"><h2>{title}</h2><ol>{(value || "").split("\n").filter(Boolean).map((step, i) => <li key={i}>{step}</li>)}</ol></section>;

export default function Routine() {
  const navigate = useNavigate(), token = localStorage.getItem("token"), auth = { Authorization: `Bearer ${token}` };
  const [routine, setRoutine] = useState(null), [message, setMessage] = useState(""), [error, setError] = useState(""), [loading, setLoading] = useState(false);
  useEffect(() => { fetch(`${API}/user/skincare-routine`, { headers: auth }).then(async r => ({ r, data: await r.json() })).then(({ r, data }) => { if (r.ok) setRoutine(data); else if (r.status !== 404) setError(data.detail || "Unable to load routine."); }).catch(() => setError("Unable to connect to backend.")); }, [token]);
  async function generate() { setLoading(true); setMessage(""); setError(""); try { const r = await fetch(`${API}/user/skincare-routine`, { method: "POST", headers: auth }); const data = await r.json(); if (!r.ok) throw new Error(data.detail || "Unable to generate routine."); setRoutine(data); setMessage("Your personalized routine is ready."); } catch (err) { setError(err.message); } finally { setLoading(false); } }
  return <div className="page"><header className="topbar"><div className="brand">Skin Intelligence</div><button className="small-btn" onClick={() => navigate("/dashboard")}>Dashboard</button></header><main className="dashboard"><h1>Personalized Routine</h1><p className="dashboard-subtitle">Based on your assessment, lifestyle, and sleep information.</p><button className="btn" onClick={generate} disabled={loading}>{loading ? "Generating..." : routine ? "Refresh Routine" : "Generate Routine"}</button>{message && <p className="message">{message}</p>}{error && <p className="message error">{error}</p>}{routine && <div className="card" style={{ marginTop: 20 }}><Section title="Morning Routine" value={routine.morning_routine} /><Section title="Evening Routine" value={routine.evening_routine} /><Section title="Weekly Plan" value={routine.weekly_routine} /><Section title="Recommendations" value={routine.recommendations} /></div>}</main></div>;
}
