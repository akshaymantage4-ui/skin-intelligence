import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../components/AppShell";
const API="/api";
export default function Dashboard(){const nav=useNavigate();const[d,setD]=useState({});const[loading,setLoading]=useState(true);const token=localStorage.getItem("token");useEffect(()=>{if(!token){nav("/login");
    return}const get = async (p) => {
  try {
    const response = await fetch(`${API}${p}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();

      console.error(
        "API Error:",
        `${API}${p}`,
        "Status:",
        response.status,
        "Details:",
        errorText
      );

      return null;
    }

    return await response.json();
  } catch (error) {
    console.error("Network Error:", p, error);
    return null;
  }
};
Promise.all([get("/auth/me"),get("/user/skin-score"),get("/user/skin-profile"),get("/user/lifestyle-profile"),get("/user/skin-assessment"),get("/user/skincare-routine"),get("/user/analytics/dashboard")]).then(([user,score,profile,lifestyle,assessment,routine,analytics])=>setD({user,score,profile,lifestyle,assessment,routine,analytics})).finally(()=>setLoading(false))},[token,nav]);if(loading)return <AppShell title="Loading..." subtitle="Preparing your skincare workspace."><div className="card">Loading your saved data...</div></AppShell>;return <AppShell title={`Welcome${d.user?.name?`, ${d.user.name}`:""}`} subtitle="M1–M3 skincare intelligence workspace."><section className="hero-card"><div><p className="eyebrow">Milestone 3</p><h2>Product intelligence & progress tracking</h2><p>Analyze ingredients, receive catalog recommendations, record progress and view analytics.</p></div><button className="btn" onClick={()=>nav("/analytics")}>Open Analytics</button></section><section className="metric-grid"><Metric title="Skin health score" value={d.score?.total_score??"—"} text="M2 score used as the starting point for M3 analytics."/><Metric title="Latest progress" value={d.analytics?.latest_skin_score??"—"} text="Latest user-entered progress score."/><Metric title="Routine adherence" value={d.analytics?.average_routine_adherence==null?"—":`${d.analytics.average_routine_adherence}%`} text="Average recorded adherence."/><Metric title="Progress records" value={d.analytics?.progress_entries??0} text="Saved in PostgreSQL."/></section><div className="section-heading"><div><p className="eyebrow">Milestone 3 modules</p><h2>Product intelligence & progress</h2></div></div><div className="workflow-grid"><Module title="Ingredient Intelligence" text="Analyze functions, reference flags and ingredient interactions." path="/ingredient-intelligence" nav={nav}/><Module title="Product Recommendations" text="Filter products by category, budget, skin type and concerns." path="/products" nav={nav}/><Module title="Progress Tracking" text="Save dated skin observations and routine adherence." path="/progress" nav={nav}/><Module title="Skincare Analytics" text="See score changes, trends and recommendation activity." path="/analytics" nav={nav}/></div>{d.routine&&<section className="card routine-preview"><p className="eyebrow">Today’s plan</p><h2>Morning routine</h2><ol>{(d.routine.morning_routine||"").split("\n").filter(Boolean).slice(0,3).map((x,i)=><li key={i}>{x}</li>)}</ol><button className="secondary-btn" onClick={()=>nav("/routine")}>View full routine</button></section>}</AppShell>}
function Metric({title,value,text}){return <article className="metric-card"><span>{title}</span><strong>{value}</strong><p>{text}</p></article>}
function Module({title,text,path,nav}){return <article className="workflow-card"><span className="step-badge complete">M3</span><h3>{title}</h3><p>{text}</p><button className="secondary-btn" onClick={()=>nav(path)}>Open module</button></article>}
