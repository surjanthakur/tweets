import "./profileeditform.css";
import { useEffect, useRef, useState } from "react";
import { X } from "lucide-react";

export default function ProfileEditForm({ onClose, isOpen }) {
  const [text, setText] = useState("");
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

  const handleSave = () => {
    if (!text.trim()) return;
    setText("");
    onClose?.();
  };

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="profile-header">
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <X size={24} />
          </button>
          <h2>Edit profile</h2>
          <button
            className={`save-btn ${text.trim() ? "active" : ""}`}
            onClick={handleSave}
            disabled={!text.trim()}
          >
            Save
          </button>
        </div>

        {/* Body */}
        <div className="profile-body">
          {/* Image URL */}
          <div className="form-group">
            <label>Profile Image URL</label>
            <input type="url" placeholder="https://example.com/photo.jpg" />
          </div>

          {/* Name */}
          <div className="form-group">
            <label>Name</label>
            <input type="text" placeholder="Your name" />
          </div>

          {/* Bio */}
          <div className="form-group">
            <label>Bio</label>
            <textarea
              ref={textareaRef}
              onChange={(e) => setText(e.target.value)}
              rows={1}
              maxLength={280}
              value={text}
              placeholder="Tell the world who you are…"
            />
          </div>

          {/* Profession */}
          <div className="form-group">
            <label>Profession</label>
            <input type="text" placeholder="Software Engineer" />
          </div>

          {/* Location */}
          <div className="form-group">
            <label>Location</label>
            <input type="text" placeholder="India" />
          </div>
        </div>
      </div>
    </div>
  );
}
