
import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const API = "http://127.0.0.1:8000";

export default function Analytics() {
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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

        setD(data);
      } catch (error) {
        setMsg(error.message || "Analytics unavailable.");
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);

  return (
    <Page
      title="Skincare Analytics"
      subtitle="Insights from your saved skin scores, progress logs, and recommendation activity."
    >
      {loading && (
        <div className="card">
          <p>Loading your analytics...</p>
        </div>
      )}

      {msg && (
        <div className="card">
          <p className="message error">{msg}</p>
        </div>
      )}

      {d && !loading && (
        <>
          <section className="metric-grid">
            <Metric
              title="Latest Skin Score"
              value={d.latest_skin_score ?? "—"}
            />

            <Metric
              title="Score Change"
              value={
                d.score_change == null
                  ? "—"
                  : `${d.score_change > 0 ? "+" : ""}${d.score_change}`
              }
            />

            <Metric
              title="Average Adherence"
              value={
                d.average_routine_adherence == null
                  ? "—"
                  : `${d.average_routine_adherence}%`
              }
            />

            <Metric
              title="Progress Entries"
              value={d.progress_entries ?? 0}
            />
          </section>

          <div className="card">
            <h2>Skin Score Trend</h2>

            {d.progress_timeline?.length > 0 ? (
              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer>
                  <LineChart data={d.progress_timeline}>
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
                No trend data available yet. Save progress entries
                with skin scores to build your chart.
              </p>
            )}
          </div>

          <div className="card">
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
          </div>

          <div className="card">
            <h2>Progress Timeline</h2>

            {d.progress_timeline?.length > 0 ? (
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
                    {d.progress_timeline.map((item, index) => (
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
              <p>No progress timeline available.</p>
            )}
          </div>
        </>
      )}
    </Page>
  );
}

function Metric({ title, value }) {
  return (
    <article className="metric-card">
      <span>{title}</span>
      <strong>{value}</strong>
      <p>Based on recorded data.</p>
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
          <a className="nav-link" href="/dashboard">
            Overview
          </a>
          <a className="nav-link" href="/ingredient-intelligence">
            Ingredients
          </a>
          <a className="nav-link" href="/products">
            Products
          </a>
          <a className="nav-link" href="/progress">
            Progress
          </a>
          <a className="nav-link" href="/analytics">
            Analytics
          </a>
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
