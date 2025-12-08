import { useState } from "react";
import { auth } from "../utils/firebase";
import { apiClient } from "../utils/api";
import { v4 as uuidv4 } from "uuid";

export default function FileUploader({ user }) {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");

  const uploadFiles = async () => {
    if (!files.length) return setStatus("Please select at least one file.");

    try {
      setStatus(`Uploading ${files.length} file(s)...`);

      const token = await auth.currentUser.getIdToken();
      const idempotencyKey = uuidv4();

      const res = await apiClient.upload(files, idempotencyKey, token);
      const data = await res.json();

      if (res.ok) {
        setStatus(`Uploaded successfully (${files.length})`);
      } else {
        throw new Error(data.detail || `HTTP Error: ${res.status}`);
      }
    } catch (err) {
      console.error(err);
      setStatus(`Upload Failed: ${err.message}`);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-xl max-w-md mx-auto my-10 border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Upload Files</h2>

      <div className="flex flex-col space-y-4">
        <input
          type="file"
          accept=".txt,.pdf,.json"
          multiple
          className="file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-indigo-50 file:text-indigo-700
            hover:file:bg-indigo-100"
          onChange={(e) => setFiles(Array.from(e.target.files))}
        />

        <button
          onClick={uploadFiles}
          disabled={!files.length}
          className="w-full py-2 px-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-gray-400 transition duration-150"
        >
          {status.includes("Uploading") ? status : "Upload"}
        </button>
      </div>

      <p className="mt-3 text-sm text-gray-600">{status}</p>

      {files.length > 0 && (
        <ul className="text-xs text-gray-500 mt-2">
          {files.map((f) => (
            <li key={f.name}>{f.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
