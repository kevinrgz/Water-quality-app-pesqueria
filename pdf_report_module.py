# =============================================================================
# MÓDULO DE GENERACIÓN DE REPORTES PDF
# Agregar este código a app.py (después de las funciones de mapas existentes)
# =============================================================================

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ── Paleta de colores institucional para el PDF ───────────────────────────────
PDF_BLUE   = colors.HexColor("#1A4F7A")
PDF_TEAL   = colors.HexColor("#2E8B8B")
PDF_GREEN  = colors.HexColor("#3DBA7A")
PDF_GREY   = colors.HexColor("#6B7280")
PDF_LIGHT  = colors.HexColor("#F0F4F8")
PDF_DARK   = colors.HexColor("#1A1A2E")

# ── Estilos de texto reutilizables ────────────────────────────────────────────
def get_pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TituloPortada", fontSize=26, leading=30, textColor=PDF_BLUE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6))
    styles.add(ParagraphStyle(
        name="SubtituloPortada", fontSize=13, leading=18, textColor=PDF_TEAL,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4))
    styles.add(ParagraphStyle(
        name="MetaPortada", fontSize=9.5, leading=14, textColor=PDF_GREY,
        fontName="Helvetica", alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        name="SeccionTitulo", fontSize=15, leading=18, textColor=PDF_BLUE,
        fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle(
        name="SubseccionTitulo", fontSize=11.5, leading=14, textColor=PDF_TEAL,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=5))
    styles.add(ParagraphStyle(
        name="CuerpoTexto", fontSize=9.5, leading=14.5, textColor=colors.HexColor("#2A2A2A"),
        fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=6))
    styles.add(ParagraphStyle(
        name="CuerpoTextoChico", fontSize=8.3, leading=12, textColor=PDF_GREY,
        fontName="Helvetica", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(
        name="FootnoteCentro", fontSize=7.5, leading=10, textColor=PDF_GREY,
        fontName="Helvetica-Oblique", alignment=TA_CENTER))
    return styles


# ── Encabezado y pie de página para cada hoja ─────────────────────────────────
def _draw_header_footer(canvas_obj, doc, titulo_corto="Calidad de Agua — Río Pesquería"):
    canvas_obj.saveState()
    width, height = letter

    canvas_obj.setStrokeColor(PDF_TEAL)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(2*cm, height - 1.4*cm, width - 2*cm, height - 1.4*cm)

    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(PDF_GREY)
    canvas_obj.drawString(2*cm, height - 1.2*cm, titulo_corto)
    canvas_obj.drawRightString(width - 2*cm, height - 1.2*cm,
                                "UANL · FIC · Depto. Geomática")

    canvas_obj.setLineWidth(0.6)
    canvas_obj.line(2*cm, 1.5*cm, width - 2*cm, 1.5*cm)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.drawString(2*cm, 1.1*cm,
                          "Kevin D. Rodríguez González · krodriguezge@uanl.edu.mx")
    canvas_obj.drawRightString(width - 2*cm, 1.1*cm, f"Página {doc.page}")
    canvas_obj.drawCentredString(width/2, 1.1*cm,
                                 "Random Forest v3 · Sentinel-2 SR")

    canvas_obj.restoreState()


# ── Construir tabla de estadísticas por parámetro ─────────────────────────────
def build_stats_table(mapas, styles):
    header = ["Parámetro", "Media", "Mín", "Máx", "Desv. Est.", "OOB R²"]
    rows = [header]
    for col, info in mapas.items():
        d = info["data"][np.isfinite(info["data"])]
        rows.append([
            f"{info['icon']} {info['label']}",
            f"{d.mean():.2f} {info['unidad']}",
            f"{d.min():.2f}",
            f"{d.max():.2f}",
            f"{d.std():.2f}",
            f"{info['oob']:.3f}",
        ])

    tbl = Table(rows, colWidths=[4.3*cm, 2.6*cm, 2.0*cm, 2.0*cm, 2.3*cm, 2.0*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8.5),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("ALIGN",      (0,0), (0,-1), "LEFT"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return tbl


# ── Generar texto interpretativo automático ───────────────────────────────────
def generar_interpretacion(mapas, fecha_dt, temporada):
    lineas = []
    lineas.append(
        f"El análisis de calidad de agua del Río Pesquería para la fecha "
        f"{fecha_dt.strftime('%d de %B de %Y')} ({temporada}) se realizó mediante "
        f"interpolación espacial (RBF thin-plate-spline) de las predicciones del "
        f"modelo Random Forest v3, entrenado con imágenes Sentinel-2 SR y datos de "
        f"muestreo fisicoquímico 2016–2019."
    )

    criticos = []
    for col, info in mapas.items():
        d = info["data"][np.isfinite(info["data"])]
        pct_rango = (d.mean() - info["vmin"]) / (info["vmax"] - info["vmin"]) * 100
        if pct_rango > 60:
            criticos.append((info["label"], pct_rango, d.mean(), info["unidad"]))

    if criticos:
        criticos.sort(key=lambda x: -x[1])
        nombres = ", ".join([c[0] for c in criticos])
        lineas.append(
            f"Los parámetros que muestran concentraciones relativamente elevadas "
            f"respecto a su rango de referencia son: {nombres}. Esto podría indicar "
            f"zonas con mayor influencia de descargas de aguas residuales o "
            f"escorrentía con carga orgánica."
        )
    else:
        lineas.append(
            "Los parámetros mapeados se encuentran dentro de rangos moderados a "
            "bajos respecto a su escala de referencia, sin evidencia de "
            "concentraciones críticas en el período analizado."
        )

    lineas.append(
        "Es importante señalar que estos mapas representan una interpolación "
        "espacial entre 7 puntos de muestreo fijos; la incertidumbre aumenta con "
        "la distancia a los puntos de muestreo. Los valores de OOB R² (out-of-bag) "
        "indican la capacidad predictiva validada del modelo para cada parámetro, "
        "siendo más confiables aquellos con OOB R² superior a 0.60."
    )

    return " ".join(lineas)


# ── FUNCIÓN PRINCIPAL: generar PDF para una sola fecha ────────────────────────
def generar_pdf_fecha_unica(mapas, fecha_dt, temporada, panel_buf,
                            bbox, n_puntos, PARAMS_DICT):
    """
    Genera un reporte PDF completo para una sola fecha de análisis.
    mapas: dict con 'data', 'individual_buf', 'label', 'icon', 'desc', etc por param
    Retorna BytesIO con el PDF.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Reporte Calidad de Agua - Río Pesquería"
    )
    styles = get_pdf_styles()
    story = []

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph("💧 REPORTE DE CALIDAD DE AGUA", styles["TituloPortada"]))
    story.append(Paragraph("Río Pesquería, Nuevo León, México", styles["SubtituloPortada"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"<b>Fecha analizada:</b> {fecha_dt.strftime('%d de %B de %Y')} &nbsp;·&nbsp; "
        f"<b>Temporada:</b> {temporada}<br/>"
        f"<b>Modelo:</b> Random Forest v3 (Sentinel-2 SR, 2016–2019)<br/>"
        f"<b>Generado:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))

    story.append(Spacer(1, 0.8*cm))
    if panel_buf:
        panel_buf.seek(0)
        story.append(RLImage(panel_buf, width=16*cm, height=9.5*cm))
    story.append(Spacer(1, 0.6*cm))

    story.append(Paragraph(
        f"<b>Investigador principal:</b> Kevin David Rodríguez González · PhD Student<br/>"
        f"Departamento de Geomática · Facultad de Ingeniería Civil · UANL<br/>"
        f"ORCID: 0009-0004-3060-8575",
        styles["FootnoteCentro"]
    ))
    story.append(PageBreak())

    # ── RESUMEN EJECUTIVO ─────────────────────────────────────────────────────
    story.append(Paragraph("1. Resumen Ejecutivo", styles["SeccionTitulo"]))
    story.append(Paragraph(
        generar_interpretacion(mapas, fecha_dt, temporada),
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── METODOLOGÍA ───────────────────────────────────────────────────────────
    story.append(Paragraph("2. Metodología", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "<b>Fuente de datos espectrales:</b> Sentinel-2 SR Harmonized (Copernicus), "
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
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── ÁREA DE ESTUDIO ───────────────────────────────────────────────────────
    story.append(Paragraph("3. Área de Estudio", styles["SeccionTitulo"]))
    lon_min, lat_min, lon_max, lat_max = bbox
    story.append(Paragraph(
        f"<b>Coordenadas (bbox):</b> Longitud {lon_min:.5f}° a {lon_max:.5f}° · "
        f"Latitud {lat_min:.5f}° a {lat_max:.5f}°<br/>"
        f"<b>Puntos de muestreo:</b> {n_puntos} estaciones fijas (Río Pesquería, "
        f"Nuevo León)<br/>"
        f"<b>Resolución espacial Sentinel-2:</b> 10 m/píxel (bandas visibles e "
        f"infrarrojo cercano)",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.4*cm))

    # ── ESTADÍSTICAS ──────────────────────────────────────────────────────────
    story.append(Paragraph("4. Estadísticas por Parámetro", styles["SeccionTitulo"]))
    story.append(build_stats_table(mapas, styles))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "<i>OOB R² (Out-of-Bag R²): métrica de validación interna del modelo "
        "Random Forest, calculada con muestras no utilizadas en el entrenamiento "
        "de cada árbol. Valores ≥ 0.60 se consideran de buena capacidad predictiva.</i>",
        styles["CuerpoTextoChico"]
    ))
    story.append(PageBreak())

    # ── DESCRIPCIÓN DE PARÁMETROS ─────────────────────────────────────────────
    story.append(Paragraph("5. Descripción de Parámetros Analizados", styles["SeccionTitulo"]))
    for col, info in mapas.items():
        story.append(Paragraph(
            f"{info['icon']} {info['label']} ({info['unidad']})",
            styles["SubseccionTitulo"]
        ))
        story.append(Paragraph(info["desc"], styles["CuerpoTexto"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # ── MAPAS INDIVIDUALES ────────────────────────────────────────────────────
    story.append(Paragraph("6. Mapas de Calidad de Agua por Parámetro", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Los siguientes mapas representan la interpolación espacial RBF de cada "
        "parámetro sobre el área de estudio, con los 7 puntos de muestreo "
        "señalados con su valor observado.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    for col, info in mapas.items():
        if info.get("individual_buf") is not None:
            info["individual_buf"].seek(0)
            story.append(KeepTogether([
                Paragraph(f"{info['icon']} {info['label']}", styles["SubseccionTitulo"]),
                RLImage(info["individual_buf"], width=15.5*cm, height=7*cm),
                Spacer(1, 0.4*cm),
            ]))

    story.append(PageBreak())

    # ── CONCLUSIONES ──────────────────────────────────────────────────────────
    story.append(Paragraph("7. Conclusiones y Limitaciones", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Este reporte presenta una estimación espacial de calidad de agua basada "
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
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        "<b>Citar como:</b> Rodríguez González, K.D. (2026). Water Quality Mapping — "
        "Río Pesquería [Aplicación web]. Universidad Autónoma de Nuevo León, "
        "Facultad de Ingeniería Civil, Departamento de Geomática.",
        styles["CuerpoTextoChico"]
    ))

    doc.build(story, onFirstPage=_draw_header_footer, onLaterPages=_draw_header_footer)
    buf.seek(0)
    return buf


# ── FUNCIÓN: generar PDF de serie temporal completa ───────────────────────────
def generar_pdf_serie_temporal(resultados_por_fecha, params_sel, bbox, n_puntos, PARAMS_DICT):
    """
    Genera un reporte PDF con la evolución temporal de todos los parámetros.
    resultados_por_fecha: dict {fecha_str: {param: {mean, max, min}}}
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Reporte Serie Temporal - Calidad de Agua Río Pesquería"
    )
    styles = get_pdf_styles()
    story = []

    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("💧 REPORTE DE SERIE TEMPORAL", styles["TituloPortada"]))
    story.append(Paragraph("Calidad de Agua — Río Pesquería 2016–2019", styles["SubtituloPortada"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))

    n_fechas = len(resultados_por_fecha)
    story.append(Paragraph(
        f"<b>Período analizado:</b> {n_fechas} fechas de muestreo (2016–2019)<br/>"
        f"<b>Parámetros:</b> {len(params_sel)} variables fisicoquímicas<br/>"
        f"<b>Modelo:</b> Random Forest v3 · Sentinel-2 SR<br/>"
        f"<b>Generado:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph(
        "<b>Investigador principal:</b> Kevin David Rodríguez González · PhD Student<br/>"
        "Departamento de Geomática · Facultad de Ingeniería Civil · UANL<br/>"
        "ORCID: 0009-0004-3060-8575",
        styles["FootnoteCentro"]
    ))
    story.append(PageBreak())

    # ── GRÁFICOS DE EVOLUCIÓN TEMPORAL ────────────────────────────────────────
    story.append(Paragraph("1. Evolución Temporal por Parámetro", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Los siguientes gráficos muestran la media espacial estimada de cada "
        "parámetro a lo largo del período de estudio, calculada sobre el área "
        "completa del wmask mediante interpolación RBF.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    fechas_dt = sorted(resultados_por_fecha.keys())

    for param in params_sel:
        if param not in PARAMS_DICT: continue
        cfg = PARAMS_DICT[param]

        medias, maximos, fechas_validas = [], [], []
        for f in fechas_dt:
            if param in resultados_por_fecha[f]:
                medias.append(resultados_por_fecha[f][param]["mean"])
                maximos.append(resultados_por_fecha[f][param]["max"])
                fechas_validas.append(f)

        if len(fechas_validas) < 2:
            continue

        fig_t, ax_t = plt.subplots(figsize=(7.5, 3))
        fig_t.patch.set_facecolor("white")
        ax_t.set_facecolor("#FAFBFC")

        ax_t.plot(fechas_validas, medias, "o-", color="#2E8B8B", lw=2, ms=5, label="Media espacial")
        ax_t.fill_between(fechas_validas, medias, maximos, alpha=0.15, color="#E74C3C")
        ax_t.plot(fechas_validas, maximos, "s--", color="#E74C3C", lw=1, ms=3, label="Máximo espacial")

        ax_t.set_title(f"{cfg['icon']} {cfg['label']} — Evolución 2016-2019",
                       fontsize=10, fontweight="bold", color="#1A4F7A")
        ax_t.set_ylabel(cfg["unidad"], fontsize=8)
        ax_t.tick_params(axis="x", rotation=40, labelsize=7)
        ax_t.tick_params(axis="y", labelsize=7)
        ax_t.legend(fontsize=7, loc="upper left")
        ax_t.grid(True, alpha=0.25)
        for sp in ax_t.spines.values(): sp.set_edgecolor("#D0D8E0")

        plt.tight_layout()
        buf_t = io.BytesIO()
        fig_t.savefig(buf_t, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig_t)
        buf_t.seek(0)

        story.append(KeepTogether([
            RLImage(buf_t, width=15.5*cm, height=6.2*cm),
            Spacer(1, 0.3*cm),
        ]))

    story.append(PageBreak())

    # ── TABLA RESUMEN POR FECHA ───────────────────────────────────────────────
    story.append(Paragraph("2. Tabla Resumen — Medias por Fecha", styles["SeccionTitulo"]))

    header = ["Fecha"] + [PARAMS_DICT[p]["label"] if p in PARAMS_DICT else p for p in params_sel]
    rows = [header]
    for f in fechas_dt:
        fila = [pd.to_datetime(f).strftime("%d/%m/%Y")]
        for p in params_sel:
            if p in resultados_por_fecha[f]:
                fila.append(f"{resultados_por_fecha[f][p]['mean']:.2f}")
            else:
                fila.append("—")
        rows.append(fila)

    col_widths = [2.4*cm] + [(17*cm - 2.4*cm)/len(params_sel)]*len(params_sel)
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 7.5),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(tbl)
    story.append(PageBreak())

    # ── INTERPRETACIÓN TEMPORAL ───────────────────────────────────────────────
    story.append(Paragraph("3. Interpretación de Tendencias", styles["SeccionTitulo"]))

    interp_parts = []
    for param in params_sel:
        if param not in PARAMS_DICT: continue
        cfg = PARAMS_DICT[param]
        vals = [resultados_por_fecha[f][param]["mean"]
               for f in fechas_dt if param in resultados_por_fecha[f]]
        if len(vals) < 2: continue

        tendencia = "incremento" if vals[-1] > vals[0] else "disminución"
        cambio_pct = abs((vals[-1] - vals[0]) / (vals[0] + 1e-9)) * 100

        interp_parts.append(
            f"<b>{cfg['label']}</b>: se observa una tendencia de {tendencia} de "
            f"aproximadamente {cambio_pct:.0f}% entre el inicio y el final del "
            f"período analizado (de {vals[0]:.2f} a {vals[-1]:.2f} {cfg['unidad']})."
        )

    story.append(Paragraph(" ".join(interp_parts), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        "<b>Nota metodológica:</b> Las variaciones temporales pueden estar "
        "influenciadas por estacionalidad (temporada seca vs. lluviosa), cambios "
        "en el caudal del río, y eventos puntuales de descarga. Se recomienda "
        "complementar este análisis con datos de precipitación y caudal para "
        "una interpretación hidrológica completa.",
        styles["CuerpoTextoChico"]
    ))

    doc.build(story, onFirstPage=_draw_header_footer, onLaterPages=_draw_header_footer)
    buf.seek(0)
    return buf
