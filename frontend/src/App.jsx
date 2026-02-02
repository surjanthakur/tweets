import axios from "axios";
import { useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import "./App.css";
import { SidebarSection, Loader } from "./components/index";
import { AuthContexProvider } from "./context/loginContext";

// Configure axios to send credentials with requests
axios.defaults.withCredentials = true;

export default function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch current user when token changes
  const currUser = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/auth/current");
      if (!response.data) {
        throw new Error("Invalid user");
      } else {
        setUser(response.data);
        return true;
      }
    } catch (error) {
      console.error("Failed to fetch user:", error);
      setUser(null);
      return false;
    }
  };

  const loginUser = async (username, password) => {
    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        params,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        },
      );
      if (response.data?.user) {
        setUser(response.data?.user);
        setIsLoading(false);
        return true;
      }
      return false;
    } catch (error) {
      console.log("login error:", error);
      const status = error.response?.status;
      if (status >= 500) return "server_error";
      return false;
    }
  };

  // User registration
  const createUser = async (username, email, password) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/register",
        { username, email, password },
        { headers: { "Content-Type": "application/json" } },
      );
      if (!response.data) throw new Error("Registration failed");
      setUser(response.data);
      setIsLoading(false);
      return true;
    } catch (error) {
      console.error("Registration error:", error);
      throw new Error("Registration failed");
    }
  };

  // Logout function
  const logout = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/auth/logout");
      if (res.status === 200) {
        setUser(null);
        setIsLoading(false);
        toast("logged out", {
          icon: "💁",
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
      throw new Error("error while logout user:", error);
    }
  };

  // Check if user is logged in on component mount
  useEffect(() => {
    const checkAuth = async () => {
      await currUser();
      setIsLoading(false);
    };
    checkAuth();
  }, []);

  const location = useLocation();
  const isLoginOrRegister =
    location.pathname === "/login" || location.pathname === "/register";

  // No user + not on login/register -> redirect to login
  if (!isLoading && !user && !isLoginOrRegister) {
    return <Navigate to="/login" replace />;
  }
  // User is logged in but on login/register -> redirect to home
  if (!isLoading && user && isLoginOrRegister) {
    return <Navigate to="/" replace />;
  }

  return (
    <>
      <Toaster
        position="top-center"
        toastOptions={{ duration: 3000 }}
        reverseOrder={false}
      />
      <AuthContexProvider
        value={{
          user,
          isLoading,
          loginUser,
          logout,
          currUser,
          createUser,
        }}
      >
        {isLoading ? (
          <div className="app-layout">
            wait checking your credentials 🧐 <Loader />
          </div>
        ) : (
          <div className="app-layout">
            <div className="box-1">
              <SidebarSection />
            </div>
            <div className="box-2">
              <Outlet />
            </div>
          </div>
        )}
      </AuthContexProvider>
    </>
  );
}
