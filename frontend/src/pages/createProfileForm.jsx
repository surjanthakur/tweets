import { useForm } from "react-hook-form";
import { useState } from "react";
import "./css/createprofile.css";

const CreateProfileForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm({
    defaultValues: {
      name: "",
      profession: "",
      bio: "",
      location: "",
      profile_picture: "",
    },
    mode: "onChange",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    const formData = new FormData();
    formData.append("name", data.name.trim());
    formData.append("bio", data.bio.trim());
    formData.append("profession", data.profession.trim());
    formData.append("location", data.location.trim());
    formData.append("profile_picture", data.profile_picture.trim());

    try {
      // Replace with your actual API call
      // const response = await fetch('/api/profile/create', {
      //   method: 'POST',
      //   body: formData,
      // });

      // console.log('Success:', await response.json());

      alert("Profile created successfully! (demo)");
      // Reset form after success
      setValue("name", "");
      setValue("bio", "");
      setValue("profession", "");
      setValue("location", "");
      setValue("profile_picture", "");
    } catch (error) {
      console.error("Error creating profile:", error);
      alert("Failed to create profile. Please try again.");
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
                  value: 2,
                  message: "Name must be at least 2 characters",
                },
                maxLength: {
                  value: 60,
                  message: "Name cannot exceed 60 characters",
                },
              })}
            />
            {errors.name && (
              <span className="error-message">{errors.name.message}</span>
            )}
          </div>

          {/* Profession */}
          <div className="form-group">
            <label htmlFor="profession">Profession / Title</label>
            <input
              id="profession"
              type="text"
              placeholder="Full Stack Developer • UI/UX Designer • Student"
              className="form-input"
              {...register("profession", {
                maxLength: {
                  value: 80,
                  message: "Profession cannot exceed 80 characters",
                },
              })}
            />
            {errors.profession && (
              <span className="error-message">{errors.profession.message}</span>
            )}
          </div>

          {/* Location */}
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              id="location"
              type="text"
              placeholder="where you are..?"
              className="form-input"
              {...register("location", {
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
            <label htmlFor="bio">Bio / About</label>
            <textarea
              id="bio"
              placeholder="Write a short description about yourself... (max 320 characters)"
              className="form-textarea"
              rows={5}
              {...register("bio", {
                maxLength: {
                  value: 320,
                  message: "Bio cannot exceed 320 characters",
                },
              })}
            />
            <div className="character-count">
              {watch("bio")?.length || 0} / 320
            </div>
            {errors.bio && (
              <span className="error-message">{errors.bio.message}</span>
            )}
          </div>

          {/* image url */}
          <div className="form-group">
            <label htmlFor="profile_picture">profile image url</label>
            <input
              id="profile_picture"
              type="url"
              placeholder="https://example.com/your-image.jpg"
              className="form-input"
              {...register("profile_picture", {
                required: "image url is required",
              })}
            />
            {errors.profile_picture && (
              <span className="error-message">
                {errors.profile_picture.message}
              </span>
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
