import { NavLink, useNavigate } from "react-router-dom";

const links = [["Overview", "/dashboard"], ["Skin profile", "/skin-profile"], ["Lifestyle", "/lifestyle"], ["Environment", "/environment"], ["Sleep", "/sleep"], ["Assessment", "/skin-assessment"], ["My routine", "/routine"]];

export default function AppShell({ title, subtitle, children }) {
  const navigate = useNavigate();
  const signOut = () => { localStorage.removeItem("token"); navigate("/login"); };
  return <div className="app-shell"><aside className="sidebar"><NavLink className="brand" to="/dashboard">Skin Intelligence</NavLink><p className="sidebar-caption">Personal skincare planning</p><nav aria-label="Main navigation">{links.map(([label, path]) => <NavLink key={path} to={path} className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>{label}</NavLink>)}</nav><button className="text-button" onClick={signOut}>Sign out</button></aside><div className="app-content"><header className="mobile-header"><NavLink className="brand" to="/dashboard">Skin Intelligence</NavLink><button className="text-button" onClick={signOut}>Sign out</button></header><main className="workspace"><div className="page-heading"><p className="eyebrow">Your skincare workspace</p><h1>{title}</h1>{subtitle && <p>{subtitle}</p>}</div>{children}</main></div></div>;
}
