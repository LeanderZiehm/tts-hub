import { NavLink } from "react-router-dom";

export const Tabs = () => (
  <nav style={{ marginBottom: 20 }}>
    <NavLink to="/dashboard" style={{ marginRight: 10 }}>Dashboard</NavLink>
    <NavLink to="/synthesize">Synthesize</NavLink>
  </nav>
);
