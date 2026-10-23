
import { useEffect, useState } from "react";

const API = "/api";

export default function Progress() {
  const [v, setV] = useState({
    log_date: new Date().toISOString().slice(0, 10),
    skin_score: "",
    routine_adherence: "",
    acne_level: "",
    dryness_level: "",
    pigmentation_level: "",
    sensitivity_level: "",
    notes: "",
  });

  const [rows, setRows] = useState([]);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);

  const token = localStorage.getItem("token");

  // GET: Load progress history
  async function load() {
    setLoadingHistory(true);
    setMsg("");

    try {
      if (!token) {
        throw new Error("Please log in to view your progress.");
      }

      const response = await fetch(`${API}/user/progress`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load progress history."
        );
      }

      setRows(Array.isArray(data) ? data : []);
    } catch (error) {
      setMsg(error.message || "Failed to load progress history.");
    } finally {
      setLoadingHistory(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  // Update form fields
  function handleChange(e) {
    const { name, value } = e.target;

    setV((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  // POST: Save a progress entry
  async function save(e) {
    e.preventDefault();
    setLoading(true);
    setMsg("");

    try {
      if (!token) {
        throw new Error("Please log in before saving progress.");
      }

      const payload = {
        ...v,
        skin_score:
          v.skin_score === "" ? null : Number(v.skin_score),
        routine_adherence:
          v.routine_adherence === ""
            ? null
            : Number(v.routine_adherence),
      };

      const response = await fetch(`${API}/user/progress`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not save progress.");
      }

      setMsg("Progress saved successfully! ✅");

      // Reload the latest records from the backend
      await load();

      // Reset the form for the next entry
      setV({
        log_date: new Date().toISOString().slice(0, 10),
        skin_score: "",
        routine_adherence: "",
        acne_level: "",
        dryness_level: "",
        pigmentation_level: "",
        sensitivity_level: "",
        notes: "",
      });
    } catch (error) {
      setMsg(error.message || "Failed to save progress.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Page
      title="Progress Tracking"
      subtitle="Record periodic skin observations and routine adherence."
    >
      <div className="card form-card">
        <h2>Add Progress Entry</h2>

        <form onSubmit={save}>
          <div className="form-group">
            <label htmlFor="log_date">Date</label>
            <input
              id="log_date"
              name="log_date"
              type="date"
              value={v.log_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="skin_score">Skin Score (0–100)</label>
            <input
              id="skin_score"
              name="skin_score"
              type="number"
              min="0"
              max="100"
              value={v.skin_score}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="routine_adherence">
              Routine Adherence (%)
            </label>
            <input
              id="routine_adherence"
              name="routine_adherence"
              type="number"
              min="0"
              max="100"
              value={v.routine_adherence}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <textarea
              id="notes"
              name="notes"
              rows="3"
              value={v.notes}
              onChange={handleChange}
              placeholder="Record any changes you noticed..."
            />
          </div>

          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Saving..." : "Save Progress Entry"}
          </button>
        </form>

        {msg && <p className="message" role="status">{msg}</p>}
      </div>

      <div className="card">
        <h2>Progress History</h2>

        {loadingHistory ? (
          <p>Loading progress history...</p>
        ) : rows.length === 0 ? (
          <p>No progress records found yet.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Skin Score</th>
                  <th>Routine Adherence</th>
                  <th>Notes</th>
                </tr>
              </thead>

              <tbody>
                {rows.map((record) => (
                  <tr key={record.id}>
                    <td>
                      {record.log_date
                        ? String(record.log_date).slice(0, 10)
                        : "—"}
                    </td>
                    <td>{record.skin_score ?? "—"}</td>
                    <td>
                      {record.routine_adherence == null
                        ? "—"
                        : `${record.routine_adherence}%`}
                    </td>
                    <td>{record.notes || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <button
          className="btn"
          type="button"
          onClick={load}
          disabled={loadingHistory}
          style={{ marginTop: "16px" }}
        >
          Refresh History
        </button>
      </div>
    </Page>
  );
}

function Page({ title, subtitle, children }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/dashboard">
          Skin Intelligence
        </a>

        <p className="sidebar-caption">
          Personal skincare planning
        </p>

        <nav>
          <a className="nav-link" href="/dashboard">Overview</a>
          <a className="nav-link" href="/ingredient-intelligence">
            Ingredients
          </a>
          <a className="nav-link" href="/products">Products</a>
          <a className="nav-link" href="/progress">Progress</a>
          <a className="nav-link" href="/analytics">Analytics</a>
        </nav>
      </aside>

      <div className="app-content">
        <main className="workspace">
          <div className="page-heading">
            <p className="eyebrow">Milestone 3</p>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>

          {children}
        </main>
      </div>
    </div>
  );
}
