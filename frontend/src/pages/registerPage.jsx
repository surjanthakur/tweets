import { useForm } from "react-hook-form";
import "./css/register.css"; // Import the raw CSS file

const RegisterForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  // Mock submission handler (replace with real API call)
  const onSubmit = (data) => {
    console.log("Form submitted:", data);
    // Example: fetch('/api/register', { method: 'POST', body: JSON.stringify(data) });
  };

  return (
    <div className="form-container">
      <h2 className="form-title">Register User</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        {/* Username Field */}
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            placeholder="@yourhandle"
            {...register("username", {
              required: "Username is required",
              pattern: {
                value: /^@/, // Must start with '@'
                message: "Username must start with @",
              },
              minLength: {
                value: 4, // Minimum length after '@' for practicality
                message: "Username must be at least 4 characters including @",
              },
            })}
            aria-invalid={errors.username ? "true" : "false"}
            aria-describedby={errors.username ? "username-error" : undefined}
          />
          {errors.username && (
            <span id="username-error" className="error-message">
              {errors.username.message}
            </span>
          )}
        </div>

        {/* Email Field */}
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            {...register("email", {
              required: "Email is required",
              pattern: {
                value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
                message: "Invalid email address",
              },
            })}
            aria-invalid={errors.email ? "true" : "false"}
            aria-describedby={errors.email ? "email-error" : undefined}
          />
          {errors.email && (
            <span id="email-error" className="error-message">
              {errors.email.message}
            </span>
          )}
        </div>

        {/* Password Field */}
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            {...register("password", {
              required: "Password is required",
              minLength: {
                value: 8,
                message: "Password must be at least 8 characters",
              },
            })}
            aria-invalid={errors.password ? "true" : "false"}
            aria-describedby={errors.password ? "password-error" : undefined}
          />
          {errors.password && (
            <span id="password-error" className="error-message">
              {errors.password.message}
            </span>
          )}
        </div>

        <button type="submit" className="submit-button">
          Register
        </button>
      </form>
    </div>
  );
};

export default RegisterForm;
