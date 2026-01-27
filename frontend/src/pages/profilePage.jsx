// src/components/Profile.jsx
import { ArrowLeft, MapPin, CalendarDays } from "lucide-react";
import { Link } from "react-router-dom";
import "./profile.css";

export default function ProfilePage() {
  const [editFormOpen, setEditFormOpen] = useState(false);
  // In real app these would come from auth context / API
  const user = {
    displayName: "epicSurjan",
    username: "@tsurjan16",
    bio: "20 programmer, build scalable backend and design production grade features.",
    location: "Ludhiana, Punjab, IN",
    joined: "July 2024",
    followers: 169,
    following: 307,
    postCount: 162,
    avatarUrl:
      "https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=200", // placeholder
    bannerUrl:
      "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200", // dark spiderman-like city
  };

  return (
    <div className="profile-page">
      {/* Header / Top bar */}
      <header className="profile-header">
        <button className="back-btn" aria-label="Go back">
          <Link to="/">
            <ArrowLeft size={20} />
          </Link>
        </button>
        <div className="header-info">
          <h1>{user.displayName}</h1>
          <p>{user.postCount} posts</p>
        </div>
      </header>

      {/* Banner + avatar + edit section */}
      <div className="profile-top">
        <div className="banner">
          <img
            src={user.bannerUrl}
            alt="Profile banner"
            className="banner-img"
          />
        </div>

        <div className="profile-info-container">
          <div className="avatar-wrapper">
            <img
              src={user.avatarUrl}
              alt={user.displayName}
              className="profile-avatar"
            />
          </div>

          <div className="action-row">
            <Link to="/profile/editForm">
              <button
                onClick={() => setEditFormOpen(true)}
                className="edit-profile-btn"
              >
                Edit profile
              </button>
            </Link>
          </div>

          <div className="profile-meta">
            <h2 className="display-name">{user.displayName}</h2>
            <p className="username">{user.username}</p>

            <p className="bio">{user.bio}</p>

            <div className="extra-info">
              {user.location && (
                <span className="location">
                  <MapPin size={16} /> {user.location}
                </span>
              )}
              <span className="joined">
                <CalendarDays size={16} /> Joined {user.joined}
              </span>
            </div>

            <div className="follow-stats">
              <button className="stat-btn">
                <span className="count">{user.following}</span> Following
              </button>
              <button className="stat-btn">
                <span className="count">{user.followers}</span> Followers
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs (for now only Posts) */}
      <nav className="profile-tabs">
        <button className="tab active">Posts</button>
        <button className="tab">Replies</button>
        <button className="tab">Highlights</button>
        <button className="tab">Articles</button>
        <button className="tab">Media</button>
        <button className="tab">Likes</button>
      </nav>
      {/* 
      Posts feed
      <div className="posts-list">
        {posts.map((post) => (
          <article key={post.id} className="tweet-card">
            <div className="tweet-header">
              <img src={user.avatarUrl} alt="" className="mini-avatar" />
              <div className="tweet-user">
                <span className="display-name">{user.displayName}</span>
                <span className="username">{user.username}</span>
                <span className="tweet-time">· {post.time}</span>
              </div>
            </div>

            <div className="tweet-content">{post.content}</div>
          </article>
        ))}
      </div> */}
    </div>
  );
}
