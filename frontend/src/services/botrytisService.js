/**
 * Servicio para comunicarse con el backend de detección de Botrytis.
 * 
 * Endpoint: POST /analyze
 * Backend (FastAPI) response example:
 * {
 *   status: "infected" | "healthy" | "no_flower_detected",
 *   message: string,
 *   total_detections: number,
 *   detections: [ { box: [...], label: string, confidence: number, is_infected: boolean } ]
 * }
 */

// TODO: Ajustar la URL base según el entorno (desarrollo/producción)
const API_BASE_URL = process.env.REACT_APP_BOTRYTIS_API_URL || 'http://localhost:8000';

export const botrytisService = {
  /**
   * Envía una imagen al endpoint /predict del backend.
   * @param {File} file - Archivo de imagen a analizar
   * @returns {Promise<{has_botrytis: boolean, confidence: number}>}
   */
  async predictImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error predicting image');
      }

      const data = await response.json();

      // If backend provides legacy shape, keep it
      if (data.hasOwnProperty('has_botrytis')) {
        return { ...data, found_flower: data.found_flower ?? null };
      }

      // Map FastAPI `/analyze` response to legacy UI shape
      // Determine if any detection indicates infection
      const detections = Array.isArray(data.detections) ? data.detections : [];
      const found_flower = (data.total_detections ?? detections.length) > 0;

      // Look for infected detections (backend sets `is_infected` or labels like 'botrytis_rose')
      let has_botrytis = false;
      let confidence = 0;
      detections.forEach(d => {
        const label = d.label || '';
        const isInf = d.is_infected === true || label.toLowerCase().includes('botrytis');
        if (isInf) {
          has_botrytis = true;
          confidence = Math.max(confidence, Number(d.confidence) || 0);
        }
      });

      // Fallback: use status field if provided
      if (!has_botrytis && typeof data.status === 'string') {
        has_botrytis = data.status === 'infected';
      }

      return { has_botrytis, confidence, found_flower };
    } catch (error) {
      console.error('Error calling botrytis prediction API:', error);
      throw error;
    }
  },
};
