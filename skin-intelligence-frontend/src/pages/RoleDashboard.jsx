import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = "http://127.0.0.1:8000";

const roles = [
  "user",
  "consultant",
  "dermatologist",
  "administrator",
];

const content = {
  consultant: [
    "Consultant Workspace",
    "Client assessment review and recommendation management will be available in Milestone 3.",
  ],
  dermatologist: [
    "Dermatologist Workspace",
    "Patient insights, condition reports, and treatment recommendations will be available in Milestone 3.",
  ],
  administrator: [
    "Administrator Workspace",
    "Manage account roles below. Platform analytics and monitoring are planned for Milestone 4.",
  ],
};

export default function RoleDashboard() {
  const navigate = useNavigate();

  const role = localStorage.getItem("role") || "user";
  const token = localStorage.getItem("token");

  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [title, description] =
    content[role] || [
      "User Workspace",
      "Manage your skin profile, assessment, and routine.",
    ];

  const headers = {
    Authorization: `Bearer ${token}`,
  };

  const loadUsers = async () => {
    try {
      const response = await fetch(`${API}/auth/users`, {
        headers,
      });

      const data = await response.json();

      if (response.ok) {
        setUsers(data);
      } else {
        setMessage(data.detail || "Unable to load accounts.");
      }
    } catch (error) {
      setMessage("Unable to connect to backend.");
    }
  };

  useEffect(() => {
    if (role === "administrator") {
      loadUsers();
    }
  }, [role]);

  async function updateRole(id, nextRole) {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API}/auth/users/${id}/role`,
        {
          method: "PATCH",
          headers: {
            ...headers,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role: nextRole,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update role."
        );
      }

      setUsers(
        users.map((user) =>
          user.id === id
            ? { ...user, role: data.role }
            : user
        )
      );

      setMessage("Role updated successfully.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function signOut() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login");
  }

  return (
    <div className="auth-page">
      <div className="auth-card role-card">

        <div className="logo">SI</div>

        <h1>{title}</h1>

        <p className="subtitle">
          {description}
        </p>

        <p className="message">
          Signed in as: <strong>{role}</strong>
        </p>

        {role === "administrator" && (
          <section className="account-management">

            <h2>Account Roles</h2>

            <p>
              New public registrations are users.
              Promote verified staff accounts here.
            </p>

            {users.map((user) => (
              <div
                className="account-row"
                key={user.id}
              >
                <div>
                  <strong>{user.name}</strong>
                  <span>{user.email}</span>
                </div>

                <select
                  value={user.role}
                  disabled={loading}
                  onChange={(event) =>
                    updateRole(
                      user.id,
                      event.target.value
                    )
                  }
                >
                  {roles.map((value) => (
                    <option
                      key={value}
                      value={value}
                    >
                      {value}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </section>
        )}

        {message && (
          <p className="message">
            {message}
          </p>
        )}

        <button
          className="btn"
          onClick={signOut}
        >
          Sign Out
        </button>

      </div>
    </div>
  );
}