import "./css/profileEditForm.css";
import { useEffect, useRef, useState } from "react";
import { X } from "lucide-react";
import { useForm } from "react-hook-form";
import axios from "axios";
import toast from "react-hot-toast";
import { useAuth } from "../context/loginContext";

const defaultValues = {
  name: "",
  bio: "",
  profession: "",
  location: "",
};

const API_BASE = "http://127.0.0.1:8000";

// Validation rules matching backend RequestProfile
const validations = {
  name: {
    required: "Name is required",
    minLength: { value: 3, message: "Name must be at least 3 characters" },
    maxLength: { value: 30, message: "Name cannot exceed 30 characters" },
  },
  profession: {
    required: "Profession is required",
    minLength: {
      value: 3,
      message: "Profession must be at least 3 characters",
    },
    maxLength: { value: 50, message: "Profession cannot exceed 50 characters" },
  },
  location: {
    required: "Location is required",
    minLength: { value: 3, message: "Location must be at least 3 characters" },
    maxLength: { value: 100, message: "Location cannot exceed 100 characters" },
  },
  bio: {
    required: "Bio is required",
    minLength: { value: 10, message: "Bio must be at least 10 characters" },
    maxLength: { value: 350, message: "Bio cannot exceed 350 characters" },
  },
};

export default function ProfileEditForm({ onClose, isOpen, onSuccess }) {
  const { user, isLoading } = useAuth();
  const textareaRef = useRef(null);
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isValid },
  } = useForm({ defaultValues, mode: "onChange" });

  const bio = watch("bio");

  useEffect(() => {
    if (isLoading) return;
    if (!user) {
      toast.error("you have to login first!");
      return null;
    }
    if (!isOpen) return;
    const fetchProfile = async () => {
      try {
        const res = await axios.get(`${API_BASE}/profile/me`);
        reset({
          name: res.data.name ?? "",
          bio: res.data.bio ?? "",
          profession: res.data.profession ?? "",
          location: res.data.location ?? "",
        });
      } catch (err) {
        toast.error("Could not load profile.");
        console.error("Failed to fetch profile for edit:", err);
      }
    };
    fetchProfile();
  }, [isOpen, reset, user, isLoading]);

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
  }, [bio]);

  const [isSubmitting, setIsSubmitting] = useState(false);

  const onSave = async (data) => {
    setIsSubmitting(true);
    try {
      await axios.put(
        `${API_BASE}/profile/edit`,
        {
          name: data.name.trim(),
          profession: data.profession.trim(),
          location: data.location.trim(),
          bio: data.bio.trim(),
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      toast.success("Profile updated!");
      onSuccess?.();
      onClose?.();
    } catch (err) {
      console.error("Failed to update profile:", err);
      toast.error(err.response?.data?.detail ?? "Failed to update profile.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const canSubmit = isValid && !isSubmitting;

  if (!isOpen) return null;

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
        <form onSubmit={handleSubmit(onSave)}>
          {/* Header */}
          <div className="profile-header">
            <button
              type="button"
              className="close-btn"
              onClick={onClose}
              aria-label="Close"
            >
              <X size={24} />
            </button>
            <h2>Edit profile</h2>
            <button
              type="submit"
              className={`save-btn ${canSubmit ? "active" : ""}`}
              disabled={!canSubmit}
            >
              {isSubmitting ? "Saving..." : "Save"}
            </button>
          </div>
          {/* Body */}
          <div className="profile-body">
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                placeholder="Your name"
                {...register("name", validations.name)}
              />
              {errors.name && (
                <span className="error-message">{errors.name.message}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                rows={1}
                maxLength={350}
                placeholder="Tell the world who you are…"
                {...register("bio", validations.bio)}
                ref={(e) => {
                  register("bio").ref(e);
                  textareaRef.current = e;
                }}
              />
              <span className="character-count">
                {watch("bio")?.length ?? 0} / 350
              </span>
              {errors.bio && (
                <span className="error-message">{errors.bio.message}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="profession">Profession</label>
              <input
                id="profession"
                type="text"
                placeholder="Software Engineer"
                {...register("profession", validations.profession)}
              />
              {errors.profession && (
                <span className="error-message">
                  {errors.profession.message}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                id="location"
                type="text"
                placeholder="India"
                {...register("location", validations.location)}
              />
              {errors.location && (
                <span className="error-message">{errors.location.message}</span>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
