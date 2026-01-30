// src/components/Profile.jsx
import { ArrowLeft, CalendarDays, MapPin } from "lucide-react";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./css/profilePage.css";
import { ProfileEditForm } from "./index";
import { useAuth } from "../context/loginContext";

const DEFAULT_AVATAR = "https://api.dicebear.com/7.x/avataaars/svg?seed=profile";
const DEFAULT_BANNER = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800";

function formatDate(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  return d.toLocaleDateString("en-IN", { month: "long", year: "numeric" });
}

function formatTweetTime(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  const now = new Date();
  const diffMs = now - d;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffMins < 60) return `${diffMins}m`;
  if (diffHours < 24) return `${diffHours}h`;
  if (diffDays < 7) return `${diffDays}d`;
  return d.toLocaleDateString();
}

export default function ProfilePage() {
  const [editFormOpen, setEditFormOpen] = useState(false);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user: authUser, token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) return;
    const fetchProfile = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/profile/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProfile(res.data);
      } catch (err) {
        if (err.response?.status === 404) {
          navigate("/create-profile", { replace: true });
          return;
        }
        console.error("Failed to fetch profile:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [token, navigate]);

  if (loading) {
    return (
      <div className="profile-page">
        <div className="profile-loading">Loading profile...</div>
      </div>
    );
  }

  if (!profile) {
    return null;
  }

  const tweets = profile.tweets ?? [];
  const username = authUser?.username ?? "";

  return (
    <>
      <div className="profile-page">
        <header className="profile-header">
          <button className="back-btn" aria-label="Go back">
            <Link to="/">
              <ArrowLeft size={20} />
            </Link>
          </button>
          <div className="header-info">
            <h1>{profile.name}</h1>
            <p>{tweets.length} posts</p>
          </div>
        </header>

        <div className="profile-top">
          <div className="banner">
            <img
              src={DEFAULT_BANNER}
              alt="Profile banner"
              className="banner-img"
            />
          </div>

          <div className="profile-info-container">
            <div className="avatar-wrapper">
              <img
                src={DEFAULT_AVATAR}
                alt={profile.name}
                className="profile-avatar"
              />
            </div>

            <div className="action-row">
              <button
                onClick={() => setEditFormOpen(true)}
                className="edit-profile-btn"
              >
                Edit profile
              </button>
            </div>

            <div className="profile-meta">
              <h2 className="display-name">{profile.name}</h2>
              <p className="username">{username}</p>
              <p className="bio">{profile.bio}</p>

              <div className="extra-info">
                {profile.location && (
                  <span className="location">
                    <MapPin size={16} /> {profile.location}
                  </span>
                )}
                <span className="joined">
                  <CalendarDays size={16} /> Joined {formatDate(profile.created_at)}
                </span>
              </div>

              <div className="follow-stats">
                <button className="stat-btn">
                  <span className="count">0</span> Following
                </button>
                <button className="stat-btn">
                  <span className="count">0</span> Followers
                </button>
              </div>
            </div>
          </div>
        </div>

        <nav className="profile-tabs">
          <button className="tab active">Posts</button>
          <button className="tab">Replies</button>
          <button className="tab">Highlights</button>
          <button className="tab">Articles</button>
          <button className="tab">Media</button>
          <button className="tab">Likes</button>
        </nav>

        <div className="posts-list">
          {tweets.length === 0 ? (
            <div className="no-tweets">
              <p>No tweets</p>
              <span>When you post tweets, they will show up here.</span>
            </div>
          ) : (
            tweets.map((tweet) => (
              <article key={tweet.tweet_id} className="tweet-card">
                <div className="tweet-header">
                  <img
                    src={DEFAULT_AVATAR}
                    alt=""
                    className="mini-avatar"
                  />
                  <div className="tweet-user">
                    <span className="display-name">{profile.name}</span>
                    <span className="username">{username}</span>
                    <span className="tweet-time">· {formatTweetTime(tweet.created_at)}</span>
                  </div>
                </div>
                <div className="tweet-content">{tweet.content}</div>
              </article>
            ))
          )}
        </div>
      </div>
      <ProfileEditForm
        isOpen={editFormOpen}
        onClose={() => setEditFormOpen(false)}
      />
    </>
  );
}
