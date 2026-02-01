import { useContext, createContext } from "react";

export const AuthContext = createContext({
  user: null,
  isLoading: true,
  currUser: () => {},
  loginUser: (username, password) => {},
  createUser: (username, email, password) => {},
  logout: () => {},
});

export const AuthContexProvider = AuthContext.Provider;

export const useAuth = () => {
  return useContext(AuthContext);
};
