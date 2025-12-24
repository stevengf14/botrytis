import { useState } from "react";
import { Link } from "react-router-dom";
import { useLanguage } from "../services/hooks/LanguageContext";
import useIsMobile from "../services/hooks/useIsMobile";
import { flagEC, flagUS } from "../utils/Constants";

const Header = () => {
  const [isActive, setIsActive] = useState(false);
  const [language, setLanguage] = useState("es");
  const isMobile = useIsMobile();

  const { t, setLocale } = useLanguage();

  const toggleMenu = () => setIsActive(!isActive);

  const botrytisGreen = "#2ecc71";

  const handleLanguageChange = (lang) => {
    setLocale(lang);
    setLanguage(lang);
    if (isMobile) setIsActive(false);
  };

  const fullscreenMenuStyle = {
    position: "fixed",
    left: "0",
    height: "100vh",
    width: "80%",
    backgroundColor: "#000000",
    display: "flex",
    flexDirection: "column",
  };

  return (
    <header
      className={`navbar ${isMobile ? "is-fixed-top" : ""}`}
      style={{ backgroundColor: "#000000", width: "100%", zIndex: 999 }}
    >
      <div className="navbar-brand">
        {!isMobile ? (
          <div className="navbar-item has-dropdown is-hoverable">
            <a className="navbar-link is-arrowless has-text-weight-bold is-size-5 has-text-white">
              {/* CAMBIO: has-text-info por estilo inline verde para el icono */}
              <span className="icon pr-1" style={{ color: botrytisGreen }}>
                <i className="fa-solid fa-seedling"></i>
              </span>
              {t("nav.project_title")}
            </a>
            <div className="navbar-dropdown is-boxed has-background-black">
              <a
                className="navbar-item has-text-white"
                onClick={() => handleLanguageChange("es")}
              >
                <img
                  src={flagEC}
                  alt="EC"
                  style={{ width: "20px", marginRight: "10px" }}
                />
                {t("project.lang_es")}
              </a>
              <a
                className="navbar-item has-text-white"
                onClick={() => handleLanguageChange("en")}
              >
                <img
                  src={flagUS}
                  alt="US"
                  style={{ width: "20px", marginRight: "10px" }}
                />
                {t("project.lang_en")}
              </a>
            </div>
          </div>
        ) : (
          <div className="navbar-item has-text-weight-bold is-size-5 has-text-white">
            {t("nav.project_title")}
          </div>
        )}
        <a
          role="button"
          className={`navbar-burger burger has-text-white ${
            isActive ? "is-active" : ""
          }`}
          onClick={toggleMenu}
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div
        className={`navbar-menu ${isActive ? "is-active" : ""}`}
        style={isActive ? fullscreenMenuStyle : {}}
      >
        <div className="navbar-end" style={{ flexGrow: 1 }}>
          <Link
            className="navbar-item text-color"
            style={{ padding: !isMobile && "0 3%" }}
            to="/"
            onClick={() => setIsActive(false)}
          >
            {t("nav.home")}
          </Link>
          <Link
            className="navbar-item text-color"
            style={{ padding: !isMobile && "0 3%" }}
            to="/information"
            onClick={() => setIsActive(false)}
          >
            {t("nav.information")}
          </Link>
          <Link
            className="navbar-item text-color"
            style={{ padding: !isMobile && "0 3%" }}
            to="/botrytis-detection"
            onClick={() => setIsActive(false)}
          >
            {t("nav.detection")}
          </Link>

          {isMobile && (
            <div
              className="mt-auto p-5 border-top"
              style={{
                borderTop: "1px solid #333",
                position: "absolute",
                bottom: 0,
                width: "100%",
              }}
            >
              <p className="has-text-grey is-size-7 mb-2">
                {t("project.lang_select")}
              </p>
              <div className="buttons">
                <button
                  className={`button is-small is-dark`}
                  onClick={() => handleLanguageChange("es")}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    backgroundColor:
                      language === "es" ? botrytisGreen : "#363636",
                    color: language === "es" ? "#000" : "#fff",
                  }}
                >
                  <img src={flagEC} alt="EC" style={{ width: "16px" }} /> ES
                </button>
                <button
                  className={`button is-small is-dark`}
                  onClick={() => handleLanguageChange("en")}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    backgroundColor:
                      language === "en" ? botrytisGreen : "#363636",
                    color: language === "en" ? "#000" : "#fff",
                  }}
                >
                  <img src={flagUS} alt="US" style={{ width: "16px" }} /> EN
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
