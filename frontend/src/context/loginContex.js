import { useContext, createContext, useEffect, useState } from "react";
import axios from "axios";

// Create the context
const AuthContext = createContext(null);

// Custom hook for consuming the context (exported)
export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within an AuthProvider");
  }
  return context;
};

// Provider component (exported)
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load token from localStorage and fetch user if present
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (storedToken) {
      setToken(storedToken);
      fetchUser(storedToken).finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []); // Empty dependency array: run once on mount

  // Helper to fetch user with token
  const fetchUser = async (authToken) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/auth/me", {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      logout(); // Auto-logout on invalid token
    }
  };

  // Login function
  const login = async (username, password) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/login", {
        username,
        password,
      });
      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token);
      setToken(access_token);
      await fetchUser(access_token); // Fetch user after login
    } catch (error) {
      throw new Error("Invalid credentials"); // Rethrow for form handling
    }
  };

  // Register function
  const register = async (username, email, password) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/register", {
        username,
        email,
        password,
      });
      setUser(response.data); // Assuming response includes user data
      // Optionally auto-login after register by calling login()
    } catch (error) {
      throw new Error("Registration failed"); // Customize based on backend errors
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
    setIsLoading(false);
  };

  // Context value: Expose state and functions
  const value = {
    user,
    token,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext };
