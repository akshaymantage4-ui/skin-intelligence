import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState(""), [password, setPassword] = useState(""), [message, setMessage] = useState(""), [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  async function login(event) {
    event.preventDefault(); if (!email || !password) return setMessage("Enter your email and password.");
    try { setLoading(true); setMessage(""); const body = new URLSearchParams({ username: email, password }); const response = await fetch("http://127.0.0.1:8000/auth/login", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body }); const data = await response.json(); if (!response.ok) throw new Error(data.detail || "Login failed."); localStorage.setItem("token", data.access_token); localStorage.setItem("role", data.role || "user"); navigate(data.role === "user" ? "/dashboard" : "/role-dashboard"); } catch (error) { setMessage(error.message || "Cannot connect to backend. Start FastAPI on port 8000."); } finally { setLoading(false); }
  }
  return <div className="auth-page"><div className="auth-card"><div className="logo">SI</div><h1>Welcome back</h1><p className="subtitle">Sign in to your Skin Intelligence workspace.</p><form onSubmit={login}><div className="form-group"><label>Email</label><input type="email" value={email} onChange={event => setEmail(event.target.value)} autoComplete="email" required /></div><div className="form-group"><label>Password</label><input type="password" value={password} onChange={event => setPassword(event.target.value)} autoComplete="current-password" required /></div><button className="btn" disabled={loading}>{loading ? "Signing in…" : "Sign in"}</button></form>{message && <p className="message error">{message}</p>}<p className="auth-footer">New user? <Link className="link" to="/register">Create a user account</Link></p></div></div>;
}
