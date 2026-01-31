import axios from "axios";
import { Heart, Reply } from "lucide-react";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import "./css/alltweets.css";

function formatTweetTime(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  const now = new Date();
  const diffMs = now - d;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins}m`;
  if (diffHours < 24) return `${diffHours}h`;
  if (diffDays < 7) return `${diffDays}d`;
  return d.toLocaleDateString();
}

export default function AllTweets() {
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const res = await axios.get("http://127.0.0.1:8000/tweet/all");
        if (cancelled) return;
        setTweets(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        if (cancelled) return;
        console.error("AllTweets fetch error:", err);
        if (err.response?.status === 404) {
          setTweets([]);
          return;
        }
        const message =
          err.response?.data?.detail ||
          err.message ||
          "Could not load tweets. Please try again.";
        toast.error(
          typeof message === "string" ? message : JSON.stringify(message)
        );
        setTweets([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="all-tweets">
        <p className="no-tweets">Loading tweets…</p>
      </div>
    );
  }

  if (!tweets || tweets.length === 0) {
    return (
      <div className="all-tweets">
        <p className="no-tweets">No tweets yet. Be the first to post!</p>
      </div>
    );
  }

  return (
    <div className="all-tweets">
      {tweets.map((tweet, idx) => (
        <article key={idx} className="tweet-card">
          <div className="tweet-header">
            <div className="user-info">
              <span className="handle">
                @
                {tweet.profile?.name?.toLowerCase().replace(/\s+/g, "") ??
                  "yourname"}
              </span>
              <span className="time">{formatTweetTime(tweet.created_at)}</span>
            </div>
          </div>
          <div className="tweet-content">
            <p className="tweet-line">{tweet.content}</p>
          </div>
          <div className="tweet-footer">
            <button type="button" className="action-btn" aria-label="Reply">
              <Reply size={18} />
              Reply
            </button>
            <button type="button" className="action-btn like" aria-label="Like">
              <Heart size={18} />
              Like
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}
