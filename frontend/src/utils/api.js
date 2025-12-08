const BASE_URL = import.meta.env.VITE_API_URL;

export const apiClient = {

  getFiles: (token, params = {}) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== "")
    );
    const query = new URLSearchParams(clean).toString();

    return fetch(`${BASE_URL}/files/${query ? `?${query}` : ""}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  },

  upload: (files, key, token) => {
    const formData = new FormData();
    files.forEach(f => formData.append("files", f));

    return fetch(`${BASE_URL}/files/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Idempotency-Key": key },
      body: formData
    });
  },

  getDownloadUrl: (id, token) =>
    fetch(`${BASE_URL}/files/download/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    }),

  deleteFile: (id, token) =>
    fetch(`${BASE_URL}/files/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    }),

  getAdminFiles: (token) =>
    fetch(`${BASE_URL}/admin/all`, {
      headers: { Authorization: `Bearer ${token}` }
    }),

  searchInsideFiles: (token, query) =>
    fetch(`${BASE_URL}/search/?q=${encodeURIComponent(query)}`, {
      headers: { Authorization: `Bearer ${token}` }
    }),

};
