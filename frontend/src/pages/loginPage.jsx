import { User } from "lucide-react";
import { useForm } from "react-hook-form";
import toast, { Toaster } from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/loginContext";
import "./css/login.css";

const LoginForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      username: "",
      password: "",
    },
    mode: "onChange",
  });
  const navigate = useNavigate();
  const { loginUser } = useAuth();
  const onSubmit = async (data) => {
    try {
      loginUser(data.username, data.password);
      toast.success("User login successfully!");
      setTimeout(() => navigate("/"), 2000);
    } catch (err) {
      toast.error(err?.message || "Invalid credentials. Please try again.");
      console.error("Login error:", err);
    }
  };

  return (
    <>
      <Toaster
        position="top-center"
        toastOptions={{ duration: 5000 }}
        reverseOrder={false}
      />
      <div className="overlay-container">
        <div className="form-container">
          <h2 className="form-title">
            <User size={24} />
            login account
          </h2>
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
                    message:
                      "Username must be at least 4 characters including @",
                  },
                })}
                aria-invalid={errors.username ? "true" : "false"}
                aria-describedby={
                  errors.username ? "username-error" : undefined
                }
              />
              {errors.username && (
                <span id="username-error" className="error-message">
                  {errors.username.message}
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
                aria-describedby={
                  errors.password ? "password-error" : undefined
                }
              />
              {errors.password && (
                <span id="password-error" className="error-message">
                  {errors.password.message}
                </span>
              )}
            </div>

            <button type="submit" className="submit-button">
              login
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default LoginForm;
