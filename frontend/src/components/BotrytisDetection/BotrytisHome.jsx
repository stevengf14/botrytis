import { FEATURES } from "../../utils/Constants";
import homeImage from "../../utils/images/botrytis_home_image.png";
import useIsMobile from "../../services/hooks/useIsMobile";
import { useLanguage } from "../../services/hooks/LanguageContext";

const BotrytisHome = () => {
  const { t } = useLanguage();
  const isMobile = useIsMobile();

  const renderImageHome = () => (
    <div className="column is-6 has-text-centered">
      <figure className="image is-5by4">
        <img
          src={homeImage}
          alt="Rosa con Botrytis analizada por IA"
          style={{
            borderRadius: "10px",
            objectFit: "cover",
            boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
          }}
        />
      </figure>
    </div>
  );

  return (
    <section
      className="section is-large has-text-light "
      style={{ minHeight: "100vh", paddingTop: "5rem", paddingBottom: "5rem" }}
    >
      <div className="container">
        <div
          className={`columns is-vcentered ${
            isMobile ? "pb-2" : "pb-6"
          } is-mobile-centered`}
        >
          <div className="column is-6">
            <h1
              className={`title ${
                isMobile ? "is-3" : "is-size-1"
              } text-color has-text-weight-bold mb-4 has-text-centered`}
            >
              {t("home.title")}
            </h1>
            <p
              className={`subtitle has-text-grey-light ${
                isMobile ? "mb-2 is-5" : "mb-6 is-3"
              } has-text-centered`}
            >
              {t("home.subtitle")}
            </p>

            <div className="buttons buttons-centered is-centered">
              {isMobile && renderImageHome()}
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
          </div>
          {!isMobile && renderImageHome()}
        </div>

        <div className="mb-6 pt-6" style={{ borderTop: "1px solid #4a4a4a" }}>
          <h3 className="title is-4 text-color has-text-weight-semibold mb-5">
            {t("home.advantages_title")}
          </h3>

          <div className="columns is-multiline">
            {FEATURES(t).map((feature, index) => (
              <div key={index} className="column is-one-third">
                <div
                  className="card has-background-black-dark is-shadowless"
                  style={{
                    border: "1px solid #000000ff",
                    transition: "transform 0.2s",
                    cursor: "pointer",
                    height: "100%",
                  }}
                  onMouseOver={(e) =>
                    (e.currentTarget.style.transform = "translateY(-5px)")
                  }
                  onMouseOut={(e) =>
                    (e.currentTarget.style.transform = "translateY(0)")
                  }
                >
                  <div className="card-content">
                    <div className=" mb-3">
                      <div className="media-content">
                        <p className="title is-4 text-color">{feature.title}</p>
                      </div>
                    </div>
                    <div className="content has-text-grey-light">
                      {feature.description}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="has-text-centered pt-6">
          <h3 className="subtitle is-4 text-color">{t("home.info_title")}</h3>
          <p className="has-text-grey-light">{t("home.info_section_title")}</p>
          <a
            className="button is-text has-text-weight-semibold mt-3 text-color"
            href="/information"
            aria-label="Enlace a la información del proyecto"
          >
            <span className="icon">
              <i className="fa-solid fa-arrow-right"></i>
            </span>
            <span>{t("home.info_link")}</span>
          </a>
        </div>
      </div>
    </section>
  );
};

export default BotrytisHome;
