Frontend Integration - Botrytis Detection
==========================================

Integración completada con componente React listo en `svision_front`.

1) Configuración rápida

   - Copiar archivo `.env.example` a `.env` en `svision_front/`:

```powershell
cd svision_front
copy .env.example .env
```

   - (Opcional) Editar `REACT_APP_BOTRYTIS_API_URL` si el backend no está en localhost:8000

2) Iniciar el servidor frontend

```powershell
cd svision_front
npm install  # si es primera vez
npm start
```

3) Acceder

   - Navegar a `http://localhost:3000/botrytis-detection`
   - Se mostrará la interfaz con:
     - Área de carga de imagen (drag & drop o clic)
     - Vista previa de la imagen seleccionada
     - Botón "Analizar Imagen"
     - Resultado: `has_botrytis` (true/false) + `confidence` (0-100%)

4) Archivos añadidos

   - `src/components/BotrytisDetection/BotrytisDetection.jsx` : componente principal
   - `src/components/BotrytisDetection/BotrytisDetection.css` : estilos
   - `src/services/botrytisService.js` : servicio JS para comunicarse con API
   - `src/App.js` : ruta agregada `/botrytis-detection`
   - `.env.example` : ejemplo de configuración

5) CORS

   - El backend en `main.py` ya tiene CORS habilitado para desarrollo local.
   - En producción, cambiar `allow_origins=["*"]` por dominios específicos.
