import axios from "axios";
import { useEffect, useState } from "react";
import { Toaster } from "react-hot-toast";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import "./App.css";
import { SidebarSection } from "./components/index";
import { AuthContexProvider } from "./context/loginContext";

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for token in localStorage on app load
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (storedToken) {
      setToken(storedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  // Fetch user when token is available (e.g. after refresh)
  useEffect(() => {
    if (token) {
      currUser(token).finally(() => setIsLoading(false));
    }
  }, [token]);

  // Fetch current user when token changes
  const currUser = async (authToken) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/auth/current", {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (!response.data) {
        throw new Error("Invalid token");
      }
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      logout(); // Auto-logout on invalid token
    }
  };

  // login function (backend expects form-urlencoded per OAuth2PasswordRequestForm)
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
      const { access_token } = response.data;
      if (!access_token) throw new Error("No token in response");
      localStorage.setItem("access_token", access_token);
      setToken(access_token);
      await currUser(access_token); // Fetch user after login
    } catch (error) {
      throw new Error("Registration failed");
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
      return true;
    } catch (error) {
      throw new Error("Registration failed");
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    setToken(null);
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
        toastOptions={{ duration: 5000 }}
        reverseOrder={false}
      />
      <AuthContexProvider
        value={{
          user,
          token,
          isLoading,
          loginUser,
          logout,
          currUser,
          createUser,
        }}
      >
        {isLoading ? (
          <div className="app-layout">Loading...</div>
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

export default App;
