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
