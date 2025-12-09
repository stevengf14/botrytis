#!/usr/bin/env python
"""
Script de verificación: Revisa que toda la estructura del proyecto está en orden.
Uso: python check_setup.py
"""
import os
import sys
from pathlib import Path


def check_file_exists(path, description):
    """Verifica si un archivo existe."""
    if os.path.exists(path):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ FALTA: {description}")
        return False


def check_directory_exists(path, description):
    """Verifica si un directorio existe."""
    if os.path.isdir(path):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ FALTA: {description}")
        return False


def main():
    print("=" * 70)
    print("VERIFICACIÓN DE ESTRUCTURA - BOTRYTIS DETECTION PROJECT")
    print("=" * 70)
    
    base_path = Path(__file__).parent
    all_good = True
    
    # Backend files
    print("\n[BACKEND - Archivos requeridos]")
    backend_files = [
        ("backend/requirements.txt", "requirements.txt"),
        ("backend/README.md", "Backend README"),
        ("backend/test_api.py", "Script de prueba de API"),
        ("backend/app/__init__.py", "Python package init"),
        ("backend/app/main.py", "FastAPI main"),
        ("backend/app/model.py", "Model wrapper"),
        ("backend/app/train.py", "Training script"),
        ("backend/app/schemas.py", "Pydantic schemas"),
    ]
    
    for file_path, desc in backend_files:
        full_path = base_path / file_path
        if not check_file_exists(full_path, desc):
            all_good = False
    
    # Backend directories
    print("\n[BACKEND - Directorios]")
    backend_dirs = [
        ("backend/app", "Backend app package"),
    ]
    
    for dir_path, desc in backend_dirs:
        full_path = base_path / dir_path
        if not check_directory_exists(full_path, desc):
            all_good = False
    
    # Frontend files (minimal)
    print("\n[FRONTEND - Archivos requeridos]")
    frontend_base = Path(__file__).parent / "frontend"
    frontend_files = [
        ("src/components/BotrytisDetection/BotrytisDetection.jsx", "React component"),
        ("src/components/BotrytisDetection/BotrytisDetection.css", "Component styles"),
        ("src/services/botrytisService.js", "Botrytis service"),
        (".env.example", ".env example"),
    ]
    
    for file_path, desc in frontend_files:
        full_path = frontend_base / file_path
        if not check_file_exists(full_path, desc):
            all_good = False
    
    # Frontend directories
    print("\n[FRONTEND - Directorios]")
    frontend_dirs = [
        ("src/components/BotrytisDetection", "Botrytis component directory"),
    ]
    
    for dir_path, desc in frontend_dirs:
        full_path = frontend_base / dir_path
        if not check_directory_exists(full_path, desc):
            all_good = False
    
    # Project root files
    print("\n[PROYECTO - Documentación]")
    root_files = [
        ("README.md", "Project README"),
        ("QUICK_START.md", "Quick start guide"),
        ("IMPLEMENTATION_SUMMARY.md", "Implementation summary"),
        ("DATAFLOW_DIAGRAM.md", "Data flow diagram"),
        (".gitignore", ".gitignore"),
    ]
    
    for file_path, desc in root_files:
        full_path = base_path / file_path
        if not check_file_exists(full_path, desc):
            all_good = False
    
    # Dataset directory (should exist or be created)
    print("\n[DATASET - Estado]")
    data_path = base_path / "backend" / "data"
    if os.path.isdir(data_path):
        print(f"  ✓ Dataset directory exists")
        for subset in ["train", "val"]:
            subset_path = data_path / subset
            if os.path.isdir(subset_path):
                print(f"    ✓ {subset}/ exists")
                for cls in ["healthy", "botrytis"]:
                    cls_path = subset_path / cls
                    if os.path.isdir(cls_path):
                        count = len(os.listdir(cls_path))
                        print(f"      ✓ {cls}/ ({count} files)")
                    else:
                        print(f"      ⚠ {cls}/ VACÍO - crear y agregar imágenes")
            else:
                print(f"    ⚠ {subset}/ FALTA - crear después")
    else:
        print(f"  ⚠ Dataset directory FALTA - crear en backend/data/")
    
    # Model file (optional, will be created after training)
    print("\n[MODELO - Estado]")
    model_path = base_path / "backend" / "model.pth"
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"  ✓ Modelo entrenado encontrado ({size_mb:.1f} MB)")
    else:
        print(f"  ⚠ Modelo no encontrado - se usará heurístico dummy")
        print(f"    Generar con: python backend/app/train.py --data-dir backend/data --epochs 20")
    
    # Summary
    print("\n" + "=" * 70)
    if all_good:
        print("✓ ESTRUCTURA COMPLETA - Listo para usar")
        print("\nPasos siguientes:")
        print("  1. Crear backend/.venv e instalar requirements.txt")
        print("  2. Crear dataset en backend/data/train y backend/data/val")
        print("  3. Entrenar modelo: python backend/app/train.py --data-dir backend/data")
        print("  4. Ejecutar backend: cd backend/app && uvicorn main:app --reload")
        print("  5. Ejecutar frontend: cd svision_front && npm start")
        return 0
    else:
        print("✗ FALTAN ARCHIVOS - Revisa lo marcado arriba")
        return 1


if __name__ == '__main__':
    sys.exit(main())
