#!/usr/bin/env python3
"""
Script de Inicialización del Proyecto - VelasJaponesas
======================================================

Propósito: Crear automáticamente la estructura de carpetas obligatoria
para el Trabajo Práctico Integrador de Redes Neuronales Profundas.

Tareas:
1. Crear estructura de directorios (data/, dev/, prod/)
2. Crear subcarpetas (data/raw/, data/processed/)
3. Generar archivos .gitkeep para asegurar tracking en Git
4. Mostrar resumen visual de la estructura creada

Uso:
    python scripts/setup_project.py

Autor: VelasJaponesas Project
Fecha: Junio 2026
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Crea la estructura de directorios requerida."""
    
    # Directorio raíz del proyecto
    root_dir = Path(__file__).parent.parent
    
    # Definir estructura de directorios
    directories = [
        "data",
        "data/raw",
        "data/processed",
        "dev",
        "prod",
        "scripts",
        "notebooks",
    ]
    
    # Crear directorios
    print("🔨 Creando estructura de directorios...\n")
    created_count = 0
    
    for dir_path in directories:
        full_path = root_dir / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creada: {dir_path}/")
            created_count += 1
        else:
            print(f"⏭️  Existe: {dir_path}/")
    
    return root_dir, created_count


def create_gitkeep_files(root_dir):
    """Crea archivos .gitkeep en directorios estratégicos."""
    
    # Directorios que necesitan .gitkeep
    gitkeep_dirs = [
        "data",
        "data/raw",
        "data/processed",
        "dev",
        "prod",
        "notebooks",
    ]
    
    print("\n📌 Creando archivos .gitkeep...\n")
    gitkeep_count = 0
    
    for dir_path in gitkeep_dirs:
        gitkeep_path = root_dir / dir_path / ".gitkeep"
        if not gitkeep_path.exists():
            gitkeep_path.touch()
            print(f"✅ Creado: {dir_path}/.gitkeep")
            gitkeep_count += 1
        else:
            print(f"⏭️  Existe: {dir_path}/.gitkeep")
    
    return gitkeep_count


def display_structure(root_dir):
    """Muestra la estructura creada de forma visual."""
    
    print("\n" + "="*60)
    print("📁 ESTRUCTURA DEL PROYECTO CREADA")
    print("="*60 + "\n")
    
    tree_output = """
    VelasJaponesas/
    ├── data/                      (contiene imágenes y particiones)
    │   ├── raw/                   (imágenes originales de Roboflow)
    │   ├── processed/             (imágenes procesadas)
    │   ├── train.csv              (será generado por split_dataset.py)
    │   ├── val.csv
    │   └── test.csv
    │
    ├── dev/                       (desarrollo y experimentación)
    │
    ├── prod/                      (código para producción)
    │
    ├── scripts/
    │   ├── setup_project.py       (este script)
    │   └── split_dataset.py       (script de particionado)
    │
    ├── notebooks/                 (Jupyter notebooks)
    │
    ├── .gitignore                 (exclusiones de Git)
    └── README.md                  (documentación)
    """
    
    print(tree_output)
    print("="*60 + "\n")


def display_summary(created_dirs, created_gitkeeps, root_dir):
    """Muestra un resumen de las acciones realizadas."""
    
    print("\n✨ RESUMEN DE INICIALIZACIÓN\n")
    print(f"📂 Directorios creados/verificados: {created_dirs}")
    print(f"📌 Archivos .gitkeep creados/verificados: {created_gitkeeps}")
    print(f"📍 Ruta del proyecto: {root_dir}\n")
    
    print("✅ El proyecto está listo para comenzar.\n")
    print("🚀 Próximos pasos:")
    print("   1. Descargar el dataset desde Roboflow")
    print("   2. Extraer imágenes en: data/raw/")
    print("   3. Ejecutar: python scripts/split_dataset.py")
    print("   4. Crear entorno virtual: python -m venv venv")
    print("   5. Instalar dependencias: pip install -r requirements.txt\n")


def main():
    """Función principal."""
    
    try:
        print("\n" + "="*60)
        print("🚀 INICIALIZADOR DEL PROYECTO - VELAS JAPONESAS")
        print("="*60 + "\n")
        
        # Crear estructura de directorios
        root_dir, created_dirs = create_directory_structure()
        
        # Crear archivos .gitkeep
        created_gitkeeps = create_gitkeep_files(root_dir)
        
        # Mostrar estructura visual
        display_structure(root_dir)
        
        # Mostrar resumen
        display_summary(created_dirs, created_gitkeeps, root_dir)
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
