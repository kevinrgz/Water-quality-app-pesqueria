# =============================================================================
# MÓDULO DE GENERACIÓN DE REPORTES PDF
# =============================================================================

import io
from datetime import date
from i18n import t, get_param_label, get_param_desc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
def _draw_header_footer(canvas_obj, doc, titulo_corto="Calidad de Agua — Río Pesquería",
                        logo_geo_path=None, lang="es"):
    canvas_obj.saveState()
    width, height = letter

    canvas_obj.setStrokeColor(PDF_TEAL)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(2*cm, height - 1.4*cm, width - 2*cm, height - 1.4*cm)

    # Logo del departamento en la esquina superior derecha
    if logo_geo_path:
        try:
            canvas_obj.drawImage(logo_geo_path, width - 4.2*cm, height - 1.85*cm,
                                 width=2.2*cm, height=0.55*cm,
                                 preserveAspectRatio=True, mask="auto")
        except Exception:
            pass

    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(PDF_GREY)
    canvas_obj.drawString(2*cm, height - 1.2*cm, titulo_corto)

    canvas_obj.setLineWidth(0.6)
    canvas_obj.line(2*cm, 1.5*cm, width - 2*cm, 1.5*cm)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.drawCentredString(width/2, 1.1*cm, f"{t('pdf_pagina', lang)} {doc.page}")
    canvas_obj.drawRightString(width - 2*cm, 1.1*cm, t("pdf_universidad", lang))

    canvas_obj.restoreState()


# ── Construir tabla de estadísticas por parámetro ─────────────────────────────
def build_stats_table(mapas, styles, lang="es"):
    header = [t("pdf_tabla_parametro", lang), t("pdf_tabla_media", lang),
              t("pdf_tabla_min", lang), t("pdf_tabla_max", lang),
              t("pdf_tabla_desv", lang), "OOB R²"]
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
def generar_interpretacion(mapas, fecha_dt, temporada, lang="es"):
    lineas = []
    lineas.append(
        t("pdf_interp_intro", lang).format(
            fecha=fecha_dt.strftime('%d de %B de %Y'), temporada=temporada
        )
    )

    criticos = []
    for col, info in mapas.items():
        d = info["data"][np.isfinite(info["data"])]
        pct_rango = (d.mean() - info["vmin"]) / (info["vmax"] - info["vmin"]) * 100
        label_t = get_param_label(col, lang) if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["label"]
        if pct_rango > 60:
            criticos.append((label_t, pct_rango, d.mean(), info["unidad"]))

    if criticos:
        criticos.sort(key=lambda x: -x[1])
        nombres = ", ".join([c[0] for c in criticos])
        lineas.append(t("pdf_interp_criticos", lang).format(nombres=nombres))
    else:
        lineas.append(t("pdf_interp_normal", lang))

    lineas.append(t("pdf_interp_cierre", lang))

    return " ".join(lineas)


