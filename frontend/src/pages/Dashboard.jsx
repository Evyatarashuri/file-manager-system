import { useContext } from "react";
import { UserContext } from "../context/UserContext";
import FileUploader from "../components/FileUploader";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { user, logout } = useContext(UserContext);

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>Dashboard</h1>

      {!user && <p>No user in context</p>}

      {user && (
        <>
          <p>✅ Logged in as: <strong>{user.email}</strong></p>

          <hr style={{ margin: "20px 0" }} />

          <FileUploader user={user} />

          <div style={{ marginTop: "20px" }}>
            <Link to="/files">
              <button
                style={{
                  padding: "10px 20px",
                  backgroundColor: "#1e90ff",
                  color: "white",
                  borderRadius: "6px",
                  border: "none",
                  cursor: "pointer",
                  fontWeight: "bold"
                }}
              >
                📁 View My Files
              </button>
            </Link>
          </div>

          {/* Logout button */}
          <button
            style={{ marginTop: 30, padding: "8px 18px", cursor: "pointer" }}
            onClick={logout}
          >
            Logout
          </button>
        </>
      )}
    </div>
  );
}
