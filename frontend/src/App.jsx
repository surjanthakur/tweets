import "./App.css";
import { SidebarSection, HomeFeed } from "./components/index";

function App() {
  return (
    <>
      <div className="app-layout">
        <div className="box-1">
          <SidebarSection />
        </div>
        <div className="box-2">
          <HomeFeed />
        </div>
      </div>
    </>
  );
}

export default App;
