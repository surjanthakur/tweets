import { Heart, MessageCircle } from "lucide-react";
import "./css/tweetcard.css";

const DEFAULT_AVATAR =
  "https://api.dicebear.com/7.x/avataaars/svg?seed=profile";

export default function TweetCard({
  profileName,
  content,
  created_at,
  likeCount = 0,
  commentsCount = 0,
  avatarUrl,
}) {
  const name = profileName ?? "User";
  const text = content ?? "";
  const avatar = avatarUrl || DEFAULT_AVATAR;
  const tweetLines = text ? text.split("\n").filter(Boolean) : [""];

  return (
    <article className="tweet-card">
      <div className="tweet-header">
        <img
          src={avatar}
          alt={`${name} profile`}
          className="avatar"
          onError={(e) => {
            e.target.src = DEFAULT_AVATAR;
          }}
        />
        <div className="user-info">
          <span className="display-name">{name}</span>
          {created_at != null && created_at !== "" && (
            <span className="time">· {created_at}</span>
          )}
        </div>
      </div>

      <div className="tweet-content">
        {tweetLines.map((line, i) => (
          <div key={i} className="tweet-line">
            {line.startsWith(">") ? line.slice(1).trim() : line}
          </div>
        ))}
      </div>

      <div className="tweet-footer">
        <button type="button" className="action-btn comment">
          <span>
            <MessageCircle size={24} />
          </span>{" "}
          {commentsCount}
        </button>
        <button type="button" className="action-btn like">
          <span>
            <Heart size={24} />
          </span>{" "}
          {likeCount}
        </button>
      </div>
    </article>
  );
}
