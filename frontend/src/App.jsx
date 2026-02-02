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
  const [isLoading, setIsLoading] = useState(false);
  const [token, setToken] = useState(null);

  // check if token exist
  useEffect(() => {
    if (token) {
      localStorage.setItem("access_token", token);
    } else {
      localStorage.removeItem("access_token");
    }
  }, [token]);

  // store current user token
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (storedToken) {
      setToken(storedToken);
      currUser(storedToken);
    } else {
      setIsLoading(false);
    }
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
        setIsLoading(false);
        return true;
      }
    } catch (error) {
      if (error.response?.status === 401) {
        setUser(null);
        setToken(null);
        toast.error("Session expired - please log in again");
        setIsLoading(false);
        return false;
      }
      console.error("Failed to fetch user:", error);
      setUser(null);
      setIsLoading(false);
      return false;
    }
  };

  // login user
  const loginUser = async (username, password) => {
    try {
      const response = await axios.post(
        "/auth/login",
        { username, password },
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        },
      );
      const { token } = response.data;
      if (token) {
        setToken(token);
        getCurrentUser(token);
        setIsLoading(false);
        toast.success("Logged in successfully!");
        return true;
      } else {
        toast.error("invalid credentials!");
        return false;
      }
    } catch (error) {
      console.log("login error:", error);
      const status = error.response?.status;
      if (status >= 500) return "server_error";
      return false;
    }
  };

  // create user
  const createUser = async (username, email, password) => {
    try {
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
      throw new Error("Registration failed");
    }
  };

  // Logout user
  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(nulll);
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
      <Toaster
        position="top-center"
        toastOptions={{ duration: 3000 }}
        reverseOrder={false}
      />
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
