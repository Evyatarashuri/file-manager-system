export default function AdminFileTable({ files }) {
  return (
    <table style={{ width:"100%", marginTop:20, borderCollapse:"collapse" }}>
      
      <thead>
        <tr style={{ background:"#222", color:"#fff" }}>
          <th style={cell}>Owner Email</th>
          <th style={cell}>Filename</th>
          <th style={cell}>Type</th>
          <th style={cell}>Size</th>
          <th style={cell}>Created</th>
        </tr>
      </thead>

      <tbody>
        {files.map(file => (
          <tr key={file.file_id} style={{ background:"#111", color:"#ddd" }}>
            <td style={cell}>{file.owner_email}</td>
            <td style={cell}>{file.filename}</td>
            <td style={cell}>{file.content_type}</td>
            <td style={cell}>{Math.round((file.size || 0) / 1024)} KB</td>
            <td style={cell}>{file.uploaded_at?.substring(0,10)}</td>
          </tr>
        ))}
      </tbody>

    </table>
  );
}

const cell = { padding:"8px 14px", borderBottom:"1px solid #333" };
