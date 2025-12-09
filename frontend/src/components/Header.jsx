import React from "react";
import { Link } from "react-router-dom";
import {
  HOME_TITLE,
  BOTRYTIS_DETECTION_TITLE,
} from "./Constants";

const Header = () => {
  return (
    <header className="navbar is-info">
      <div className="navbar-brand">
        <Link className="navbar-item" to="/">
          <img src="/assets/images/logo.png" alt="Logo" />
        </Link>
        {/* Menú hamburguesa para móviles */}
        <a
          role="button"
          className="navbar-burger burger"
          aria-label="menu"
          aria-expanded="false"
          href="#"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" className="navbar-menu">
        <div className="navbar-start">
          {/* Enlaces de navegación */}
          <Link className="navbar-item" to="/">
            {HOME_TITLE}
          </Link>
          <Link
            className="navbar-item"
            to="/botrytis-detection"
          >
            {BOTRYTIS_DETECTION_TITLE}
          </Link>
          {/* Agrega más enlaces aquí para futuras funcionalidades */}
        </div>
      </div>
    </header>
  );
};

export default Header;
