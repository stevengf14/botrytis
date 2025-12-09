#!/usr/bin/env python
"""
Script de prueba para verificar que el endpoint /predict funciona correctamente.
Genera una imagen de prueba y la envía al servidor FastAPI.

Uso:
    python test_api.py [--api-url http://localhost:8000]
"""
import argparse
import requests
from PIL import Image
import io
import numpy as np
import sys


def create_dummy_image(width=224, height=224, name="dummy.jpg"):
    """Crea una imagen RGB de prueba."""
    data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(data, 'RGB')
    img.save(name)
    return name


def test_predict(api_url, image_path):
    """Envía una imagen al endpoint /predict y muestra el resultado."""
    endpoint = f"{api_url}/predict"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            print(f"Enviando imagen {image_path} a {endpoint}...")
            response = requests.post(endpoint, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ Respuesta exitosa:")
            print(f"  has_botrytis: {result.get('has_botrytis')}")
            print(f"  confidence: {result.get('confidence'):.2%}")
            return True
        else:
            print(f"\n✗ Error HTTP {response.status_code}")
            print(f"  Detalle: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"\n✗ No se pudo conectar a {api_url}")
        print("  Asegúrate de que el servidor FastAPI está corriendo en ese puerto.")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test endpoint /predict del backend Botrytis')
    parser.add_argument('--api-url', type=str, default='http://localhost:8000',
                        help='URL base del servidor FastAPI (default: http://localhost:8000)')
    parser.add_argument('--image', type=str, default='test_image.jpg',
                        help='Ruta de imagen a enviar (default: crea una aleatoria)')
    parser.add_argument('--keep', action='store_true',
                        help='Mantener imagen de prueba después de test')
    
    args = parser.parse_args()
    
    # Crear imagen de prueba si no existe
    if not args.image.endswith(('jpg', 'jpeg', 'png', 'gif')):
        print("Error: --image debe ser una ruta válida a imagen")
        sys.exit(1)
    
    if args.image == 'test_image.jpg':
        print("Creando imagen de prueba...")
        create_dummy_image(name=args.image)
    
    # Probar API
    success = test_predict(args.api_url, args.image)
    
    # Limpiar si es necesario
    if not args.keep and args.image == 'test_image.jpg':
        import os
        os.remove(args.image)
        print(f"Imagen de prueba eliminada.")
    
    sys.exit(0 if success else 1)
