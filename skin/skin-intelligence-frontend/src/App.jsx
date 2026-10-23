
import { lazy, Suspense } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const RoleDashboard = lazy(() => import("./pages/RoleDashboard"));
const SkinProfile = lazy(() => import("./pages/SkinProfile"));
const Lifestyle = lazy(() => import("./pages/Lifestyle"));
const Environment = lazy(() => import("./pages/Environment"));
const SleepTracking = lazy(() => import("./pages/SleepTracking"));
const SkinAssessment = lazy(() => import("./pages/SkinAssessment"));
const Routine = lazy(() => import("./pages/Routine"));
const IngredientIntelligence = lazy(
  () => import("./pages/IngredientIntelligence")
);
const Products = lazy(() => import("./pages/Products"));
const Progress = lazy(() => import("./pages/Progress"));
const Analytics = lazy(() => import("./pages/Analytics"));

function Protected({ children }) {
  return localStorage.getItem("token")
    ? children
    : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Suspense
        fallback={
          <div className="card" style={{ margin: "2rem" }}>
            Loading page...
          </div>
        }
      >
        <Routes>
          <Route
            path="/"
            element={<Navigate to="/login" replace />}
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/dashboard"
            element={<Protected><Dashboard /></Protected>}
          />
          <Route
            path="/role-dashboard"
            element={<Protected><RoleDashboard /></Protected>}
          />
          <Route
            path="/skin-profile"
            element={<Protected><SkinProfile /></Protected>}
          />
          <Route
            path="/lifestyle"
            element={<Protected><Lifestyle /></Protected>}
          />
          <Route
            path="/environment"
            element={<Protected><Environment /></Protected>}
          />
          <Route
            path="/sleep"
            element={<Protected><SleepTracking /></Protected>}
          />
          <Route
            path="/skin-assessment"
            element={<Protected><SkinAssessment /></Protected>}
          />
          <Route
            path="/routine"
            element={<Protected><Routine /></Protected>}
          />
          <Route
            path="/ingredient-intelligence"
            element={<Protected><IngredientIntelligence /></Protected>}
          />
          <Route
            path="/products"
            element={<Protected><Products /></Protected>}
          />
          <Route
            path="/progress"
            element={<Protected><Progress /></Protected>}
          />
          <Route
            path="/analytics"
            element={<Protected><Analytics /></Protected>}
          />

          <Route
            path="*"
            element={<Navigate to="/login" replace />}
          />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
