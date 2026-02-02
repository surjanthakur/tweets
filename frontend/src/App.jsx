import axios from "axios";
import { useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import "./App.css";
import { SidebarSection, Loader } from "./components/index";
import { AuthContexProvider } from "./context/loginContext";

axios.defaults.baseURL = "http://127.0.0.1:8000";

export default function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const validateUser = async () => {
      const stored_token = localStorage.getItem("access_token");

      if (stored_token) {
        setIsLoading(true);
        setToken(stored_token);
        try {
          await getCurrentUser(stored_token);
        } catch (error) {
          localStorage.removeItem("access_token");
          setToken(null);
          setUser(null);
        } finally {
          setIsLoading(false);
        }
      } else {
        setIsLoading(false);
      }
    };

    validateUser();
  }, []);
  // Fetch current user
  const getCurrentUser = async (authToken) => {
    try {
      const response = await axios.get("/auth/current", {
        headers: {
          Authorization: `Bearer ${authToken || token}`,
        },
      });
      if (!response.data) {
        throw new Error("cant get curr user");
      } else {
        setUser(response.data);
        return true;
      }
    } catch (error) {
      if (error.response?.status === 401) {
        setUser(null);
        setToken(null);
        toast.error("Session expired - please log in again");
        return false;
      }
      console.error("Failed to fetch user:", error);
      setUser(null);
      return false;
    }
  };

  // login user
  const loginUser = async (username, password) => {
    try {
      setIsLoading(true);
      const response = await axios.post(
        "/auth/login",
        { username, password },
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        },
      );
      const { token } = response.data;
      if (token) {
        localStorage.setItem("access_token", token);
        setToken(token);
        await getCurrentUser(token);
        setIsLoading(false);
        toast.success("Logged in successfully!");
        return true;
      } else {
        toast.error("invalid credentials!");
        setIsLoading(false);
        return false;
      }
    } catch (error) {
      console.log("login error:", error);
      setIsLoading(false);
      const status = error.response?.status;
      if (status >= 500) return "server_error";
      return false;
    }
  };

  // create user
  const createUser = async (username, email, password) => {
    try {
      setIsLoading(true);
      const response = await axios.post(
        "/auth/register",
        { username, email, password },
        { headers: { "Content-Type": "application/json" } },
      );
      if (!response.data) throw new Error("Registration failed");
      setUser(response.data);
      setIsLoading(false);
      return true;
    } catch (error) {
      console.error("Registration error:", error);
      setIsLoading(false);
      throw new Error("Registration failed");
    }
  };

  // Logout user
  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
    setIsLoading(false);
  };

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
      <AuthContexProvider
        value={{
          token,
          user,
          isLoading,
          loginUser,
          logout,
          getCurrentUser,
          createUser,
        }}
      >
        {isLoading ? (
          <div className="app-layout">
            browser security checking 🧐 <Loader />
          </div>
        ) : (
          <div className="app-layout">
            <Toaster
              position="top-center"
              toastOptions={{ duration: 2000 }}
              reverseOrder={false}
            />
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
