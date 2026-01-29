import { useContext, createContext, useEffect, useState } from "react";
import axios from "axios";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    stored_token = localStorage.getItem("access_token");
    if (stored_token) {
      setToken(stored_token);
    } else {
      setIsLoading(false);
    }
  });

  const login_user = async (username, password) => {
    const res = await axios.post("http://127.0.0.1:8000/auth/login", {
      username: username,
      password: password,
    });
    if (!res.ok) {
      throw new Error("invalid credentials");
    } else {
      user_data = res.data;
      localStorage.setItem("access_token", user_data.access_token);
      setToken(user_data.access_token);
    }
  };

  const register_user = async (username, email, password) => {
    const res = await axios.post("http://127.0.0.1:8000/auth/register", {
      username: username,
      email: email,
      password: password,
    });

    if (!res.ok) {
      throw new Error("invalid credentials");
    } else {
      user_data = res.data;
      setUser(user_data);
    }
  };

  const logout_user = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
    setIsLoading(false);
  };

  return (
    <AuthContext.Provider
      value={{ user, token, isLoading, login_user, logout_user, register_user }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = useContext(AuthContext);
