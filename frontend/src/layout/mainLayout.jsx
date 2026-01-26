import { SidebarSection, HomeFeed } from "../components/index";

export const MainLayout = () => {
  return (
    <div className="app-layout">
      <SidebarSection />
      <HomeFeed />
    </div>
  );
};
