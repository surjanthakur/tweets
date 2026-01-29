import "./App.css";
import { SidebarSection } from "./components/index";
import { Outlet } from "react-router-dom";
import { AuthContexProvider } from "./context/loginContext";
import { useState, useEffect } from "react";
import axios from "axios";

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

  // Fetch current user when token changes
  const currUser = async (authToken) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/auth/me", {
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

  // login function
  const loginUser = async (username, password) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/login", {
        username,
        password,
      });
      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token);

      setToken(access_token);
      await currUser(access_token); // Fetch user after login
    } catch (error) {
      throw new Error("Invalid credentials");
    }
  };

  // User registration
  const createUser = async (username, email, password) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/register", {
        username,
        email,
        password,
      });
      if (!response.data) {
        throw new Error("Registration failed");
      }
      setUser(response.data);
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
  return (
    <>
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
        <div className="app-layout">
          <div className="box-1">
            <SidebarSection />
          </div>
          <div className="box-2">
            <Outlet />
          </div>
        </div>
      </AuthContexProvider>
    </>
  );
}

export default App;
