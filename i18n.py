# =============================================================================
# MÓDULO DE INTERNACIONALIZACIÓN (i18n)
# Calidad de Agua — Río Pesquería
# Idiomas: Español (es), Inglés (en), Portugués (pt)
# =============================================================================
import re

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
        "es": "Calidad del Agua · Índices Espectrales · Random Forest · Sentinel-2 SR · UANL · FIC · Depto. Geomática",
        "en": "Water Quality · Spectral Indices · Random Forest · Sentinel-2 SR · UANL · FIC · Geomatics Dept.",
        "pt": "Qualidade da Água · Índices Espectrais · Random Forest · Sentinel-2 SR · UANL · FIC · Depto. Geomática",
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

    # ── Reporte espectral — selección de contenido ────────────────────────────
    "rep_sel_indices": {
        "es": "Índices a incluir en el reporte",
        "en": "Indices to include in the report",
        "pt": "Índices a incluir no relatório",
    },
    "rep_sel_capas": {
        "es": "Capas / secciones adicionales",
        "en": "Additional layers / sections",
        "pt": "Camadas / seções adicionais",
    },
    "rep_capa_worldcover": {
        "es": "🟩 ESA WorldCover (Uso de Suelo)",
        "en": "🟩 ESA WorldCover (Land Use)",
        "pt": "🟩 ESA WorldCover (Uso do Solo)",
    },
    "rep_capa_series": {
        "es": "📈 Series temporales GEE",
        "en": "📈 GEE time series",
        "pt": "📈 Séries temporais GEE",
    },
    "rep_extrayendo_series": {
        "es": "Extrayendo series temporales GEE…",
        "en": "Extracting GEE time series…",
        "pt": "Extraindo séries temporais GEE…",
    },

    # ── Botones de análisis GEE ────────────────────────────────────────────────
    "btn_serie_temporal": {
        "es": "📊 Generar serie temporal",
        "en": "📊 Generate time series",
        "pt": "📊 Gerar série temporal",
    },
    "btn_cuenca": {
        "es": "🌍 Ejecutar análisis de cuenca",
        "en": "🌍 Run watershed analysis",
        "pt": "🌍 Executar análise de bacia",
    },
    "btn_perfil_espectral": {
        "es": "📡 Extraer perfil espectral",
        "en": "📡 Extract spectral profile",
        "pt": "📡 Extrair perfil espectral",
    },
    "btn_mcda": {
        "es": "🗺️ Generar mapa de riesgo MCDA",
        "en": "🗺️ Generate MCDA risk map",
        "pt": "🗺️ Gerar mapa de risco MCDA",
    },
    "btn_descargar_csv": {
        "es": "⬇ Descargar CSV", "en": "⬇ Download CSV", "pt": "⬇ Baixar CSV",
    },
    "slider_nubes": {
        "es": "Máx nubes %", "en": "Max clouds %", "pt": "Máx nuvens %",
    },
    "date_referencia": {
        "es": "Fecha referencia", "en": "Reference date", "pt": "Data de referência",
    },
    "date_muestreo": {
        "es": "Fecha de muestreo *", "en": "Sampling date *", "pt": "Data de amostragem *",
    },

    # ── Mensajes de estado (warnings, errors, info) ────────────────────────────
    "msg_contribucion_ok": {
        "es": "✅ Contribución enviada. Será revisada antes de incluirse en el modelo. ¡Gracias!",
        "en": "✅ Contribution submitted. It will be reviewed before being added to the model. Thank you!",
        "pt": "✅ Contribuição enviada. Será revisada antes de ser incluída no modelo. Obrigado!",
    },
    "msg_no_imagenes": {
        "es": "No se encontraron imágenes con los parámetros seleccionados. Amplía el rango de fechas o reduce el filtro de nubes.",
        "en": "No images found with the selected parameters. Try expanding the date range or reducing the cloud filter.",
        "pt": "Nenhuma imagem encontrada com os parâmetros selecionados. Amplie o intervalo de datas ou reduza o filtro de nuvens.",
    },
    "msg_no_s2_punto": {
        "es": "No se encontró imagen Sentinel-2 disponible en ese punto/fecha. Ajusta las coordenadas o la fecha.",
        "en": "No Sentinel-2 image available for that point/date. Adjust the coordinates or date.",
        "pt": "Nenhuma imagem Sentinel-2 disponível para esse ponto/data. Ajuste as coordenadas ou a data.",
    },
    "msg_no_s2_fecha": {
        "es": "No se encontró imagen S2 disponible para esa fecha. Amplía el rango o reduce el filtro de nubes.",
        "en": "No S2 image available for that date. Expand the range or reduce the cloud filter.",
        "pt": "Nenhuma imagem S2 disponível para essa data. Amplie o intervalo ou reduza o filtro de nuvens.",
    },
    "msg_error_cuenca": {
        "es": "No se pudo conectar con GEE para el análisis de cuenca.",
        "en": "Could not connect to GEE for watershed analysis.",
        "pt": "Não foi possível conectar ao GEE para a análise de bacia.",
    },
    "msg_sin_jrc": {
        "es": "Sin datos JRC para este polígono.",
        "en": "No JRC data for this polygon.",
        "pt": "Sem dados JRC para este polígono.",
    },
    "msg_sin_worldcover": {
        "es": "Sin datos WorldCover para esta zona.",
        "en": "No WorldCover data for this area.",
        "pt": "Sem dados WorldCover para esta área.",
    },
    "msg_pesos_mcda": {
        "es": "ℹ️ Pesos MCDA: NDCI×0.30 + NDTI×0.25 + CDOM×0.25 + AWEInsh⁻¹×0.20 | Paleta: azul (bajo) → rojo (alto riesgo)",
        "en": "ℹ️ MCDA weights: NDCI×0.30 + NDTI×0.25 + CDOM×0.25 + AWEInsh⁻¹×0.20 | Palette: blue (low) → red (high risk)",
        "pt": "ℹ️ Pesos MCDA: NDCI×0.30 + NDTI×0.25 + CDOM×0.25 + AWEInsh⁻¹×0.20 | Paleta: azul (baixo) → vermelho (alto risco)",
    },

    # ── Pantalla inicial (empty state) ─────────────────────────────────────────
    "empty_step1": {
        "es": "Sube un <b>wmask.zip</b> con tu shapefile (.shp + .dbf + .prj + .cpg) de cualquier zona",
        "en": "Upload a <b>wmask.zip</b> with your shapefile (.shp + .dbf + .prj + .cpg) for any area",
        "pt": "Carregue um <b>wmask.zip</b> com seu shapefile (.shp + .dbf + .prj + .cpg) de qualquer zona",
    },
    "empty_step2": {
        "es": "Selecciona el rango de fechas Sentinel-2 y la cobertura de nubes",
        "en": "Select the Sentinel-2 date range and cloud cover threshold",
        "pt": "Selecione o intervalo de datas Sentinel-2 e a cobertura de nuvens",
    },
    "empty_step3": {
        "es": "Obtén índices espectrales, animaciones GIF y reportes PDF para cualquier área del mundo",
        "en": "Get spectral indices, GIF animations and PDF reports for any area in the world",
        "pt": "Obtenha índices espectrais, animações GIF e relatórios PDF para qualquer área do mundo",
    },
    "empty_coords": {
        "es": "Río Pesquería · 7 puntos · 25.77°N – 25.83°N · 100.02°W – 100.35°W · EPSG:4326 · Modelo RF activo solo para esta zona",
        "en": "Pesquería River · 7 sampling points · 25.77°N – 25.83°N · 100.02°W – 100.35°W · EPSG:4326 · RF model active for this area only",
        "pt": "Rio Pesquería · 7 pontos · 25.77°N – 25.83°N · 100.02°W – 100.35°W · EPSG:4326 · Modelo RF ativo apenas para esta zona",
    },

    # ── Contribuir punto ───────────────────────────────────────────────────────
    "contribuir_expander": {
        "es": "➕  Contribuir un punto de muestreo",
        "en": "➕  Contribute a sampling point",
        "pt": "➕  Contribuir com um ponto de amostragem",
    },
    "contribuir_desc": {
        "es": "Ayuda a expandir el modelo aportando datos de campo verificados. Cada contribución es revisada antes de ser incluida.",
        "en": "Help expand the model by contributing verified field data. Each contribution is reviewed before being included.",
        "pt": "Ajude a expandir o modelo contribuindo com dados de campo verificados. Cada contribuição é revisada antes de ser incluída.",
    },

    # ── Tabla datos históricos ──────────────────────────────────────────────────
    "hist_titulo": {
        "es": "Datos históricos de campo · Serie completa",
        "en": "Historical field data · Full time series",
        "pt": "Dados históricos de campo · Série completa",
    },
    "hist_col_fecha": {"es": "Fecha", "en": "Date", "pt": "Data"},
    "hist_col_punto": {"es": "Punto", "en": "Station", "pt": "Ponto"},
    "hist_registros": {
        "es": "registros · 19 campañas · 7 puntos",
        "en": "records · 19 campaigns · 7 stations",
        "pt": "registros · 19 campanhas · 7 pontos",
    },
    "hist_badge_warn": {
        "es": "≥90% límite", "en": "≥90% limit", "pt": "≥90% limite",
    },
    "hist_badge_err": {
        "es": "Excede NOM", "en": "Exceeds NOM", "pt": "Excede NOM",
    },
    "hist_descargar_btn": {
        "es": "⬇ Descargar CSV histórico completo",
        "en": "⬇ Download full historical CSV",
        "pt": "⬇ Baixar CSV histórico completo",
    },

    # ── Hero section ───────────────────────────────────────────────────────────
    "hero_eyebrow": {
        "es": "TELEDETECCIÓN · NL, MÉXICO · UANL",
        "en": "REMOTE SENSING · NL, MEXICO · UANL",
        "pt": "SENSORIAMENTO REMOTO · NL, MÉXICO · UANL",
    },
    "hero_sub2": {
        "es": "Sube cualquier shapefile · Análisis global",
        "en": "Upload any shapefile · Global analysis",
        "pt": "Carregue qualquer shapefile · Análise global",
    },
    "hero_btn": {
        "es": "Explorar Ahora",
        "en": "Explore Now",
        "pt": "Explorar Agora",
    },
    "hero_pill_calidad": {
        "es": "Calidad del Agua", "en": "Water Quality", "pt": "Qualidade da Água",
    },
    "hero_pill_indices": {
        "es": "Índices Espectrales", "en": "Spectral Indices", "pt": "Índices Espectrais",
    },
    "hero_qlabel": {
        "es": "MONITOREO REMOTO SATELITAL",
        "en": "SATELLITE REMOTE MONITORING",
        "pt": "MONITORAMENTO REMOTO SATELITAL",
    },
    "hero_qtext_em": {
        "es": "Observar el planeta desde el espacio,",
        "en": "Observing the planet from space,",
        "pt": "Observar o planeta desde o espaço,",
    },
    "hero_qtext_rest": {
        "es": "para comprender el agua que habitamos.",
        "en": "to understand the water we inhabit.",
        "pt": "para compreender a água que habitamos.",
    },

    # ── Stepper sidebar ────────────────────────────────────────────────────────
    "stepper_titulo": {
        "es": "FLUJO DE TRABAJO", "en": "WORKFLOW", "pt": "FLUXO DE TRABALHO",
    },
    "stepper_paso1": {
        "es": "Subir shapefile (wmask.zip)",
        "en": "Upload shapefile (wmask.zip)",
        "pt": "Carregar shapefile (wmask.zip)",
    },
    "stepper_paso2": {
        "es": "Configurar fechas y nubes",
        "en": "Set dates & cloud cover",
        "pt": "Configurar datas e nuvens",
    },
    "stepper_paso3": {
        "es": "Generar mapas e índices",
        "en": "Generate maps & indices",
        "pt": "Gerar mapas e índices",
    },
    "stepper_paso4": {
        "es": "Descargar / reportes",
        "en": "Download / reports",
        "pt": "Download / relatórios",
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
    "zona_pesqueria_si": {
        "es": "✅ Área del Río Pesquería detectada — modelo de calidad de "
              "agua disponible",
        "en": "✅ Pesquería River area detected — water quality model "
              "available",
        "pt": "✅ Área do Rio Pesquería detectada — modelo de qualidade da "
              "água disponível",
    },
    "zona_pesqueria_no": {
        "es": "ℹ️ Área fuera del Río Pesquería — disponibles RGB, índices "
              "espectrales, descarga GeoTIFF y animación GIF. Los mapas de "
              "calidad de agua (parámetros fisicoquímicos) solo están "
              "disponibles para el Río Pesquería, donde el modelo fue "
              "entrenado y validado con datos de campo.",
        "en": "ℹ️ Area outside the Pesquería River — RGB, spectral indices, "
              "GeoTIFF download, and GIF animation are available. Water "
              "quality maps (physicochemical parameters) are only "
              "available for the Pesquería River, where the model was "
              "trained and validated with field data.",
        "pt": "ℹ️ Área fora do Rio Pesquería — disponíveis RGB, índices "
              "espectrais, download GeoTIFF e animação GIF. Os mapas de "
              "qualidade da água (parâmetros físico-químicos) estão "
              "disponíveis apenas para o Rio Pesquería, onde o modelo foi "
              "treinado e validado com dados de campo.",
    },
    "zona_pesqueria_boton_disabled": {
        "es": "Generar Mapas está deshabilitado: solo funciona para el "
              "área del Río Pesquería. Usa RGB/índices/GIF/TIFF para "
              "esta zona.",
        "en": "Generate Maps is disabled: it only works for the Pesquería "
              "River area. Use RGB/indices/GIF/TIFF for this zone.",
        "pt": "Gerar Mapas está desabilitado: funciona apenas para a área "
              "do Rio Pesquería. Use RGB/índices/GIF/TIFF para esta zona.",
    },

    # ── Reportes duales: Calidad de Agua vs Índices Espectrales ───────────────
    "reportes_titulo": {
        "es": "📄 Generar Reporte PDF", "en": "📄 Generate PDF Report",
        "pt": "📄 Gerar Relatório PDF",
    },
    "reportes_caption": {
        "es": "Elige el tipo de reporte que necesitas: calidad de agua "
              "(exclusivo Río Pesquería) o índices espectrales (cualquier "
              "zona del mundo).",
        "en": "Choose the type of report you need: water quality "
              "(Pesquería River exclusive) or spectral indices (any area "
              "in the world).",
        "pt": "Escolha o tipo de relatório que você precisa: qualidade da "
              "água (exclusivo do Rio Pesquería) ou índices espectrais "
              "(qualquer área do mundo).",
    },
    "reporte_calidad_titulo": {
        "es": "💧 Calidad de Agua", "en": "💧 Water Quality", "pt": "💧 Qualidade da Água",
    },
    "reporte_calidad_disponible": {
        "es": "Disponible — modelo RF validado para esta zona.",
        "en": "Available — RF model validated for this area.",
        "pt": "Disponível — modelo RF validado para esta área.",
    },
    "reporte_calidad_no_disponible": {
        "es": "No disponible — el modelo solo aplica al Río Pesquería.",
        "en": "Not available — the model only applies to the Pesquería River.",
        "pt": "Não disponível — o modelo aplica-se apenas ao Rio Pesquería.",
    },
    "reporte_calidad_btn": {
        "es": "Generar Reporte de Calidad de Agua",
        "en": "Generate Water Quality Report",
        "pt": "Gerar Relatório de Qualidade da Água",
    },
    "reporte_calidad_redirigir": {
        "es": "Usa el botón 🗺️ Generar Mapas en el sidebar y luego descarga "
              "el reporte PDF en la pantalla de resultados.",
        "en": "Use the 🗺️ Generate Maps button in the sidebar, then "
              "download the PDF report on the results screen.",
        "pt": "Use o botão 🗺️ Gerar Mapas na barra lateral e depois baixe "
              "o relatório PDF na tela de resultados.",
    },
    "reporte_espectral_titulo": {
        "es": "📡 Índices Espectrales", "en": "📡 Spectral Indices",
        "pt": "📡 Índices Espectrais",
    },
    "reporte_espectral_disponible": {
        "es": "Disponible para cualquier zona del mundo.",
        "en": "Available for any area in the world.",
        "pt": "Disponível para qualquer área do mundo.",
    },
    "reporte_espectral_btn": {
        "es": "Generar Reporte Espectral", "en": "Generate Spectral Report",
        "pt": "Gerar Relatório Espectral",
    },
    "reporte_espectral_generando": {
        "es": "Calculando estadísticas zonales y generando reporte... "
              "(puede tardar 1-2 minutos)",
        "en": "Calculating zonal statistics and generating report... "
              "(may take 1-2 minutes)",
        "pt": "Calculando estatísticas zonais e gerando relatório... "
              "(pode levar 1-2 minutos)",
    },
    "reporte_espectral_exito": {
        "es": "✅ Reporte de índices espectrales generado",
        "en": "✅ Spectral indices report generated",
        "pt": "✅ Relatório de índices espectrais gerado",
    },
    "reporte_espectral_descargar": {
        "es": "📥 Descargar Reporte Espectral (PDF)",
        "en": "📥 Download Spectral Report (PDF)",
        "pt": "📥 Baixar Relatório Espectral (PDF)",
    },
    "reporte_espectral_error": {
        "es": "Error generando reporte:", "en": "Error generating report:",
        "pt": "Erro ao gerar relatório:",
    },
    "reporte_espectral_sin_datos": {
        "es": "No se pudieron obtener suficientes datos para el reporte. "
              "Intenta ampliar el rango de fechas o el umbral de nubes.",
        "en": "Could not retrieve enough data for the report. Try widening "
              "the date range or cloud threshold.",
        "pt": "Não foi possível obter dados suficientes para o relatório. "
              "Tente ampliar o intervalo de datas ou o limite de nuvens.",
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

    "NDCI_nombre": {"es": "🌿 NDCI (Clorofila Red Edge)", "en": "🌿 NDCI (Red Edge Chlorophyll)", "pt": "🌿 NDCI (Clorofila Red Edge)"},
    "NDCI_desc": {
        "es": "Índice de clorofila usando banda red edge (B5). Verde intenso = eutrofización activa.",
        "en": "Chlorophyll index using red edge band (B5). Intense green = active eutrophication.",
        "pt": "Índice de clorofila usando banda red edge (B5). Verde intenso = eutrofização ativa.",
    },
    "SABI_nombre": {"es": "🦠 SABI (Floraciones Algales)", "en": "🦠 SABI (Algal Bloom)", "pt": "🦠 SABI (Floração de Algas)"},
    "SABI_desc": {
        "es": "Surface Algal Bloom Index. Detecta proliferación de algas y cianobacterias en superficie.",
        "en": "Surface Algal Bloom Index. Detects algae and cyanobacteria proliferation on the surface.",
        "pt": "Surface Algal Bloom Index. Detecta proliferação de algas e cianobactérias na superfície.",
    },
    "CDOM_nombre": {"es": "🟤 CDOM (Materia Orgánica Disuelta)", "en": "🟤 CDOM (Dissolved Organic Matter)", "pt": "🟤 CDOM (Matéria Orgânica Dissolvida)"},
    "CDOM_desc": {
        "es": "Proxy de materia orgánica coloreada disuelta (ratio B3/B4). Relacionado con DBO y carbono orgánico.",
        "en": "Colored dissolved organic matter proxy (B3/B4 ratio). Related to BOD and organic carbon.",
        "pt": "Proxy de matéria orgânica colorida dissolvida (razão B3/B4). Relacionado com DBO e carbono orgânico.",
    },
    "AWEInsh_nombre": {"es": "💧 AWEInsh (Extracción de Agua)", "en": "💧 AWEInsh (Water Extraction)", "pt": "💧 AWEInsh (Extração de Água)"},
    "AWEInsh_desc": {
        "es": "Automated Water Extraction Index (no shadow). Mayor precisión que NDWI en zonas urbanas. Umbral=0.",
        "en": "Automated Water Extraction Index (no shadow). More accurate than NDWI in urban areas. Threshold=0.",
        "pt": "Automated Water Extraction Index (sem sombra). Maior precisão que NDWI em zonas urbanas. Limiar=0.",
    },
    "EVI_nombre": {"es": "🌱 EVI (Vegetación Mejorado)", "en": "🌱 EVI (Enhanced Vegetation)", "pt": "🌱 EVI (Vegetação Aprimorada)"},
    "EVI_desc": {
        "es": "Enhanced Vegetation Index. Corrige efectos de suelo y atmósfera. Mejor que NDVI en zonas densas.",
        "en": "Enhanced Vegetation Index. Corrects soil and atmosphere effects. Better than NDVI in dense areas.",
        "pt": "Enhanced Vegetation Index. Corrige efeitos de solo e atmosfera. Melhor que NDVI em áreas densas.",
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
        "es": "incremento", "en": "increasing", "pt": "aumento",
    },
    "pdf_serie_tendencia_disminucion": {
        "es": "disminución", "en": "decreasing", "pt": "diminuição",
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
    # ── PDF: Reporte de Índices Espectrales (cualquier zona del mundo) ───────
    "pdf_idx_titulo_reporte": {
        "es": "📡 REPORTE DE ÍNDICES ESPECTRALES",
        "en": "📡 SPECTRAL INDICES REPORT",
        "pt": "📡 RELATÓRIO DE ÍNDICES ESPECTRAIS",
    },
    "pdf_idx_subtitulo": {
        "es": "Análisis Sentinel-2 — RGB, Vegetación, Agua y Turbidez",
        "en": "Sentinel-2 Analysis — RGB, Vegetation, Water, and Turbidity",
        "pt": "Análise Sentinel-2 — RGB, Vegetação, Água e Turbidez",
    },
    "pdf_idx_periodo_imagen": {
        "es": "Período de búsqueda", "en": "Search period", "pt": "Período de busca",
    },
    "pdf_idx_fecha_real": {
        "es": "Fecha de la imagen", "en": "Image date", "pt": "Data da imagem",
    },
    "pdf_idx_area": {
        "es": "Área del polígono", "en": "Polygon area", "pt": "Área do polígono",
    },
    "pdf_idx_nubes": {"es": "Nubes", "en": "Clouds", "pt": "Nuvens"},
    "pdf_idx_nota_auto": {
        "es": "Reporte generado automáticamente a partir de imágenes Sentinel-2 "
              "(Copernicus), procesadas en Google Earth Engine. Válido para "
              "cualquier área de estudio del planeta.",
        "en": "Report automatically generated from Sentinel-2 imagery "
              "(Copernicus), processed in Google Earth Engine. Valid for "
              "any study area on the planet.",
        "pt": "Relatório gerado automaticamente a partir de imagens Sentinel-2 "
              "(Copernicus), processadas no Google Earth Engine. Válido para "
              "qualquer área de estudo do planeta.",
    },
    "pdf_idx_sec1_titulo": {
        "es": "1. Resumen Interpretativo", "en": "1. Interpretive Summary",
        "pt": "1. Resumo Interpretativo",
    },
    "pdf_idx_interp_intro": {
        "es": "El presente análisis caracteriza espectralmente el área de "
              "estudio a partir de una imagen Sentinel-2 SR, calculando "
              "índices estandarizados de vegetación, cuerpos de agua y "
              "turbidez relativa.",
        "en": "This analysis spectrally characterizes the study area using "
              "a Sentinel-2 SR image, calculating standardized indices for "
              "vegetation, water bodies, and relative turbidity.",
        "pt": "Esta análise caracteriza espectralmente a área de estudo a "
              "partir de uma imagem Sentinel-2 SR, calculando índices "
              "padronizados de vegetação, corpos d'água e turbidez relativa.",
    },
    "pdf_idx_interp_valor_medio": {
        "es": "valor medio en el área", "en": "area mean value",
        "pt": "valor médio na área",
    },
    "pdf_idx_interp_cierre": {
        "es": "Estos índices son adimensionales (rango −1 a 1) y se calculan "
              "directamente de la reflectancia de superficie, sin necesidad "
              "de calibración local ni datos de campo — son aplicables a "
              "cualquier ecosistema o región del mundo.",
        "en": "These indices are dimensionless (range −1 to 1) and are "
              "calculated directly from surface reflectance, requiring no "
              "local calibration or field data — they are applicable to "
              "any ecosystem or region in the world.",
        "pt": "Esses índices são adimensionais (faixa −1 a 1) e são "
              "calculados diretamente a partir da refletância de "
              "superfície, sem necessidade de calibração local ou dados de "
              "campo — são aplicáveis a qualquer ecossistema ou região do "
              "mundo.",
    },
    "pdf_idx_sec2_titulo": {
        "es": "2. Metodología", "en": "2. Methodology", "pt": "2. Metodologia",
    },
    "pdf_idx_metodologia_texto": {
        "es": "<b>Fuente de datos:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "procesado vía Google Earth Engine. Se construye un mosaico de "
              "todas las escenas disponibles en el rango de fechas con menor "
              "cobertura de nubes, garantizando cobertura completa del área "
              "de estudio sin huecos.<br/><br/>"
              "<b>Índices calculados:</b><br/>"
              "• NDVI = (B8−B4)/(B8+B4) — vegetación (Tucker, 1979)<br/>"
              "• NDWI = (B3−B8)/(B3+B8) — agua superficial (McFeeters, 1996)<br/>"
              "• MNDWI = (B3−B11)/(B3+B11) — agua en zonas urbanas/turbias (Xu, 2006)<br/>"
              "• NDTI = (B4−B3)/(B4+B3) — turbidez relativa<br/><br/>"
              "<b>Estadísticas zonales:</b> calculadas mediante reduceRegion "
              "sobre la geometría completa del polígono subido, a 20 m de "
              "resolución espacial.",
        "en": "<b>Data source:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "processed via Google Earth Engine. A mosaic is built from all "
              "available scenes in the date range with the lowest cloud "
              "cover, ensuring complete coverage of the study area with no "
              "gaps.<br/><br/>"
              "<b>Calculated indices:</b><br/>"
              "• NDVI = (B8−B4)/(B8+B4) — vegetation (Tucker, 1979)<br/>"
              "• NDWI = (B3−B8)/(B3+B8) — surface water (McFeeters, 1996)<br/>"
              "• MNDWI = (B3−B11)/(B3+B11) — water in urban/turbid areas (Xu, 2006)<br/>"
              "• NDTI = (B4−B3)/(B4+B3) — relative turbidity<br/><br/>"
              "<b>Zonal statistics:</b> calculated via reduceRegion over the "
              "complete geometry of the uploaded polygon, at 20 m spatial "
              "resolution.",
        "pt": "<b>Fonte de dados:</b> Sentinel-2 SR Harmonized (Copernicus), "
              "processado via Google Earth Engine. É construído um mosaico "
              "de todas as cenas disponíveis no intervalo de datas com menor "
              "cobertura de nuvens, garantindo cobertura completa da área de "
              "estudo sem lacunas.<br/><br/>"
              "<b>Índices calculados:</b><br/>"
              "• NDVI = (B8−B4)/(B8+B4) — vegetação (Tucker, 1979)<br/>"
              "• NDWI = (B3−B8)/(B3+B8) — água superficial (McFeeters, 1996)<br/>"
              "• MNDWI = (B3−B11)/(B3+B11) — água em áreas urbanas/turvas (Xu, 2006)<br/>"
              "• NDTI = (B4−B3)/(B4+B3) — turbidez relativa<br/><br/>"
              "<b>Estatísticas zonais:</b> calculadas via reduceRegion sobre "
              "a geometria completa do polígono enviado, com resolução "
              "espacial de 20 m.",
    },
    "pdf_idx_sec3_titulo": {
        "es": "3. Área de Estudio", "en": "3. Study Area", "pt": "3. Área de Estudo",
    },
    "pdf_idx_sec4_titulo": {
        "es": "4. Estadísticas Zonales por Índice",
        "en": "4. Zonal Statistics by Index",
        "pt": "4. Estatísticas Zonais por Índice",
    },
    "pdf_idx_tabla_indice": {"es": "Índice", "en": "Index", "pt": "Índice"},
    "pdf_idx_tabla_desv": {"es": "Desv. Est.", "en": "Std. Dev.", "pt": "Desv. Pad."},
    "pdf_idx_stats_nota": {
        "es": "<i>Estadísticas calculadas sobre la totalidad del área del "
              "polígono subido (reduceRegion, 20 m/píxel). σ = desviación "
              "estándar; P50 = mediana.</i>",
        "en": "<i>Statistics calculated over the entire uploaded polygon "
              "area (reduceRegion, 20 m/pixel). σ = standard deviation; "
              "P50 = median.</i>",
        "pt": "<i>Estatísticas calculadas sobre toda a área do polígono "
              "enviado (reduceRegion, 20 m/pixel). σ = desvio padrão; "
              "P50 = mediana.</i>",
    },
    "pdf_idx_sec5_titulo": {
        "es": "5. Mapas por Índice e Interpretación",
        "en": "5. Maps by Index and Interpretation",
        "pt": "5. Mapas por Índice e Interpretação",
    },
    "pdf_idx_sec5_texto": {
        "es": "Cada mapa muestra la distribución espacial del índice "
              "correspondiente sobre el área de estudio, junto con su valor "
              "medio y la clasificación interpretativa asociada.",
        "en": "Each map shows the spatial distribution of the corresponding "
              "index over the study area, along with its mean value and "
              "associated interpretive classification.",
        "pt": "Cada mapa mostra a distribuição espacial do índice "
              "correspondente sobre a área de estudo, junto com seu valor "
              "médio e a classificação interpretativa associada.",
    },
    "pdf_idx_valor_medio_zona": {
        "es": "Valor medio en la zona", "en": "Zone mean value",
        "pt": "Valor médio na zona",
    },
    "pdf_idx_sin_datos": {
        "es": "sin datos suficientes", "en": "insufficient data",
        "pt": "dados insuficientes",
    },
    "pdf_idx_sec6_titulo": {
        "es": "6. Aplicaciones y Recomendaciones",
        "en": "6. Applications and Recommendations",
        "pt": "6. Aplicações e Recomendações",
    },
    "pdf_idx_sec6_texto": {
        "es": "Estos índices espectrales son herramientas de diagnóstico "
              "rápido aplicables a monitoreo ambiental, agricultura de "
              "precisión, gestión de cuencas, planeación urbana y estudios "
              "de cambio de cobertura del suelo. Para análisis cuantitativos "
              "que requieran unidades físicas (mg/L, NTU, etc.), se "
              "recomienda complementar con datos de campo y, si aplica, un "
              "modelo de calibración específico para la zona de interés, "
              "similar al desarrollado para el Río Pesquería en esta misma "
              "plataforma.",
        "en": "These spectral indices are rapid diagnostic tools applicable "
              "to environmental monitoring, precision agriculture, "
              "watershed management, urban planning, and land cover change "
              "studies. For quantitative analyses requiring physical units "
              "(mg/L, NTU, etc.), it is recommended to complement with "
              "field data and, if applicable, a site-specific calibration "
              "model, similar to the one developed for the Pesquería River "
              "on this same platform.",
        "pt": "Esses índices espectrais são ferramentas de diagnóstico "
              "rápido aplicáveis ao monitoramento ambiental, agricultura de "
              "precisão, gestão de bacias hidrográficas, planejamento "
              "urbano e estudos de mudança de cobertura do solo. Para "
              "análises quantitativas que exijam unidades físicas (mg/L, "
              "NTU, etc.), recomenda-se complementar com dados de campo e, "
              "se aplicável, um modelo de calibração específico para a "
              "área de interesse, semelhante ao desenvolvido para o Rio "
              "Pesquería nesta mesma plataforma.",
    },

    # ── Interpretación NDVI ────────────────────────────────────────────────────
    "pdf_idx_sin_datos_corto": {"es": "sin datos", "en": "no data", "pt": "sem dados"},
    "pdf_ndvi_agua_suelo": {
        "es": "valor negativo, típico de agua, suelo desnudo o superficies "
              "artificiales sin vegetación",
        "en": "negative value, typical of water, bare soil, or "
              "non-vegetated artificial surfaces",
        "pt": "valor negativo, típico de água, solo exposto ou superfícies "
              "artificiais sem vegetação",
    },
    "pdf_ndvi_muy_baja": {
        "es": "vegetación muy escasa o ausente (zona urbana, roca, suelo "
              "desnudo)",
        "en": "very sparse or absent vegetation (urban area, rock, bare soil)",
        "pt": "vegetação muito escassa ou ausente (área urbana, rocha, "
              "solo exposto)",
    },
    "pdf_ndvi_baja": {
        "es": "vegetación baja o dispersa (pastizal ralo, vegetación "
              "estresada o en transición)",
        "en": "low or sparse vegetation (thin grassland, stressed or "
              "transitional vegetation)",
        "pt": "vegetação baixa ou dispersa (pastagem rala, vegetação "
              "estressada ou em transição)",
    },
    "pdf_ndvi_moderada": {
        "es": "vegetación moderada (pastizal denso, cultivo en desarrollo, "
              "matorral)",
        "en": "moderate vegetation (dense grassland, developing crops, "
              "shrubland)",
        "pt": "vegetação moderada (pastagem densa, cultivo em "
              "desenvolvimento, arbusto)",
    },
    "pdf_ndvi_alta": {
        "es": "vegetación densa y vigorosa (bosque, cultivo en plenitud, "
              "vegetación ribereña sana)",
        "en": "dense and vigorous vegetation (forest, crops at peak growth, "
              "healthy riparian vegetation)",
        "pt": "vegetação densa e vigorosa (floresta, cultivo em pleno "
              "desenvolvimento, vegetação ribeirinha saudável)",
    },

    # ── Interpretación NDWI ────────────────────────────────────────────────────
    "pdf_ndwi_agua_clara": {
        "es": "alta probabilidad de cuerpo de agua, bien delimitado",
        "en": "high probability of a well-delineated water body",
        "pt": "alta probabilidade de corpo d'água bem delimitado",
    },
    "pdf_ndwi_agua_posible": {
        "es": "posible presencia de agua superficial o suelo saturado",
        "en": "possible presence of surface water or saturated soil",
        "pt": "possível presença de água superficial ou solo saturado",
    },
    "pdf_ndwi_suelo_mixto": {
        "es": "suelo o vegetación mixta, sin agua superficial dominante",
        "en": "mixed soil or vegetation, no dominant surface water",
        "pt": "solo ou vegetação mista, sem água superficial dominante",
    },
    "pdf_ndwi_vegetacion_suelo": {
        "es": "vegetación densa o suelo seco, sin señal de agua",
        "en": "dense vegetation or dry soil, no water signal",
        "pt": "vegetação densa ou solo seco, sem sinal de água",
    },

    # ── Interpretación MNDWI ───────────────────────────────────────────────────
    "pdf_mndwi_agua_clara": {
        "es": "cuerpo de agua claramente delimitado, incluso en entornos "
              "urbanos o con sombras",
        "en": "clearly delineated water body, even in urban or shadowed "
              "environments",
        "pt": "corpo d'água claramente delimitado, mesmo em ambientes "
              "urbanos ou com sombras",
    },
    "pdf_mndwi_agua_turbia": {
        "es": "agua probable, posiblemente con alta turbidez o sedimentos",
        "en": "probable water, possibly with high turbidity or sediments",
        "pt": "água provável, possivelmente com alta turbidez ou sedimentos",
    },
    "pdf_mndwi_suelo_humedo": {
        "es": "suelo húmedo o vegetación con alto contenido de agua",
        "en": "moist soil or vegetation with high water content",
        "pt": "solo úmido ou vegetação com alto teor de água",
    },
    "pdf_mndwi_suelo_seco": {
        "es": "superficie seca, urbana o con vegetación densa",
        "en": "dry, urban, or densely vegetated surface",
        "pt": "superfície seca, urbana ou com vegetação densa",
    },

    # ── Interpretación NDTI ────────────────────────────────────────────────────
    "pdf_ndti_muy_baja": {
        "es": "turbidez muy baja — agua ópticamente clara",
        "en": "very low turbidity — optically clear water",
        "pt": "turbidez muito baixa — água opticamente clara",
    },
    "pdf_ndti_baja": {
        "es": "turbidez baja — agua relativamente clara",
        "en": "low turbidity — relatively clear water",
        "pt": "turbidez baixa — água relativamente clara",
    },
    "pdf_ndti_moderada": {
        "es": "turbidez moderada — presencia visible de sedimentos en "
              "suspensión",
        "en": "moderate turbidity — visible presence of suspended sediments",
        "pt": "turbidez moderada — presença visível de sedimentos em "
              "suspensão",
    },
    "pdf_ndti_alta": {
        "es": "turbidez alta — fuerte carga de sedimentos o materia "
              "orgánica en suspensión",
        "en": "high turbidity — strong load of sediments or suspended "
              "organic matter",
        "pt": "turbidez alta — forte carga de sedimentos ou matéria "
              "orgânica em suspensão",
    },

    # ── LST (faltaba: se mostraba "LST_nombre") ───────────────────────────────
    "LST_nombre": {"es": "🌡️ LST (Temperatura Superficial)", "en": "🌡️ LST (Surface Temperature)",
                   "pt": "🌡️ LST (Temperatura de Superfície)"},
    "LST_desc": {
        "es": "Temperatura superficial en °C desde Landsat 8/9 (ST_B10), con downscaling a 10 m vía TsHARP usando NDVI Sentinel-2.",
        "en": "Surface temperature in °C from Landsat 8/9 (ST_B10), downscaled to 10 m via TsHARP using Sentinel-2 NDVI.",
        "pt": "Temperatura de superfície em °C do Landsat 8/9 (ST_B10), com downscaling para 10 m via TsHARP usando NDVI Sentinel-2.",
    },

    # ── Estado del sistema / pantalla inicial / genéricos ─────────────────────
    "status_campanas": {"es": "campañas", "en": "campaigns", "pt": "campanhas"},
    "status_puntos": {"es": "puntos", "en": "stations", "pt": "pontos"},
    "status_sistema_activo": {"es": "SISTEMA ACTIVO", "en": "SYSTEM ONLINE", "pt": "SISTEMA ATIVO"},
    "paso_label": {"es": "PASO", "en": "STEP", "pt": "PASSO"},
    "error_generico": {"es": "Error", "en": "Error", "pt": "Erro"},
    "error_sin_shp": {"es": "El ZIP no contiene un archivo .shp", "en": "The ZIP does not contain a .shp file",
                      "pt": "O ZIP não contém um arquivo .shp"},
    "temporada_seca": {"es": "Temporada seca", "en": "Dry season", "pt": "Estação seca"},
    "temporada_lluviosa": {"es": "Temporada lluviosa", "en": "Rainy season", "pt": "Estação chuvosa"},
    "meses": {"es": "meses", "en": "months", "pt": "meses"},
    "anio": {"es": "Año", "en": "Year", "pt": "Ano"},
    "mes": {"es": "Mes", "en": "Month", "pt": "Mês"},
    "coordenadas": {"es": "Coordenadas", "en": "Coordinates", "pt": "Coordenadas"},

    # ── Capas del mapa Folium ─────────────────────────────────────────────────
    "capa_jrc": {"es": "JRC Ocurrencia de agua (histórico)", "en": "JRC Water occurrence (historical)",
                 "pt": "JRC Ocorrência de água (histórico)"},
    "capa_worldcover": {"es": "ESA WorldCover 2021 (Uso de suelo)", "en": "ESA WorldCover 2021 (Land cover)",
                        "pt": "ESA WorldCover 2021 (Uso do solo)"},
    "capa_esri": {"es": "Satélite Esri (referencia)", "en": "Esri satellite (reference)", "pt": "Satélite Esri (referência)"},
    "capa_area_estudio": {"es": "Área de estudio", "en": "Study area", "pt": "Área de estudo"},
    "capas_grupo_visualizacion": {"es": "Visualización", "en": "Display", "pt": "Visualização"},
    "capas_grupo_analisis": {"es": "Capas de análisis", "en": "Analysis layers", "pt": "Camadas de análise"},

    # ── Resultados: panel, semáforo NOM, pie de página, nombres de archivo ────
    "titulo_calidad_rio": {"es": "Calidad de Agua — Río Pesquería", "en": "Water Quality — Pesquería River",
                           "pt": "Qualidade da Água — Rio Pesquería"},
    "rio_pesqueria": {"es": "Río Pesquería", "en": "Pesquería River", "pt": "Rio Pesquería"},
    "geomatica": {"es": "Geomática", "en": "Geomatics", "pt": "Geomática"},
    "eje_longitud": {"es": "Longitud (°)", "en": "Longitude (°)", "pt": "Longitude (°)"},
    "eje_latitud": {"es": "Latitud (°)", "en": "Latitude (°)", "pt": "Latitude (°)"},
    "credito_mapa": {"es": "Kevin D. Rodríguez G. · UANL · Depto. Geomática",
                     "en": "Kevin D. Rodríguez G. · UANL · Geomatics Dept.",
                     "pt": "Kevin D. Rodríguez G. · UANL · Depto. Geomática"},
    "nom_titulo": {"es": "Semáforo NOM-001-SEMARNAT-1996 · Valores por punto de muestreo",
                   "en": "NOM-001-SEMARNAT-1996 traffic light · Values by sampling station",
                   "pt": "Semáforo NOM-001-SEMARNAT-1996 · Valores por ponto de amostragem"},
    "nom_encabezado": {"es": "Norma Oficial Mexicana NOM-001-SEMARNAT-1996",
                       "en": "Mexican Official Standard NOM-001-SEMARNAT-1996",
                       "pt": "Norma Oficial Mexicana NOM-001-SEMARNAT-1996"},
    "lim_abrev": {"es": "lím.", "en": "limit", "pt": "lim."},
    "footer_depto": {"es": "Departamento de Geomática · FIC · UANL", "en": "Geomatics Department · FIC · UANL",
                     "pt": "Departamento de Geomática · FIC · UANL"},
    "footer_app": {"es": "Water Quality Mapping — Río Pesquería · NL · México",
                   "en": "Water Quality Mapping — Pesquería River · NL · Mexico",
                   "pt": "Water Quality Mapping — Rio Pesquería · NL · México"},
    "archivo_rep_calidad": {"es": "Reporte_CalidadAgua", "en": "WaterQuality_Report", "pt": "Relatorio_QualidadeAgua"},
    "archivo_rep_espectral": {"es": "Reporte_Espectral", "en": "Spectral_Report", "pt": "Relatorio_Espectral"},
    "archivo_rep_serie": {"es": "Reporte_SerieTemporal_Pesqueria", "en": "TimeSeries_Report_Pesqueria",
                          "pt": "Relatorio_SerieTemporal_Pesqueria"},
    "archivo_mapas": {"es": "mapas", "en": "maps", "pt": "mapas"},
    "archivo_mapa": {"es": "mapa", "en": "map", "pt": "mapa"},
    "archivo_animacion": {"es": "Animacion_S2", "en": "Animation_S2", "pt": "Animacao_S2"},
    "archivo_datos_campo": {"es": "datos_campo_pesqueria", "en": "field_data_pesqueria", "pt": "dados_campo_pesqueria"},
    "archivo_serie_csv": {"es": "serie", "en": "series", "pt": "serie"},
    "csv_fecha_valor": {"es": "fecha,valor", "en": "date,value", "pt": "data,valor"},

    # ── Serie temporal de índices (panel GEE) ─────────────────────────────────
    "ts_titulo": {"es": "📈 Serie temporal de índices (GEE)", "en": "📈 Index time series (GEE)",
                  "pt": "📈 Série temporal de índices (GEE)"},
    "ts_caption": {
        "es": "Evolución temporal del índice seleccionado en tu área de estudio — cada punto representa la media zonal de una imagen Sentinel-2.",
        "en": "Temporal evolution of the selected index over your study area — each point is the zonal mean of one Sentinel-2 image.",
        "pt": "Evolução temporal do índice selecionado na sua área de estudo — cada ponto representa a média zonal de uma imagem Sentinel-2.",
    },
    "ts_indice": {"es": "Índice a graficar", "en": "Index to plot", "pt": "Índice a plotar"},
    "ts_extrayendo": {"es": "Extrayendo {idx} desde GEE…", "en": "Extracting {idx} from GEE…", "pt": "Extraindo {idx} do GEE…"},
    "ts_tendencia": {"es": "Tendencia", "en": "Trend", "pt": "Tendência"},
    "ts_media_zonal": {"es": "media zonal", "en": "zonal mean", "pt": "média zonal"},
    "ts_n_imagenes": {"es": "N imágenes", "en": "N images", "pt": "N imagens"},
    "mk_ascendente": {"es": "↑ Ascendente", "en": "↑ Increasing", "pt": "↑ Crescente"},
    "mk_descendente": {"es": "↓ Descendente", "en": "↓ Decreasing", "pt": "↓ Decrescente"},
    "mk_significativa": {"es": "p<0.05 · Significativa", "en": "p<0.05 · Significant", "pt": "p<0.05 · Significativa"},
    "mk_no_significativa": {"es": "p≥0.05 · No significativa", "en": "p≥0.05 · Not significant",
                            "pt": "p≥0.05 · Não significativa"},

    # ── Análisis de cuenca (JRC + WorldCover) ─────────────────────────────────
    "cuenca_titulo": {"es": "Análisis de cuenca — JRC &amp; WorldCover", "en": "Watershed analysis — JRC &amp; WorldCover",
                      "pt": "Análise de bacia — JRC &amp; WorldCover"},
    "cuenca_caption": {
        "es": "Análisis integrado de ocurrencia histórica de agua (JRC 1984–2021) y uso de suelo (ESA WorldCover 2021) en tu área de estudio.",
        "en": "Combined analysis of historical water occurrence (JRC 1984–2021) and land cover (ESA WorldCover 2021) in your study area.",
        "pt": "Análise integrada da ocorrência histórica de água (JRC 1984–2021) e do uso do solo (ESA WorldCover 2021) na sua área de estudo.",
    },
    "cuenca_consultando": {"es": "Consultando JRC Global Surface Water y ESA WorldCover en GEE…",
                           "en": "Querying JRC Global Surface Water and ESA WorldCover in GEE…",
                           "pt": "Consultando JRC Global Surface Water e ESA WorldCover no GEE…"},
    "cuenca_occ_media": {"es": "Ocurrencia media", "en": "Mean occurrence", "pt": "Ocorrência média"},
    "cuenca_occ_media_help": {"es": "% de tiempo con agua en el período 1984-2021", "en": "% of time with water during 1984–2021",
                              "pt": "% do tempo com água no período 1984–2021"},
    "cuenca_occ_max": {"es": "Ocurrencia máx.", "en": "Max. occurrence", "pt": "Ocorrência máx."},
    "cuenca_occ_max_help": {"es": "Píxeles con presencia de agua permanente", "en": "Pixels with permanent water",
                            "pt": "Pixels com presença de água permanente"},
    "cuenca_estacionalidad": {"es": "Estacionalidad", "en": "Seasonality", "pt": "Sazonalidade"},
    "cuenca_estacionalidad_help": {"es": "Meses promedio con agua por año", "en": "Average months with water per year",
                                   "pt": "Média de meses com água por ano"},
    "cuenca_lulc_titulo": {"es": "ESA WorldCover 2021 — Uso de suelo", "en": "ESA WorldCover 2021 — Land cover",
                           "pt": "ESA WorldCover 2021 — Uso do solo"},
    "wc_10": {"es": "Árboles", "en": "Trees", "pt": "Árvores"},
    "wc_20": {"es": "Arbustos", "en": "Shrubland", "pt": "Arbustos"},
    "wc_30": {"es": "Pastizal", "en": "Grassland", "pt": "Pastagem"},
    "wc_40": {"es": "Cultivos", "en": "Cropland", "pt": "Agricultura"},
    "wc_50": {"es": "Zona urbana", "en": "Built-up", "pt": "Área urbana"},
    "wc_60": {"es": "Suelo desnudo", "en": "Bare ground", "pt": "Solo exposto"},
    "wc_70": {"es": "Nieve/Hielo", "en": "Snow/Ice", "pt": "Neve/Gelo"},
    "wc_80": {"es": "Agua permanente", "en": "Permanent water", "pt": "Água permanente"},
    "wc_90": {"es": "Humedales", "en": "Wetlands", "pt": "Áreas úmidas"},
    "wc_95": {"es": "Manglar", "en": "Mangroves", "pt": "Manguezal"},
    "wc_100": {"es": "Musgo/Liquen", "en": "Moss/Lichen", "pt": "Musgo/Líquen"},
    "wc_otro": {"es": "Clase {k}", "en": "Class {k}", "pt": "Classe {k}"},

    # ── Perfil espectral ──────────────────────────────────────────────────────
    "perfil_titulo": {"es": "Perfil espectral interactivo — Sentinel-2", "en": "Interactive spectral profile — Sentinel-2",
                      "pt": "Perfil espectral interativo — Sentinel-2"},
    "perfil_caption": {
        "es": "Ingresa las coordenadas de un punto en tu área de estudio para extraer la reflectancia de todas las bandas Sentinel-2.",
        "en": "Enter the coordinates of a point in your study area to extract the reflectance of every Sentinel-2 band.",
        "pt": "Insira as coordenadas de um ponto na sua área de estudo para extrair a refletância de todas as bandas Sentinel-2.",
    },
    "perfil_consultando": {"es": "Consultando GEE para el perfil espectral…", "en": "Querying GEE for the spectral profile…",
                           "pt": "Consultando o GEE para o perfil espectral…"},
    "reflectancia": {"es": "Reflectancia", "en": "Reflectance", "pt": "Refletância"},
    "perfil_firma": {"es": "Firma espectral", "en": "Spectral signature", "pt": "Assinatura espectral"},
    "perfil_en_punto": {"es": "{idx} en el punto", "en": "{idx} at the point", "pt": "{idx} no ponto"},

    # ── Mapa de riesgo MCDA ───────────────────────────────────────────────────
    "mcda_titulo": {"es": "Mapa de riesgo de contaminación — MCDA", "en": "Pollution risk map — MCDA",
                    "pt": "Mapa de risco de contaminação — MCDA"},
    "mcda_caption": {
        "es": "Índice compuesto de riesgo = 0.30·NDCI + 0.25·NDTI + 0.25·CDOM + 0.20·AWEInsh⁻¹ (escala 0–1, donde 1 = mayor riesgo potencial de contaminación).",
        "en": "Composite risk index = 0.30·NDCI + 0.25·NDTI + 0.25·CDOM + 0.20·AWEInsh⁻¹ (0–1 scale, where 1 = highest potential pollution risk).",
        "pt": "Índice composto de risco = 0.30·NDCI + 0.25·NDTI + 0.25·CDOM + 0.20·AWEInsh⁻¹ (escala 0–1, onde 1 = maior risco potencial de contaminação).",
    },
    "mcda_calculando": {"es": "Calculando composite MCDA en GEE…", "en": "Computing MCDA composite in GEE…",
                        "pt": "Calculando composto MCDA no GEE…"},
    "mcda_capa": {"es": "Riesgo MCDA", "en": "MCDA risk", "pt": "Risco MCDA"},
    "mcda_centro": {"es": "Centro del área de estudio", "en": "Study area center", "pt": "Centro da área de estudo"},
    "mcda_riesgo_medio": {"es": "Riesgo medio zonal", "en": "Mean zonal risk", "pt": "Risco médio zonal"},
    "mcda_riesgo_max": {"es": "Riesgo máximo", "en": "Maximum risk", "pt": "Risco máximo"},
    "nivel_alto": {"es": "ALTO", "en": "HIGH", "pt": "ALTO"},
    "nivel_medio": {"es": "MEDIO", "en": "MEDIUM", "pt": "MÉDIO"},
    "nivel_bajo": {"es": "BAJO", "en": "LOW", "pt": "BAIXO"},

    # ── Formulario de contribución ────────────────────────────────────────────
    "form_rio": {"es": "Nombre del río *", "en": "River name *", "pt": "Nome do rio *"},
    "form_rio_ph": {"es": "Ej. Río Bravo", "en": "e.g. Rio Grande", "pt": "Ex. Rio Bravo"},
    "form_estado": {"es": "Estado / Municipio *", "en": "State / Municipality *", "pt": "Estado / Município *"},
    "form_estado_ph": {"es": "Ej. Tamaulipas", "en": "e.g. Tamaulipas", "pt": "Ex. Tamaulipas"},
    "form_nombre": {"es": "Tu nombre *", "en": "Your name *", "pt": "Seu nome *"},
    "form_nombre_ph": {"es": "Ej. Juan Pérez", "en": "e.g. Jane Smith", "pt": "Ex. João Silva"},
    "form_inst": {"es": "Institución / Organización", "en": "Institution / Organization", "pt": "Instituição / Organização"},
    "form_inst_ph": {"es": "Ej. UANL, CONAGUA, IMTA", "en": "e.g. UANL, CONAGUA, IMTA", "pt": "Ex. UANL, CONAGUA, IMTA"},
    "form_lat": {"es": "Latitud *", "en": "Latitude *", "pt": "Latitude *"},
    "form_lon": {"es": "Longitud *", "en": "Longitude *", "pt": "Longitude *"},
    "form_fuente": {"es": "Fuente de los datos *", "en": "Data source *", "pt": "Fonte dos dados *"},
    "fuente_tesis": {"es": "Tesis/Artículo científico", "en": "Thesis/Scientific paper", "pt": "Tese/Artigo científico"},
    "fuente_reporte": {"es": "Reporte institucional", "en": "Institutional report", "pt": "Relatório institucional"},
    "fuente_otra": {"es": "Otra", "en": "Other", "pt": "Outra"},
    "form_params": {"es": "**Parámetros fisicoquímicos** (al menos uno requerido)",
                    "en": "**Physicochemical parameters** (at least one required)",
                    "pt": "**Parâmetros físico-químicos** (pelo menos um obrigatório)"},
    "form_url": {"es": "URL o referencia de la evidencia *", "en": "Evidence URL or reference *",
                 "pt": "URL ou referência da evidência *"},
    "form_url_ph": {"es": "https://... o cita bibliográfica completa", "en": "https://... or full bibliographic citation",
                    "pt": "https://... ou citação bibliográfica completa"},
    "form_notas": {"es": "Notas adicionales (opcional)", "en": "Additional notes (optional)", "pt": "Notas adicionais (opcional)"},
    "form_notas_ph": {"es": "Método de análisis, condiciones del muestreo, etc.",
                      "en": "Analysis method, sampling conditions, etc.",
                      "pt": "Método de análise, condições da amostragem, etc."},
    "form_enviar": {"es": "📤  Enviar contribución", "en": "📤  Submit contribution", "pt": "📤  Enviar contribuição"},
    "form_req_rio": {"es": "Nombre del río", "en": "River name", "pt": "Nome do rio"},
    "form_req_estado": {"es": "Estado/Municipio", "en": "State/Municipality", "pt": "Estado/Município"},
    "form_req_nombre": {"es": "Tu nombre", "en": "Your name", "pt": "Seu nome"},
    "form_req_url": {"es": "URL/referencia de evidencia", "en": "Evidence URL/reference", "pt": "URL/referência da evidência"},
    "form_req_param": {"es": "Al menos un parámetro fisicoquímico (> 0)", "en": "At least one physicochemical parameter (> 0)",
                       "pt": "Pelo menos um parâmetro físico-químico (> 0)"},
    "form_campos_req": {"es": "Campos requeridos:", "en": "Required fields:", "pt": "Campos obrigatórios:"},
    "form_error_envio": {"es": "Error al enviar ({code}). Intenta de nuevo.", "en": "Submission failed ({code}). Please try again.",
                         "pt": "Erro ao enviar ({code}). Tente novamente."},
    "form_error_conexion": {"es": "Error de conexión:", "en": "Connection error:", "pt": "Erro de conexão:"},

    # ── Sección ENSO (interfaz) ───────────────────────────────────────────────
    "enso_titulo": {"es": "Variables climáticas oceánicas — ENSO · El Niño / La Niña",
                    "en": "Ocean climate variables — ENSO · El Niño / La Niña",
                    "pt": "Variáveis climáticas oceânicas — ENSO · El Niño / La Niña"},
    "enso_intro": {
        "es": "Análisis de la <b>Temperatura Superficial del Mar (SST)</b>, sus anomalías y la <b>Clorofila-a</b> "
              "oceánica en la región <b>Niño 3.4</b> (5°N–5°S · 170°W–120°W). "
              "Fuente: NOAA CDR OISST v2.1 · NASA MODIS-Aqua · Google Earth Engine. "
              "La anomalía positiva (≥+0.5°C) indica {nino}; la negativa (≤−0.5°C) indica {nina}. "
              "En años El Niño la clorofila disminuye; en La Niña aumenta por mayor surgencia.",
        "en": "Analysis of <b>Sea Surface Temperature (SST)</b>, its anomalies and ocean <b>Chlorophyll-a</b> "
              "in the <b>Niño 3.4</b> region (5°N–5°S · 170°W–120°W). "
              "Source: NOAA CDR OISST v2.1 · NASA MODIS-Aqua · Google Earth Engine. "
              "A positive anomaly (≥+0.5°C) indicates {nino}; a negative one (≤−0.5°C) indicates {nina}. "
              "Chlorophyll decreases in El Niño years and increases in La Niña years due to stronger upwelling.",
        "pt": "Análise da <b>Temperatura da Superfície do Mar (SST)</b>, suas anomalias e a <b>Clorofila-a</b> "
              "oceânica na região <b>Niño 3.4</b> (5°N–5°S · 170°W–120°W). "
              "Fonte: NOAA CDR OISST v2.1 · NASA MODIS-Aqua · Google Earth Engine. "
              "A anomalia positiva (≥+0.5°C) indica {nino}; a negativa (≤−0.5°C) indica {nina}. "
              "Em anos de El Niño a clorofila diminui; em La Niña aumenta devido à maior ressurgência.",
    },
    "enso_expander_mapa": {"es": "Mapa oceánico — SST / Anomalía / Clorofila-a", "en": "Ocean map — SST / Anomaly / Chlorophyll-a",
                           "pt": "Mapa oceânico — SST / Anomalia / Clorofila-a"},
    "enso_leg_anomalia": {"es": "Anomalía:", "en": "Anomaly:", "pt": "Anomalia:"},
    "enso_leg_clorofila": {"es": "Clorofila:", "en": "Chlorophyll:", "pt": "Clorofila:"},
    "enso_leg_chl_fuente": {"es": "(2002–hoy · MODIS-Aqua / VIIRS-Snpp)", "en": "(2002–present · MODIS-Aqua / VIIRS-Snpp)",
                            "pt": "(2002–hoje · MODIS-Aqua / VIIRS-Snpp)"},
    "enso_cargando": {"es": "Cargando {periodo} y eventos de referencia…", "en": "Loading {periodo} and reference events…",
                      "pt": "Carregando {periodo} e eventos de referência…"},
    "enso_capa_anomalia": {"es": "Anomalía SST", "en": "SST anomaly", "pt": "Anomalia SST"},
    "clorofila_a": {"es": "Clorofila-a", "en": "Chlorophyll-a", "pt": "Clorofila-a"},
    "enso_region": {"es": "Región Niño 3.4", "en": "Niño 3.4 region", "pt": "Região Niño 3.4"},
    "enso_umbral_nino": {"es": "Umbral El Niño", "en": "El Niño threshold", "pt": "Limiar El Niño"},
    "enso_neutral": {"es": "Neutral", "en": "Neutral", "pt": "Neutro"},
    "enso_grupo_periodo": {"es": "Datos del período", "en": "Selected period", "pt": "Dados do período"},
    "enso_grupo_referencia": {"es": "Capas de referencia", "en": "Reference layers", "pt": "Camadas de referência"},
    "enso_mapa_nota": {
        "es": "Panel de capas (arriba a la derecha) para activar/desactivar capas. Mapa base: Esri World Street Map · GEE · NOAA CDR OISST v2.1",
        "en": "Use the layers panel (top right) to toggle layers. Basemap: Esri World Street Map · GEE · NOAA CDR OISST v2.1",
        "pt": "Painel de camadas (canto superior direito) para ativar/desativar camadas. Mapa base: Esri World Street Map · GEE · NOAA CDR OISST v2.1",
    },
    "enso_pdf_preparar": {"es": "Preparar reporte PDF con mapa", "en": "Prepare PDF report with map",
                          "pt": "Preparar relatório PDF com mapa"},
    "enso_pdf_preparar_help": {"es": "Obtiene imágenes del mapa desde GEE (~20-30 s) y genera el reporte PDF.",
                               "en": "Fetches map images from GEE (~20–30 s) and builds the PDF report.",
                               "pt": "Obtém imagens do mapa do GEE (~20–30 s) e gera o relatório PDF."},
    "enso_pdf_mapas_gen": {"es": "Generando imágenes del mapa desde GEE…", "en": "Generating map images from GEE…",
                           "pt": "Gerando imagens do mapa a partir do GEE…"},
    "enso_pdf_mapa_error": {"es": "No se pudo obtener el mapa desde GEE:", "en": "Could not fetch the map from GEE:",
                            "pt": "Não foi possível obter o mapa do GEE:"},
    "enso_pdf_descargar": {"es": "Descargar reporte PDF", "en": "Download PDF report", "pt": "Baixar relatório PDF"},
    "enso_pdf_descargar_help": {
        "es": "Reporte SST/ENSO con mapas, barras de color, tabla de umbrales y estadísticas históricas.",
        "en": "SST/ENSO report with maps, color bars, threshold table and historical statistics.",
        "pt": "Relatório SST/ENSO com mapas, barras de cores, tabela de limiares e estatísticas históricas.",
    },
    "enso_sin_tiles": {"es": "No se obtuvieron tiles GEE para el período seleccionado.",
                       "en": "No GEE tiles were returned for the selected period.",
                       "pt": "Nenhum tile do GEE foi obtido para o período selecionado."},
    "enso_conecta_gee": {"es": "Conecta a Google Earth Engine para visualizar el mapa SST.",
                         "en": "Connect to Google Earth Engine to view the SST map.",
                         "pt": "Conecte-se ao Google Earth Engine para visualizar o mapa SST."},
    "enso_expander_serie": {"es": "📈 Serie histórica Índice Niño 3.4 (1982–2025)", "en": "📈 Niño 3.4 index historical series (1982–2025)",
                            "pt": "📈 Série histórica do índice Niño 3.4 (1982–2025)"},
    "enso_serie_nota": {
        "es": "El cálculo incluye ~528 imágenes mensuales. La primera carga puede tomar ~30–60 s; el resultado se almacena en caché 24 h.",
        "en": "The calculation covers ~528 monthly images. The first load can take ~30–60 s; the result is cached for 24 h.",
        "pt": "O cálculo inclui ~528 imagens mensais. O primeiro carregamento pode levar ~30–60 s; o resultado fica em cache por 24 h.",
    },
    "enso_btn_calcular": {"es": "Calcular Índice Niño 3.4", "en": "Compute Niño 3.4 index", "pt": "Calcular índice Niño 3.4"},
    "enso_btn_calcular_help": {"es": "Conecta a GEE y calcula la serie 1982-2025", "en": "Connects to GEE and computes the 1982–2025 series",
                               "pt": "Conecta ao GEE e calcula a série 1982–2025"},
    "enso_calculando": {"es": "Calculando serie ENSO 1982–2025… puede tomar hasta 60 s.",
                        "en": "Computing ENSO series 1982–2025… this can take up to 60 s.",
                        "pt": "Calculando série ENSO 1982–2025… pode levar até 60 s."},
    "enso_gee_no_disp": {"es": "GEE no disponible. Verifica las credenciales en los secretos de la app.",
                         "en": "GEE not available. Check the credentials in the app secrets.",
                         "pt": "GEE indisponível. Verifique as credenciais nos segredos do app."},
    "enso_sin_datos": {"es": "No se pudieron obtener datos ENSO de GEE.", "en": "Could not retrieve ENSO data from GEE.",
                       "pt": "Não foi possível obter dados ENSO do GEE."},
    "enso_traza_anom": {"es": "Anomalía SST Niño 3.4", "en": "Niño 3.4 SST anomaly", "pt": "Anomalia SST Niño 3.4"},
    "enso_fase": {"es": "Fase ENSO", "en": "ENSO phase", "pt": "Fase ENSO"},
    "enso_mm3": {"es": "MM 3 meses", "en": "3-month MA", "pt": "MM 3 meses"},
    "enso_mm3_corto": {"es": "MM 3m", "en": "3m MA", "pt": "MM 3m"},
    "enso_eje_anom": {"es": "Anomalía SST (°C)", "en": "SST anomaly (°C)", "pt": "Anomalia SST (°C)"},
    "enso_meses_nino": {"es": "meses El Niño (≥+0.5°C)", "en": "El Niño months (≥+0.5°C)", "pt": "meses El Niño (≥+0.5°C)"},
    "enso_meses_nina": {"es": "meses La Niña (≤−0.5°C)", "en": "La Niña months (≤−0.5°C)", "pt": "meses La Niña (≤−0.5°C)"},
    "enso_meses_neutral": {"es": "meses neutrales", "en": "neutral months", "pt": "meses neutros"},
    "enso_pico": {"es": "Pico", "en": "Peak", "pt": "Pico"},
    "enso_total": {"es": "Total analizado: {n} meses", "en": "Total analyzed: {n} months", "pt": "Total analisado: {n} meses"},

    # ── PDF: elementos comunes ────────────────────────────────────────────────
    "pdf_disenado_por": {"es": "Diseñado por Kevin Rodríguez González", "en": "Designed by Kevin Rodríguez González",
                         "pt": "Desenvolvido por Kevin Rodríguez González"},
    "pdf_credito_depto": {"es": "Departamento de Geomática · UANL · FIC", "en": "Geomatics Department · UANL · FIC",
                          "pt": "Departamento de Geomática · UANL · FIC"},
    "pdf_h_introduccion": {"es": "Introducción", "en": "Introduction", "pt": "Introdução"},
    "pdf_h_resumen_ejecutivo": {"es": "Resumen Ejecutivo", "en": "Executive Summary", "pt": "Resumo Executivo"},
    "pdf_h_metodologia": {"es": "Metodología", "en": "Methodology", "pt": "Metodologia"},
    "pdf_h_area_estudio": {"es": "Área de Estudio", "en": "Study Area", "pt": "Área de Estudo"},
    "pdf_h_estadisticas_param": {"es": "Estadísticas por Parámetro", "en": "Statistics by Parameter",
                                 "pt": "Estatísticas por Parâmetro"},
    "pdf_h_serie_campo": {"es": "Serie Temporal — Datos Históricos de Campo", "en": "Time Series — Historical Field Data",
                          "pt": "Série Temporal — Dados Históricos de Campo"},
    "pdf_h_serie_rf": {"es": "Serie Temporal — Predicción del Modelo RF", "en": "Time Series — RF Model Prediction",
                       "pt": "Série Temporal — Previsão do Modelo RF"},
    "pdf_h_desc_param": {"es": "Descripción de Parámetros", "en": "Parameter Description", "pt": "Descrição dos Parâmetros"},
    "pdf_h_mapas_param": {"es": "Mapas Espaciales por Parámetro", "en": "Spatial Maps by Parameter",
                          "pt": "Mapas Espaciais por Parâmetro"},
    "pdf_h_conclusiones": {"es": "Conclusiones", "en": "Conclusions", "pt": "Conclusões"},
    "pdf_h_evolucion_param": {"es": "Evolución Temporal por Parámetro", "en": "Temporal Evolution by Parameter",
                              "pt": "Evolução Temporal por Parâmetro"},
    "pdf_h_tabla_fecha": {"es": "Tabla Resumen por Fecha", "en": "Summary Table by Date", "pt": "Tabela-Resumo por Data"},
    "pdf_h_interp_tendencias": {"es": "Interpretación y Tendencias", "en": "Interpretation and Trends",
                                "pt": "Interpretação e Tendências"},
    "pdf_tbl_componente": {"es": "Componente", "en": "Component", "pt": "Componente"},
    "pdf_tbl_detalle": {"es": "Detalle", "en": "Detail", "pt": "Detalhe"},
    "pdf_met_sensor": {"es": "Sensor", "en": "Sensor", "pt": "Sensor"},
    "pdf_met_sensor_v": {"es": "Sentinel-2 MSI (ESA Copernicus), 10 m de resolución espacial",
                         "en": "Sentinel-2 MSI (ESA Copernicus), 10 m spatial resolution",
                         "pt": "Sentinel-2 MSI (ESA Copernicus), resolução espacial de 10 m"},
    "pdf_met_coleccion": {"es": "Colección GEE", "en": "GEE collection", "pt": "Coleção GEE"},
    "pdf_met_coleccion_v": {"es": "COPERNICUS/S2_SR_HARMONIZED (reflectancia de superficie)",
                            "en": "COPERNICUS/S2_SR_HARMONIZED (surface reflectance)",
                            "pt": "COPERNICUS/S2_SR_HARMONIZED (refletância de superfície)"},
    "pdf_met_modelo": {"es": "Modelo ML", "en": "ML model", "pt": "Modelo ML"},
    "pdf_met_modelo_v": {"es": "Random Forest v3 — 500 árboles, variables: B2, B3, B4, B5, B8, NDVI, NDWI",
                         "en": "Random Forest v3 — 500 trees, features: B2, B3, B4, B5, B8, NDVI, NDWI",
                         "pt": "Random Forest v3 — 500 árvores, variáveis: B2, B3, B4, B5, B8, NDVI, NDWI"},
    "pdf_met_validacion": {"es": "Validación", "en": "Validation", "pt": "Validação"},
    "pdf_met_validacion_v": {"es": "Out-Of-Bag (OOB) R² y RMSE con datos de campo 2016–2019 (7 estaciones)",
                             "en": "Out-Of-Bag (OOB) R² and RMSE with 2016–2019 field data (7 stations)",
                             "pt": "Out-Of-Bag (OOB) R² e RMSE com dados de campo 2016–2019 (7 estações)"},
    "pdf_met_generado_con": {"es": "Generado con", "en": "Built with", "pt": "Gerado com"},
    "pdf_met_plataforma_v": {"es": "Google Earth Engine · Python · Streamlit · Geomática UANL",
                             "en": "Google Earth Engine · Python · Streamlit · UANL Geomatics",
                             "pt": "Google Earth Engine · Python · Streamlit · Geomática UANL"},
    "pdf_res_detalle2": {"es": "10 m (bandas visibles/NIR) · 20 m (SWIR/Red-Edge)",
                         "en": "10 m (visible/NIR bands) · 20 m (SWIR/Red-Edge)",
                         "pt": "10 m (bandas visíveis/NIR) · 20 m (SWIR/Red-Edge)"},
    "pdf_intro_calidad": {
        "es": "El monitoreo de la calidad del agua en cuerpos superficiales es fundamental para la gestión ambiental y la "
              "protección de los recursos hídricos. Este reporte presenta los resultados del análisis de parámetros "
              "fisicoquímicos y microbiológicos del Río Pesquería, Nuevo León, México, obtenidos mediante teledetección "
              "satelital con Sentinel-2 y modelos de machine learning (Random Forest) calibrados con datos de campo del "
              "período 2016–2019. La plataforma Water Quality Mapping, desarrollada por el Departamento de Geomática de la "
              "UANL, integra imágenes Sentinel-2 SR a 10 m de resolución con algoritmos de estimación de calidad de agua "
              "para producir mapas espacialmente continuos de los principales indicadores ambientales.",
        "en": "Monitoring water quality in surface water bodies is essential for environmental management and the protection "
              "of water resources. This report presents the results of the analysis of physicochemical and microbiological "
              "parameters of the Pesquería River, Nuevo León, Mexico, obtained through Sentinel-2 satellite remote sensing "
              "and machine learning models (Random Forest) calibrated with 2016–2019 field data. The Water Quality Mapping "
              "platform, developed by the Department of Geomatics at UANL, combines 10 m Sentinel-2 SR imagery with water "
              "quality estimation algorithms to produce spatially continuous maps of the main environmental indicators.",
        "pt": "O monitoramento da qualidade da água em corpos hídricos superficiais é fundamental para a gestão ambiental e a "
              "proteção dos recursos hídricos. Este relatório apresenta os resultados da análise de parâmetros "
              "físico-químicos e microbiológicos do Rio Pesquería, Nuevo León, México, obtidos por sensoriamento remoto com "
              "Sentinel-2 e modelos de machine learning (Random Forest) calibrados com dados de campo do período "
              "2016–2019. A plataforma Water Quality Mapping, desenvolvida pelo Departamento de Geomática da UANL, integra "
              "imagens Sentinel-2 SR com 10 m de resolução e algoritmos de estimativa da qualidade da água para produzir "
              "mapas espacialmente contínuos dos principais indicadores ambientais.",
    },
    "pdf_serie_campo_texto": {
        "es": "Los siguientes gráficos muestran la evolución temporal de los parámetros fisicoquímicos medidos directamente "
              "en campo en las 7 estaciones de muestreo del Río Pesquería durante el período 2016–2019 (19 campañas). Cada "
              "gráfico incluye la media espacial entre estaciones (línea azul), el máximo registrado (línea roja "
              "discontinua), la tendencia lineal (línea dorada) y el resultado del test de Mann-Kendall (τ de Kendall, "
              "α = 0.05) para detectar tendencias monótonas estadísticamente significativas.",
        "en": "The following charts show the temporal evolution of the physicochemical parameters measured directly in the "
              "field at the 7 sampling stations of the Pesquería River during 2016–2019 (19 campaigns). Each chart includes "
              "the spatial mean across stations (blue line), the maximum recorded value (dashed red line), the linear trend "
              "(gold line) and the Mann-Kendall test result (Kendall's τ, α = 0.05) to detect statistically significant "
              "monotonic trends.",
        "pt": "Os gráficos a seguir mostram a evolução temporal dos parâmetros físico-químicos medidos diretamente em campo "
              "nas 7 estações de amostragem do Rio Pesquería durante o período 2016–2019 (19 campanhas). Cada gráfico inclui "
              "a média espacial entre estações (linha azul), o máximo registrado (linha vermelha tracejada), a tendência "
              "linear (linha dourada) e o resultado do teste de Mann-Kendall (τ de Kendall, α = 0.05) para detectar "
              "tendências monotônicas estatisticamente significativas.",
    },
    "pdf_serie_rf_texto": {
        "es": "La siguiente sección presenta la evolución temporal de los parámetros de calidad de agua estimados por el "
              "modelo Random Forest a lo largo de las fechas de muestreo disponibles. Se incluye la media espacial entre "
              "los puntos, el máximo registrado y la tendencia lineal con el resultado del test de Mann-Kendall (α = 0.05).",
        "en": "This section presents the temporal evolution of the water quality parameters estimated by the Random Forest "
              "model across the available sampling dates. It includes the spatial mean across points, the maximum "
              "recorded value and the linear trend with the Mann-Kendall test result (α = 0.05).",
        "pt": "A seção a seguir apresenta a evolução temporal dos parâmetros de qualidade da água estimados pelo modelo "
              "Random Forest ao longo das datas de amostragem disponíveis. Inclui a média espacial entre os pontos, o "
              "máximo registrado e a tendência linear com o resultado do teste de Mann-Kendall (α = 0.05).",
    },
    "pdf_cita_calidad": {
        "es": "Rodríguez González, K.D. ({anio}). Water Quality Mapping — Río Pesquería [Aplicación web]. Universidad "
              "Autónoma de Nuevo León, Facultad de Ingeniería Civil, Departamento de Geomática.",
        "en": "Rodríguez González, K.D. ({anio}). Water Quality Mapping — Pesquería River [Web application]. Universidad "
              "Autónoma de Nuevo León, Faculty of Civil Engineering, Department of Geomatics.",
        "pt": "Rodríguez González, K.D. ({anio}). Water Quality Mapping — Rio Pesquería [Aplicação web]. Universidad "
              "Autónoma de Nuevo León, Faculdade de Engenharia Civil, Departamento de Geomática.",
    },
    "pdf_graf_tendencia_lineal": {"es": "Tendencia lineal", "en": "Linear trend", "pt": "Tendência linear"},
    "pdf_graf_evolucion": {"es": "Evolución temporal", "en": "Temporal evolution", "pt": "Evolução temporal"},
    "pdf_graf_media_zonal": {"es": "Media zonal", "en": "Zonal mean", "pt": "Média zonal"},
    "pdf_graf_serie_zonal": {"es": "Serie temporal (media zonal)", "en": "Time series (zonal mean)",
                             "pt": "Série temporal (média zonal)"},
    "pdf_tendencia_mk": {"es": "Tendencia MK", "en": "MK trend", "pt": "Tendência MK"},

    # ── PDF: serie temporal ───────────────────────────────────────────────────
    "pdf_serie_intro": {
        "es": "Este reporte documenta la evolución temporal de los parámetros de calidad del agua en el Río Pesquería, "
              "Nuevo León, México, a partir del análisis multitemporal de imágenes Sentinel-2 SR procesadas en Google Earth "
              "Engine (GEE). La estimación de cada variable fisicoquímica se realiza mediante un modelo Random Forest "
              "entrenado con datos de campo colectados en 7 estaciones de muestreo durante el período 2016–2019. El "
              "análisis de tendencias incluye el test no paramétrico de Mann-Kendall (τ de Kendall) para detectar "
              "tendencias monótonas estadísticamente significativas (α = 0.05), complementado con la pendiente de Sen "
              "para estimar la magnitud del cambio.",
        "en": "This report documents the temporal evolution of water quality parameters in the Pesquería River, Nuevo León, "
              "Mexico, based on multitemporal analysis of Sentinel-2 SR imagery processed in Google Earth Engine (GEE). "
              "Each physicochemical variable is estimated with a Random Forest model trained on field data collected at 7 "
              "sampling stations during 2016–2019. The trend analysis includes the non-parametric Mann-Kendall test "
              "(Kendall's τ) to detect statistically significant monotonic trends (α = 0.05), complemented by Sen's slope "
              "to estimate the magnitude of change.",
        "pt": "Este relatório documenta a evolução temporal dos parâmetros de qualidade da água no Rio Pesquería, Nuevo "
              "León, México, a partir da análise multitemporal de imagens Sentinel-2 SR processadas no Google Earth Engine "
              "(GEE). Cada variável físico-química é estimada por um modelo Random Forest treinado com dados de campo "
              "coletados em 7 estações de amostragem durante o período 2016–2019. A análise de tendências inclui o teste "
              "não paramétrico de Mann-Kendall (τ de Kendall) para detectar tendências monotônicas estatisticamente "
              "significativas (α = 0.05), complementado pela inclinação de Sen para estimar a magnitude da mudança.",
    },
    "pdf_serie_metodologia": {
        "es": "El flujo de trabajo comprende: (1) búsqueda y composición de mosaicos Sentinel-2 SR sin nubes para cada fecha "
              "de muestreo mediante GEE; (2) extracción de reflectancias en los puntos de muestreo; (3) aplicación del "
              "modelo Random Forest para estimar los parámetros fisicoquímicos; (4) cálculo de estadísticas zonales (media, "
              "máximo, mínimo); y (5) análisis de tendencias mediante Mann-Kendall y regresión lineal. Los resultados se "
              "presentan como gráficos de evolución temporal con bandas de incertidumbre.",
        "en": "The workflow comprises: (1) search and compositing of cloud-free Sentinel-2 SR mosaics for each sampling date "
              "in GEE; (2) reflectance extraction at the sampling points; (3) application of the Random Forest model to "
              "estimate the physicochemical parameters; (4) computation of zonal statistics (mean, maximum, minimum); and "
              "(5) trend analysis with Mann-Kendall and linear regression. Results are shown as temporal evolution charts "
              "with uncertainty bands.",
        "pt": "O fluxo de trabalho compreende: (1) busca e composição de mosaicos Sentinel-2 SR sem nuvens para cada data de "
              "amostragem no GEE; (2) extração de refletâncias nos pontos de amostragem; (3) aplicação do modelo Random "
              "Forest para estimar os parâmetros físico-químicos; (4) cálculo de estatísticas zonais (média, máximo, "
              "mínimo); e (5) análise de tendências por Mann-Kendall e regressão linear. Os resultados são apresentados "
              "como gráficos de evolução temporal com faixas de incerteza.",
    },
    "pdf_serie_evolucion_texto": {
        "es": "Cada gráfico muestra la media espacial (línea azul), el máximo entre estaciones (línea roja discontinua) y la "
              "tendencia lineal (línea dorada). El resultado del test de Mann-Kendall se indica en el recuadro superior "
              "izquierdo de cada gráfico.",
        "en": "Each chart shows the spatial mean (blue line), the maximum across stations (dashed red line) and the linear "
              "trend (gold line). The Mann-Kendall test result is shown in the upper-left box of each chart.",
        "pt": "Cada gráfico mostra a média espacial (linha azul), o máximo entre estações (linha vermelha tracejada) e a "
              "tendência linear (linha dourada). O resultado do teste de Mann-Kendall é indicado no quadro superior "
              "esquerdo de cada gráfico.",
    },
    "pdf_serie_interp": {
        "es": "<b>{param}</b>: tendencia de {tendencia} {sig} (τ={tau}, p={p}), variación de {v0} a {v1} {unidad} (~{pct}% de cambio).",
        "en": "<b>{param}</b>: {tendencia} trend, {sig} (τ={tau}, p={p}); change from {v0} to {v1} {unidad} (~{pct}% change).",
        "pt": "<b>{param}</b>: tendência de {tendencia} {sig} (τ={tau}, p={p}), variação de {v0} a {v1} {unidad} (~{pct}% de mudança).",
    },
    "pdf_sig_si": {"es": "estadísticamente significativa (p<0.05)", "en": "statistically significant (p<0.05)",
                   "pt": "estatisticamente significativa (p<0.05)"},
    "pdf_sig_no": {"es": "no significativa estadísticamente", "en": "not statistically significant",
                   "pt": "não significativa estatisticamente"},

    # ── PDF: índices espectrales ──────────────────────────────────────────────
    "pdf_h_resumen_interp": {"es": "Resumen Interpretativo", "en": "Interpretive Summary", "pt": "Resumo Interpretativo"},
    "pdf_h_estadisticas_zonales": {"es": "Estadísticas Zonales por Índice", "en": "Zonal Statistics by Index",
                                   "pt": "Estatísticas Zonais por Índice"},
    "pdf_h_mapas_indice": {"es": "Mapas Espectrales por Índice", "en": "Spectral Maps by Index",
                           "pt": "Mapas Espectrais por Índice"},
    "pdf_h_series_gee": {"es": "Series Temporales (Google Earth Engine)", "en": "Time Series (Google Earth Engine)",
                         "pt": "Séries Temporais (Google Earth Engine)"},
    "pdf_h_resumen_mk": {"es": "Resumen de Tendencias (Mann-Kendall)", "en": "Trend Summary (Mann-Kendall)",
                         "pt": "Resumo de Tendências (Mann-Kendall)"},
    "pdf_h_aplicaciones": {"es": "Aplicaciones y Recomendaciones", "en": "Applications and Recommendations",
                           "pt": "Aplicações e Recomendações"},
    "pdf_h_formulas": {"es": "Fórmulas de los Índices Espectrales", "en": "Spectral Index Formulas",
                       "pt": "Fórmulas dos Índices Espectrais"},
    "pdf_indices": {"es": "Índices", "en": "Indices", "pt": "Índices"},
    "pdf_formula": {"es": "Fórmula", "en": "Formula", "pt": "Fórmula"},
    "pdf_referencia": {"es": "Referencia", "en": "Reference", "pt": "Referência"},
    "pdf_area_estimada": {"es": "Área estimada", "en": "Estimated area", "pt": "Área estimada"},
    "pdf_resolucion_espacial": {"es": "Resolución espacial", "en": "Spatial resolution", "pt": "Resolução espacial"},
    "pdf_p50": {"es": "P50 (mediana)", "en": "P50 (median)", "pt": "P50 (mediana)"},
    "pdf_titulo_corto_espectral": {"es": "Reporte de Índices Espectrales — Water Quality Mapping",
                                   "en": "Spectral Indices Report — Water Quality Mapping",
                                   "pt": "Relatório de Índices Espectrais — Water Quality Mapping"},
    "pdf_met_sensor_v2": {"es": "Sentinel-2 MSI (ESA Copernicus), 10 m / 20 m de resolución espacial",
                          "en": "Sentinel-2 MSI (ESA Copernicus), 10 m / 20 m spatial resolution",
                          "pt": "Sentinel-2 MSI (ESA Copernicus), resolução espacial de 10 m / 20 m"},
    "pdf_met_composicion": {"es": "Composición", "en": "Compositing", "pt": "Composição"},
    "pdf_met_composicion_v": {"es": "Compuesto mediano con máscara de nubes QA60 píxel a píxel",
                              "en": "Median composite with per-pixel QA60 cloud mask",
                              "pt": "Composto mediano com máscara de nuvens QA60 pixel a pixel"},
    "pdf_met_clip": {"es": "Clip espacial", "en": "Spatial clip", "pt": "Recorte espacial"},
    "pdf_met_clip_v": {"es": "Recorte exacto al polígono del shapefile cargado (no rectangular)",
                       "en": "Exact clip to the uploaded shapefile polygon (not rectangular)",
                       "pt": "Recorte exato ao polígono do shapefile enviado (não retangular)"},
    "pdf_met_estadisticas": {"es": "Estadísticas", "en": "Statistics", "pt": "Estatísticas"},
    "pdf_met_estadisticas_v": {"es": "reduceRegion — media, desv. estándar, mín., máx., percentil 50 y 90",
                               "en": "reduceRegion — mean, std. dev., min, max, 50th and 90th percentiles",
                               "pt": "reduceRegion — média, desvio padrão, mín., máx., percentis 50 e 90"},
    "pdf_met_tendencias": {"es": "Tendencias", "en": "Trends", "pt": "Tendências"},
    "pdf_met_tendencias_v": {"es": "Mann-Kendall (τ de Kendall) + regresión lineal por mínimos cuadrados",
                             "en": "Mann-Kendall (Kendall's τ) + least-squares linear regression",
                             "pt": "Mann-Kendall (τ de Kendall) + regressão linear por mínimos quadrados"},
    "pdf_met_plataforma": {"es": "Plataforma", "en": "Platform", "pt": "Plataforma"},
    "pdf_intro_espectral": {
        "es": "Los índices espectrales derivados de imágenes Sentinel-2 (ESA Copernicus) permiten caracterizar propiedades "
              "biofísicas y ópticas del agua superficial de forma espacialmente continua y repetible. Este reporte presenta "
              "los resultados del análisis multivariado de índices espectrales computados en Google Earth Engine (GEE) para "
              "el área de estudio definida por el shapefile cargado en la plataforma Water Quality Mapping. Los índices "
              "cubren aspectos de calidad del agua (NDCI, SABI, CDOM, NDTI), presencia de agua superficial (NDWI, MNDWI, "
              "AWEInsh), vegetación (NDVI, EVI) y temperatura de superficie (LST). El análisis temporal incluye el test de "
              "Mann-Kendall para detectar tendencias significativas en las series históricas.",
        "en": "Spectral indices derived from Sentinel-2 imagery (ESA Copernicus) make it possible to characterize biophysical "
              "and optical properties of surface water in a spatially continuous and repeatable way. This report presents "
              "the results of the multivariate analysis of spectral indices computed in Google Earth Engine (GEE) for the "
              "study area defined by the shapefile uploaded to the Water Quality Mapping platform. The indices cover water "
              "quality (NDCI, SABI, CDOM, NDTI), surface water presence (NDWI, MNDWI, AWEInsh), vegetation (NDVI, EVI) and "
              "surface temperature (LST). The temporal analysis includes the Mann-Kendall test to detect significant "
              "trends in the historical series.",
        "pt": "Os índices espectrais derivados de imagens Sentinel-2 (ESA Copernicus) permitem caracterizar propriedades "
              "biofísicas e ópticas da água superficial de forma espacialmente contínua e repetível. Este relatório "
              "apresenta os resultados da análise multivariada de índices espectrais calculados no Google Earth Engine "
              "(GEE) para a área de estudo definida pelo shapefile carregado na plataforma Water Quality Mapping. Os "
              "índices abrangem qualidade da água (NDCI, SABI, CDOM, NDTI), presença de água superficial (NDWI, MNDWI, "
              "AWEInsh), vegetação (NDVI, EVI) e temperatura de superfície (LST). A análise temporal inclui o teste de "
              "Mann-Kendall para detectar tendências significativas nas séries históricas.",
    },
    "pdf_series_gee_texto": {
        "es": "Las series temporales se extrajeron de Google Earth Engine calculando la media zonal de cada índice sobre el "
              "área de estudio para cada imagen Sentinel-2 disponible. Se presentan la evolución temporal, la línea de "
              "tendencia lineal y el resultado del test de Mann-Kendall para evaluar la significancia estadística de la "
              "tendencia (α = 0.05).",
        "en": "The time series were extracted from Google Earth Engine by computing the zonal mean of each index over the "
              "study area for every available Sentinel-2 image. The temporal evolution, the linear trend line and the "
              "Mann-Kendall test result are shown to assess the statistical significance of the trend (α = 0.05).",
        "pt": "As séries temporais foram extraídas do Google Earth Engine calculando a média zonal de cada índice sobre a "
              "área de estudo para cada imagem Sentinel-2 disponível. São apresentadas a evolução temporal, a linha de "
              "tendência linear e o resultado do teste de Mann-Kendall para avaliar a significância estatística da "
              "tendência (α = 0.05).",
    },
    "pdf_cita_espectral": {
        "es": "Rodríguez González, K.D. ({anio}). Water Quality &amp; Spectral Indices Mapping Tool. Universidad Autónoma de "
              "Nuevo León, Facultad de Ingeniería Civil, Departamento de Geomática. https://waterqualitygeomaticauanl.streamlit.app/",
        "en": "Rodríguez González, K.D. ({anio}). Water Quality &amp; Spectral Indices Mapping Tool. Universidad Autónoma de "
              "Nuevo León, Faculty of Civil Engineering, Department of Geomatics. https://waterqualitygeomaticauanl.streamlit.app/",
        "pt": "Rodríguez González, K.D. ({anio}). Water Quality &amp; Spectral Indices Mapping Tool. Universidad Autónoma de "
              "Nuevo León, Faculdade de Engenharia Civil, Departamento de Geomática. https://waterqualitygeomaticauanl.streamlit.app/",
    },
    "pdf_ndci_alta": {"es": "alta concentración de clorofila-a — posible floración algal",
                      "en": "high chlorophyll-a concentration — possible algal bloom",
                      "pt": "alta concentração de clorofila-a — possível floração de algas"},
    "pdf_ndci_moderada": {"es": "concentración moderada de clorofila-a", "en": "moderate chlorophyll-a concentration",
                          "pt": "concentração moderada de clorofila-a"},
    "pdf_ndci_baja": {"es": "baja clorofila-a — aguas con escasa productividad fitoplanctónica",
                      "en": "low chlorophyll-a — waters with low phytoplankton productivity",
                      "pt": "baixa clorofila-a — águas com pouca produtividade fitoplanctônica"},
    "pdf_sabi_alta": {"es": "alta biomasa algal superficial detectada", "en": "high surface algal biomass detected",
                      "pt": "alta biomassa algal superficial detectada"},
    "pdf_sabi_moderada": {"es": "biomasa algal moderada", "en": "moderate algal biomass", "pt": "biomassa algal moderada"},
    "pdf_sabi_baja": {"es": "baja biomasa algal — aguas con buena transparencia", "en": "low algal biomass — good water transparency",
                      "pt": "baixa biomassa algal — águas com boa transparência"},
    "pdf_cdom_alta": {"es": "alta concentración de CDOM — probable aporte de materia orgánica disuelta",
                      "en": "high CDOM concentration — likely input of dissolved organic matter",
                      "pt": "alta concentração de CDOM — provável aporte de matéria orgânica dissolvida"},
    "pdf_cdom_moderada": {"es": "CDOM moderado", "en": "moderate CDOM", "pt": "CDOM moderado"},
    "pdf_cdom_baja": {"es": "CDOM bajo — aguas con alta transparencia óptica", "en": "low CDOM — high optical transparency",
                      "pt": "CDOM baixo — águas com alta transparência óptica"},
    "pdf_awei_agua": {"es": "superficie acuática claramente diferenciada del suelo",
                      "en": "water surface clearly distinguished from land",
                      "pt": "superfície aquática claramente diferenciada do solo"},
    "pdf_awei_transicion": {"es": "zona de transición agua-suelo o agua somera", "en": "water–land transition zone or shallow water",
                            "pt": "zona de transição água-solo ou água rasa"},
    "pdf_awei_tierra": {"es": "superficie terrestre o ausencia de agua libre", "en": "land surface or no open water",
                        "pt": "superfície terrestre ou ausência de água livre"},
    "pdf_evi_densa": {"es": "vegetación densa — alta actividad fotosintética ribereña",
                      "en": "dense vegetation — high riparian photosynthetic activity",
                      "pt": "vegetação densa — alta atividade fotossintética ribeirinha"},
    "pdf_evi_moderada": {"es": "vegetación moderada en la zona de influencia del cauce",
                         "en": "moderate vegetation in the river corridor",
                         "pt": "vegetação moderada na zona de influência do canal"},
    "pdf_evi_escasa": {"es": "vegetación escasa o suelo parcialmente cubierto", "en": "sparse vegetation or partially covered soil",
                       "pt": "vegetação escassa ou solo parcialmente coberto"},
    "pdf_evi_nula": {"es": "sin vegetación — agua, suelo desnudo o área urbana", "en": "no vegetation — water, bare soil or urban area",
                     "pt": "sem vegetação — água, solo exposto ou área urbana"},

    # ── PDF: SST / ENSO ───────────────────────────────────────────────────────
    "pdf_enso_titulo": {"es": "Análisis SST / Fenómeno ENSO", "en": "SST / ENSO Analysis", "pt": "Análise SST / Fenômeno ENSO"},
    "pdf_enso_subtitulo": {"es": "Temperatura Superficial del Mar · Anomalía · Región Niño 3.4",
                           "en": "Sea Surface Temperature · Anomaly · Niño 3.4 Region",
                           "pt": "Temperatura da Superfície do Mar · Anomalia · Região Niño 3.4"},
    "pdf_enso_resolucion": {"es": "resolución", "en": "resolution", "pt": "resolução"},
    "pdf_procesamiento": {"es": "Procesamiento", "en": "Processing", "pt": "Processamento"},
    "pdf_enso_nota_auto": {"es": "Reporte generado automáticamente por la plataforma Water Quality Mapping.",
                           "en": "Report automatically generated by the Water Quality Mapping platform.",
                           "pt": "Relatório gerado automaticamente pela plataforma Water Quality Mapping."},
    "pdf_enso_intro": {
        "es": "El Fenómeno El Niño–Oscilación del Sur (ENSO) es el principal modo de variabilidad climática interanual del "
              "planeta. Se manifiesta como variaciones anómalas de la Temperatura Superficial del Mar (SST) en el Océano "
              "Pacífico Tropical, particularmente en la región Niño 3.4 (5°N–5°S · 170°W–120°W). Las anomalías positivas "
              "≥+0.5°C (El Niño) y negativas ≤−0.5°C (La Niña) alteran los patrones de precipitación, temperatura y "
              "productividad biológica oceánica a escala global. En México el ENSO afecta directamente la disponibilidad "
              "hídrica, la frecuencia de eventos extremos y la calidad del agua en cuerpos continentales como el Río "
              "Pesquería, Nuevo León.",
        "en": "The El Niño–Southern Oscillation (ENSO) is the planet's dominant mode of interannual climate variability. It "
              "appears as anomalous variations in Sea Surface Temperature (SST) across the tropical Pacific Ocean, "
              "particularly in the Niño 3.4 region (5°N–5°S · 170°W–120°W). Positive anomalies ≥+0.5°C (El Niño) and "
              "negative anomalies ≤−0.5°C (La Niña) alter precipitation, temperature and ocean biological productivity "
              "patterns worldwide. In Mexico, ENSO directly affects water availability, the frequency of extreme events and "
              "water quality in inland water bodies such as the Pesquería River, Nuevo León.",
        "pt": "O fenômeno El Niño–Oscilação Sul (ENSO) é o principal modo de variabilidade climática interanual do planeta. "
              "Manifesta-se como variações anômalas da Temperatura da Superfície do Mar (SST) no Oceano Pacífico Tropical, "
              "particularmente na região Niño 3.4 (5°N–5°S · 170°W–120°W). As anomalias positivas ≥+0.5°C (El Niño) e "
              "negativas ≤−0.5°C (La Niña) alteram os padrões de precipitação, temperatura e produtividade biológica "
              "oceânica em escala global. No México, o ENSO afeta diretamente a disponibilidade hídrica, a frequência de "
              "eventos extremos e a qualidade da água em corpos continentais como o Rio Pesquería, Nuevo León.",
    },
    "pdf_enso_h_sst": {"es": "Temperatura Superficial del Mar (SST)", "en": "Sea Surface Temperature (SST)",
                       "pt": "Temperatura da Superfície do Mar (SST)"},
    "pdf_enso_sst_texto": {
        "es": "El mapa de SST para <b>{periodo}</b> proviene de la colección NOAA OISST v2.1 (Optimum Interpolation Sea "
              "Surface Temperature), derivada de datos AVHRR con resolución espacial de 0.25° (~28 km). La escala de color "
              "cubre el rango típico 10°C–32°C.",
        "en": "The SST map for <b>{periodo}</b> comes from the NOAA OISST v2.1 collection (Optimum Interpolation Sea Surface "
              "Temperature), derived from AVHRR data at 0.25° (~28 km) spatial resolution. The color scale covers the "
              "typical 10°C–32°C range.",
        "pt": "O mapa de SST para <b>{periodo}</b> provém da coleção NOAA OISST v2.1 (Optimum Interpolation Sea Surface "
              "Temperature), derivada de dados AVHRR com resolução espacial de 0.25° (~28 km). A escala de cores cobre a "
              "faixa típica de 10°C–32°C.",
    },
    "pdf_enso_cbar_sst": {"es": "SST (°C) — Escala RdYlBu · NOAA OISST v2.1", "en": "SST (°C) — RdYlBu scale · NOAA OISST v2.1",
                          "pt": "SST (°C) — Escala RdYlBu · NOAA OISST v2.1"},
    "pdf_enso_cbar_anom": {"es": "Anomalía SST (°C) — Divergente azul-rojo · NOAA OISST v2.1",
                           "en": "SST anomaly (°C) — Diverging blue-red · NOAA OISST v2.1",
                           "pt": "Anomalia SST (°C) — Divergente azul-vermelho · NOAA OISST v2.1"},
    "pdf_enso_cap_sst": {"es": "Mapa SST — {periodo} · NOAA CDR OISST v2.1 · GEE", "en": "SST map — {periodo} · NOAA CDR OISST v2.1 · GEE",
                         "pt": "Mapa SST — {periodo} · NOAA CDR OISST v2.1 · GEE"},
    "pdf_enso_cap_anom": {"es": "Anomalía SST — {periodo} · Referencia climatológica 1982–2025 · GEE",
                          "en": "SST anomaly — {periodo} · 1982–2025 climatological baseline · GEE",
                          "pt": "Anomalia SST — {periodo} · Referência climatológica 1982–2025 · GEE"},
    "pdf_enso_h_anom": {"es": "Anomalía SST — Región Niño 3.4", "en": "SST Anomaly — Niño 3.4 Region",
                        "pt": "Anomalia SST — Região Niño 3.4"},
    "pdf_enso_anom_texto": {
        "es": "La anomalía es la diferencia entre la SST de <b>{periodo}</b> y la climatología mensual 1982–2025. Anomalía "
              "positiva (cálida) en Niño 3.4 → El Niño; negativa (fría) → La Niña. Umbral operacional NOAA/CPC: ±0.5°C "
              "durante cinco meses consecutivos. En El Niño la clorofila-a oceánica disminuye (menor surgencia); en La Niña "
              "aumenta (mayor mezcla de aguas frías ricas en nutrientes).",
        "en": "The anomaly is the difference between the SST of <b>{periodo}</b> and the 1982–2025 monthly climatology. A "
              "positive (warm) anomaly in Niño 3.4 → El Niño; a negative (cold) one → La Niña. NOAA/CPC operational "
              "threshold: ±0.5°C for five consecutive months. During El Niño ocean chlorophyll-a decreases (weaker "
              "upwelling); during La Niña it increases (stronger mixing of cold, nutrient-rich water).",
        "pt": "A anomalia é a diferença entre a SST de <b>{periodo}</b> e a climatologia mensal 1982–2025. Anomalia positiva "
              "(quente) no Niño 3.4 → El Niño; negativa (fria) → La Niña. Limiar operacional NOAA/CPC: ±0.5°C durante "
              "cinco meses consecutivos. No El Niño a clorofila-a oceânica diminui (menor ressurgência); na La Niña aumenta "
              "(maior mistura de águas frias ricas em nutrientes).",
    },
    "pdf_enso_h_umbrales": {"es": "Clasificación ENSO — Umbrales operacionales (NOAA/CPC):",
                            "en": "ENSO classification — Operational thresholds (NOAA/CPC):",
                            "pt": "Classificação ENSO — Limiares operacionais (NOAA/CPC):"},
    "pdf_enso_condicion": {"es": "Condición", "en": "Condition", "pt": "Condição"},
    "pdf_enso_color_mapa": {"es": "Color en mapa", "en": "Map color", "pt": "Cor no mapa"},
    "pdf_enso_impacto": {"es": "Impacto Clorofila-a oceánica", "en": "Ocean chlorophyll-a impact",
                         "pt": "Impacto na clorofila-a oceânica"},
    "pdf_color_rojo": {"es": "Rojo", "en": "Red", "pt": "Vermelho"},
    "pdf_color_azul": {"es": "Azul", "en": "Blue", "pt": "Azul"},
    "pdf_color_blanco": {"es": "Blanco/amarillo", "en": "White/yellow", "pt": "Branco/amarelo"},
    "pdf_enso_imp_nino": {"es": "Disminuye — aguas más cálidas, menor surgencia", "en": "Decreases — warmer water, weaker upwelling",
                          "pt": "Diminui — águas mais quentes, menor ressurgência"},
    "pdf_enso_imp_nina": {"es": "Aumenta — mayor surgencia de aguas frías", "en": "Increases — stronger upwelling of cold water",
                          "pt": "Aumenta — maior ressurgência de águas frias"},
    "pdf_enso_imp_neutral": {"es": "Normal estacional", "en": "Seasonal normal", "pt": "Normal sazonal"},
    "pdf_enso_h_hist": {"es": "Estadísticas Históricas ENSO — 1982–2025", "en": "Historical ENSO Statistics — 1982–2025",
                        "pt": "Estatísticas Históricas ENSO — 1982–2025"},
    "pdf_enso_hist_texto": {
        "es": "La serie comprende <b>{total} meses</b> (1982–2025). Media anomalía Niño 3.4: <b>{media}°C</b> · Desviación estándar: <b>{std}°C</b>.",
        "en": "The series covers <b>{total} months</b> (1982–2025). Mean Niño 3.4 anomaly: <b>{media}°C</b> · Standard deviation: <b>{std}°C</b>.",
        "pt": "A série abrange <b>{total} meses</b> (1982–2025). Anomalia média Niño 3.4: <b>{media}°C</b> · Desvio padrão: <b>{std}°C</b>.",
    },
    "pdf_enso_n_meses": {"es": "N (meses)", "en": "N (months)", "pt": "N (meses)"},
    "pdf_enso_pct": {"es": "% período", "en": "% of period", "pt": "% período"},
    "pdf_enso_pico_anom": {"es": "Pico anomalía", "en": "Peak anomaly", "pt": "Pico de anomalia"},
    "pdf_enso_fecha_pico": {"es": "Fecha pico", "en": "Peak date", "pt": "Data do pico"},
    "pdf_enso_h_grafico": {"es": "Serie Temporal Anomalía SST Niño 3.4 (1982–2025):",
                           "en": "Niño 3.4 SST Anomaly Time Series (1982–2025):",
                           "pt": "Série Temporal da Anomalia SST Niño 3.4 (1982–2025):"},
    "pdf_enso_graf_titulo": {"es": "Índice Niño 3.4 — NOAA OISST v2.1 · GEE", "en": "Niño 3.4 Index — NOAA OISST v2.1 · GEE",
                             "pt": "Índice Niño 3.4 — NOAA OISST v2.1 · GEE"},
    "pdf_enso_graf_nota": {
        "es": "<i>Puntos rojos: El Niño (≥+0.5°C) · Azules: La Niña (≤−0.5°C) · Grises: Neutral · Línea azul: media móvil 3 meses.</i>",
        "en": "<i>Red dots: El Niño (≥+0.5°C) · Blue: La Niña (≤−0.5°C) · Grey: Neutral · Blue line: 3-month moving average.</i>",
        "pt": "<i>Pontos vermelhos: El Niño (≥+0.5°C) · Azuis: La Niña (≤−0.5°C) · Cinzas: Neutro · Linha azul: média móvel de 3 meses.</i>",
    },
    "pdf_enso_h_fuentes": {"es": "Fuentes de Datos y Referencias", "en": "Data Sources and References",
                           "pt": "Fontes de Dados e Referências"},
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


def get_indice_nombre(idx_key, lang="es", plain=False):
    nombre = t(f"{idx_key}_nombre", lang)
    # plain=True quita el emoji inicial (matplotlib y Leaflet no lo necesitan)
    return re.sub(r"^\W+", "", nombre) if plain else nombre


def get_indice_desc(idx_key, lang="es"):
    return t(f"{idx_key}_desc", lang)


MESES = {
    "es": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
           "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "pt": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
           "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
}


def mes_nombre(mes, lang="es"):
    return MESES.get(lang, MESES["es"])[int(mes) - 1]


def mes_abrev(mes, lang="es"):
    return mes_nombre(mes, lang)[:3]


def fecha_corta(d, lang="es", anio=True):
    """'08 Oct 2018' con el mes abreviado en el idioma (strftime %b depende del locale del servidor)."""
    s = f"{d.day:02d} {mes_abrev(d.month, lang)}"
    return f"{s} {d.year}" if anio else s


def fecha_larga(d, lang="es"):
    if lang == "en":
        return f"{mes_nombre(d.month, lang)} {d.day}, {d.year}"
    return f"{d.day} de {mes_nombre(d.month, lang).lower()} de {d.year}"
