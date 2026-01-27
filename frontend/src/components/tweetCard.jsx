import "./css/tweetcard.css";
import { useState } from "react";
import { MessageCircle, Heart } from "lucide-react";

export default function TweetCard() {
  // You can pass these as props later
  const username = "epicSurjan";
  const handle = "@tsurjan16";
  const timeAgo = "10h";
  const avatarUrl =
    "https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=200"; // ← replace with real URL or prop

  const tweetLines = [
    "so rainy weather today no electricity 😭",
    "uvloop for async fast speed.",
    "apply some production grade code .",
    "uvloop for async fast speed.",
    "api's versioning.",
    "api's versioning.",
    "23/60hrs only , lets touch the milestone 😊.",
    "2 days left only, lets touch the milestone 😊.",
    "23hrs week.",
    "i know i lost the two days consistency 😔.",
  ];

  const engagement = {
    comments: "3",
    retweets: "2h 14m", // ← looks like time spent?
    likes: "100",
    views: "9",
    bookmarks: "",
  };

  return (
    <article className="tweet-card">
      {/* Top section - avatar + name + time */}
      <div className="tweet-header">
        <img
          src={avatarUrl}
          alt={`${username} profile`}
          className="avatar"
          onError={(e) => {
            e.target.src = "https://via.placeholder.com/48";
          }}
        />
        <div className="user-info">
          <span className="display-name">{username}</span>
          <span className="handle">{handle}</span>
          <span className="time">· {timeAgo}</span>
        </div>
      </div>

      {/* Middle - main content (bullet-like lines) */}
      <div className="tweet-content">
        {tweetLines.map((line, i) => (
          <div key={i} className="tweet-line">
            {line.startsWith(">") ? line.slice(1).trim() : line}
          </div>
        ))}
      </div>
      {/* Bottom engagement bar */}
      <div className="tweet-footer">
        <button className="action-btn comment">
          <span>
            <MessageCircle size={24} />
          </span>{" "}
          {engagement.comments}
        </button>
        <button className="action-btn like">
          <span>
            {" "}
            <Heart size={24} />
          </span>{" "}
          {engagement.likes}
        </button>
      </div>
    </article>
  );
}
