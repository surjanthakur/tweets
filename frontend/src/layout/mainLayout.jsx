import { SidebarSection, HomeFeed } from "../components/index";
import "./layout.css";
export default function MainLayout() {
  return (
    <div className="app-layout">
      <SidebarSection />
      <HomeFeed />
    </div>
  );
}
