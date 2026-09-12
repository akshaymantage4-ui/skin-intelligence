import { useEffect, useState } from "react";
import "../index.css";

function SleepTracking() {
  const [sleepDate, setSleepDate] = useState("");
  const [sleepDuration, setSleepDuration] = useState("");
  const [sleepQuality, setSleepQuality] = useState("");

  const [sleepHistory, setSleepHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchSleepHistory();
  }, []);

  const fetchSleepHistory = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login first.");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/user/sleep",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const result = await response.json();

      if (!response.ok) {
        setMessage(
          typeof result.detail === "string"
            ? result.detail
            : "Failed to load sleep history."
        );
        return;
      }

      setSleepHistory(result);
    } catch (error) {
      console.error("GET SLEEP ERROR:", error);
      setMessage("Cannot connect to backend.");
    }
  };

  const saveSleepLog = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login first.");
      return;
    }

    if (!sleepDate || !sleepDuration || !sleepQuality) {
      setMessage("Please fill all sleep details.");
      return;
    }

    const data = {
      sleep_date: sleepDate,
      sleep_duration: Number(sleepDuration),
      sleep_quality: sleepQuality,
    };

    try {
      setLoading(true);
      setMessage("");

      const response = await fetch(
        "http://127.0.0.1:8000/user/sleep",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(data),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        setMessage(
          typeof result.detail === "string"
            ? result.detail
            : "Failed to save sleep log."
        );
        return;
      }

      setMessage("Sleep log saved successfully! ✅");

      setSleepDate("");
      setSleepDuration("");
      setSleepQuality("");

      fetchSleepHistory();

    } catch (error) {
      console.error("SAVE SLEEP ERROR:", error);
      setMessage("Cannot connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">

      <h1>😴 Sleep Tracking</h1>

      <p className="dashboard-subtitle">
        Track your sleep and monitor your sleep history
      </p>

      <div className="card">

        <h2>Daily Sleep Log</h2>

        <form onSubmit={saveSleepLog}>

          <label>Date</label>

          <input
            type="date"
            value={sleepDate}
            onChange={(e) => setSleepDate(e.target.value)}
          />

          <br />
          <br />

          <label>Sleep Duration (hours)</label>

          <input
            type="number"
            step="0.5"
            min="0"
            max="24"
            placeholder="e.g. 8"
            value={sleepDuration}
            onChange={(e) => setSleepDuration(e.target.value)}
          />

          <br />
          <br />

          <label>Sleep Quality</label>

          <select
            value={sleepQuality}
            onChange={(e) => setSleepQuality(e.target.value)}
          >
            <option value="">
              Select sleep quality
            </option>

            <option value="poor">
              Poor
            </option>

            <option value="fair">
              Fair
            </option>

            <option value="good">
              Good
            </option>

            <option value="excellent">
              Excellent
            </option>
          </select>

          <br />
          <br />

          <button
            type="submit"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save Sleep Log"}
          </button>

        </form>

        {message && (
          <p>{message}</p>
        )}

      </div>

      <div className="card">

        <h2>📊 Sleep History</h2>

        {sleepHistory.length === 0 ? (

          <p>No sleep records available yet.</p>

        ) : (

          sleepHistory.map((log) => (

            <div
              key={log.id}
              className="sleep-record"
            >

              <h3>
                📅 {log.sleep_date}
              </h3>

              <p>
                <strong>Sleep Duration:</strong>{" "}
                {log.sleep_duration} hours
              </p>

              <p>
                <strong>Sleep Quality:</strong>{" "}
                {log.sleep_quality}
              </p>

            </div>

          ))

        )}

      </div>

    </div>
  );
}

export default SleepTracking;