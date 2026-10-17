import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import RoleDashboard from "./pages/RoleDashboard";
import SkinProfile from "./pages/SkinProfile";
import Lifestyle from "./pages/Lifestyle";
import Environment from "./pages/Environment";
import SleepTracking from "./pages/SleepTracking";
import SkinAssessment from "./pages/SkinAssessment";
import Routine from "./pages/Routine";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/role-dashboard" element={<RoleDashboard />} />

        <Route path="/skin-profile" element={<SkinProfile />} />
        <Route path="/lifestyle" element={<Lifestyle />} />
        <Route path="/environment" element={<Environment />} />
        <Route path="/sleep" element={<SleepTracking />} />
        <Route path="/skin-assessment" element={<SkinAssessment />} />
        <Route path="/routine" element={<Routine />} />

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
