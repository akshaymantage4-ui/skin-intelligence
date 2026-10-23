
import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const API = "/api";

export default function Analytics() {
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadAnalytics() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          throw new Error("Please log in to view analytics.");
        }

        const response = await fetch(
          `${API}/user/analytics/dashboard`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Could not load analytics."
          );
        }

        if (active) setD(data);
      } catch (error) {
        if (active) {
          setMsg(error.message || "Analytics unavailable.");
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadAnalytics();

    return () => {
      active = false;
    };
  }, []);

  const timeline = (d?.progress_timeline || []).map((item) => ({
    ...item,
    skin_score:
      item.skin_score == null ? null : Number(item.skin_score),
    routine_adherence:
      item.routine_adherence == null
        ? null
        : Number(item.routine_adherence),
  }));

  function downloadCSV() {
    if (!d) return;

    const rows = [
      ["Date", "Skin Score", "Routine Adherence"],
      ...timeline.map((item) => [
        item.date,
        item.skin_score ?? "",
        item.routine_adherence ?? "",
      ]),
    ];

    const csv = rows
      .map((row) =>
        row
          .map((value) => {
            const safe = String(value).replace(/"/g, '""');
            return `"${safe}"`;
          })
          .join(",")
      )
      .join("\r\n");

    const blob = new Blob(["\uFEFF" + csv], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "skin-intelligence-report.csv";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  return (
    <Page
      title="Skincare Analytics"
      subtitle="Track recorded skin scores, routine adherence, and progress."
    >
      {loading && (
        <div className="card">
          <p>Loading your analytics...</p>
        </div>
      )}

      {msg && (
        <div className="card">
          <p className="message error">{msg}</p>
          <button
            className="secondary-btn"
            onClick={() => (window.location.href = "/login")}
          >
            Go to Login
          </button>
        </div>
      )}

      {d && !loading && (
        <>
          <section className="hero-card">
            <div>
              <p className="eyebrow">Personal report</p>
              <h2>Your skincare progress</h2>
              <p>
                Review your saved observations and export your
                progress timeline for further analysis.
              </p>
            </div>

            <button className="btn" onClick={downloadCSV}>
              Export CSV Report
            </button>
          </section>

          <section className="metric-grid">
            <Metric
              title="Latest Skin Score"
              value={d.latest_skin_score ?? "—"}
              description="Latest available recorded score"
            />

            <Metric
              title="Score Change"
              value={
                d.score_change == null
                  ? "—"
                  : `${d.score_change > 0 ? "+" : ""}${d.score_change}`
              }
              description="First to latest available score"
            />

            <Metric
              title="Average Adherence"
              value={
                d.average_routine_adherence == null
                  ? "—"
                  : `${d.average_routine_adherence}%`
              }
              description="Average of recorded adherence values"
            />

            <Metric
              title="Progress Entries"
              value={d.progress_entries ?? 0}
              description="Saved progress observations"
            />
          </section>

          <section className="card">
            <h2>Skin Score Trend</h2>
            <p className="muted">
              Skin scores over the dates recorded in your progress log.
            </p>

            {timeline.some((item) => item.skin_score != null) ? (
              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timeline}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="skin_score"
                      name="Skin Score"
                      stroke="#2e7d52"
                      strokeWidth={3}
                      connectNulls
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p>
                No skin-score timeline is available yet. Save progress
                entries with a skin score to build this chart.
              </p>
            )}
          </section>

          <section className="card">
            <h2>Routine Adherence Trend</h2>
            <p className="muted">
              Recorded routine adherence as a percentage.
            </p>

            {timeline.some(
              (item) => item.routine_adherence != null
            ) ? (
              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timeline}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="routine_adherence"
                      name="Routine Adherence (%)"
                      stroke="#2876b8"
                      strokeWidth={3}
                      connectNulls
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p>
                No adherence records are available yet. Record your
                routine adherence in the Progress module.
              </p>
            )}
          </section>

          <section className="card">
            <h2>Analytics Summary</h2>

            <p>
              <strong>Current trend:</strong>{" "}
              {d.trend ?? "Not available"}
            </p>

            <p>
              <strong>First recorded score:</strong>{" "}
              {d.first_skin_score ?? "—"}
            </p>

            <p>
              <strong>Latest routine adherence:</strong>{" "}
              {d.latest_routine_adherence == null
                ? "—"
                : `${d.latest_routine_adherence}%`}
            </p>

            <p>
              <strong>Recommendation requests:</strong>{" "}
              {d.recommendation_requests ?? 0}
            </p>

            <p>
              <strong>Score-history entries:</strong>{" "}
              {d.score_history_entries ?? 0}
            </p>

            <p className="muted">
              These analytics summarize recorded data and are not
              a medical diagnosis.
            </p>
          </section>

          <section className="card">
            <h2>Progress Timeline</h2>

            {timeline.length > 0 ? (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Skin Score</th>
                      <th>Routine Adherence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {timeline.map((item, index) => (
                      <tr key={`${item.date}-${index}`}>
                        <td>{item.date}</td>
                        <td>{item.skin_score ?? "—"}</td>
                        <td>
                          {item.routine_adherence == null
                            ? "—"
                            : `${item.routine_adherence}%`}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No progress records are available yet.</p>
            )}

            <button
              className="secondary-btn"
              onClick={downloadCSV}
              disabled={timeline.length === 0}
            >
              Download Progress Data
            </button>
          </section>
        </>
      )}
    </Page>
  );
}

function Metric({ title, value, description }) {
  return (
    <article className="metric-card">
      <span>{title}</span>
      <strong>{value}</strong>
      <p>{description}</p>
    </article>
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
            <p className="eyebrow">Milestone 4</p>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>

          {children}
        </main>
      </div>
    </div>
  );
}
