// src/components/TweetForm.jsx
import axios from "axios";
import { Image as ImageIcon, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { useAuth } from "../context/loginContext";
import "./css/tweetform.css";

const API_BASE = "http://127.0.0.1:8000";

export default function TweetForm({ isOpen, onClose, onPost }) {
  const [text, setText] = useState("");
  const textareaRef = useRef(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      content: "",
    },
    mode: "onChange",
  });

  const { token } = useAuth();

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

  const onSubmit = async (data) => {
    if (!token) {
      toast.error("Please login to post a tweet");
      return;
    }
    try {
      const res = await axios.post(
        `${API_BASE}/tweet/create`,
        { content: data.content },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      toast.success("posted new tweet");
      setText("");
      reset({ content: "" });
      onClose?.();
      onPost?.(res.data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      const status = err.response?.status;
      if (status === 401) {
        toast.error("Session expired. Please log in again.");
      } else if (
        status === 404 &&
        typeof detail === "string" &&
        detail.includes("Profile")
      ) {
        toast.error("Create a profile first before tweeting.");
      } else if (status === 422 && err.response?.data?.detail) {
        const msg = Array.isArray(detail)
          ? detail.map((e) => e.msg).join(", ")
          : String(detail);
        toast.error(msg || "Invalid tweet content");
      } else if (status >= 500) {
        toast.error(detail || "Server error. Try again later.");
      } else {
        toast.error(detail || err.message || "Failed to create tweet");
      }
    }
  };

  const modalContent = (
    <div className="tweet-modal-overlay" onClick={onClose}>
      <div className="tweet-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <X size={24} />
          </button>
          <h2 className="text-white font-bold">adding tweet</h2>
          <div className="drafts-link">Drafts</div>
        </div>

        {/* Main content */}
        <div className="modal-body">
          <div className="tweet-form">
            <div className="form-content">
              {/* Reply visibility dropdown */}
              <button className="reply-setting-btn">
                Everyone can read&nbsp;<span className="arrow">🌏</span>
              </button>
              <form onSubmit={handleSubmit(onSubmit)} noValidate>
                {/* Textarea */}
                <textarea
                  id="content"
                  type="text"
                  ref={textareaRef}
                  placeholder="What's happening?!"
                  onChange={(e) => setText(e.target.value)}
                  rows={1}
                  {...register("content", {
                    required: "Content is required",
                    minLength: {
                      value: 10,
                      message: "At least 10 characters required",
                    },
                    maxLength: {
                      value: 750,
                      message: "Max 750 characters allowed",
                    },
                  })}
                  aria-invalid={errors.content ? "true" : "false"}
                  aria-describedby={
                    errors.content ? "content-error" : undefined
                  }
                />
                {errors.content && (
                  <span id="content-error" className="error-message">
                    {errors.content.message}
                  </span>
                )}

                {/* Bottom bar */}
                <div className="form-footer">
                  <button className="media-btn" aria-label="Add media">
                    <ImageIcon size={20} />
                  </button>

                  <div className="spacer" />

                  <button type="submit" className="post-btn">
                    Post
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
}
