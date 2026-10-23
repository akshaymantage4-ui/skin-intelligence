
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = "/api";

const roles = [
  "user",
  "consultant",
  "dermatologist",
  "administrator",
];

const pages = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Skin Profile", path: "/skin-profile" },
  { label: "Skin Assessment", path: "/skin-assessment" },
  { label: "Lifestyle", path: "/lifestyle" },
  { label: "Environment", path: "/environment" },
  { label: "Sleep Tracking", path: "/sleep" },
  { label: "Skincare Routine", path: "/routine" },
  { label: "Ingredient Intelligence", path: "/ingredient-intelligence" },
  { label: "Products", path: "/products" },
  { label: "Progress Tracking", path: "/progress" },
  { label: "Analytics", path: "/analytics" },
];

const content = {
  consultant: [
    "Consultant Workspace",
    "Review client information and recommendations.",
  ],
  dermatologist: [
    "Dermatologist Workspace",
    "Review skin information and recommendations.",
  ],
  administrator: [
    "Administrator Workspace",
    "Manage accounts and access application features.",
  ],
  admin: [
    "Administrator Workspace",
    "Manage accounts and access application features.",
  ],
  user: [
    "Skin Intelligence Workspace",
    "Manage your skin profile, assessment, lifestyle and routine.",
  ],
};

export default function RoleDashboard() {
  const navigate = useNavigate();

  const role = localStorage.getItem("role") || "user";
  const token = localStorage.getItem("token");

  const isAdmin = ["admin", "administrator"].includes(
    role.toLowerCase()
  );

  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [title, description] =
    content[role.toLowerCase()] || content.user;

  const headers = {
    Authorization: `Bearer ${token}`,
  };

  async function loadUsers() {
    try {
      const response = await fetch(`${API}/auth/users`, {
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to load accounts.");
      }

      setUsers(data);
    } catch (error) {
      setMessage(error.message || "Unable to connect to backend.");
    }
  }

  useEffect(() => {
    if (isAdmin) {
      loadUsers();
    }
  }, [isAdmin]);

  async function updateRole(id, nextRole) {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API}/auth/users/${id}/role`, {
        method: "PATCH",
        headers: {
          ...headers,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ role: nextRole }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to update role.");
      }

      setUsers((previous) =>
        previous.map((user) =>
          user.id === id ? { ...user, role: data.role } : user
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
    navigate("/login", { replace: true });
  }

  return (
    <div className="auth-page">
      <div className="auth-card role-card">
        <div className="logo">SI</div>

        <h1>{title}</h1>
        <p className="subtitle">{description}</p>

        <p className="message">
          Signed in as: <strong>{role}</strong>
        </p>

        <section className="workspace-navigation">
          <h2>Application Menu</h2>
          <p>Select a page to continue.</p>

          <div className="page-grid">
            {pages.map((page) => (
              <button
                key={page.path}
                type="button"
                className="btn"
                onClick={() => navigate(page.path)}
              >
                {page.label}
              </button>
            ))}
          </div>
        </section>

        {isAdmin && (
          <section className="account-management">
            <h2>Account Roles</h2>
            <p>Manage registered account roles.</p>

            {users.map((user) => (
              <div className="account-row" key={user.id}>
                <div>
                  <strong>{user.name}</strong>
                  <span>{user.email}</span>
                </div>

                <select
                  value={user.role}
                  disabled={loading}
                  onChange={(event) =>
                    updateRole(user.id, event.target.value)
                  }
                >
                  {roles.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </section>
        )}

        {message && <p className="message">{message}</p>}

        <button className="btn" type="button" onClick={signOut}>
          Sign Out
        </button>
      </div>
    </div>
  );
}
