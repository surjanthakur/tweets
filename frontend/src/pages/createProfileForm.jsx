import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import "./css/createprofile.css";
import { useAuth } from "../context/loginContext";

const CreateProfileForm = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const { user, token } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm({
    defaultValues: {
      name: "",
      profession: "",
      bio: "",
      location: "",
    },
    mode: "onChange",
  });

  const onSubmit = async (data) => {
    if (!user) {
      toast.error("You have to login first");
      return;
    }
    setIsSubmitting(true);
    try {
      const res = await axios.post(
        "/profile/create",
        {
          name: data.name.trim(),
          profession: data.profession.trim(),
          location: data.location.trim(),
          bio: data.bio.trim(),
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        },
      );
      toast.success("Profile created successfully! 🎉");
      navigate("/profile");
    } catch (error) {
      console.error("Error creating profile:", error);

      const status = error.response?.status;
      const detail = error.response?.data?.detail;

      if (status === 401) {
        toast.error("Session expired. Please login again.");
        navigate("/login");
      } else if (
        status === 409 ||
        (status === 400 && detail?.includes("already exists"))
      ) {
        toast.error("Profile already exists. Redirecting...");
        navigate("/profile");
      } else if (status >= 500) {
        toast.error("Server error. Please try again later.");
      } else {
        toast.error(detail || "Failed to create profile. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };
  return (
    <div className="profile-container">
      <div className="create-profile-card">
        <h1 className="form-title">Create Your Profile</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="profile-form">
          {/* Name */}
          <div className="form-group">
            <label htmlFor="name">Full Name *</label>
            <input
              id="name"
              type="text"
              placeholder="John Doe"
              className="form-input"
              {...register("name", {
                required: "Name is required",
                minLength: {
                  value: 3,
                  message: "Name must be at least 3 characters",
                },
                maxLength: {
                  value: 30,
                  message: "Name cannot exceed 30 characters",
                },
              })}
            />
            {errors.name && (
              <span className="error-message">{errors.name.message}</span>
            )}
          </div>

          {/* Profession */}
          <div className="form-group">
            <label htmlFor="profession">Profession / Title *</label>
            <input
              id="profession"
              type="text"
              placeholder="Full Stack Developer • UI/UX Designer • Student"
              className="form-input"
              {...register("profession", {
                required: "Profession is required",
                minLength: {
                  value: 3,
                  message: "Profession must be at least 3 characters",
                },
                maxLength: {
                  value: 50,
                  message: "Profession cannot exceed 50 characters",
                },
              })}
            />
            {errors.profession && (
              <span className="error-message">{errors.profession.message}</span>
            )}
          </div>

          {/* Location */}
          <div className="form-group">
            <label htmlFor="location">Location *</label>
            <input
              id="location"
              type="text"
              placeholder="where you are..?"
              className="form-input"
              {...register("location", {
                required: "Location is required",
                minLength: {
                  value: 3,
                  message: "Location must be at least 3 characters",
                },
                maxLength: {
                  value: 100,
                  message: "Location cannot exceed 100 characters",
                },
              })}
            />
            {errors.location && (
              <span className="error-message">{errors.location.message}</span>
            )}
          </div>

          {/* Bio */}
          <div className="form-group">
            <label htmlFor="bio">Bio / About *</label>
            <textarea
              id="bio"
              placeholder="Write a short description about yourself... (max 350 characters)"
              className="form-textarea"
              rows={5}
              {...register("bio", {
                required: "Bio is required",
                minLength: {
                  value: 10,
                  message: "Bio must be at least 10 characters",
                },
                maxLength: {
                  value: 350,
                  message: "Bio cannot exceed 350 characters",
                },
              })}
            />
            <div className="character-count">
              {watch("bio")?.length || 0} / 350
            </div>
            {errors.bio && (
              <span className="error-message">{errors.bio.message}</span>
            )}
          </div>

          <button
            type="submit"
            className={`submit-btn ${isSubmitting ? "submitting" : ""}`}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Saving..." : "Create Profile"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateProfileForm;
