import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";

import App from "./App";
import "bulma/css/bulma.min.css";
import "bulma-prefers-dark/css/bulma-prefers-dark.min.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <App />
);
