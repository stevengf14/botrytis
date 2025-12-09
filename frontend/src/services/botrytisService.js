/**
 * Servicio para comunicarse con el backend de detección de Botrytis.
 * 
 * Endpoint: POST /predict
 * Response: { has_botrytis: boolean, confidence: float }
 */

const API_BASE_URL = process.env.REACT_APP_BOTRYTIS_API_URL || 'http://localhost:5002';

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
      // Normalize response to older shape expected by UI, but preserve `found_flower` when present
      if (data.hasOwnProperty('has_botrytis')) {
        // Preserve found_flower if present, otherwise set to null
        return { ...data, found_flower: data.found_flower ?? null };
      }

      // New analyze response: { found_flower, flower_confidence, disease_label, disease_confidence }
      const has_botrytis = data.disease_label === 'botrytis';
      const confidence = data.disease_confidence ?? 0;
      return { has_botrytis, confidence, found_flower: data.found_flower ?? null };
    } catch (error) {
      console.error('Error calling botrytis prediction API:', error);
      throw error;
    }
  },
};
