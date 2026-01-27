import "./App.css";
import { SidebarSection } from "./components/index";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <>
      <div className="app-layout">
        <div className="box-1">
          <SidebarSection />
        </div>
        <div className="box-2">
          <Outlet />
        </div>
      </div>
    </>
  );
}

export default App;
