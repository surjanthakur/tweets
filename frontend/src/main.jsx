import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import App from "./App.jsx";
import "./index.css";

import {
  AllTweets,
  CreateProfileForm,
  LoginForm,
  ProfilePage,
  RegisterForm,
} from "./pages/index.js";

const my_router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route index element={<AllTweets />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/createProfile" element={<CreateProfileForm />} />
      <Route path="/register" element={<RegisterForm />} />
      <Route path="/login" element={<LoginForm />} />
    </Route>
  )
);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={my_router} />
  </StrictMode>
);
