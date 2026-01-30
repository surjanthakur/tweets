import {
  Bell,
  Bookmark,
  Home,
  Mail,
  MoreHorizontal,
  Search,
  User,
} from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/loginContext";
import { TweetForm } from "../pages/index";
import "./css/sidebar.css";

export default function SidebarSection() {
  const [active, setActive] = useState("Home");
  const [showTweetForm, setShowTweetForm] = useState(false);
  const {user} = useAuth()

  const navItems = [
    { name: "Explore", icon: Search, path: "/explore" },
    { name: "Notifications", icon: Bell, path: "/notifications" },
    { name: "Chat", icon: Mail, path: "/messages" },
    { name: "Bookmarks", icon: Bookmark, path: "/bookmarks" },
    { name: "Profile", icon: User, path: "/profile" },
    { name: "More", icon: MoreHorizontal, path: "#" },
  ];

  return (
    <>
      <aside className="sidebar">
        <div className="sidebar-container">
          {/* Logo / X mark */}
          <div className="logo-wrapper">
            <div className="x-logo">X</div>
          </div>

          {/* Navigation */}
          <nav className="sidebar-nav">
            <ul>
              {/* get all tweets if press the home button */}
              <button
                className={`nav-item ${active === "Home" ? "active" : ""}`}
              >
                <Home size={28} strokeWidth={2} />
                <span className="nav-text">Home</span>
              </button>
              {navItems.map((item) => (
                <NavLink key={item.name} to={item.path}>
                  <button
                    className={`nav-item ${active === item.name ? "active" : ""}`}
                    onClick={() => setActive(item.name)}
                  >
                    <item.icon size={28} strokeWidth={2} />
                    <span className="nav-text">{item.name}</span>
                  </button>
                </NavLink>
              ))}
            </ul>
          </nav>

          {/* create new tweet if press the post pop up tweetform */}
          <button
            className="post-button"
            onClick={() => setShowTweetForm(true)}
          >
            Post
          </button>

          {/* Bottom user section (authenticated user) */}
          <div className="user-section">
            <div className="user-avatar">
              {/* Replace with real image or placeholder */}
              <img
                src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=100&h=100&fit=crop"
                alt="User avatar"
              />
            </div>
            <div className="user-info">
              <div className="display-name">{user?.username}</div>
              <div className="username">{user?.email}</div>
            </div>
            <button className="more-btn">⋯</button>
          </div>
        </div>
      </aside>
      <TweetForm
        isOpen={showTweetForm}
        onClose={() => setShowTweetForm(false)}
        onPost={(data) => {
          console.log("new post", data);
        }}
      />
    </>
  );
}
