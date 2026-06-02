#!/usr/bin/env python3
"""
Script de Particionado del Dataset - VelasJaponesas
===================================================

Propósito: Particionar automáticamente el dataset de 1,160 imágenes
en tres conjuntos mutuamente excluyentes:
- Train: 70% (812 imágenes)
- Val:   20% (232 imágenes)
- Test:  10% (116 imágenes)

Genera tres archivos CSV indexados livianos que mapean rutas de imágenes
y sus etiquetas correspondientes (formato YOLO).

Reproducibilidad: Utiliza seed=42 para garantizar resultados consistentes
en todas las ejecuciones y máquinas.

Uso:
    python scripts/split_dataset.py

Salida:
    - data/train.csv (812 registros)
    - data/val.csv (232 registros)
    - data/test.csv (116 registros)

Formato de CSV:
    image_path,label_path
    data/raw/image_001.jpg,data/raw/image_001.txt
    data/raw/image_002.jpg,data/raw/image_002.txt

Autor: VelasJaponesas Project
Fecha: Junio 2026
"""

import os
import sys
import csv
from pathlib import Path
from typing import List, Tuple
import random


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

SEED = 42  # Semilla para reproducibilidad
RAW_DATA_DIR = "data/raw"  # Directorio con imágenes originales
OUTPUT_DIR = "data"  # Directorio para guardar CSVs
EXPECTED_IMAGES = 1160  # Cantidad esperada de imágenes

# Proporciones de partición
TRAIN_RATIO = 0.70  # 70% = 812 imágenes
VAL_RATIO = 0.20    # 20% = 232 imágenes
TEST_RATIO = 0.10   # 10% = 116 imágenes

# Extensiones de imagen soportadas
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG'}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def set_seed(seed: int):
    """Establece la semilla para reproducibilidad."""
    random.seed(seed)
    print(f"🌱 Semilla establecida: {seed}")


def find_images(directory: str) -> List[str]:
    """
    Encuentra todas las imágenes en un directorio.
    
    Args:
        directory: Ruta del directorio
    
    Returns:
        Lista de nombres de archivo de imágenes
    """
    if not os.path.exists(directory):
        print(f"❌ Error: El directorio '{directory}' no existe.")
        sys.exit(1)
    
    images = []
    for filename in os.listdir(directory):
        if Path(filename).suffix in IMAGE_EXTENSIONS:
            images.append(filename)
    
    return sorted(images)


def get_label_filename(image_filename: str) -> str:
    """
    Obtiene el nombre del archivo de etiqueta correspondiente.
    
    Asume formato YOLO: image.jpg -> image.txt
    
    Args:
        image_filename: Nombre del archivo de imagen
    
    Returns:
        Nombre del archivo de etiqueta
    """
    return Path(image_filename).stem + ".txt"


def calculate_split_counts(total: int) -> Tuple[int, int, int]:
    """
    Calcula la cantidad de imágenes por partición.
    
    Args:
        total: Cantidad total de imágenes
    
    Returns:
        Tupla (train_count, val_count, test_count)
    """
    train_count = int(total * TRAIN_RATIO)
    val_count = int(total * VAL_RATIO)
    test_count = total - train_count - val_count
    
    return train_count, val_count, test_count


def create_csv_mapping(
    image_files: List[str],
    start_idx: int,
    count: int,
    subset_name: str
) -> List[Tuple[str, str]]:
    """
    Crea un mapeo de rutas imagen -> etiqueta para una partición.
    
    Args:
        image_files: Lista de nombres de archivo
        start_idx: Índice inicial en la lista
        count: Cantidad de imágenes para esta partición
        subset_name: Nombre del subconjunto (train/val/test)
    
    Returns:
        Lista de tuplas (image_path, label_path)
    """
    mappings = []
    end_idx = start_idx + count
    
    for image_file in image_files[start_idx:end_idx]:
        image_path = f"{RAW_DATA_DIR}/{image_file}"
        label_file = get_label_filename(image_file)
        label_path = f"{RAW_DATA_DIR}/{label_file}"
        
        mappings.append((image_path, label_path))
    
    return mappings


