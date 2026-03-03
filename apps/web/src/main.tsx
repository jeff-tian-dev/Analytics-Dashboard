import React from "react";
import ReactDOM from "react-dom/client";
import { Theme } from "@radix-ui/themes";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Theme accentColor="amber" grayColor="sand" radius="medium" scaling="100%">
      <App />
    </Theme>
  </React.StrictMode>
);
