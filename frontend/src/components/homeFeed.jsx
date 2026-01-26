import { Outlet } from "react-router-dom";
import "./homeFeed.css";
export default function HomeFeed() {
  return (
    <main cladssName="home-feed">
      <Outlet />
    </main>
  );
}
