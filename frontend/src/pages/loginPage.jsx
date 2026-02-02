import { User, Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/loginContext";
import "./css/login.css";

const LoginForm = () => {
  const navigate = useNavigate();
  const { loginUser } = useAuth();
  const [isLogin, setIsLogin] = useState(false);
  const [showPass, setShowPass] = useState(false);

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

  const onSubmit = async (data) => {
    setIsLogin(true);
    const result = await loginUser(data.username, data.password);
    if (result === true) {
      toast.success("Logged in successfully!");
      setIsLogin(false);
      setTimeout(() => navigate("/"), 1500);
    } else if (result === "server_error") {
      toast.error("Server error - try again later.");
      setIsLogin(false);
    } else {
      toast.error("Invalid credentials. Please try again.");
      setIsLogin(false);
    }
  };

  return (
    <>
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
                type={showPass ? "text" : "password"}
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
              <button type="button" onClick={() => setShowPass(!showPass)}>
                {showPass ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
              {errors.password && (
                <span id="password-error" className="error-message">
                  {errors.password.message}
                </span>
              )}
            </div>

            <button type="submit" className="submit-button">
              {isLogin ? "loging user.." : "login"}
            </button>

            <p className="form-footer">
              Don't have an account?{" "}
              <Link to="/register" className="form-link">
                Register here
              </Link>
            </p>
          </form>
        </div>
      </div>
    </>
  );
};

export default LoginForm;
