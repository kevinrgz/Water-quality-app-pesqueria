# =============================================================================
# MÓDULO DE INTERNACIONALIZACIÓN (i18n)
# Calidad de Agua — Río Pesquería
# Idiomas: Español (es), Inglés (en), Portugués (pt)
# =============================================================================

IDIOMAS = {
    "es": "🇲🇽 Español",
    "en": "🇺🇸 English",
    "pt": "🇧🇷 Português",
}

T = {
    # ── Header / Encabezado ────────────────────────────────────────────────────
    "app_title": {
        "es": "💧 Water Quality Mapping",
        "en": "💧 Water Quality Mapping",
        "pt": "💧 Water Quality Mapping",
    },
    "app_subtitle": {
        "es": "Río Pesquería, Nuevo León, México · Sentinel-2 SR 2016–2019 · "
              "Universidad Autónoma de Nuevo León · FIC · Depto. Geomática",
        "en": "Pesquería River, Nuevo León, Mexico · Sentinel-2 SR 2016–2019 · "
              "Universidad Autónoma de Nuevo León · FIC · Geomatics Dept.",
        "pt": "Rio Pesquería, Nuevo León, México · Sentinel-2 SR 2016–2019 · "
              "Universidad Autónoma de Nuevo León · FIC · Depto. Geomática",
    },
    "modelo_cargado": {
        "es": "✅  Modelo cargado  ·  Datos de muestreo 2016–2019 listos",
        "en": "✅  Model loaded  ·  2016–2019 sampling data ready",
        "pt": "✅  Modelo carregado  ·  Dados de amostragem 2016–2019 prontos",
    },
    "gee_activo": {
        "es": "✅  Conexión a Google Earth Engine activa",
        "en": "✅  Google Earth Engine connection active",
        "pt": "✅  Conexão com Google Earth Engine ativa",
    },
    "gee_no_disponible": {
        "es": "⚠️  GEE no disponible — se usará imagen de referencia.",
        "en": "⚠️  GEE not available — reference imagery will be used.",
        "pt": "⚠️  GEE não disponível — será usada imagem de referência.",
    },
    "error_modelo": {
        "es": "⚠️ No se pudo cargar el modelo. Detalle:",
        "en": "⚠️ The model could not be loaded. Detail:",
        "pt": "⚠️ Não foi possível carregar o modelo. Detalhe:",
    },
    "error_csv": {
        "es": "⚠️ INDICES_completo.csv no encontrado",
        "en": "⚠️ INDICES_completo.csv not found",
        "pt": "⚠️ INDICES_completo.csv não encontrado",
    },

    # ── Sidebar ────────────────────────────────────────────────────────────────
    "sidebar_idioma": {
        "es": "🌐 Idioma", "en": "🌐 Language", "pt": "🌐 Idioma",
    },
    "sidebar_area": {
        "es": "📍 Área de estudio", "en": "📍 Study area", "pt": "📍 Área de estudo",
    },
    "sidebar_area_caption": {
        "es": "Comprime: .shp + .dbf + .prj + .cpg → ZIP",
        "en": "Zip together: .shp + .dbf + .prj + .cpg",
        "pt": "Compacte: .shp + .dbf + .prj + .cpg → ZIP",
    },
    "sidebar_upload": {
        "es": "Sube wmask.zip", "en": "Upload wmask.zip", "pt": "Envie wmask.zip",
    },
    "sidebar_fecha_muestreo": {
        "es": "🧪 Fecha de muestreo", "en": "🧪 Sampling date", "pt": "🧪 Data de amostragem",
    },
    "sidebar_rango_s2": {
        "es": "🛰️ Rango imagen Sentinel-2", "en": "🛰️ Sentinel-2 image range",
        "pt": "🛰️ Intervalo de imagem Sentinel-2",
    },
    "sidebar_desde": {"es": "Desde", "en": "From", "pt": "De"},
    "sidebar_hasta": {"es": "Hasta", "en": "To", "pt": "Até"},
    "sidebar_temp_seca": {"es": "🌵 Temporada Seca", "en": "🌵 Dry Season", "pt": "🌵 Estação Seca"},
    "sidebar_temp_lluvia": {"es": "🌧️ Temporada Lluviosa", "en": "🌧️ Rainy Season", "pt": "🌧️ Estação Chuvosa"},
    "sidebar_filtro_nubes": {
        "es": "☁️ Filtro de nubes", "en": "☁️ Cloud filter", "pt": "☁️ Filtro de nuvens",
    },
    "sidebar_max_nubes": {
        "es": "Máx. cobertura (%)", "en": "Max. coverage (%)", "pt": "Cobertura máx. (%)",
    },
    "sidebar_fecha_error": {
        "es": "⚠️ Fecha inicio debe ser anterior a fin",
        "en": "⚠️ Start date must be before end date",
        "pt": "⚠️ Data inicial deve ser anterior à final",
    },
    "sidebar_desfase": {"es": "Desfase", "en": "Offset", "pt": "Defasagem"},
    "sidebar_dias": {"es": "días", "en": "days", "pt": "dias"},
    "sidebar_parametros": {
        "es": "🔬 Parámetros a mapear", "en": "🔬 Parameters to map",
        "pt": "🔬 Parâmetros para mapear",
    },
    "sidebar_resolucion": {
        "es": "🎯 Resolución de grilla", "en": "🎯 Grid resolution",
        "pt": "🎯 Resolução da grade",
    },
    "sidebar_celdas": {"es": "celdas", "en": "cells", "pt": "células"},
    "sidebar_generar_mapas": {
        "es": "🗺️  Generar Mapas", "en": "🗺️  Generate Maps", "pt": "🗺️  Gerar Mapas",
    },
    "sidebar_sube_wmask_warn": {
        "es": "⬆️  Sube tu wmask.zip para continuar",
        "en": "⬆️  Upload your wmask.zip to continue",
        "pt": "⬆️  Envie seu wmask.zip para continuar",
    },

    # ── Pasos de uso ───────────────────────────────────────────────────────────
    "paso1_titulo": {"es": "① Shapefile", "en": "① Shapefile", "pt": "① Shapefile"},
    "paso1_texto": {
        "es": "Comprime tu shapefile en un ZIP y súbelo en el panel izquierdo. "
              "Archivos requeridos: .shp · .dbf · .prj · .cpg",
        "en": "Zip your shapefile and upload it in the left panel. "
              "Required files: .shp · .dbf · .prj · .cpg",
        "pt": "Compacte seu shapefile em um ZIP e envie-o no painel esquerdo. "
              "Arquivos necessários: .shp · .dbf · .prj · .cpg",
    },
    "paso2_titulo": {"es": "② Verifica imagen", "en": "② Check imagery", "pt": "② Verifique a imagem"},
    "paso2_texto": {
        "es": "Se busca automáticamente en GEE la imagen real con menos nubes del período.",
        "en": "GEE automatically searches for the clearest image in the chosen period.",
        "pt": "O GEE busca automaticamente a imagem real com menos nuvens do período.",
    },
    "paso3_titulo": {"es": "③ Genera y Descarga", "en": "③ Generate & Download", "pt": "③ Gere e Baixe"},
    "paso3_texto": {
        "es": "Panel PNG · Mapas individuales ZIP · Estadísticas espaciales",
        "en": "PNG panel · Individual maps ZIP · Spatial statistics",
        "pt": "Painel PNG · Mapas individuais ZIP · Estatísticas espaciais",
    },

    # ── Previsualización / mapa ────────────────────────────────────────────────
    "previsualizacion_titulo": {
        "es": "🛰️ Previsualización del Área de Estudio",
        "en": "🛰️ Study Area Preview",
        "pt": "🛰️ Pré-visualização da Área de Estudo",
    },
    "buscando_imagen": {
        "es": "Buscando imagen Sentinel-2 y calculando índices espectrales...",
        "en": "Searching Sentinel-2 imagery and computing spectral indices...",
        "pt": "Buscando imagem Sentinel-2 e calculando índices espectrais...",
    },
    "imagen_satelital_titulo": {
        "es": "🛰️ Imagen Satelital — Río Pesquería",
        "en": "🛰️ Satellite Imagery — Pesquería River",
        "pt": "🛰️ Imagem de Satélite — Rio Pesquería",
    },
    "sin_imagenes": {
        "es": "❌ Sin imágenes en este rango con menos nubes que el umbral",
        "en": "❌ No images found in this range under the cloud threshold",
        "pt": "❌ Nenhuma imagem encontrada nesse intervalo com menos nuvens que o limite",
    },
    "amplia_rango": {
        "es": "Amplía el rango de fechas o aumenta el umbral de nubes en el sidebar.",
        "en": "Widen the date range or increase the cloud threshold in the sidebar.",
        "pt": "Amplie o intervalo de datas ou aumente o limite de nuvens na barra lateral.",
    },
    "capa_referencia": {
        "es": "⚠️ Mostrando capa de referencia (Esri actual)",
        "en": "⚠️ Showing reference layer (current Esri)",
        "pt": "⚠️ Exibindo camada de referência (Esri atual)",
    },
    "no_conexion_gee": {
        "es": "No se pudo conectar a GEE.",
        "en": "Could not connect to GEE.",
        "pt": "Não foi possível conectar ao GEE.",
    },
    "imagenes_encontradas": {
        "es": "imagen(es) encontrada(s)", "en": "image(s) found", "pt": "imagem(ns) encontrada(s)",
    },
    "nubes_reales": {"es": "Nubes reales", "en": "Actual clouds", "pt": "Nuvens reais"},
    "muestreo": {"es": "Muestreo", "en": "Sampling", "pt": "Amostragem"},
    "capas_disponibles": {
        "es": "5 capas disponibles: usa el panel de capas a la derecha del mapa "
              "para alternar entre RGB, NDVI (vegetación), NDWI y MNDWI (agua), "
              "y NDTI (turbidez) — la misma imagen que usará el modelo.",
        "en": "5 layers available: use the layers panel on the right side of the map "
              "to switch between RGB, NDVI (vegetation), NDWI and MNDWI (water), "
              "and NDTI (turbidity) — the same image the model will use.",
        "pt": "5 camadas disponíveis: use o painel de camadas à direita do mapa "
              "para alternar entre RGB, NDVI (vegetação), NDWI e MNDWI (água), "
              "e NDTI (turbidez) — a mesma imagem que o modelo usará.",
    },
    "indices_disponibles_titulo": {
        "es": "📡 Índices Espectrales Disponibles en el Mapa",
        "en": "📡 Spectral Indices Available on the Map",
        "pt": "📡 Índices Espectrais Disponíveis no Mapa",
    },

    # ── Descarga TIFF ──────────────────────────────────────────────────────────
    "tiff_titulo": {
        "es": "⬇️ Descargar Capas en GeoTIFF",
        "en": "⬇️ Download Layers as GeoTIFF",
        "pt": "⬇️ Baixar Camadas em GeoTIFF",
    },
    "tiff_caption": {
        "es": "Descarga cada banda/índice como archivo .tif georreferenciado "
              "(EPSG:4326, 10m/píxel) listo para QGIS o ArcGIS.",
        "en": "Download each band/index as a georeferenced .tif file "
              "(EPSG:4326, 10m/pixel) ready for QGIS or ArcGIS.",
        "pt": "Baixe cada banda/índice como arquivo .tif georreferenciado "
              "(EPSG:4326, 10m/pixel) pronto para QGIS ou ArcGIS.",
    },
    "tiff_generando": {
        "es": "Generando enlace de descarga", "en": "Generating download link",
        "pt": "Gerando link de download",
    },
    "tiff_listo": {"es": "✅ Listo", "en": "✅ Ready", "pt": "✅ Pronto"},
    "tiff_descargar": {"es": "⬇️ Descargar", "en": "⬇️ Download", "pt": "⬇️ Baixar"},
    "tiff_error": {
        "es": "No se pudo generar el enlace", "en": "Could not generate the link",
        "pt": "Não foi possível gerar o link",
    },

    # ── Animación GIF Sentinel-2 ───────────────────────────────────────────────
    "gif_titulo": {
        "es": "🎬 Animación Temporal Sentinel-2 (GIF)",
        "en": "🎬 Sentinel-2 Time-lapse Animation (GIF)",
        "pt": "🎬 Animação Temporal Sentinel-2 (GIF)",
    },
    "gif_caption": {
        "es": "Genera un GIF animado con imágenes Sentinel-2 reales del rango de "
              "fechas que definiste arriba en el sidebar (🛰️ Rango imagen Sentinel-2). "
              "El rango se divide automáticamente en sub-períodos para mostrar la "
              "evolución temporal real del área de estudio.",
        "en": "Generate an animated GIF using real Sentinel-2 imagery from the date "
              "range defined above in the sidebar (🛰️ Sentinel-2 image range). "
              "The range is automatically split into sub-periods to show the "
              "real temporal evolution of the study area.",
        "pt": "Gere um GIF animado com imagens Sentinel-2 reais do intervalo de "
              "datas definido acima na barra lateral (🛰️ Intervalo de imagem Sentinel-2). "
              "O intervalo é dividido automaticamente em subperíodos para mostrar a "
              "evolução temporal real da área de estudo.",
    },
    "gif_capa_animar": {"es": "Capa a animar", "en": "Layer to animate", "pt": "Camada para animar"},
    "gif_max_fotogramas": {
        "es": "Máx. fotogramas", "en": "Max. frames", "pt": "Máx. quadros",
    },
    "gif_rango_actual": {"es": "Rango actual", "en": "Current range", "pt": "Intervalo atual"},
    "gif_nubes": {"es": "Nubes", "en": "Clouds", "pt": "Nuvens"},
    "gif_rango_corto_warn": {
        "es": "⚠️ El rango de fechas es corto para una animación significativa. "
              "Amplía el rango '🛰️ Rango imagen Sentinel-2' en el sidebar para "
              "cubrir varios meses o años.",
        "en": "⚠️ The date range is short for a meaningful animation. "
              "Widen the '🛰️ Sentinel-2 image range' in the sidebar to "
              "cover several months or years.",
        "pt": "⚠️ O intervalo de datas é curto para uma animação significativa. "
              "Amplie o '🛰️ Intervalo de imagem Sentinel-2' na barra lateral para "
              "cobrir vários meses ou anos.",
    },
    "gif_generar_btn": {
        "es": "🎬  Generar Animación Sentinel-2", "en": "🎬  Generate Sentinel-2 Animation",
        "pt": "🎬  Gerar Animação Sentinel-2",
    },
    "gif_generando": {
        "es": "Descargando imágenes Sentinel-2 y generando animación... "
              "(puede tardar 1-3 minutos según el número de fotogramas)",
        "en": "Downloading Sentinel-2 imagery and generating animation... "
              "(may take 1-3 minutes depending on the number of frames)",
        "pt": "Baixando imagens Sentinel-2 e gerando animação... "
              "(pode levar 1-3 minutos dependendo do número de quadros)",
    },
    "gif_exito": {
        "es": "✅ Animación generada con", "en": "✅ Animation generated with",
        "pt": "✅ Animação gerada com",
    },
    "gif_fotogramas": {"es": "fotogramas", "en": "frames", "pt": "quadros"},
    "gif_descargar_btn": {
        "es": "📥  Descargar Animación GIF", "en": "📥  Download GIF Animation",
        "pt": "📥  Baixar Animação GIF",
    },
    "gif_sin_imagenes": {
        "es": "No se encontraron suficientes imágenes Sentinel-2 sin nubes "
              "en el rango seleccionado. Intenta ampliar el rango de fechas "
              "o aumentar el umbral de nubes permitido.",
        "en": "Not enough cloud-free Sentinel-2 images were found in the "
              "selected range. Try widening the date range or increasing "
              "the allowed cloud threshold.",
        "pt": "Não foram encontradas imagens Sentinel-2 suficientes sem nuvens "
              "no intervalo selecionado. Tente ampliar o intervalo de datas "
              "ou aumentar o limite de nuvens permitido.",
    },

    # ── Bbox / info panels ─────────────────────────────────────────────────────
    "bbox_titulo": {"es": "📐 Bbox", "en": "📐 Bounding box", "pt": "📐 Caixa delimitadora"},
    "bbox_poligonos": {"es": "Polígonos", "en": "Polygons", "pt": "Polígonos"},
    "s2_titulo": {"es": "🛰️ Sentinel-2", "en": "🛰️ Sentinel-2", "pt": "🛰️ Sentinel-2"},
    "s2_coleccion": {"es": "Colección", "en": "Collection", "pt": "Coleção"},
    "s2_rango": {"es": "Rango", "en": "Range", "pt": "Intervalo"},
    "parametros_titulo_corto": {
        "es": "🔬 Parámetros", "en": "🔬 Parameters", "pt": "🔬 Parâmetros",
    },

    # ── Sección de parámetros detallada ───────────────────────────────────────
    "parametros_seccion_titulo": {
        "es": "📊 Parámetros Fisicoquímicos del Modelo",
        "en": "📊 Model Physicochemical Parameters",
        "pt": "📊 Parâmetros Físico-Químicos do Modelo",
    },
    "param_validado": {
        "es": "Validado ✓", "en": "Validated ✓", "pt": "Validado ✓",
    },
    "param_unidad": {"es": "Unidad", "en": "Unit", "pt": "Unidade"},
    "param_rango": {"es": "Rango", "en": "Range", "pt": "Faixa"},
    "param_estado": {"es": "Estado", "en": "Status", "pt": "Status"},
    "param_bueno": {"es": "🟢 Bueno", "en": "🟢 Good", "pt": "🟢 Bom"},

    # ── Puntos de muestreo ─────────────────────────────────────────────────────
    "puntos_titulo": {
        "es": "📍 Puntos de Muestreo", "en": "📍 Sampling Points",
        "pt": "📍 Pontos de Amostragem",
    },
    "sube_wmask_para_ver": {
        "es": "⬅️  Sube tu wmask.zip para ver la imagen Sentinel-2 real del área.",
        "en": "⬅️  Upload your wmask.zip to see the real Sentinel-2 image of the area.",
        "pt": "⬅️  Envie seu wmask.zip para ver a imagem Sentinel-2 real da área.",
    },
    "ph_od_nota": {
        "es": "ℹ️ pH y OD excluidos del modelo — su OOB R² fue negativo, "
              "lo que indica que Sentinel-2 no tiene señal óptica suficiente "
              "para estimar esos parámetros en este río.",
        "en": "ℹ️ pH and DO excluded from the model — their OOB R² was negative, "
              "indicating Sentinel-2 lacks sufficient optical signal "
              "to estimate those parameters in this river.",
        "pt": "ℹ️ pH e OD excluídos do modelo — seu OOB R² foi negativo, "
              "indicando que o Sentinel-2 não tem sinal óptico suficiente "
              "para estimar esses parâmetros neste rio.",
    },

    # ── Resultados (después de generar mapas) ─────────────────────────────────
    "cargando_shapefile": {
        "es": "Cargando shapefile...", "en": "Loading shapefile...", "pt": "Carregando shapefile...",
    },
    "obteniendo_imagen": {
        "es": "Obteniendo imagen satelital del área de estudio...",
        "en": "Fetching satellite image of the study area...",
        "pt": "Obtendo imagem de satélite da área de estudo...",
    },
    "generando_grilla": {
        "es": "Generando grilla...", "en": "Generating grid...", "pt": "Gerando grade...",
    },
    "aplicando_modelo": {
        "es": "Aplicando modelo RF...", "en": "Applying RF model...", "pt": "Aplicando modelo RF...",
    },
    "generando_visualizaciones": {
        "es": "Generando visualizaciones...", "en": "Generating visualizations...",
        "pt": "Gerando visualizações...",
    },
    "mapas_generados": {
        "es": "mapas —", "en": "maps —", "pt": "mapas —",
    },
    "panel_caption": {
        "es": "Panel de calidad de agua · Río Pesquería",
        "en": "Water quality panel · Pesquería River",
        "pt": "Painel de qualidade da água · Rio Pesquería",
    },
    "descargar_resultados": {
        "es": "📥 Descargar resultados", "en": "📥 Download results", "pt": "📥 Baixar resultados",
    },
    "descargar_panel_png": {
        "es": "⬇️  Panel completo PNG", "en": "⬇️  Full panel PNG", "pt": "⬇️  Painel completo PNG",
    },
    "descargar_mapas_zip": {
        "es": "⬇️  Mapas individuales ZIP", "en": "⬇️  Individual maps ZIP",
        "pt": "⬇️  Mapas individuais ZIP",
    },
    "descargar_pdf_btn": {
        "es": "📄  Reporte PDF completo", "en": "📄  Full PDF report", "pt": "📄  Relatório PDF completo",
    },
    "generando_pdf": {
        "es": "Generando reporte PDF...", "en": "Generating PDF report...",
        "pt": "Gerando relatório PDF...",
    },
    "error_pdf": {
        "es": "Error generando PDF:", "en": "Error generating PDF:",
        "pt": "Erro ao gerar PDF:",
    },
    "estadisticas_espaciales": {
        "es": "📊 Estadísticas espaciales", "en": "📊 Spatial statistics",
        "pt": "📊 Estatísticas espaciais",
    },
    "stat_media": {"es": "Media", "en": "Mean", "pt": "Média"},
    "stat_maximo": {"es": "Máximo", "en": "Maximum", "pt": "Máximo"},
    "stat_minimo": {"es": "Mínimo", "en": "Minimum", "pt": "Mínimo"},

    # ── Investigador ───────────────────────────────────────────────────────────
    "investigador_titulo": {
        "es": "👨‍🔬 Investigador Principal", "en": "👨‍🔬 Principal Investigator",
        "pt": "👨‍🔬 Pesquisador Principal",
    },
    "investigador_cargo": {
        "es": "PhD Student · Environmental Water Quality & Remote Sensing",
        "en": "PhD Student · Environmental Water Quality & Remote Sensing",
        "pt": "Doutorando · Qualidade da Água Ambiental & Sensoriamento Remoto",
    },
    "investigador_depto": {
        "es": "Departamento de Geomática · Facultad de Ingeniería Civil · UANL",
        "en": "Geomatics Department · Civil Engineering Faculty · UANL",
        "pt": "Departamento de Geomática · Faculdade de Engenharia Civil · UANL",
    },

    # ── Reporte serie temporal ─────────────────────────────────────────────────
    "serie_titulo": {
        "es": "📈 Reporte de Serie Temporal Completa",
        "en": "📈 Full Time Series Report",
        "pt": "📈 Relatório de Série Temporal Completa",
    },
    "serie_caption": {
        "es": "Genera un PDF con la evolución 2016–2019 de los parámetros "
              "seleccionados, incluyendo gráficos de tendencia, tabla resumen "
              "e interpretación automática. Requiere haber subido tu wmask.zip.",
        "en": "Generate a PDF with the 2016–2019 evolution of the selected "
              "parameters, including trend charts, summary table, and "
              "automatic interpretation. Requires your wmask.zip uploaded.",
        "pt": "Gere um PDF com a evolução 2016–2019 dos parâmetros "
              "selecionados, incluindo gráficos de tendência, tabela-resumo "
              "e interpretação automática. Requer o wmask.zip enviado.",
    },
    "serie_generar_btn": {
        "es": "📈  Generar Reporte de Serie Temporal (PDF)",
        "en": "📈  Generate Time Series Report (PDF)",
        "pt": "📈  Gerar Relatório de Série Temporal (PDF)",
    },
    "serie_sube_wmask": {
        "es": "⬅️ Sube tu wmask.zip para habilitar esta función.",
        "en": "⬅️ Upload your wmask.zip to enable this feature.",
        "pt": "⬅️ Envie seu wmask.zip para habilitar este recurso.",
    },
    "serie_min_fechas": {
        "es": "Selecciona al menos 2 fechas para crear la animación.",
        "en": "Select at least 2 dates to create the animation.",
        "pt": "Selecione pelo menos 2 datas para criar a animação.",
    },
    "serie_calculando": {
        "es": "Calculando serie temporal para todas las fechas disponibles... "
              "(puede tardar 1-2 minutos)",
        "en": "Calculating time series for all available dates... "
              "(may take 1-2 minutes)",
        "pt": "Calculando série temporal para todas as datas disponíveis... "
              "(pode levar 1-2 minutos)",
    },
    "serie_exito": {
        "es": "✅ Reporte generado con", "en": "✅ Report generated with",
        "pt": "✅ Relatório gerado com",
    },
    "serie_fechas": {"es": "fechas", "en": "dates", "pt": "datas"},
    "serie_descargar_btn": {
        "es": "📥  Descargar Reporte de Serie Temporal (PDF)",
        "en": "📥  Download Time Series Report (PDF)",
        "pt": "📥  Baixar Relatório de Série Temporal (PDF)",
    },
    "serie_sin_datos": {
        "es": "No hay suficientes fechas con datos válidos para generar la serie.",
        "en": "Not enough dates with valid data to generate the series.",
        "pt": "Não há datas suficientes com dados válidos para gerar a série.",
    },
    "serie_error": {
        "es": "Error generando reporte de serie temporal:",
        "en": "Error generating time series report:",
        "pt": "Erro ao gerar relatório de série temporal:",
    },

    # ── Footer ─────────────────────────────────────────────────────────────────
    "footer_texto": {
        "es": "Sentinel-2 SR · UANL · FIC · Depto. Geomática",
        "en": "Sentinel-2 SR · UANL · FIC · Geomatics Dept.",
        "pt": "Sentinel-2 SR · UANL · FIC · Depto. Geomática",
    },

    # ── Parámetros (etiquetas y descripciones) ────────────────────────────────
    "P_TOT_label": {"es": "Fósforo Total", "en": "Total Phosphorus", "pt": "Fósforo Total"},
    "P_TOT_desc": {
        "es": "Nutriente clave en eutrofización. Indica descargas de aguas "
              "residuales, efluentes industriales y escorrentía agrícola. "
              "Ref. NOM-001: 5 mg/L.",
        "en": "Key nutrient in eutrophication. Indicates wastewater discharges, "
              "industrial effluents, and agricultural runoff. "
              "Ref. NOM-001: 5 mg/L.",
        "pt": "Nutriente-chave na eutrofização. Indica descargas de águas "
              "residuais, efluentes industriais e escoamento agrícola. "
              "Ref. NOM-001: 5 mg/L.",
    },
    "N_NH3_label": {"es": "N-Amoniaco", "en": "Ammonia-N", "pt": "N-Amônia"},
    "N_NH3_desc": {
        "es": "Forma reducida del nitrógeno. Indicador directo de "
              "contaminación orgánica reciente. Tóxico para fauna acuática. "
              "Ref. NOM-001: 25 mg/L.",
        "en": "Reduced form of nitrogen. Direct indicator of recent organic "
              "pollution. Toxic to aquatic fauna. Ref. NOM-001: 25 mg/L.",
        "pt": "Forma reduzida do nitrogênio. Indicador direto de "
              "contaminação orgânica recente. Tóxico para a fauna aquática. "
              "Ref. NOM-001: 25 mg/L.",
    },
    "N_TOT_label": {"es": "N-Total", "en": "Total N", "pt": "N-Total"},
    "N_TOT_desc": {
        "es": "Suma de todas las formas de nitrógeno disuelto. Indicador "
              "integral de carga nitrogenada y riesgo de eutrofización del "
              "ecosistema acuático.",
        "en": "Sum of all dissolved nitrogen forms. Comprehensive indicator "
              "of nitrogen load and eutrophication risk for the aquatic "
              "ecosystem.",
        "pt": "Soma de todas as formas de nitrogênio dissolvido. Indicador "
              "integral da carga de nitrogênio e risco de eutrofização do "
              "ecossistema aquático.",
    },
    "N_TOTK_label": {"es": "N-Total Kjeldahl", "en": "Total Kjeldahl N", "pt": "N-Total Kjeldahl"},
    "N_TOTK_desc": {
        "es": "Nitrógeno orgánico + amoniaco por método Kjeldahl. Estándar "
              "internacional para evaluar carga orgánica y potencial de "
              "demanda bioquímica de oxígeno.",
        "en": "Organic nitrogen + ammonia via Kjeldahl method. International "
              "standard for assessing organic load and biochemical oxygen "
              "demand potential.",
        "pt": "Nitrogênio orgânico + amônia pelo método Kjeldahl. Padrão "
              "internacional para avaliar carga orgânica e potencial de "
              "demanda bioquímica de oxigênio.",
    },

    # ── Índices espectrales ────────────────────────────────────────────────────
    "RGB_nombre": {"es": "📷 RGB (Color natural)", "en": "📷 RGB (Natural color)", "pt": "📷 RGB (Cor natural)"},
    "NDVI_nombre": {"es": "🌿 NDVI (Vegetación)", "en": "🌿 NDVI (Vegetation)", "pt": "🌿 NDVI (Vegetação)"},
    "NDVI_desc": {
        "es": "Detecta vegetación ribereña que puede contaminar el píxel de "
              "agua. Verde=vegetación densa, café=suelo/agua.",
        "en": "Detects riparian vegetation that may contaminate the water "
              "pixel. Green=dense vegetation, brown=soil/water.",
        "pt": "Detecta vegetação ribeirinha que pode contaminar o pixel de "
              "água. Verde=vegetação densa, marrom=solo/água.",
    },
    "NDWI_nombre": {"es": "💧 NDWI (Índice de Agua)", "en": "💧 NDWI (Water Index)", "pt": "💧 NDWI (Índice de Água)"},
    "NDWI_desc": {
        "es": "Índice McFeeters. Azul intenso=agua, café=tierra. Delimita "
              "el cuerpo de agua dentro de tu wmask.",
        "en": "McFeeters index. Deep blue=water, brown=land. Delineates "
              "the water body within your wmask.",
        "pt": "Índice de McFeeters. Azul intenso=água, marrom=terra. "
              "Delimita o corpo d'água dentro do seu wmask.",
    },
    "MNDWI_nombre": {"es": "🌊 MNDWI (Agua mejorado)", "en": "🌊 MNDWI (Enhanced water)", "pt": "🌊 MNDWI (Água aprimorada)"},
    "MNDWI_desc": {
        "es": "Índice Xu, mejor para aguas turbias que NDWI estándar. "
              "Recomendado para ríos con alta carga de sedimentos.",
        "en": "Xu index, better for turbid waters than standard NDWI. "
              "Recommended for rivers with high sediment load.",
        "pt": "Índice de Xu, melhor para águas turvas do que o NDWI padrão. "
              "Recomendado para rios com alta carga de sedimentos.",
    },
    "NDTI_nombre": {"es": "🟤 NDTI (Turbidez)", "en": "🟤 NDTI (Turbidity)", "pt": "🟤 NDTI (Turbidez)"},
    "NDTI_desc": {
        "es": "Índice de turbidez normalizado. Rojo=alta turbidez, "
              "azul=agua clara. Correlaciona con SST y color del agua.",
        "en": "Normalized turbidity index. Red=high turbidity, "
              "blue=clear water. Correlates with TSS and water color.",
        "pt": "Índice de turbidez normalizado. Vermelho=alta turbidez, "
              "azul=água clara. Correlaciona-se com SST e cor da água.",
    },

    # ── PDF — Reporte fecha única ─────────────────────────────────────────────
    "pdf_titulo_reporte": {
        "es": "💧 REPORTE DE CALIDAD DE AGUA", "en": "💧 WATER QUALITY REPORT",
        "pt": "💧 RELATÓRIO DE QUALIDADE DA ÁGUA",
    },
    "pdf_subtitulo_rio": {
        "es": "Río Pesquería, Nuevo León, México",
        "en": "Pesquería River, Nuevo León, Mexico",
        "pt": "Rio Pesquería, Nuevo León, México",
    },
    "pdf_fecha_analizada": {"es": "Fecha analizada", "en": "Analyzed date", "pt": "Data analisada"},
    "pdf_temporada": {"es": "Temporada", "en": "Season", "pt": "Estação"},
    "pdf_modelo": {"es": "Modelo", "en": "Model", "pt": "Modelo"},
    "pdf_generado": {"es": "Generado", "en": "Generated", "pt": "Gerado"},
    "pdf_nota_auto": {
        "es": "Reporte generado automáticamente por el sistema de mapeo de calidad "
              "de agua del Río Pesquería, basado en sensores remotos Sentinel-2 y "
              "modelos de aprendizaje automático.",
        "en": "Report automatically generated by the Pesquería River water quality "
              "mapping system, based on Sentinel-2 remote sensing and machine "
              "learning models.",
        "pt": "Relatório gerado automaticamente pelo sistema de mapeamento de "
              "qualidade da água do Rio Pesquería, baseado em sensoriamento remoto "
              "Sentinel-2 e modelos de aprendizado de máquina.",
    },
    "pdf_sec1_titulo": {
        "es": "1. Resumen Ejecutivo", "en": "1. Executive Summary", "pt": "1. Resumo Executivo",
    },
    "pdf_sec2_titulo": {
        "es": "2. Metodología", "en": "2. Methodology", "pt": "2. Metodologia",
    },
    "pdf_metodologia_texto": {
        "es": "<b>Fuente de datos espectrales:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "bandas B1–B12 y 19 índices espectrales derivados (incluyendo NDWI, MNDWI, "
              "NDCI, NDTI, FAI, NDVI).<br/><br/>"
              "<b>Modelo predictivo:</b> Random Forest (scikit-learn), entrenado con "
              "centrado por punto (within-group), medias espectrales por sitio "
              "(between-group) e identidad del punto como features adicionales, "
              "corrigiendo la Paradoja de Simpson identificada en el análisis exploratorio.<br/><br/>"
              "<b>Interpolación espacial:</b> Radial Basis Function (RBF) con kernel "
              "thin-plate-spline, aplicada sobre los 7 puntos de muestreo y restringida "
              "al polígono del área de estudio (wmask).<br/><br/>"
              "<b>Validación:</b> K-Fold cross-validation (k=5) y Out-of-Bag (OOB) score, "
              "reportados como R² para cada parámetro.",
        "en": "<b>Spectral data source:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "bands B1–B12 and 19 derived spectral indices (including NDWI, MNDWI, "
              "NDCI, NDTI, FAI, NDVI).<br/><br/>"
              "<b>Predictive model:</b> Random Forest (scikit-learn), trained with "
              "per-point centering (within-group), per-site spectral means "
              "(between-group), and point identity as additional features, "
              "correcting the Simpson's Paradox identified during exploratory analysis.<br/><br/>"
              "<b>Spatial interpolation:</b> Radial Basis Function (RBF) with "
              "thin-plate-spline kernel, applied over the 7 sampling points and "
              "constrained to the study area polygon (wmask).<br/><br/>"
              "<b>Validation:</b> K-Fold cross-validation (k=5) and Out-of-Bag (OOB) "
              "score, reported as R² for each parameter.",
        "pt": "<b>Fonte de dados espectrais:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "bandas B1–B12 e 19 índices espectrais derivados (incluindo NDWI, MNDWI, "
              "NDCI, NDTI, FAI, NDVI).<br/><br/>"
              "<b>Modelo preditivo:</b> Random Forest (scikit-learn), treinado com "
              "centralização por ponto (within-group), médias espectrais por local "
              "(between-group) e identidade do ponto como features adicionais, "
              "corrigindo o Paradoxo de Simpson identificado na análise exploratória.<br/><br/>"
              "<b>Interpolação espacial:</b> Radial Basis Function (RBF) com kernel "
              "thin-plate-spline, aplicada sobre os 7 pontos de amostragem e restrita "
              "ao polígono da área de estudo (wmask).<br/><br/>"
              "<b>Validação:</b> K-Fold cross-validation (k=5) e Out-of-Bag (OOB) "
              "score, reportados como R² para cada parâmetro.",
    },
    "pdf_sec3_titulo": {
        "es": "3. Área de Estudio", "en": "3. Study Area", "pt": "3. Área de Estudo",
    },
    "pdf_coordenadas": {"es": "Coordenadas (bbox)", "en": "Coordinates (bbox)", "pt": "Coordenadas (bbox)"},
    "pdf_longitud": {"es": "Longitud", "en": "Longitude", "pt": "Longitude"},
    "pdf_latitud": {"es": "Latitud", "en": "Latitude", "pt": "Latitude"},
    "pdf_puntos_muestreo": {
        "es": "Puntos de muestreo", "en": "Sampling points", "pt": "Pontos de amostragem",
    },
    "pdf_estaciones_fijas": {
        "es": "estaciones fijas (Río Pesquería, Nuevo León)",
        "en": "fixed stations (Pesquería River, Nuevo León)",
        "pt": "estações fixas (Rio Pesquería, Nuevo León)",
    },
    "pdf_resolucion_s2": {
        "es": "Resolución espacial Sentinel-2",
        "en": "Sentinel-2 spatial resolution",
        "pt": "Resolução espacial Sentinel-2",
    },
    "pdf_res_detalle": {
        "es": "10 m/píxel (bandas visibles e infrarrojo cercano)",
        "en": "10 m/pixel (visible and near-infrared bands)",
        "pt": "10 m/pixel (bandas visíveis e infravermelho próximo)",
    },
    "pdf_imagen_satelital_texto": {
        "es": "Imagen satelital Sentinel-2 (composición RGB natural, bandas B4-B3-B2) "
              "del área de estudio correspondiente a la fecha analizada:",
        "en": "Sentinel-2 satellite image (natural RGB composite, bands B4-B3-B2) "
              "of the study area corresponding to the analyzed date:",
        "pt": "Imagem de satélite Sentinel-2 (composição RGB natural, bandas B4-B3-B2) "
              "da área de estudo correspondente à data analisada:",
    },
    "pdf_fuente_copernicus": {
        "es": "Fuente: Copernicus Sentinel-2 SR Harmonized, vía Google Earth Engine.",
        "en": "Source: Copernicus Sentinel-2 SR Harmonized, via Google Earth Engine.",
        "pt": "Fonte: Copernicus Sentinel-2 SR Harmonized, via Google Earth Engine.",
    },
    "pdf_sec4_titulo": {
        "es": "4. Estadísticas por Parámetro", "en": "4. Statistics by Parameter",
        "pt": "4. Estatísticas por Parâmetro",
    },
    "pdf_tabla_parametro": {"es": "Parámetro", "en": "Parameter", "pt": "Parâmetro"},
    "pdf_tabla_media": {"es": "Media", "en": "Mean", "pt": "Média"},
    "pdf_tabla_min": {"es": "Mín", "en": "Min", "pt": "Mín"},
    "pdf_tabla_max": {"es": "Máx", "en": "Max", "pt": "Máx"},
    "pdf_tabla_desv": {"es": "Desv. Est.", "en": "Std. Dev.", "pt": "Desv. Pad."},
    "pdf_oob_nota": {
        "es": "<i>OOB R² (Out-of-Bag R²): métrica de validación interna del modelo "
              "Random Forest, calculada con muestras no utilizadas en el entrenamiento "
              "de cada árbol. Valores ≥ 0.60 se consideran de buena capacidad predictiva.</i>",
        "en": "<i>OOB R² (Out-of-Bag R²): internal validation metric of the Random "
              "Forest model, computed using samples not used to train each tree. "
              "Values ≥ 0.60 are considered good predictive capacity.</i>",
        "pt": "<i>OOB R² (Out-of-Bag R²): métrica de validação interna do modelo "
              "Random Forest, calculada com amostras não utilizadas no treinamento "
              "de cada árvore. Valores ≥ 0.60 são considerados boa capacidade preditiva.</i>",
    },
    "pdf_sec5_titulo": {
        "es": "5. Descripción de Parámetros Analizados",
        "en": "5. Description of Analyzed Parameters",
        "pt": "5. Descrição dos Parâmetros Analisados",
    },
    "pdf_sec6_titulo": {
        "es": "6. Mapas de Calidad de Agua por Parámetro",
        "en": "6. Water Quality Maps by Parameter",
        "pt": "6. Mapas de Qualidade da Água por Parâmetro",
    },
    "pdf_sec6_texto": {
        "es": "Los siguientes mapas representan la interpolación espacial RBF de cada "
              "parámetro sobre el área de estudio, con los 7 puntos de muestreo "
              "señalados con su valor observado.",
        "en": "The following maps represent the RBF spatial interpolation of each "
              "parameter over the study area, with the 7 sampling points "
              "marked with their observed value.",
        "pt": "Os mapas a seguir representam a interpolação espacial RBF de cada "
              "parâmetro sobre a área de estudo, com os 7 pontos de amostragem "
              "marcados com seu valor observado.",
    },
    "pdf_sec7_titulo": {
        "es": "7. Conclusiones y Limitaciones", "en": "7. Conclusions and Limitations",
        "pt": "7. Conclusões e Limitações",
    },
    "pdf_conclusiones_texto": {
        "es": "Este reporte presenta una estimación espacial de calidad de agua basada "
              "en sensores remotos, calibrada con datos de campo. Los parámetros con "
              "mayor confiabilidad predictiva (OOB R² ≥ 0.60) son Fósforo Total, "
              "N-Amoniaco y N-Total Kjeldahl, asociados a procesos de eutrofización y "
              "contaminación orgánica detectables ópticamente.<br/><br/>"
              "<b>Limitaciones:</b> (1) La interpolación entre 7 puntos fijos introduce "
              "incertidumbre creciente con la distancia a los sitios de muestreo. "
              "(2) Parámetros sin señal óptica directa (pH, Oxígeno Disuelto) fueron "
              "excluidos del modelo por su OOB R² negativo. (3) Los resultados son "
              "válidos para las condiciones atmosféricas e hidrológicas de la fecha "
              "analizada y no deben extrapolarse sin validación adicional.",
        "en": "This report presents a spatial estimate of water quality based on "
              "remote sensing, calibrated with field data. The parameters with "
              "the highest predictive reliability (OOB R² ≥ 0.60) are Total "
              "Phosphorus, Ammonia-N, and Total Kjeldahl-N, associated with "
              "eutrophication processes and optically detectable organic "
              "pollution.<br/><br/>"
              "<b>Limitations:</b> (1) Interpolation between 7 fixed points "
              "introduces increasing uncertainty with distance from the sampling "
              "sites. (2) Parameters without direct optical signal (pH, Dissolved "
              "Oxygen) were excluded from the model due to their negative OOB R². "
              "(3) Results are valid for the atmospheric and hydrological conditions "
              "of the analyzed date and should not be extrapolated without further "
              "validation.",
        "pt": "Este relatório apresenta uma estimativa espacial de qualidade da água "
              "baseada em sensoriamento remoto, calibrada com dados de campo. Os "
              "parâmetros com maior confiabilidade preditiva (OOB R² ≥ 0.60) são "
              "Fósforo Total, N-Amônia e N-Total Kjeldahl, associados a processos "
              "de eutrofização e contaminação orgânica detectáveis opticamente.<br/><br/>"
              "<b>Limitações:</b> (1) A interpolação entre 7 pontos fixos introduz "
              "incerteza crescente com a distância dos locais de amostragem. "
              "(2) Parâmetros sem sinal óptico direto (pH, Oxigênio Dissolvido) "
              "foram excluídos do modelo devido ao seu OOB R² negativo. (3) Os "
              "resultados são válidos para as condições atmosféricas e hidrológicas "
              "da data analisada e não devem ser extrapolados sem validação adicional.",
    },
    "pdf_citar_como": {"es": "Citar como", "en": "Cite as", "pt": "Citar como"},

    # ── PDF — Reporte serie temporal ──────────────────────────────────────────
    "pdf_serie_titulo": {
        "es": "💧 REPORTE DE SERIE TEMPORAL", "en": "💧 TIME SERIES REPORT",
        "pt": "💧 RELATÓRIO DE SÉRIE TEMPORAL",
    },
    "pdf_serie_subtitulo": {
        "es": "Calidad de Agua — Río Pesquería 2016–2019",
        "en": "Water Quality — Pesquería River 2016–2019",
        "pt": "Qualidade da Água — Rio Pesquería 2016–2019",
    },
    "pdf_serie_periodo": {"es": "Período analizado", "en": "Analyzed period", "pt": "Período analisado"},
    "pdf_serie_fechas_muestreo": {
        "es": "fechas de muestreo (2016–2019)",
        "en": "sampling dates (2016–2019)",
        "pt": "datas de amostragem (2016–2019)",
    },
    "pdf_serie_parametros": {
        "es": "Parámetros", "en": "Parameters", "pt": "Parâmetros",
    },
    "pdf_serie_variables": {
        "es": "variables fisicoquímicas", "en": "physicochemical variables",
        "pt": "variáveis físico-químicas",
    },
    "pdf_serie_sec1": {
        "es": "1. Evolución Temporal por Parámetro",
        "en": "1. Temporal Evolution by Parameter",
        "pt": "1. Evolução Temporal por Parâmetro",
    },
    "pdf_serie_sec1_texto": {
        "es": "Los siguientes gráficos muestran la media espacial estimada de cada "
              "parámetro a lo largo del período de estudio, calculada sobre el área "
              "completa del wmask mediante interpolación RBF.",
        "en": "The following charts show the estimated spatial mean of each "
              "parameter throughout the study period, calculated over the entire "
              "wmask area via RBF interpolation.",
        "pt": "Os gráficos a seguir mostram a média espacial estimada de cada "
              "parâmetro ao longo do período de estudo, calculada sobre toda a "
              "área do wmask por interpolação RBF.",
    },
    "pdf_serie_media_espacial": {
        "es": "Media espacial", "en": "Spatial mean", "pt": "Média espacial",
    },
    "pdf_serie_maximo_espacial": {
        "es": "Máximo espacial", "en": "Spatial maximum", "pt": "Máximo espacial",
    },
    "pdf_serie_evolucion": {
        "es": "Evolución 2016-2019", "en": "2016-2019 Evolution", "pt": "Evolução 2016-2019",
    },
    "pdf_serie_sec2": {
        "es": "2. Tabla Resumen — Medias por Fecha",
        "en": "2. Summary Table — Means by Date",
        "pt": "2. Tabela-Resumo — Médias por Data",
    },
    "pdf_serie_fecha": {"es": "Fecha", "en": "Date", "pt": "Data"},
    "pdf_serie_sec3": {
        "es": "3. Interpretación de Tendencias",
        "en": "3. Trend Interpretation",
        "pt": "3. Interpretação de Tendências",
    },
    "pdf_serie_tendencia_incremento": {
        "es": "incremento", "en": "increase", "pt": "aumento",
    },
    "pdf_serie_tendencia_disminucion": {
        "es": "disminución", "en": "decrease", "pt": "diminuição",
    },
    "pdf_serie_tendencia_texto": {
        "es": "se observa una tendencia de",
        "en": "a trend of",
        "pt": "observa-se uma tendência de",
    },
    "pdf_serie_tendencia_texto2": {
        "es": "entre el inicio y el final del período analizado (de",
        "en": "is observed between the beginning and end of the analyzed period (from",
        "pt": "é observada entre o início e o fim do período analisado (de",
    },
    "pdf_serie_tendencia_texto3": {
        "es": "a", "en": "to", "pt": "a",
    },
    "pdf_serie_nota_metodologica": {
        "es": "<b>Nota metodológica:</b> Las variaciones temporales pueden estar "
              "influenciadas por estacionalidad (temporada seca vs. lluviosa), cambios "
              "en el caudal del río, y eventos puntuales de descarga. Se recomienda "
              "complementar este análisis con datos de precipitación y caudal para "
              "una interpretación hidrológica completa.",
        "en": "<b>Methodological note:</b> Temporal variations may be influenced by "
              "seasonality (dry vs. rainy season), changes in river flow, and "
              "point discharge events. It is recommended to complement this "
              "analysis with precipitation and flow data for a complete "
              "hydrological interpretation.",
        "pt": "<b>Nota metodológica:</b> As variações temporais podem ser "
              "influenciadas pela sazonalidade (estação seca vs. chuvosa), "
              "mudanças na vazão do rio e eventos pontuais de descarga. "
              "Recomenda-se complementar esta análise com dados de precipitação "
              "e vazão para uma interpretação hidrológica completa.",
    },
    "pdf_pagina": {"es": "Página", "en": "Page", "pt": "Página"},
    "pdf_universidad": {
        "es": "Universidad Autónoma de Nuevo León · FIC · Depto. Geomática",
        "en": "Universidad Autónoma de Nuevo León · FIC · Geomatics Dept.",
        "pt": "Universidad Autónoma de Nuevo León · FIC · Depto. Geomática",
    },

    # ── Interpretación automática del PDF ─────────────────────────────────────
    "pdf_tabla_header_param": {"es": "Parámetro", "en": "Parameter", "pt": "Parâmetro"},
    "pdf_interp_intro": {
        "es": "El análisis de calidad de agua del Río Pesquería para la fecha "
              "{fecha} ({temporada}) se realizó mediante interpolación espacial "
              "(RBF thin-plate-spline) de las predicciones del modelo Random "
              "Forest v3, entrenado con imágenes Sentinel-2 SR y datos de "
              "muestreo fisicoquímico 2016–2019.",
        "en": "The water quality analysis of the Pesquería River for the date "
              "{fecha} ({temporada}) was performed using spatial interpolation "
              "(RBF thin-plate-spline) of the Random Forest v3 model predictions, "
              "trained with Sentinel-2 SR imagery and 2016–2019 physicochemical "
              "sampling data.",
        "pt": "A análise de qualidade da água do Rio Pesquería para a data "
              "{fecha} ({temporada}) foi realizada por meio de interpolação "
              "espacial (RBF thin-plate-spline) das previsões do modelo Random "
              "Forest v3, treinado com imagens Sentinel-2 SR e dados de "
              "amostragem físico-química 2016–2019.",
    },
    "pdf_interp_criticos": {
        "es": "Los parámetros que muestran concentraciones relativamente elevadas "
              "respecto a su rango de referencia son: {nombres}. Esto podría "
              "indicar zonas con mayor influencia de descargas de aguas "
              "residuales o escorrentía con carga orgánica.",
        "en": "The parameters showing relatively elevated concentrations "
              "compared to their reference range are: {nombres}. This could "
              "indicate areas with greater influence from wastewater discharges "
              "or organic-load runoff.",
        "pt": "Os parâmetros que mostram concentrações relativamente elevadas "
              "em relação à sua faixa de referência são: {nombres}. Isso pode "
              "indicar áreas com maior influência de descargas de águas "
              "residuais ou escoamento com carga orgânica.",
    },
    "pdf_interp_normal": {
        "es": "Los parámetros mapeados se encuentran dentro de rangos moderados "
              "a bajos respecto a su escala de referencia, sin evidencia de "
              "concentraciones críticas en el período analizado.",
        "en": "The mapped parameters fall within moderate to low ranges "
              "relative to their reference scale, with no evidence of critical "
              "concentrations during the analyzed period.",
        "pt": "Os parâmetros mapeados estão dentro de faixas moderadas a baixas "
              "em relação à sua escala de referência, sem evidência de "
              "concentrações críticas no período analisado.",
    },
    "pdf_interp_cierre": {
        "es": "Es importante señalar que estos mapas representan una "
              "interpolación espacial entre 7 puntos de muestreo fijos; la "
              "incertidumbre aumenta con la distancia a los puntos de muestreo. "
              "Los valores de OOB R² (out-of-bag) indican la capacidad predictiva "
              "validada del modelo para cada parámetro, siendo más confiables "
              "aquellos con OOB R² superior a 0.60.",
        "en": "It is important to note that these maps represent a spatial "
              "interpolation between 7 fixed sampling points; uncertainty "
              "increases with distance from the sampling points. OOB R² "
              "(out-of-bag) values indicate the validated predictive capacity "
              "of the model for each parameter, with values above 0.60 being "
              "more reliable.",
        "pt": "É importante notar que esses mapas representam uma interpolação "
              "espacial entre 7 pontos de amostragem fixos; a incerteza aumenta "
              "com a distância dos pontos de amostragem. Os valores de OOB R² "
              "(out-of-bag) indicam a capacidade preditiva validada do modelo "
              "para cada parâmetro, sendo mais confiáveis aqueles com OOB R² "
              "superior a 0.60.",
    },
}


def t(key, lang="es"):
    """Traduce una clave al idioma indicado. Si no existe, retorna la clave en español."""
    entry = T.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("es", key))


def get_param_label(param_key, lang="es"):
    return t(f"{param_key}_label", lang)


def get_param_desc(param_key, lang="es"):
    return t(f"{param_key}_desc", lang)


def get_indice_nombre(idx_key, lang="es"):
    return t(f"{idx_key}_nombre", lang)


def get_indice_desc(idx_key, lang="es"):
    return t(f"{idx_key}_desc", lang)
