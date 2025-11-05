
import { NavLink } from "react-router-dom";
import "./Tabs.css";
import "./Tabs.css";

export const Tabs = () => (
  <nav className="tabs-nav">
    <NavLink to="/dashboard">Dashboard</NavLink>
    <NavLink to="/synthesize">Synthesize</NavLink>
  </nav>
);

