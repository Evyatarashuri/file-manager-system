import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "./context/UserContext";

import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import FilesPage from "./pages/FilesPage";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  const { user } = useContext(UserContext);

  const RequireAuth = ({ children }) =>
    user ? children : <Navigate to="/login" replace />;

  const RequireAdmin = ({ children }) =>
    user?.admin ? children : <Navigate to="/login" replace />;

  return (
    <Router>
      <Routes>

        {/* LOGIN */}
        <Route path="/login" element={<LoginPage />} />

        {/* ROOT — Regular user is redirected to Dashboard (upload) */}
        <Route
          path="/"
          element={
            user
              ? (user.admin ? <Navigate to="/admin" /> : <Dashboard />)
              : <Navigate to="/login" />
          }
        />

        {/* upload page Dashboard */}
        <Route
          path="/upload"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />

        {/* Regular Files Page */}
        <Route
          path="/files"
          element={
            <RequireAuth>
              <FilesPage />
            </RequireAuth>
          }
        />

        {/* Admin Dashboard */}
        <Route
          path="/admin"
          element={
            <RequireAdmin>
              <AdminDashboard />
            </RequireAdmin>
          }
        />

        {/* 404 */}
        <Route path="*" element={<h1>404 Page Not Found</h1>} />

      </Routes>
    </Router>
  );
}
