import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function IngredientIntelligence() {
  const [text, setText] = useState("Niacinamide, Hyaluronic Acid, Retinol");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function analyze(mode) {
    const token = localStorage.getItem("token");
    const ingredients = text.split(",").map(x => x.trim()).filter(Boolean);
    if (!ingredients.length) return setMessage("Enter at least one ingredient.");
    setLoading(true); setMessage("");
    try {
      const response = await fetch(`${API}/user/ingredients/${mode}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ ingredients }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Ingredient analysis failed.");
      setResult(data);
    } catch (error) { setMessage(error.message); }
    finally { setLoading(false); }
  }

  return <AppPage title="Ingredient Intelligence" subtitle="Analyze ingredient functions, reference flags and routine interactions.">
    <div className="card form-card">
      <label>Ingredients (comma separated)</label>
      <textarea rows="4" value={text} onChange={e => setText(e.target.value)} />
      <div className="button-row">
        <button className="btn" disabled={loading} onClick={() => analyze("analyze")}>{loading ? "Analyzing..." : "Analyze Ingredients"}</button>
        <button className="secondary-btn" disabled={loading} onClick={() => analyze("suitability")}>Check With My Skin Profile</button>
      </div>
      {message && <p className="message error">{message}</p>}
    </div>
    {result && <div className="card">
      <h2>Analysis Results</h2>
      <p className="message">{result.notice}</p>
      {result.ingredients?.map(item => <article className="result-item" key={item.display_name}>
        <div><h3>{item.display_name}</h3><p>{item.function}</p></div>
        <div className="flag-grid">
          {Object.entries(item.reference_flags || {}).map(([key, value]) => <span className={`flag ${value ? "flag-on" : ""}`} key={key}>{key.replaceAll("_", " ")}: {value ? "Yes" : "No"}</span>)}
        </div>
        {item.reference_notes?.length > 0 && <ul>{item.reference_notes.map(note => <li key={note}>{note}</li>)}</ul>}
      </article>)}
      {result.not_found?.length > 0 && <p className="message error">Not found: {result.not_found.join(", ")}</p>}
      {result.interactions?.length > 0 && <><h3>Routine interaction notes</h3>{result.interactions.map(x => <div className="routine-item" key={x.message}>{x.ingredients.join(" + ")}: {x.message}</div>)}</>}
    </div>}
  </AppPage>;
}

function AppPage({ title, subtitle, children }) {
  return <div className="app-shell"><aside className="sidebar"><a className="brand" href="/dashboard">Skin Intelligence</a><p className="sidebar-caption">Personal skincare planning</p><nav><a className="nav-link" href="/dashboard">Overview</a><a className="nav-link" href="/ingredient-intelligence">Ingredients</a><a className="nav-link" href="/products">Products</a><a className="nav-link" href="/progress">Progress</a><a className="nav-link" href="/analytics">Analytics</a></nav></aside><div className="app-content"><main className="workspace"><div className="page-heading"><p className="eyebrow">Milestone 3</p><h1>{title}</h1><p>{subtitle}</p></div>{children}</main></div></div>;
}
