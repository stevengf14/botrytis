import { useState } from "react";
import useIsMobile from "../../services/hooks/useIsMobile";
import { SECTIONS } from "../../utils/Constants";
import { useLanguage } from "../../services/hooks/LanguageContext";

const BotrytisInformation = () => {
  const { t } = useLanguage();
  const isMobile = useIsMobile();
  const mobileCompensatedPadding = isMobile ? "6.25rem" : "5rem";
  const [activeTab, setActiveTab] = useState("que-es");
  const [activeAccordion, setActiveAccordion] = useState(null);

  const botrytisGreen = "#2ecc71";

  const toggleAccordion = (id) => {
    setActiveAccordion(activeAccordion === id ? null : id);
  };

  const activeContent = SECTIONS(t).find((section) => section.id === activeTab);

  const renderContentPanel = (section) => (
    <div key={section.id} className="content-panel has-text-centered">
      <h2
        className="title is-3 text-color has-text-weight-bold mb-4"
        style={{ color: botrytisGreen }}
      >
        {section.titleComplete}
      </h2>
      <p
        className="has-text-grey-light is-size-5 has-text-justified"
        style={{
          lineHeight: "1.7",
          maxWidth: "800px",
          margin: "0 auto",
        }}
      >
        {section.content}
      </p>
    </div>
  );

  return (
    <section
      className="section is-medium has-text-light"
      style={{
        paddingTop: mobileCompensatedPadding,
        paddingBottom: "5rem",
      }}
    >
      <div className="container">
        <div className="has-text-centered pb-6">
          <h1
            className={`title ${
              isMobile ? "is-3 pb-5" : "is-1"
            } text-color has-text-weight-bold`}
          >
            {t("info.title")}
          </h1>
          <p className="subtitle is-5 has-text-grey-light pt-3">
            {t("info.subtitle")}
          </p>
        </div>
        {!isMobile && (
          <>
            <div className="tabs is-centered is-medium is-toggle is-fullwidth">
              <ul>
                {SECTIONS(t).map((section) => (
                  <li
                    key={section.id}
                    className={activeTab === section.id ? "is-active" : ""}
                    onClick={() => setActiveTab(section.id)}
                    style={{
                      backgroundColor:
                        activeTab === section.id
                          ? botrytisGreen
                          : "transparent",
                      borderRadius: "4px",
                    }}
                  >
                    <a
                      className=" has-text-weight-bold"
                      style={{
                        backgroundColor:
                          activeTab === section.id
                            ? botrytisGreen
                            : "transparent",
                        borderColor:
                          activeTab === section.id ? botrytisGreen : "#4a4a4a",
                        color:
                          activeTab === section.id ? "#fff" : botrytisGreen,
                      }}
                    >
                      <span>{section.title}</span>
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div
              className="box p-6 mt-5 has-background-black-dark"
              style={{
                minHeight: "300px",
                borderTop: `3px solid ${botrytisGreen}`,
              }}
            >
              {activeContent && renderContentPanel(activeContent)}
            </div>
          </>
        )}
        {isMobile && (
          <div className="pb-5">
            {SECTIONS(t).map((section) => (
              <div key={section.id} className="mb-4">
                <a
                  className="button is-fullwidth is-large is-dark has-text-weight-bold"
                  onClick={() => toggleAccordion(section.id)}
                  style={{
                    justifyContent: "space-between",
                    backgroundColor:
                      activeAccordion === section.id ? botrytisGreen : "#222",
                    color:
                      activeAccordion === section.id ? "#fff" : botrytisGreen,
                    border: "1px solid #4a4a4a",
                    borderRadius: "6px",
                    transition: "all 0.2s",
                  }}
                >
                  <span>{section.title}</span>
                  <span className="icon">
                    <i
                      className={`fa-solid fa-chevron-down ${
                        activeAccordion === section.id ? "fa-rotate-180" : ""
                      }`}
                    ></i>
                  </span>
                </a>

                {activeAccordion === section.id && (
                  <div
                    className="box p-5 mt-2"
                    style={{
                      borderTop: `2px solid ${botrytisGreen}`,
                      borderTopLeftRadius: 0,
                      borderTopRightRadius: 0,
                    }}
                  >
                    <div className="content-panel">
                      <h2
                        className="title is-5 has-text-centered has-text-weight-bold mb-4"
                        style={{ color: botrytisGreen }}
                      >
                        {section.titleComplete}
                      </h2>
                      <p
                        className="has-text-grey-light is-size-6 has-text-justified"
                        style={{ lineHeight: "1.6" }}
                      >
                        {section.content}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="container pb-6">
          <div
            className="box has-background-grey-darker"
            style={{
              border: "1px solid #4a4a4a",
              marginTop: "2rem",
            }}
          >
            <div className="columns is-vcentered">
              <div className="column is-narrow has-text-centered">
                <span
                  className="icon is-large"
                  style={{ color: botrytisGreen }}
                >
                  <i className="fa-brands fa-github fa-3x"></i>
                </span>
              </div>
              <div className="column">
                <p
                  className="has-text-grey-light is-size-6"
                  style={{ lineHeight: "1.6" }}
                >
                  {t("info.github_text")}
                </p>
              </div>
              <div
                className={`${
                  !isMobile && "column"
                } is-narrow has-text-centered`}
              >
                <a
                  href="https://github.com/stevengf14/botrytis"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="button is-rounded has-text-weight-bold"
                  style={{
                    color: botrytisGreen,
                    borderColor: botrytisGreen,
                    width: isMobile ? "100%" : "auto",
                  }}
                >
                  <span className="icon">
                    <i className="fa-solid fa-code"></i>
                  </span>
                  <span>{t("info.github_link")}</span>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="buttons buttons-centered is-centered">
          <a
            className="button is-medium is-info is-rounded has-text-weight-bold is-light"
            href="/botrytis-detection"
            aria-label="Comenzar Análisis Ahora"
          >
            <span className="icon is-medium">
              <i className="fa-solid fa-cloud-arrow-up"></i>
            </span>
            <span>{t("btn.begin_analysis")}</span>
          </a>
        </div>
        <div className="has-text-centered pt-5">
          <p className="has-text-grey-light">{t("home.return_msg")} </p>
          <a
            className="button is-text has-text-weight-semibold mt-3"
            href="/"
            aria-label="Enlace a la información del proyecto"
            style={{ color: botrytisGreen }}
          >
            <span className="icon">
              <i className="fa-solid fa-arrow-left"></i>
            </span>
            <span>{t("info.home_link")}</span>
          </a>
        </div>
      </div>
    </section>
  );
};

export default BotrytisInformation;