import { createContext, useState, useContext, useMemo } from "react";
import { es } from "../../utils/Messages_es";
import { en } from "../../utils/Messages_en";

const LanguageContext = createContext(undefined);

export const LanguageProvider = ({ children }) => {
  const [locale, setLocale] = useState("es");
  const messages = locale === "es" ? es : en;

  const value = useMemo(
    () => ({
      locale,
      setLocale,
      t: (key) => messages[key] || key,
    }),
    [locale, messages]
  );

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error("useLanguage debe usarse dentro de un LanguageProvider");
  }
  return context;
};