# ── FUNCIÓN PRINCIPAL: generar PDF para una sola fecha ────────────────────────
def generar_pdf_fecha_unica(mapas, fecha_dt, temporada, panel_buf,
                            bbox, n_puntos, PARAMS_DICT,
                            rgb_buf=None, logo_geo_path=None, lang="es"):
    """
    Genera un reporte PDF completo para una sola fecha de análisis.
    mapas: dict con 'data', 'individual_buf', 'label', 'icon', 'desc', etc por param
    lang: "es", "en" o "pt" — idioma del reporte completo
    Retorna BytesIO con el PDF.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Water Quality Report - Pesqueria River"
    )
    styles = get_pdf_styles()
    story = []

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph(t("pdf_titulo_reporte", lang), styles["TituloPortada"]))
    story.append(Paragraph(t("pdf_subtitulo_rio", lang), styles["SubtituloPortada"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"<b>{t('pdf_fecha_analizada', lang)}:</b> {fecha_dt.strftime('%d de %B de %Y')} &nbsp;·&nbsp; "
        f"<b>{t('pdf_temporada', lang)}:</b> {temporada}<br/>"
        f"<b>{t('pdf_modelo', lang)}:</b> Random Forest v3 (Sentinel-2 SR, 2016–2019)<br/>"
        f"<b>{t('pdf_generado', lang)}:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))

    story.append(Spacer(1, 0.8*cm))
    if panel_buf:
        panel_buf.seek(0)
        story.append(RLImage(panel_buf, width=16*cm, height=9.5*cm))
    story.append(Spacer(1, 0.6*cm))

    story.append(Paragraph(t("pdf_nota_auto", lang), styles["FootnoteCentro"]))
    story.append(PageBreak())

    # ── RESUMEN EJECUTIVO ─────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec1_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(
        generar_interpretacion(mapas, fecha_dt, temporada, lang),
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── METODOLOGÍA ───────────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec2_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_metodologia_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))

    # ── ÁREA DE ESTUDIO ───────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec3_titulo", lang), styles["SeccionTitulo"]))
    lon_min, lat_min, lon_max, lat_max = bbox
    story.append(Paragraph(
        f"<b>{t('pdf_coordenadas', lang)}:</b> {t('pdf_longitud', lang)} {lon_min:.5f}° "
        f"a {lon_max:.5f}° · {t('pdf_latitud', lang)} {lat_min:.5f}° a {lat_max:.5f}°<br/>"
        f"<b>{t('pdf_puntos_muestreo', lang)}:</b> {n_puntos} {t('pdf_estaciones_fijas', lang)}<br/>"
        f"<b>{t('pdf_resolucion_s2', lang)}:</b> {t('pdf_res_detalle', lang)}",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    if rgb_buf is not None:
        story.append(Paragraph(t("pdf_imagen_satelital_texto", lang), styles["CuerpoTextoChico"]))
        story.append(Spacer(1, 0.2*cm))
        rgb_buf.seek(0)
        story.append(RLImage(rgb_buf, width=14*cm, height=8*cm))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"<i>{t('pdf_fuente_copernicus', lang)}</i>", styles["FootnoteCentro"]))

    story.append(Spacer(1, 0.4*cm))

    # ── ESTADÍSTICAS ──────────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec4_titulo", lang), styles["SeccionTitulo"]))
    story.append(build_stats_table(mapas, styles, lang))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(t("pdf_oob_nota", lang), styles["CuerpoTextoChico"]))
    story.append(PageBreak())

    # ── DESCRIPCIÓN DE PARÁMETROS ─────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec5_titulo", lang), styles["SeccionTitulo"]))
    for col, info in mapas.items():
        label_t = get_param_label(col, lang) if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["label"]
        desc_t  = get_param_desc(col, lang)  if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["desc"]
        story.append(Paragraph(
            f"{info['icon']} {label_t} ({info['unidad']})",
            styles["SubseccionTitulo"]
        ))
        story.append(Paragraph(desc_t, styles["CuerpoTexto"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # ── MAPAS INDIVIDUALES ────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec6_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_sec6_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))

    for col, info in mapas.items():
        label_t = get_param_label(col, lang) if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["label"]
        if info.get("individual_buf") is not None:
            info["individual_buf"].seek(0)
            story.append(KeepTogether([
                Paragraph(f"{info['icon']} {label_t}", styles["SubseccionTitulo"]),
                RLImage(info["individual_buf"], width=15.5*cm, height=7*cm),
                Spacer(1, 0.4*cm),
            ]))

    story.append(PageBreak())

    # ── CONCLUSIONES ──────────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_sec7_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_conclusiones_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"<b>{t('pdf_citar_como', lang)}:</b> Rodríguez González, K.D. (2026). "
        f"Water Quality Mapping — Río Pesquería [Web Application]. "
        f"Universidad Autónoma de Nuevo León, Facultad de Ingeniería Civil, "
        f"Departamento de Geomática.",
        styles["CuerpoTextoChico"]
    ))

    from functools import partial
    header_fn = partial(_draw_header_footer, logo_geo_path=logo_geo_path, lang=lang)
    doc.build(story, onFirstPage=header_fn, onLaterPages=header_fn)
    buf.seek(0)
    return buf


# ── FUNCIÓN: generar PDF de serie temporal completa ───────────────────────────
def generar_pdf_serie_temporal(resultados_por_fecha, params_sel, bbox, n_puntos, PARAMS_DICT,
                               logo_geo_path=None, lang="es"):
    """
    Genera un reporte PDF con la evolución temporal de todos los parámetros.
    resultados_por_fecha: dict {fecha_str: {param: {mean, max, min}}}
    lang: "es", "en" o "pt"
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Time Series Report - Pesqueria River Water Quality"
    )
    styles = get_pdf_styles()
    story = []

    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(t("pdf_serie_titulo", lang), styles["TituloPortada"]))
    story.append(Paragraph(t("pdf_serie_subtitulo", lang), styles["SubtituloPortada"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))

    n_fechas = len(resultados_por_fecha)
    story.append(Paragraph(
        f"<b>{t('pdf_serie_periodo', lang)}:</b> {n_fechas} {t('pdf_serie_fechas_muestreo', lang)}<br/>"
        f"<b>{t('pdf_serie_parametros', lang)}:</b> {len(params_sel)} {t('pdf_serie_variables', lang)}<br/>"
        f"<b>{t('pdf_modelo', lang)}:</b> Random Forest v3 · Sentinel-2 SR<br/>"
        f"<b>{t('pdf_generado', lang)}:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph(t("pdf_nota_auto", lang), styles["FootnoteCentro"]))
    story.append(PageBreak())

    # ── GRÁFICOS DE EVOLUCIÓN TEMPORAL ────────────────────────────────────────
    story.append(Paragraph(t("pdf_serie_sec1", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_serie_sec1_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))

    fechas_dt = sorted(resultados_por_fecha.keys())

    for param in params_sel:
        if param not in PARAMS_DICT: continue
        cfg = PARAMS_DICT[param]
        label_t = get_param_label(param, lang) if param in ("P_TOT","N_NH3","N_TOT","N_TOTK") else cfg["label"]

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

        media_label = t("pdf_serie_media_espacial", lang)
        max_label   = t("pdf_serie_maximo_espacial", lang)

        ax_t.plot(fechas_validas, medias, "o-", color="#2E8B8B", lw=2, ms=5, label=media_label)
        ax_t.fill_between(fechas_validas, medias, maximos, alpha=0.15, color="#E74C3C")
        ax_t.plot(fechas_validas, maximos, "s--", color="#E74C3C", lw=1, ms=3, label=max_label)

        ax_t.set_title(f"{label_t} — {t('pdf_serie_evolucion', lang)}",
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
    story.append(Paragraph(t("pdf_serie_sec2", lang), styles["SeccionTitulo"]))

    header = [t("pdf_serie_fecha", lang)] + [
        get_param_label(p, lang) if p in ("P_TOT","N_NH3","N_TOT","N_TOTK")
        else (PARAMS_DICT[p]["label"] if p in PARAMS_DICT else p)
        for p in params_sel
    ]
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
    story.append(Paragraph(t("pdf_serie_sec3", lang), styles["SeccionTitulo"]))

    interp_parts = []
    for param in params_sel:
        if param not in PARAMS_DICT: continue
        cfg = PARAMS_DICT[param]
        label_t = get_param_label(param, lang) if param in ("P_TOT","N_NH3","N_TOT","N_TOTK") else cfg["label"]
        vals = [resultados_por_fecha[f][param]["mean"]
               for f in fechas_dt if param in resultados_por_fecha[f]]
        if len(vals) < 2: continue

        tendencia = (t("pdf_serie_tendencia_incremento", lang) if vals[-1] > vals[0]
                    else t("pdf_serie_tendencia_disminucion", lang))
        cambio_pct = abs((vals[-1] - vals[0]) / (vals[0] + 1e-9)) * 100

        interp_parts.append(
            f"<b>{label_t}</b>: {t('pdf_serie_tendencia_texto', lang)} {tendencia} "
            f"~{cambio_pct:.0f}% {t('pdf_serie_tendencia_texto2', lang)} "
            f"{vals[0]:.2f} {t('pdf_serie_tendencia_texto3', lang)} "
            f"{vals[-1]:.2f} {cfg['unidad']})."
        )

    story.append(Paragraph(" ".join(interp_parts), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(t("pdf_serie_nota_metodologica", lang), styles["CuerpoTextoChico"]))

    from functools import partial
    header_fn2 = partial(_draw_header_footer, logo_geo_path=logo_geo_path, lang=lang)
    doc.build(story, onFirstPage=header_fn2, onLaterPages=header_fn2)
    buf.seek(0)
    return buf


# =============================================================================
# REPORTE DE ÍNDICES ESPECTRALES — válido para cualquier zona del mundo
# =============================================================================

def _interpretar_ndvi(valor, lang="es"):
    """Clasifica NDVI según umbrales estándar (Tucker, 1979; Huete et al.)."""
    if valor is None: return t("pdf_idx_sin_datos", lang)
    if valor < 0.0:   return t("pdf_ndvi_agua_suelo", lang)
    if valor < 0.2:   return t("pdf_ndvi_muy_baja", lang)
    if valor < 0.4:   return t("pdf_ndvi_baja", lang)
    if valor < 0.6:   return t("pdf_ndvi_moderada", lang)
    return t("pdf_ndvi_alta", lang)

def _interpretar_ndwi(valor, lang="es"):
    """Clasifica NDWI según McFeeters (1996)."""
    if valor is None: return t("pdf_idx_sin_datos", lang)
    if valor > 0.3:   return t("pdf_ndwi_agua_clara", lang)
    if valor > 0.0:   return t("pdf_ndwi_agua_posible", lang)
    if valor > -0.3:  return t("pdf_ndwi_suelo_mixto", lang)
    return t("pdf_ndwi_vegetacion_suelo", lang)

def _interpretar_mndwi(valor, lang="es"):
    """Clasifica MNDWI según Xu (2006), mejor para zonas urbanas/turbias."""
    if valor is None: return t("pdf_idx_sin_datos", lang)
    if valor > 0.3:   return t("pdf_mndwi_agua_clara", lang)
    if valor > 0.0:   return t("pdf_mndwi_agua_turbia", lang)
    if valor > -0.3:  return t("pdf_mndwi_suelo_humedo", lang)
    return t("pdf_mndwi_suelo_seco", lang)

def _interpretar_ndti(valor, lang="es"):
    """Clasifica NDTI (turbidez relativa, sin unidades absolutas en NTU)."""
    if valor is None: return t("pdf_idx_sin_datos", lang)
    if valor < -0.1:  return t("pdf_ndti_muy_baja", lang)
    if valor < 0.05:  return t("pdf_ndti_baja", lang)
    if valor < 0.15:  return t("pdf_ndti_moderada", lang)
    return t("pdf_ndti_alta", lang)

_INTERPRETADORES = {
    "NDVI": _interpretar_ndvi, "NDWI": _interpretar_ndwi,
    "MNDWI": _interpretar_mndwi, "NDTI": _interpretar_ndti,
}


def build_indices_stats_table(stats, indices_sel, styles, lang="es"):
    """Tabla de estadísticas zonales reales por índice espectral."""
    header = [t("pdf_idx_tabla_indice", lang), t("pdf_tabla_media", lang),
              t("pdf_idx_tabla_desv", lang), t("pdf_tabla_min", lang),
              t("pdf_tabla_max", lang), "P50 (mediana)"]
    rows = [header]
    for idx_name in indices_sel:
        s = stats.get(idx_name, {})
        mean_v = s.get("mean")
        rows.append([
            idx_name,
            f"{mean_v:.3f}" if mean_v is not None else "—",
            f"{s.get('std'):.3f}" if s.get('std') is not None else "—",
            f"{s.get('min'):.3f}" if s.get('min') is not None else "—",
            f"{s.get('max'):.3f}" if s.get('max') is not None else "—",
            f"{s.get('p50'):.3f}" if s.get('p50') is not None else "—",
        ])

    tbl = Table(rows, colWidths=[2.5*cm, 2.6*cm, 2.6*cm, 2.5*cm, 2.5*cm, 2.8*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_TEAL),
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


def generar_interpretacion_espectral(stats, indices_sel, lang="es"):
    """Genera un párrafo interpretativo automático para el reporte espectral."""
    partes = [t("pdf_idx_interp_intro", lang)]

    for idx_name in indices_sel:
        s = stats.get(idx_name, {})
        mean_v = s.get("mean")
        if mean_v is None:
            continue
        interpretador = _INTERPRETADORES.get(idx_name)
        clase = interpretador(mean_v, lang) if interpretador else ""
        partes.append(
            f"<b>{idx_name}</b>: {t('pdf_idx_interp_valor_medio', lang)} "
            f"{mean_v:.3f} — {clase}."
        )

    partes.append(t("pdf_idx_interp_cierre", lang))
    return " ".join(partes)


def generar_pdf_reporte_espectral(info, stats, thumbnails, indices_sel, bbox,
                                  fecha_ini, fecha_fin, logo_geo_path=None,
                                  lang="es"):
    """
    Genera un reporte PDF de índices espectrales (RGB + NDVI/NDWI/MNDWI/NDTI)
    válido para CUALQUIER zona del mundo — no depende de ningún modelo
    entrenado, solo de la imagen Sentinel-2 real y sus bandas.

    info: dict con n_imagenes, nubes_pct, fecha_real, area_km2
    stats: dict {indice: {mean, std, min, max, p10, p50, p90}}
    thumbnails: dict {capa: BytesIO} con las imágenes PNG de cada capa
    indices_sel: lista de índices a incluir (ej. ["NDVI","NDWI","MNDWI","NDTI"])
    bbox: (lon_min, lat_min, lon_max, lat_max)
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Spectral Indices Report"
    )
    styles = get_pdf_styles()
    story = []

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph(t("pdf_idx_titulo_reporte", lang), styles["TituloPortada"]))
    story.append(Paragraph(t("pdf_idx_subtitulo", lang), styles["SubtituloPortada"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))

    lon_min, lat_min, lon_max, lat_max = bbox
    story.append(Paragraph(
        f"<b>{t('pdf_idx_periodo_imagen', lang)}:</b> "
        f"{fecha_ini.strftime('%d %b %Y')} → {fecha_fin.strftime('%d %b %Y')}<br/>"
        f"<b>{t('pdf_idx_fecha_real', lang)}:</b> {info.get('fecha_real', 'N/D')}<br/>"
        f"<b>{t('pdf_idx_area', lang)}:</b> {info.get('area_km2', '—')} km² &nbsp;·&nbsp; "
        f"<b>{t('pdf_idx_nubes', lang)}:</b> {info.get('nubes_pct', '—')}%<br/>"
        f"<b>{t('pdf_generado', lang)}:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 0.7*cm))

    if "RGB" in thumbnails:
        thumbnails["RGB"].seek(0)
        story.append(RLImage(thumbnails["RGB"], width=13*cm, height=9*cm))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"<i>{t('pdf_fuente_copernicus', lang)}</i>",
                               styles["FootnoteCentro"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(t("pdf_idx_nota_auto", lang), styles["FootnoteCentro"]))
    story.append(PageBreak())

    # ── RESUMEN INTERPRETATIVO ────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec1_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(
        generar_interpretacion_espectral(stats, indices_sel, lang),
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── METODOLOGÍA ───────────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec2_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_idx_metodologia_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))

    # ── ÁREA DE ESTUDIO ───────────────────────────────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec3_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(
        f"<b>{t('pdf_coordenadas', lang)}:</b> {t('pdf_longitud', lang)} "
        f"{lon_min:.5f}° a {lon_max:.5f}° · {t('pdf_latitud', lang)} "
        f"{lat_min:.5f}° a {lat_max:.5f}°<br/>"
        f"<b>{t('pdf_idx_area', lang)}:</b> {info.get('area_km2', '—')} km²<br/>"
        f"<b>{t('pdf_resolucion_s2', lang)}:</b> {t('pdf_res_detalle', lang)}",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.4*cm))

    # ── TABLA DE ESTADÍSTICAS ZONALES ─────────────────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec4_titulo", lang), styles["SeccionTitulo"]))
    story.append(build_indices_stats_table(stats, indices_sel, styles, lang))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(t("pdf_idx_stats_nota", lang), styles["CuerpoTextoChico"]))
    story.append(PageBreak())

    # ── MAPAS DE CADA ÍNDICE CON INTERPRETACIÓN ───────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec5_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_idx_sec5_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))

    for idx_name in indices_sel:
        if idx_name not in thumbnails:
            continue
        s = stats.get(idx_name, {})
        mean_v = s.get("mean")
        interpretador = _INTERPRETADORES.get(idx_name)
        clase = interpretador(mean_v, lang) if interpretador else ""

        thumbnails[idx_name].seek(0)
        bloque = [
            Paragraph(idx_name, styles["SubseccionTitulo"]),
            RLImage(thumbnails[idx_name], width=11*cm, height=7.7*cm),
            Spacer(1, 0.15*cm),
            Paragraph(
                f"{t('pdf_idx_valor_medio_zona', lang)}: <b>{mean_v:.3f}</b> "
                f"(σ={s.get('std', 0):.3f}) — {clase}",
                styles["CuerpoTextoChico"]
            ),
            Spacer(1, 0.4*cm),
        ]
        story.append(KeepTogether(bloque))

    story.append(PageBreak())

    # ── APLICACIONES Y RECOMENDACIONES ────────────────────────────────────────
    story.append(Paragraph(t("pdf_idx_sec6_titulo", lang), styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_idx_sec6_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        f"<b>{t('pdf_citar_como', lang)}:</b> Water Quality &amp; Spectral "
        f"Indices Mapping Tool. Universidad Autónoma de Nuevo León, "
        f"Facultad de Ingeniería Civil, Departamento de Geomática.",
        styles["CuerpoTextoChico"]
    ))

    from functools import partial
    header_fn3 = partial(_draw_header_footer, logo_geo_path=logo_geo_path, lang=lang,
                         titulo_corto="Spectral Indices Report")
    doc.build(story, onFirstPage=header_fn3, onLaterPages=header_fn3)
    buf.seek(0)
    return buf
