import React, { useState } from 'react';
import { botrytisService } from '../../services/botrytisService';
import './BotrytisDetection.css';

function BotrytisDetection() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
      setResult(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Por favor selecciona una imagen');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await botrytisService.predictImage(selectedImage);

      // If backend explicitly reports no flower detected, show an error message
      if (data && data.found_flower === false) {
        setResult(null);
        setError('No se ha detectado una flor en la imagen. Por favor sube otra imagen que contenga la flor claramente.');
        return;
      }

      setResult(data);
    } catch (err) {
      setError(err.message || 'Error al procesar la imagen');
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
    <div className="botrytis-container">
      <div className="botrytis-header">
        <h1>Detección de Botrytis en Rosas</h1>
        <p>Sube una foto de una rosa para detectar si tiene Botrytis cinerea</p>
      </div>

      <div className="botrytis-content">
        <div className="upload-section">
          <div className="upload-box">
            <label htmlFor="imageInput" className="upload-label">
              <i className="fas fa-cloud-upload-alt"></i>
              <span>Haz clic para seleccionar una imagen</span>
            </label>
            <input
              id="imageInput"
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="file-input"
            />
          </div>

          {preview && (
            <div className="preview-section">
              <h3>Vista previa</h3>
              <img src={preview} alt="Preview" className="preview-image" />
            </div>
          )}
        </div>

        <div className="result-section">
          {error && (
            <div className="error-box">
              <i className="fas fa-exclamation-circle"></i>
              <p>{error}</p>
            </div>
          )}

          {loading && (
            <div className="loading-box">
              <div className="spinner"></div>
              <p>Analizando imagen...</p>
            </div>
          )}

          {result && !loading && (
            <div className={`result-box ${result.has_botrytis ? 'positive' : 'negative'}`}>
              <div className="result-status">
                <i
                  className={`fas ${
                    result.has_botrytis
                      ? 'fa-exclamation-triangle'
                      : 'fa-check-circle'
                  }`}
                ></i>
                <h2>
                  {result.has_botrytis ? 'Botrytis Detectada' : 'Rosa Sana'}
                </h2>
              </div>

              <div className="confidence-box">
                <p className="confidence-label">Confiabilidad:</p>
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${result.confidence * 100}%`,
                      backgroundColor: result.has_botrytis ? '#e74c3c' : '#27ae60',
                    }}
                  ></div>
                </div>
                <p className="confidence-value">
                  {(result.confidence * 100).toFixed(2)}%
                </p>
              </div>

              <div className="result-message">
                {result.has_botrytis ? (
                  <p>
                    ⚠️ Se ha detectado Botrytis en la rosa. Recomendamos
                    aplicar fungicida y aislar el espécimen afectado.
                  </p>
                ) : (
                  <p>
                    ✓ La rosa parece estar en buen estado. Continúa con el
                    monitoreo regular.
                  </p>
                )}
              </div>
            </div>
          )}

          <div className="button-group">
            <button
              onClick={handlePredict}
              disabled={!selectedImage || loading}
              className="btn-predict"
            >
              {loading ? 'Analizando...' : 'Analizar Imagen'}
            </button>
            <button onClick={handleClear} className="btn-clear">
              Limpiar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BotrytisDetection;
