# VelasJaponesas - Trabajo Práctico Integrador de Redes Neuronales Profundas

## 📊 Descripción del Proyecto

Este repositorio contiene la implementación de un **modelo de Object Detection en PyTorch** para el reconocimiento automático de **patrones de velas japonesas (Candlestick Patterns)** en gráficos financieros.

**Características:**
- Dataset de 1,160 imágenes de Roboflow
- Modelo basado en Deep Learning (Redes Neuronales Profundas)
- Partición estricta: Train (70%), Validation (20%), Test (10%)
- Reproducibilidad garantizada (seed=42)

## 🗂️ Estructura del Proyecto

```
VelasJaponesas/
├── data/
│   ├── raw/                  # Imágenes originales del dataset (Roboflow)
│   ├── processed/            # Imágenes procesadas y aumentadas
│   ├── train.csv             # Índice de imágenes de entrenamiento
│   ├── val.csv               # Índice de imágenes de validación
│   └── test.csv              # Índice de imágenes de prueba
├── dev/                      # Desarrollo y experimentación
├── prod/                     # Modelos y código para producción
├── scripts/
│   ├── setup_project.py      # Script de inicialización del proyecto
│   └── split_dataset.py      # Script para particionar el dataset
├── notebooks/                # Jupyter notebooks para análisis
├── README.md                 # Este archivo
├── .gitignore                # Configuración de Git
└── requirements.txt          # Dependencias de Python
```

## 🚀 Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/Octaviores/VelasJaponesas.git
cd VelasJaponesas
```

### 2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. **Instalar dependencias** (próximamente)
```bash
pip install -r requirements.txt
```

### 4. **Ejecutar setup automático**
```bash
python scripts/setup_project.py
```

### 5. **Descargar dataset de Roboflow**
- Descargar el dataset desde [Roboflow](https://roboflow.com/)
- Extraer las imágenes en `data/raw/`

### 6. **Particionar el dataset**
```bash
python scripts/split_dataset.py
```

## 📋 Archivos Generados

### `train.csv`
Contiene la partición de entrenamiento (70% = 812 imágenes)
```csv
image_path,label_path
data/raw/image_001.jpg,data/raw/image_001.txt
data/raw/image_002.jpg,data/raw/image_002.txt
...
```

### `val.csv`
Contiene la partición de validación (20% = 232 imágenes)

### `test.csv`
Contiene la partición de prueba (10% = 116 imágenes)

## 🔧 Requisitos Técnicos

- **Python:** 3.8+
- **PyTorch:** 1.9+
- **NumPy:** 1.19+
- **Pandas:** 1.1+
- **Pillow:** 8.0+

## 📌 Notas Importantes

- **Reproducibilidad:** Todos los scripts utilizan `seed=42` para garantizar resultados consistentes
- **Límite de GitHub:** El .gitignore excluye automáticamente archivos pesados (imágenes, modelos)
- **Partición:** La división train/val/test es estricta y no se superpone

## 🤝 Contribuciones

Este es un proyecto académico para la cátedra de Redes Neuronales Profundas.

## 📄 Licencia

Especificar según corresponda.

---

**Última actualización:** Junio 2026  
**Estado:** Semana 2 - Estructura y Dataset
