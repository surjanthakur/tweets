import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route,
} from "react-router-dom";

import {
  ProfilePage,
  CreateProfileForm,
  RegisterForm,
  LoginForm,
} from "./pages/index.js";
import { AuthProvider } from "./context/loginContex.js";

const my_router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/create-profile" element={<CreateProfileForm />} />
      <Route path="/register" element={<RegisterForm />} />
      <Route path="/login" element={<LoginForm />} />
    </Route>,
  ),
);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={my_router} />
    </AuthProvider>
  </StrictMode>,
);
