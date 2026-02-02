import {
  Bell,
  Bookmark,
  HomeIcon,
  Mail,
  MoreHorizontal,
  Search,
  User,
  PenIcon,
  LogOut,
} from "lucide-react";
import { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useAuth } from "../context/loginContext";
import { TweetForm } from "../pages/index";
import "./css/sidebar.css";

export default function SidebarSection() {
  const [active, setActive] = useState("Home");
  const [showTweetForm, setShowTweetForm] = useState(false);
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Home", icon: HomeIcon, path: "/" },
    { name: "Explore", icon: Search, path: "/" },
    { name: "Notifications", icon: Bell, path: "/" },
    { name: "Chat", icon: Mail, path: "/messages" },
    { name: "Bookmarks", icon: Bookmark, path: "/" },
    { name: "Profile", icon: User, path: "/profile" },
    { name: "More", icon: MoreHorizontal, path: "/" },
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
              {navItems.map((item) => (
                <NavLink key={item.name} to={item.path}>
                  <button
                    className={`nav-item ${
                      active === item.name ? "active" : ""
                    }`}
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
            className="post-button flex justify-center align-middle"
            onClick={() => setShowTweetForm(true)}
          >
            <PenIcon size={24} />
            &nbsp;Post
          </button>
          <button
            className="post-button flex justify-center align-middle"
            onClick={() => logout()}
          >
            <LogOut size={24} />
            &nbsp;logout
          </button>

          {/* Bottom user section (authenticated user) */}
          <div className="user-section">
            <Link to="/profile">
              <div className="user-avatar">
                {/* Replace with real image or placeholder */}
                <img
                  src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=100&h=100&fit=crop"
                  alt="User avatar"
                />
              </div>
              <div className="user-info">
                <div className="username">{user?.username}</div>
              </div>
            </Link>
          </div>
        </div>
      </aside>
      <TweetForm
        isOpen={showTweetForm}
        onClose={() => setShowTweetForm(false)}
      />
    </>
  );
}
