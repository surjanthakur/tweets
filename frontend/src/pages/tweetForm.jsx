// src/components/TweetForm.jsx
import { useState, useRef, useEffect } from "react";
import { X, Image as ImageIcon } from "lucide-react";
import "./tweetform.css";

export default function TweetForm({ isOpen, onClose, onPost }) {
  const [text, setText] = useState("");
  const [replySetting, setReplySetting] = useState("everyone"); // everyone | mentioned | following
  const textareaRef = useRef(null);

  // Auto-grow textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const resetHeight = () => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    };

    resetHeight();
    window.addEventListener("resize", resetHeight);
    return () => window.removeEventListener("resize", resetHeight);
  }, [text]);

  if (!isOpen) return null;

  const handlePost = () => {
    if (!text.trim()) return;
    // You would normally send this to your backend / context here
    onPost?.({ text, replySetting });
    setText("");
    onClose?.();
  };

  return (
    <div className="tweet-modal-overlay" onClick={onClose}>
      <div className="tweet-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <X size={24} />
          </button>
          <div className="drafts-link">Drafts</div>
        </div>

        {/* Main content */}
        <div className="modal-body">
          <div className="tweet-form">
            {/* Profile picture */}
            <div className="avatar-wrapper">
              <img
                src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=120"
                alt="Your profile"
                className="user-avatar"
              />
            </div>

            <div className="form-content">
              {/* Reply visibility dropdown */}
              <button className="reply-setting-btn">
                Everyone <span className="arrow">▼</span>
              </button>

              {/* Textarea */}
              <textarea
                ref={textareaRef}
                placeholder="What's happening?!"
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={1}
                maxLength={280}
              />

              {/* Bottom bar */}
              <div className="form-footer">
                <button className="media-btn" aria-label="Add media">
                  <ImageIcon size={20} />
                </button>

                <div className="spacer" />

                <button
                  className={`post-btn ${text.trim() ? "active" : ""}`}
                  onClick={handlePost}
                  disabled={!text.trim()}
                >
                  Post
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
