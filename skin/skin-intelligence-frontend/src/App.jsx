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
import IngredientIntelligence from "./pages/IngredientIntelligence";
import Products from "./pages/Products";
import Progress from "./pages/Progress";
import Analytics from "./pages/Analytics";

function Protected({ children }) {
  return localStorage.getItem("token") ? children : <Navigate to="/login" replace />;
}

export default function App(){return <BrowserRouter><Routes>
  <Route path="/" element={<Navigate to="/login" replace/>}/>
  <Route path="/login" element={<Login/>}/><Route path="/register" element={<Register/>}/>
  <Route path="/dashboard" element={<Protected><Dashboard/></Protected>}/>
  <Route path="/role-dashboard" element={<Protected><RoleDashboard/></Protected>}/>
  <Route path="/skin-profile" element={<Protected><SkinProfile/></Protected>}/>
  <Route path="/lifestyle" element={<Protected><Lifestyle/></Protected>}/>
  <Route path="/environment" element={<Protected><Environment/></Protected>}/>
  <Route path="/sleep" element={<Protected><SleepTracking/></Protected>}/>
  <Route path="/skin-assessment" element={<Protected><SkinAssessment/></Protected>}/>
  <Route path="/routine" element={<Protected><Routine/></Protected>}/>
  <Route path="/ingredient-intelligence" element={<Protected><IngredientIntelligence/></Protected>}/>
  <Route path="/products" element={<Protected><Products/></Protected>}/>
  <Route path="/progress" element={<Protected><Progress/></Protected>}/>
  <Route path="/analytics" element={<Protected><Analytics/></Protected>}/>
  <Route path="*" element={<Navigate to="/login" replace/>}/>
</Routes></BrowserRouter>}
