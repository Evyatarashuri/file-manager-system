import { useEffect, useState, useContext } from "react";
import { apiClient } from "../utils/api";
import { auth } from "../utils/firebase";
import { UserContext } from "../context/UserContext";
import AdminFileTable from "../components/AdminFileTable";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {
  const { user, logout } = useContext(UserContext);
  const [files, setFiles] = useState([]);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  // redirect if not admin
  useEffect(() => {
    if (!user?.admin) navigate("/login");
  }, [user]);

  // fetch files
  useEffect(() => {
    if (!user?.admin) return;

    const fetchAdminFiles = async () => {
      const token = await auth.currentUser.getIdToken();
      const res = await apiClient.getAdminFiles(token);
      const data = await res.json();
      setFiles(data);
    };

    fetchAdminFiles();
  }, [user]);


  const filtered = files.filter(f =>
    f.filename.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ padding: 30 }}>

      {/* ====== Logout top-right ====== */}
      <div style={{ display:"flex", justifyContent:"flex-end", marginBottom: 10 }}>
        <button 
          onClick={logout}
          style={{
            background:"#ff5050",
            color:"#fff",
            padding:"8px 15px",
            borderRadius:6,
            fontSize:15,
            cursor:"pointer",
            fontWeight:"bold"
          }}
        >
          Logout ⛔
        </button>
      </div>
      {/* ================================= */}
      

      <h1>🔥 Admin Control Panel</h1>
      <p>Total Files: <b>{files.length}</b></p>

      <input
        placeholder="Search files..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{ margin: "20px 0", padding: 8, width: 300 }}
      />

      <AdminFileTable files={filtered} />
    </div>
  );
}
