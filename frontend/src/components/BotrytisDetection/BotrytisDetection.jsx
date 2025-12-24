import { useState } from "react";
import { botrytisService } from "../../services/botrytisService";
import "../../utils/styles/BotrytisDetection.css";
import { useLanguage } from "../../services/hooks/LanguageContext";
import useIsMobile from "../../services/hooks/useIsMobile";
import { FaMinus, FaPlus } from "react-icons/fa";

function BotrytisDetection() {
  const { t } = useLanguage();
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isMobile = useIsMobile();
  const mobileCompensatedPadding = isMobile ? "4.25rem" : "3.25rem";
  const [isCollapsed, setIsCollapsed] = useState(isMobile ? true : false);
  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
      setResult(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError(t("botrytis.detection.error_no_image"));
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await botrytisService.predictImage(selectedImage);
      if (data && data.found_flower === false) {
        setError(t("botrytis.detection.error_detection"));
        return;
      }
      setResult(data);
    } catch (err) {
      setError(err.message || t("botrytis.detection.error_processing_image"));
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <section
      className="section is-medium detection-page"
      style={{
        paddingTop: mobileCompensatedPadding,
        paddingBottom: "5rem",
      }}
    >
      <div className="container">
        <div
          className={`botrytis-header text-color has-text-weight-bold ${
            isMobile ? "is-3" : "is-1"
          } `}
        >
          <h1>{t("botrytis.detection.title")}</h1>
          <p className="subtitle is-5 has-text-grey-light pt-3">
            {t("botrytis.detection.upload_prompt")}
          </p>
        </div>

        <div className="columns is-gapless dashboard-main">
          <div
            className={`column is-7 ${
              isMobile ? "dashboard-panel-left-mobile" : "dashboard-panel-left"
            }`}
          >
            {!preview ? (
              <div
                className={`${isMobile ? "upload-zone-mobile" : "upload-zone"}`}
              >
                <label htmlFor="imageInput" className="upload-trigger">
                  <div className="scanner-line"></div>
                  <i className="fas fa-microscope mb-4"></i>
                  <span>{t("botrytis.detection.select_image")}</span>
                </label>
                <input
                  id="imageInput"
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  hidden
                />
              </div>
            ) : (
              <div className="preview-container">
                <div className="preview-header">
                  <span>ANALYSIS_INPUT_v1.0</span>
                  <button className="delete-btn" onClick={handleClear}>
                    <i className="fas fa-times"></i>
                  </button>
                </div>
                <img src={preview} alt="Preview" className="scan-effect" />
                {loading && <div className="laser-scanner"></div>}
              </div>
            )}
          </div>

          <div
            className={` ${
              isMobile ? "result-section-mobile" : "result-section"
            }`}
          >
            {error && (
              <div className="error-box">
                <i className="fas fa-exclamation-circle"></i>
                <p>{error}</p>
              </div>
            )}

            {loading && (
              <div className="loading-box">
                <div className="spinner"></div>
                <p>{t("botrytis.detection.analyzing_image")}</p>
              </div>
            )}

            {result && !loading && (
              <div
                className={`result-box ${
                  result.has_botrytis ? "positive" : "negative"
                }`}
              >
                <div className="result-status">
                  <i
                    className={`fas ${
                      result.has_botrytis
                        ? "fa-exclamation-triangle"
                        : "fa-check-circle"
                    }`}
                  ></i>
                  <h2>
                    {result.has_botrytis
                      ? t("botrytis.detection.has_botrytis")
                      : t("botrytis.detection.no_botrytis")}
                  </h2>
                </div>

                <div className="confidence-box">
                  <p className="confidence-label">
                    {t("botrytis.detection.confidence")}:
                  </p>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${result.confidence * 100}%`,
                        backgroundColor: result.has_botrytis
                          ? "#e74c3c"
                          : "#27ae60",
                      }}
                    ></div>
                  </div>
                  <p className="confidence-value">
                    {(result.confidence * 100).toFixed(2)}%
                  </p>
                </div>

                <div className="result-message">
                  {result.has_botrytis ? (
                    <p>{t("botrytis.detection.result_message_botrytis")}</p>
                  ) : (
                    <p>{t("botrytis.detection.result_message_no_botrytis")}</p>
                  )}
                </div>
              </div>
            )}

            <div className="button-group">
              <button
                onClick={handlePredict}
                disabled={!selectedImage || loading}
                className="btn-predict button is-info"
              >
                {loading
                  ? t("botrytis.detection.analyzing")
                  : t("botrytis.detection.analyze_now")}
              </button>
              <button onClick={handleClear} className="btn-clear">
                {t("botrytis.detection.clean")}
              </button>
            </div>
            <div className="card">
              <div className="card-header text-background-color mt-6">
                <p className="card-header-title has-text-white">
                  <i className="fas fa-info-circle mr-2"></i>{" "}
                  {t("botrytis.detection.info_title")}
                </p>
                {isMobile && (
                  <button
                    className="button is-small mr-3"
                    style={{
                      backgroundColor: "transparent",
                      border: "none",
                      boxShadow: "none",
                    }}
                    onClick={() => setIsCollapsed(!isCollapsed)}
                  >
                    {isCollapsed ? <FaPlus /> : <FaMinus />}
                  </button>
                )}
              </div>
              {!isCollapsed && (
                <div className="card-content">
                  <ul className="content">
                    <li
                      dangerouslySetInnerHTML={{
                        __html: t("botrytis.detection.info_step1"),
                      }}
                    ></li>
                    <li
                      dangerouslySetInnerHTML={{
                        __html: t("botrytis.detection.info_step2"),
                      }}
                    ></li>
                    <li
                      dangerouslySetInnerHTML={{
                        __html: t("botrytis.detection.info_step3"),
                      }}
                    ></li>
                  </ul>
                  <div className="notification  mt-4">
                    <p
                      dangerouslySetInnerHTML={{
                        __html: t("botrytis.detection.info_step4"),
                      }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="has-text-centered pt-6">
          <p className="has-text-grey-light">{t("home.return_msg")}  </p>
          <a
            className="button is-text text-color has-text-weight-semibold mt-3"
            href="/"
            aria-label="Enlace a la información del proyecto"
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
}

export default BotrytisDetection;
