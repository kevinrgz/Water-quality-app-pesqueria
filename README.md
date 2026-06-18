# 💧 Calidad de Agua — Río Pesquería

Aplicación web para mapeo de calidad de agua usando Random Forest entrenado con Sentinel-2.

## Parámetros disponibles

| Parámetro | OOB R² | Estado |
|---|---|---|
| Fósforo Total (P_TOT) | 0.684 | 🟢 Bueno |
| N-Amoniaco (N_NH3) | 0.645 | 🟢 Bueno |
| N-Total Kjeldahl (N_TOTK) | 0.662 | 🟢 Bueno |
| N-Total (N_TOT) | 0.615 | 🟢 Bueno |

## Cómo usar

1. Sube tu `modelos_rf_v3.pkl`
2. Sube tu `wmask.zip` (shapefile comprimido)
3. Sube tu `INDICES_completo.csv`
4. Selecciona fecha y parámetros
5. Haz clic en **Generar Mapas**
6. Descarga los resultados

## Archivos necesarios para subir a GitHub

- `app.py` — código de la aplicación
- `requirements.txt` — librerías necesarias

> El archivo `modelos_rf_v3.pkl` se sube directamente en la interfaz de la app,
> no en GitHub (es demasiado grande para el repositorio).

## Tecnologías

- Python + Streamlit
- Random Forest (scikit-learn)
- Sentinel-2 SR (Copernicus)
- Interpolación RBF thin-plate-spline
- GeoPandas + Shapely
