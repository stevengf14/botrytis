Frontend Integration - Botrytis Detection
==========================================

Integración completada con componente React listo en `svision_front`.

1) Iniciar el servidor frontend

```powershell
cd ./frontend
npm install  # si es primera vez
npm start
```

2) Acceder

   - Navegar a `http://localhost:3000/`
   - Se mostrará la interfaz con:
     - Área de carga de imagen (drag & drop o clic)
     - Vista previa de la imagen seleccionada
     - Botón "Analizar Imagen"
     - Resultado: `has_botrytis` (true/false) + `confidence` (0-100%)
