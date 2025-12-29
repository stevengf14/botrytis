const API_BASE_URL = process.env.REACT_APP_BOTRYTIS_API_URL || "http://localhost:8000";

export const botrytisService = {
  async predictImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error processing image");
      }

      const data = await response.json();

      const detections = Array.isArray(data.detections) ? data.detections : [];
      const found_flower = data.status !== "no_flower_detected" && (data.total_detections > 0 || detections.length > 0);

      let has_botrytis = false;
      let maxConfidenceInfected = 0;
      let maxConfidenceHealthy = 0;

      detections.forEach((d) => {
        const label = d.label || "";
        const conf = Number(d.confidence) || 0;
        const isInfected = d.is_infected === true || label.toLowerCase().includes("botrytis");

        if (isInfected) {
          has_botrytis = true;
          maxConfidenceInfected = Math.max(maxConfidenceInfected, conf);
        } else {
          maxConfidenceHealthy = Math.max(maxConfidenceHealthy, conf);
        }
      });
      // Final confirmation using global status if needed
      if (!has_botrytis && data.status === "infected") {
        has_botrytis = true;
      }
      // Final confidence selection
      let finalConfidence = 0;
      
      if (has_botrytis) {
        finalConfidence = maxConfidenceInfected;
      } else if (found_flower) {
        finalConfidence = maxConfidenceHealthy;
      }

      return { 
        has_botrytis, 
        confidence: finalConfidence, 
        found_flower 
      };

    } catch (error) {
      console.error("Error calling prediction service:", error);
      throw error;
    }
  },
};