def save_csv(filename: str, mappings: List[Tuple[str, str]]):
    """
    Guarda un CSV con los mapeos imagen-etiqueta.
    
    Args:
        filename: Ruta del archivo CSV
        mappings: Lista de tuplas (image_path, label_path)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image_path', 'label_path'])  # Header
        writer.writerows(mappings)
    
    print(f"✅ Guardado: {filepath} ({len(mappings)} registros)")


def validate_dataset_structure(image_files: List[str]) -> bool:
    """
    Valida que existan archivos de etiqueta para todas las imágenes.
    
    Args:
        image_files: Lista de nombres de archivo de imagen
    
    Returns:
        True si la validación es exitosa, False en caso contrario
    """
    print("\n🔍 Validando estructura del dataset...")
    
    missing_labels = []
    
    for image_file in image_files:
        label_file = get_label_filename(image_file)
        label_path = os.path.join(RAW_DATA_DIR, label_file)
        
        if not os.path.exists(label_path):
            missing_labels.append((image_file, label_file))
    
    if missing_labels:
        print(f"⚠️  Advertencia: Se encontraron {len(missing_labels)} imágenes sin etiqueta:")
        for img, lbl in missing_labels[:5]:  # Mostrar primeras 5
            print(f"   - {img} (falta: {lbl})")
        if len(missing_labels) > 5:
            print(f"   ... y {len(missing_labels) - 5} más")
        return False
    
    print("✅ Todas las imágenes tienen archivos de etiqueta")
    return True


def display_statistics(train_mappings, val_mappings, test_mappings):
    """Muestra estadísticas del particionado."""
    
    total = len(train_mappings) + len(val_mappings) + len(test_mappings)
    
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DEL PARTICIONADO")
    print("="*60)
    
    print(f"\n📈 Distribución del dataset:")
    print(f"   Train: {len(train_mappings):4d} imágenes ({len(train_mappings)/total*100:5.1f}%)")
    print(f"   Val:   {len(val_mappings):4d} imágenes ({len(val_mappings)/total*100:5.1f}%)")
    print(f"   Test:  {len(test_mappings):4d} imágenes ({len(test_mappings)/total*100:5.1f}%)")
    print(f"   " + "-"*40)
    print(f"   TOTAL: {total:4d} imágenes (100.0%)")
    
    print(f"\n📍 Archivos CSV generados:")
    print(f"   - data/train.csv")
    print(f"   - data/val.csv")
    print(f"   - data/test.csv")
    
    print("\n" + "="*60 + "\n")


def main():
    """Función principal."""
    
    try:
        print("\n" + "="*60)
        print("📊 PARTICIONADOR DE DATASET - VELAS JAPONESAS")
        print("="*60 + "\n")
        
        # 1. Establecer semilla
        set_seed(SEED)
        
        # 2. Encontrar imágenes
        print(f"\n🔎 Buscando imágenes en: {RAW_DATA_DIR}")
        image_files = find_images(RAW_DATA_DIR)
        
        if not image_files:
            print(f"❌ Error: No se encontraron imágenes en {RAW_DATA_DIR}")
            sys.exit(1)
        
        print(f"✅ Encontradas {len(image_files)} imágenes")
        
        # Advertencia si la cantidad no coincide
        if len(image_files) != EXPECTED_IMAGES:
            print(f"⚠️  Advertencia: Se esperaban {EXPECTED_IMAGES} imágenes, "
                  f"pero se encontraron {len(image_files)}")
        
        # 3. Validar estructura del dataset
        validate_dataset_structure(image_files)
        
        # 4. Barajar lista de imágenes (para particionado aleatorio reproducible)
        random.shuffle(image_files)
        
        # 5. Calcular cantidades de partición
        print(f"\n📐 Calculando proporciones...")
        train_count, val_count, test_count = calculate_split_counts(len(image_files))
        print(f"   Train: {train_count} ({TRAIN_RATIO*100:.0f}%)")
        print(f"   Val:   {val_count} ({VAL_RATIO*100:.0f}%)")
        print(f"   Test:  {test_count} ({TEST_RATIO*100:.0f}%)")
        
        # 6. Crear mapeos para cada partición
        print(f"\n🔗 Creando mapeos imagen-etiqueta...")
        
        train_mappings = create_csv_mapping(image_files, 0, train_count, "train")
        val_mappings = create_csv_mapping(image_files, train_count, val_count, "val")
        test_mappings = create_csv_mapping(
            image_files, train_count + val_count, test_count, "test"
        )
        
        # 7. Guardar archivos CSV
        print(f"\n💾 Guardando archivos CSV...")
        save_csv("train.csv", train_mappings)
        save_csv("val.csv", val_mappings)
        save_csv("test.csv", test_mappings)
        
        # 8. Mostrar estadísticas
        display_statistics(train_mappings, val_mappings, test_mappings)
        
        # 9. Resumen final
        print("✨ Particionado completado exitosamente")
        print("   Seed: 42 (reproducible en cualquier máquina)")
        print("   Sin superposición entre conjuntos")
        print()
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error durante el particionado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
