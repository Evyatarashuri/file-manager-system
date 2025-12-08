import { useState, useEffect, useContext } from "react";
import { apiClient } from "../utils/api";
import { auth } from "../utils/firebase";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function FilesPage() {
  const [files, setFiles] = useState([]);
  const [search, setSearch] = useState("");
  const [deepSearch, setDeepSearch] = useState("");
  const [results, setResults] = useState([]);
  const [sort, setSort] = useState(localStorage.getItem("files_sort") || "");
  const [fileType, setFileType] = useState("");
  const navigate = useNavigate(); 
  const { user } = useContext(UserContext);


  /** === LOAD FILE LIST === */
  const fetchFiles = async () => {
    const token = await auth.currentUser.getIdToken();

    const res = await apiClient.getFiles(token, {
      sort_by: sort || undefined,
      file_type: fileType || undefined,
      search: search || undefined
    });

    const data = await res.json();
    setFiles(data);
  };

  useEffect(() => { fetchFiles(); }, [search, sort, fileType]);
  useEffect(() => { localStorage.setItem("files_sort", sort); }, [sort]);


  /** === SEARCH INSIDE FILES === */
  const searchInsideFiles = async () => {
    if (!deepSearch.trim()) return;
    const token = await auth.currentUser.getIdToken();
    const res = await apiClient.searchInsideFiles(token, deepSearch);
    const data = await res.json();
    setResults(data.results || []);
  };


  /** ⬇ Download */
  const downloadFile = async (id) => {
    const token = await auth.currentUser.getIdToken();
    const res = await apiClient.getDownloadUrl(id, token);
    const data = await res.json();
    if (data.url) window.open(data.url, "_blank");
  };

  /** Delete */
  const deleteFile = async (id) => {
    const token = await auth.currentUser.getIdToken();
    await apiClient.deleteFile(id, token);
    fetchFiles();
  };


  return (
    <div style={{ padding: 20 }}>

      {/* Back to dashboard */}
      <button
        onClick={() => navigate("/upload")}
        style={{
          float:"right",
          background:"#4b8df7",
          border:"none",
          color:"#fff",
          padding:"8px 14px",
          borderRadius:"6px",
          cursor:"pointer",
          fontSize:"14px"
        }}
      >
        ⬅ Back to Dashboard
      </button>
      
      <h2>📁 Your Files</h2>

      {/* Standard search */}
      <input
        placeholder="Search file name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginRight: 10 }}
      />

      {/* Filter */}
      <select value={fileType} onChange={(e) => setFileType(e.target.value)} style={{ marginRight: 10 }}>
        <option value="">All Types</option>
        <option value="application/pdf">PDF</option>
        <option value="text/plain">TXT</option>
        <option value="application/json">JSON</option>
      </select>

      {/* Sort */}
      <select value={sort} onChange={(e) => setSort(e.target.value)}>
        <option value="">No Sort</option>
        <option value="date">Date</option>
        <option value="size">Size</option>
      </select>

      <hr/>

      {/* ============================= */}
      {/* 🔥 New: Deep Content Search   */}
      {/* ============================= */}
      <h3>🔎 Search inside files</h3>

      <input
        placeholder="Search words inside PDF/TXT/JSON..."
        value={deepSearch}
        onChange={(e)=>setDeepSearch(e.target.value)}
        style={{width:260, padding:8}}
      />
      <button onClick={searchInsideFiles} style={{marginLeft:10}}>
        Search 🔥
      </button>

      {/* Show deep search results if exist */}
      {results.length > 0 && (
        <div style={{marginTop:20}}>
          <h3>Results ({results.length})</h3>

          {results.map(r => (
            <div key={r.file_id} style={{marginBottom:14}}>
              <strong>{r.filename}</strong>  
              <p style={{fontSize:13, opacity:0.75}}>{r.snippet || "(No preview)"}</p>
            </div>
          ))}
        </div>
      )}

      {/* If no deep search → show normal list */}
      {results.length === 0 && files.map(f => (
        <div key={f.file_id} style={{ marginBottom: 14 }}>
          <strong>{f.filename}</strong> — {Math.round(f.size / 1024)} KB
          <span style={{ marginLeft: 10, opacity: 0.65 }}>
            📅 {f.uploaded_at ? new Date(f.uploaded_at).toLocaleString() : "Unknown"}
          </span>

          <button onClick={() => downloadFile(f.file_id)} style={{ marginLeft: 10 }}>⬇ Download</button>
          <button onClick={() => deleteFile(f.file_id)} style={{ marginLeft: 10 }}>🗑 Delete</button>
        </div>
      ))}

    </div>
  );
}
