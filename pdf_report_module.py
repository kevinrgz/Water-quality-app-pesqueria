# =============================================================================
# MÓDULO DE GENERACIÓN DE REPORTES PDF
# =============================================================================

import io
from datetime import date
from i18n import t, get_param_label, get_param_desc, get_indice_nombre, get_indice_desc
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats as sp_stats

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

# ── Paleta institucional ──────────────────────────────────────────────────────
PDF_BLUE   = colors.HexColor("#1A4F7A")
PDF_TEAL   = colors.HexColor("#2E8B8B")
PDF_GREEN  = colors.HexColor("#3DBA7A")
PDF_GREY   = colors.HexColor("#6B7280")
PDF_LIGHT  = colors.HexColor("#F0F4F8")
PDF_DARK   = colors.HexColor("#1A1A2E")
PDF_AMBER  = colors.HexColor("#D97706")
PDF_RED    = colors.HexColor("#DC2626")


# ── Estilos de texto ──────────────────────────────────────────────────────────
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
        name="CuerpoTexto", fontSize=9.5, leading=14.5,
        textColor=colors.HexColor("#2A2A2A"),
        fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=6))
    styles.add(ParagraphStyle(
        name="CuerpoTextoChico", fontSize=8.3, leading=12, textColor=PDF_GREY,
        fontName="Helvetica", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(
        name="FootnoteCentro", fontSize=7.5, leading=10, textColor=PDF_GREY,
        fontName="Helvetica-Oblique", alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        name="Credito", fontSize=8, leading=11,
        textColor=colors.HexColor("#94A3B8"),
        fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=2))
    styles.add(ParagraphStyle(
        name="AlertaRoja", fontSize=9, leading=13,
        textColor=colors.HexColor("#7F1D1D"),
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        backColor=colors.HexColor("#FEE2E2"),
        borderPadding=(4, 6, 4, 6)))
    return styles


# ── Encabezado y pie de página ────────────────────────────────────────────────
def _draw_header_footer(canvas_obj, doc, titulo_corto="Calidad de Agua — Río Pesquería",
                        logo_geo_path=None, lang="es"):
    canvas_obj.saveState()
    width, height = letter

    _logo_w, _logo_h = 3.6*cm, 0.74*cm
    _logo_x = width - _logo_w - 1.5*cm
    _logo_y = height - _logo_h - 0.35*cm
    if logo_geo_path:
        try:
            import os as _os
            _orig = logo_geo_path.replace("logo_geomatica.png", "logo_geomatica_original.png")
            _logo_pdf = _orig if _os.path.exists(_orig) else logo_geo_path
            canvas_obj.drawImage(_logo_pdf, _logo_x, _logo_y,
                                 width=_logo_w, height=_logo_h,
                                 preserveAspectRatio=True, mask="auto")
        except Exception:
            pass

    _line_y = _logo_y - 0.18*cm
    canvas_obj.setStrokeColor(PDF_TEAL)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(2*cm, _line_y, width - 2*cm, _line_y)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(PDF_GREY)
    canvas_obj.drawString(2*cm, _line_y + 0.22*cm, titulo_corto)

    canvas_obj.setLineWidth(0.6)
    canvas_obj.line(2*cm, 1.5*cm, width - 2*cm, 1.5*cm)
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.drawCentredString(width/2, 1.1*cm, f"{t('pdf_pagina', lang)} {doc.page}")
    canvas_obj.drawRightString(width - 2*cm, 1.1*cm, t("pdf_universidad", lang))
    canvas_obj.restoreState()


# ── Tabla de estadísticas de calidad de agua ──────────────────────────────────
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
            f"{d.min():.2f}", f"{d.max():.2f}",
            f"{d.std():.2f}", f"{info['oob']:.3f}",
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


# ── Texto interpretativo automático (calidad de agua) ─────────────────────────
def generar_interpretacion(mapas, fecha_dt, temporada, lang="es"):
    lineas = [t("pdf_interp_intro", lang).format(
        fecha=fecha_dt.strftime('%d de %B de %Y'), temporada=temporada)]
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


# ── Utilidad: reducir etiquetas de fechas si hay demasiadas ──────────────────
def _format_fechas_eje(fechas_str, max_ticks=12):
    """
    Convierte lista de strings de fecha a etiquetas legibles tipo 'Ene 18'.
    Si hay más de max_ticks puntos, muestra solo un subconjunto equiespaciado.
    Retorna (indices_a_mostrar, etiquetas).
    """
    meses_es = ["","Ene","Feb","Mar","Abr","May","Jun",
                "Jul","Ago","Sep","Oct","Nov","Dic"]
    etiquetas = []
    for f in fechas_str:
        try:
            dt = pd.to_datetime(f)
            etiquetas.append(f"{meses_es[dt.month]} {str(dt.year)[2:]}")
        except Exception:
            etiquetas.append(str(f)[:7])

    n = len(etiquetas)
    if n <= max_ticks:
        return list(range(n)), etiquetas

    # Subconjunto equiespaciado incluyendo primero y último
    step = max(1, n // max_ticks)
    idx = list(range(0, n, step))
    if (n - 1) not in idx:
        idx.append(n - 1)
    return idx, [etiquetas[i] for i in idx]


def _aplicar_eje_x(ax, fechas_str, max_ticks=12):
    idx, labels = _format_fechas_eje(fechas_str, max_ticks)
    ax.set_xticks(idx)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7.5)


# ── Gráfico de serie temporal para un parámetro (matplotlib → BytesIO) ────────
def _figura_serie_param(fechas, medias, maximos, label, unidad, color_linea="#2E8B8B"):
    xnum = np.arange(len(fechas))
    fig, ax = plt.subplots(figsize=(7.5, 2.9))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#FAFBFC")
    ax.plot(xnum, medias, "o-", color=color_linea, lw=2, ms=5, label="Media espacial")
    if maximos and any(m is not None for m in maximos):
        ax.fill_between(xnum, medias, maximos, alpha=0.13, color="#E74C3C")
        ax.plot(xnum, maximos, "s--", color="#E74C3C", lw=1, ms=3, label="Máximo espacial")
    if len(xnum) >= 3:
        z = np.polyfit(xnum, medias, 1)
        trend = np.polyval(z, xnum)
        ax.plot(xnum, trend, "--", color="#F59E0B", lw=1.2, alpha=0.8, label="Tendencia lineal")
        tau, pval = sp_stats.kendalltau(xnum, medias)
        dir_str = "↑ Ascendente" if tau > 0 else "↓ Descendente"
        sig_str = "(p<0.05 ✓)" if pval < 0.05 else f"(p={pval:.2f})"
        ax.text(0.01, 0.96, f"Mann-Kendall: {dir_str} {sig_str}",
                transform=ax.transAxes, fontsize=7, color="#374151",
                verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="#F0F4F8", ec="#D0D8E0", lw=0.6))
    ax.set_title(f"{label} — Evolución temporal", fontsize=9.5, fontweight="bold", color="#1A4F7A")
    ax.set_ylabel(unidad, fontsize=7.5)
    _aplicar_eje_x(ax, fechas)
    ax.tick_params(axis="y", labelsize=7)
    ax.legend(fontsize=7, loc="upper right", framealpha=0.7)
    ax.grid(True, alpha=0.2, linestyle="--")
    for sp in ax.spines.values(): sp.set_edgecolor("#D0D8E0")
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf


# ── Gráfico de serie temporal GEE para un índice espectral ───────────────────
def _figura_serie_gee(serie, nombre_idx, color="#22D3EE"):
    """serie: lista de (fecha_str, valor)"""
    if not serie or len(serie) < 2:
        return None
    fechas = [s[0] for s in serie]
    vals   = [s[1] for s in serie]
    xnum   = np.arange(len(vals))
    fig, ax = plt.subplots(figsize=(7.5, 2.9))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#FAFBFC")
    ax.plot(xnum, vals, "o-", color=color, lw=2, ms=5, label="Media zonal")
    z = np.polyfit(xnum, vals, 1)
    trend = np.polyval(z, xnum)
    ax.plot(xnum, trend, "--", color="#F59E0B", lw=1.2, alpha=0.8, label="Tendencia lineal")
    tau, pval = sp_stats.kendalltau(xnum, vals)
    dir_str = "↑ Ascendente" if tau > 0 else "↓ Descendente"
    sig_str = "(p<0.05 ✓)" if pval < 0.05 else f"(p={pval:.2f})"
    ax.text(0.01, 0.96, f"Mann-Kendall: {dir_str} {sig_str}",
            transform=ax.transAxes, fontsize=7, color="#374151",
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", fc="#F0F4F8", ec="#D0D8E0", lw=0.6))
    ax.set_title(f"{nombre_idx} — Serie temporal (media zonal)", fontsize=9.5,
                 fontweight="bold", color="#1A4F7A")
    ax.set_ylabel(nombre_idx, fontsize=7.5)
    _aplicar_eje_x(ax, fechas)
    ax.tick_params(axis="y", labelsize=7)
    ax.legend(fontsize=7, loc="upper right", framealpha=0.7)
    ax.grid(True, alpha=0.2, linestyle="--")
    for sp in ax.spines.values(): sp.set_edgecolor("#D0D8E0")
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf


# ── Tabla resumen de series temporales GEE ────────────────────────────────────
def _tabla_resumen_series(series_gee, indices_sel, styles):
    """series_gee: {indice: [(fecha, valor), ...]}"""
    header = ["Índice", "N imágenes", "Mínimo", "Máximo", "Media", "Tendencia MK"]
    rows = [header]
    for idx in indices_sel:
        serie = series_gee.get(idx, [])
        if not serie:
            rows.append([idx, "—", "—", "—", "—", "—"])
            continue
        vals = [v for _, v in serie]
        tau, pval = sp_stats.kendalltau(range(len(vals)), vals)
        dir_str = "↑" if tau > 0 else "↓"
        sig = "sig." if pval < 0.05 else "n.s."
        rows.append([
            idx, str(len(serie)),
            f"{min(vals):.4f}", f"{max(vals):.4f}",
            f"{sum(vals)/len(vals):.4f}",
            f"{dir_str} τ={tau:.2f} ({sig})"
        ])
    tbl = Table(rows, colWidths=[2.2*cm, 2.0*cm, 2.2*cm, 2.2*cm, 2.2*cm, 4.2*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_TEAL),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("ALIGN",      (0,0), (0,-1), "LEFT"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return tbl


# =============================================================================
# FUNCIÓN: PDF para una sola fecha de calidad de agua
# =============================================================================
def generar_pdf_fecha_unica(mapas, fecha_dt, temporada, panel_buf,
                            bbox, n_puntos, PARAMS_DICT,
                            rgb_buf=None, logo_geo_path=None, lang="es",
                            resultados_por_fecha=None, df_campo=None):
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
    story.append(Spacer(1, 0.25*cm))
    story.append(HRFlowable(width="40%", thickness=0.5, color=colors.HexColor("#CBD5E1"), hAlign="CENTER"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Designed by Kevin Rodríguez González", styles["Credito"]))
    story.append(Paragraph("Departamento de Geomática · UANL · FIC", styles["Credito"]))
    story.append(PageBreak())

    # ── 1. INTRODUCCIÓN ────────────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "El monitoreo de la calidad del agua en cuerpos superficiales es fundamental para la "
        "gestión ambiental y la protección de los recursos hídricos. Este reporte presenta los "
        "resultados del análisis de parámetros fisicoquímicos y microbiológicos del Río Pesquería, "
        "Nuevo León, México, obtenidos mediante teledetección satelital con Sentinel-2 y modelos "
        "de machine learning (Random Forest) calibrados con datos de campo del período 2016–2019. "
        "La plataforma Water Quality Mapping, desarrollada por el Departamento de Geomática de la "
        "UANL, integra imágenes Sentinel-2 SR a 10 m de resolución con algoritmos de estimación "
        "de calidad de agua para producir mapas espacialmente continuos de los principales "
        "indicadores ambientales.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 2. RESUMEN EJECUTIVO ───────────────────────────────────────────────────
    story.append(Paragraph("2. Resumen Ejecutivo", styles["SeccionTitulo"]))
    story.append(Paragraph(
        generar_interpretacion(mapas, fecha_dt, temporada, lang),
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 3. METODOLOGÍA ────────────────────────────────────────────────────────
    story.append(Paragraph("3. Metodología", styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_metodologia_texto", lang), styles["CuerpoTexto"]))

    # Tabla metodológica compacta
    met_rows = [
        ["Componente", "Detalle"],
        ["Sensor", "Sentinel-2 MSI (ESA Copernicus), 10 m de resolución espacial"],
        ["Colección GEE", "COPERNICUS/S2_SR_HARMONIZED (reflectancia de superficie)"],
        ["Modelo ML", "Random Forest v3 — 500 árboles, variables: B2, B3, B4, B5, B8, NDVI, NDWI"],
        ["Validación", "Out-Of-Bag (OOB) R² y RMSE con datos de campo 2016–2019 (7 estaciones)"],
        ["Parámetros", f"{len(mapas)} variables fisicoquímicas y microbiológicas"],
        ["Generado con", "Google Earth Engine · Python · Streamlit · Geomática UANL"],
    ]
    met_tbl = Table(met_rows, colWidths=[4*cm, 12*cm])
    met_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(met_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── 4. ÁREA DE ESTUDIO ────────────────────────────────────────────────────
    story.append(Paragraph("4. Área de Estudio", styles["SeccionTitulo"]))
    lon_min, lat_min, lon_max, lat_max = bbox
    story.append(Paragraph(
        f"<b>{t('pdf_coordenadas', lang)}:</b> Longitud {lon_min:.5f}° a {lon_max:.5f}° · "
        f"Latitud {lat_min:.5f}° a {lat_max:.5f}°<br/>"
        f"<b>Puntos de muestreo:</b> {n_puntos} estaciones fijas a lo largo del cauce<br/>"
        f"<b>Resolución espacial Sentinel-2:</b> 10 m (bandas visibles/NIR), 20 m (SWIR/Red-Edge)",
        styles["CuerpoTexto"]
    ))
    if rgb_buf is not None:
        story.append(Spacer(1, 0.2*cm))
        rgb_buf.seek(0)
        story.append(RLImage(rgb_buf, width=14*cm, height=8*cm))
        story.append(Paragraph(f"<i>{t('pdf_fuente_copernicus', lang)}</i>", styles["FootnoteCentro"]))
    story.append(Spacer(1, 0.4*cm))

    # ── 5. ESTADÍSTICAS ZONALES ────────────────────────────────────────────────
    story.append(Paragraph("5. Estadísticas por Parámetro", styles["SeccionTitulo"]))
    story.append(build_stats_table(mapas, styles, lang))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(t("pdf_oob_nota", lang), styles["CuerpoTextoChico"]))
    story.append(PageBreak())

    # ── Numeración dinámica de secciones ──────────────────────────────────────
    _sec = 6

    # ── 6+. SERIE TEMPORAL — DATOS HISTÓRICOS DE CAMPO ───────────────────────
    if df_campo is not None and not df_campo.empty:
        story.append(Paragraph(
            f"{_sec}. Serie Temporal — Datos Históricos de Campo",
            styles["SeccionTitulo"]
        ))
        story.append(Paragraph(
            "Los siguientes gráficos muestran la evolución temporal de los parámetros "
            "fisicoquímicos medidos directamente en campo en las 7 estaciones de muestreo "
            "del Río Pesquería durante el período 2016–2019 (19 campañas). Cada gráfico "
            "incluye la media espacial entre estaciones (línea azul), el máximo registrado "
            "(línea roja discontinua), la tendencia lineal (línea dorada) y el resultado del "
            "test de Mann-Kendall (τ de Kendall, α = 0.05) para detectar tendencias "
            "monótonas estadísticamente significativas.",
            styles["CuerpoTexto"]
        ))
        story.append(Spacer(1, 0.3*cm))
        _params_campo = [p for p in ["P_TOT","N_NH3","N_TOT","N_TOTK"] if p in df_campo.columns]
        for _pc in _params_campo:
            if _pc not in PARAMS_DICT:
                continue
            _cfg_c = PARAMS_DICT[_pc]
            _lbl_c = get_param_label(_pc, lang)
            _df_p = df_campo[["target_date", _pc]].dropna().copy()
            _df_p["target_date"] = pd.to_datetime(_df_p["target_date"])
            _df_grp = (
                _df_p.groupby("target_date")[_pc]
                .agg(["mean", "max"])
                .reset_index()
                .sort_values("target_date")
            )
            if len(_df_grp) < 2:
                continue
            _fv = [d.strftime("%d/%m/%y") for d in _df_grp["target_date"]]
            _mv = _df_grp["mean"].tolist()
            _xv = _df_grp["max"].tolist()
            _bf = _figura_serie_param(_fv, _mv, _xv, _lbl_c, _cfg_c["unidad"])
            story.append(KeepTogether([
                RLImage(_bf, width=15.5*cm, height=5.8*cm),
                Spacer(1, 0.3*cm),
            ]))
        story.append(PageBreak())
        _sec += 1

    # ── 7+. SERIE TEMPORAL — MODELO RF (multifecha) ───────────────────────────
    if resultados_por_fecha and len(resultados_por_fecha) >= 2:
        story.append(Paragraph(
            f"{_sec}. Serie Temporal — Predicción del Modelo RF",
            styles["SeccionTitulo"]
        ))
        story.append(Paragraph(
            "La siguiente sección presenta la evolución temporal de los parámetros de calidad "
            "de agua estimados por el modelo Random Forest a lo largo de las fechas de muestreo "
            "disponibles. Se incluye la media espacial entre los puntos, el máximo registrado "
            "y la tendencia lineal con el resultado del test de Mann-Kendall (α = 0.05).",
            styles["CuerpoTexto"]
        ))
        story.append(Spacer(1, 0.3*cm))
        fechas_dt_ord = sorted(resultados_por_fecha.keys())
        params_con_datos = [p for p in mapas.keys()
                            if any(p in resultados_por_fecha[f] for f in fechas_dt_ord)]
        for param in params_con_datos:
            cfg = mapas[param]
            label_t = get_param_label(param, lang) if param in ("P_TOT","N_NH3","N_TOT","N_TOTK") else cfg["label"]
            medias, maximos, fechas_v = [], [], []
            for f in fechas_dt_ord:
                if param in resultados_por_fecha[f]:
                    medias.append(resultados_por_fecha[f][param]["mean"])
                    maximos.append(resultados_por_fecha[f][param].get("max"))
                    fechas_v.append(pd.to_datetime(f).strftime("%d/%m/%y"))
            if len(fechas_v) < 2:
                continue
            buf_fig = _figura_serie_param(fechas_v, medias, maximos, label_t, cfg["unidad"])
            story.append(KeepTogether([
                RLImage(buf_fig, width=15.5*cm, height=5.8*cm),
                Spacer(1, 0.3*cm),
            ]))
        story.append(PageBreak())
        _sec += 1

    sec_mapas = str(_sec); _sec += 1
    sec_desc  = str(_sec); _sec += 1
    sec_concl = str(_sec)

    # ── DESCRIPCIÓN DE PARÁMETROS ─────────────────────────────────────────────
    story.append(Paragraph(f"{sec_desc}. Descripción de Parámetros", styles["SeccionTitulo"]))
    for col, info in mapas.items():
        label_t = get_param_label(col, lang) if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["label"]
        desc_t  = get_param_desc(col, lang)  if col in ("P_TOT","N_NH3","N_TOT","N_TOTK") else info["desc"]
        story.append(Paragraph(f"{info['icon']} {label_t} ({info['unidad']})", styles["SubseccionTitulo"]))
        story.append(Paragraph(desc_t, styles["CuerpoTexto"]))
        story.append(Spacer(1, 0.15*cm))
    story.append(PageBreak())

    # ── MAPAS INDIVIDUALES ────────────────────────────────────────────────────
    story.append(Paragraph(f"{sec_mapas}. Mapas Espaciales por Parámetro", styles["SeccionTitulo"]))
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
    story.append(Paragraph(f"{sec_concl}. Conclusiones", styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_conclusiones_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        f"<b>Cómo citar:</b> Rodríguez González, K.D. ({date.today().year}). "
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


# =============================================================================
# FUNCIÓN: PDF de serie temporal de calidad de agua
# =============================================================================
def generar_pdf_serie_temporal(resultados_por_fecha, params_sel, bbox, n_puntos, PARAMS_DICT,
                               logo_geo_path=None, lang="es"):
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
        f"<b>Período:</b> {n_fechas} fechas de muestreo disponibles<br/>"
        f"<b>Parámetros:</b> {len(params_sel)} variables fisicoquímicas y microbiológicas<br/>"
        f"<b>Modelo:</b> Random Forest v3 · Sentinel-2 SR<br/>"
        f"<b>Generado:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(t("pdf_nota_auto", lang), styles["FootnoteCentro"]))
    story.append(Spacer(1, 0.25*cm))
    story.append(HRFlowable(width="40%", thickness=0.5, color=colors.HexColor("#CBD5E1"), hAlign="CENTER"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Designed by Kevin Rodríguez González", styles["Credito"]))
    story.append(Paragraph("Departamento de Geomática · UANL · FIC", styles["Credito"]))
    story.append(PageBreak())

    # ── 1. INTRODUCCIÓN ────────────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Este reporte documenta la evolución temporal de los parámetros de calidad del agua "
        "en el Río Pesquería, Nuevo León, México, a partir del análisis multitemporal de "
        "imágenes Sentinel-2 SR procesadas en Google Earth Engine (GEE). La estimación de "
        "cada variable fisicoquímica se realiza mediante un modelo Random Forest entrenado con "
        "datos de campo colectados en 7 estaciones de muestreo durante el período 2016–2019. "
        "El análisis de tendencias incluye el test no paramétrico de Mann-Kendall (τ de Kendall) "
        "para detectar tendencias monótonas estadísticamente significativas (α = 0.05), "
        "complementado con la pendiente de Sen para estimar la magnitud del cambio.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 2. METODOLOGÍA ────────────────────────────────────────────────────────
    story.append(Paragraph("2. Metodología", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "El flujo de trabajo comprende: (1) búsqueda y composición de mosaicos Sentinel-2 SR "
        "sin nubes para cada fecha de muestreo mediante GEE; (2) extracción de reflectancias "
        "en los puntos de muestreo; (3) aplicación del modelo Random Forest para estimar los "
        "parámetros fisicoquímicos; (4) cálculo de estadísticas zonales (media, máximo, mínimo); "
        "y (5) análisis de tendencias mediante Mann-Kendall y regresión lineal. Los resultados "
        "se presentan como gráficos de evolución temporal con bandas de incertidumbre.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 3. SERIES TEMPORALES ──────────────────────────────────────────────────
    story.append(Paragraph("3. Evolución Temporal por Parámetro", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Cada gráfico muestra la media espacial (línea azul), el máximo entre estaciones "
        "(línea roja discontinua) y la tendencia lineal (línea dorada). El resultado del test "
        "de Mann-Kendall se indica en el recuadro superior izquierdo de cada gráfico.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    fechas_dt = sorted(resultados_por_fecha.keys())
    for param in params_sel:
        if param not in PARAMS_DICT:
            continue
        cfg = PARAMS_DICT[param]
        label_t = get_param_label(param, lang) if param in ("P_TOT","N_NH3","N_TOT","N_TOTK") else cfg["label"]
        medias, maximos, fechas_validas = [], [], []
        for f in fechas_dt:
            if param in resultados_por_fecha[f]:
                medias.append(resultados_por_fecha[f][param]["mean"])
                maximos.append(resultados_por_fecha[f][param].get("max"))
                fechas_validas.append(pd.to_datetime(f).strftime("%d/%m/%y"))
        if len(fechas_validas) < 2:
            continue
        buf_fig = _figura_serie_param(fechas_validas, medias, maximos, label_t, cfg["unidad"])
        story.append(KeepTogether([
            RLImage(buf_fig, width=15.5*cm, height=5.8*cm),
            Spacer(1, 0.3*cm),
        ]))

    story.append(PageBreak())

    # ── 4. TABLA RESUMEN ──────────────────────────────────────────────────────
    story.append(Paragraph("4. Tabla Resumen por Fecha", styles["SeccionTitulo"]))
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

    # ── 5. INTERPRETACIÓN TEMPORAL ────────────────────────────────────────────
    story.append(Paragraph("5. Interpretación y Tendencias", styles["SeccionTitulo"]))
    interp_parts = []
    for param in params_sel:
        if param not in PARAMS_DICT:
            continue
        cfg = PARAMS_DICT[param]
        label_t = get_param_label(param, lang) if param in ("P_TOT","N_NH3","N_TOT","N_TOTK") else cfg["label"]
        vals = [resultados_por_fecha[f][param]["mean"]
                for f in fechas_dt if param in resultados_por_fecha[f]]
        if len(vals) < 2:
            continue
        tau, pval = sp_stats.kendalltau(range(len(vals)), vals)
        tendencia = "incremento" if tau > 0 else "disminución"
        sig = "estadísticamente significativa (p<0.05)" if pval < 0.05 else "no significativa estadísticamente"
        cambio_pct = abs((vals[-1] - vals[0]) / (vals[0] + 1e-9)) * 100
        interp_parts.append(
            f"<b>{label_t}</b>: tendencia de {tendencia} {sig} "
            f"(τ={tau:.2f}, p={pval:.3f}), variación de {vals[0]:.2f} a {vals[-1]:.2f} "
            f"{cfg['unidad']} (~{cambio_pct:.0f}% de cambio)."
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
# Interpretadores de índices espectrales
# =============================================================================
def _interpretar_ndvi(v, lang="es"):
    if v is None: return t("pdf_idx_sin_datos", lang)
    if v < 0.0:  return t("pdf_ndvi_agua_suelo", lang)
    if v < 0.2:  return t("pdf_ndvi_muy_baja", lang)
    if v < 0.4:  return t("pdf_ndvi_baja", lang)
    if v < 0.6:  return t("pdf_ndvi_moderada", lang)
    return t("pdf_ndvi_alta", lang)

def _interpretar_ndwi(v, lang="es"):
    if v is None: return t("pdf_idx_sin_datos", lang)
    if v > 0.3:  return t("pdf_ndwi_agua_clara", lang)
    if v > 0.0:  return t("pdf_ndwi_agua_posible", lang)
    if v > -0.3: return t("pdf_ndwi_suelo_mixto", lang)
    return t("pdf_ndwi_vegetacion_suelo", lang)

def _interpretar_mndwi(v, lang="es"):
    if v is None: return t("pdf_idx_sin_datos", lang)
    if v > 0.3:  return t("pdf_mndwi_agua_clara", lang)
    if v > 0.0:  return t("pdf_mndwi_agua_turbia", lang)
    if v > -0.3: return t("pdf_mndwi_suelo_humedo", lang)
    return t("pdf_mndwi_suelo_seco", lang)

def _interpretar_ndti(v, lang="es"):
    if v is None: return t("pdf_idx_sin_datos", lang)
    if v < -0.1: return t("pdf_ndti_muy_baja", lang)
    if v < 0.05: return t("pdf_ndti_baja", lang)
    if v < 0.15: return t("pdf_ndti_moderada", lang)
    return t("pdf_ndti_alta", lang)

def _interpretar_ndci(v, lang="es"):
    if v is None: return "Sin datos"
    if v > 0.2:  return "Alta concentración de clorofila-a — posible floración algal"
    if v > 0.0:  return "Concentración moderada de clorofila-a"
    return "Baja clorofila-a — aguas con escasa productividad fitoplantónica"

def _interpretar_sabi(v, lang="es"):
    if v is None: return "Sin datos"
    if v > 0.1:  return "Alta biomasa algal superficial detectada"
    if v > -0.1: return "Biomasa algal moderada"
    return "Baja biomasa algal — aguas con buena transparencia"

def _interpretar_cdom(v, lang="es"):
    if v is None: return "Sin datos"
    if v > 1.5:  return "Alta concentración de CDOM — probable aporte de materia orgánica disuelta"
    if v > 1.0:  return "CDOM moderado"
    return "CDOM bajo — aguas con alta transparencia óptica"

def _interpretar_awei(v, lang="es"):
    if v is None: return "Sin datos"
    if v > 0.1:  return "Superficie acuática claramente diferenciada del suelo"
    if v > -0.1: return "Zona de transición agua-suelo o agua somera"
    return "Superficie terrestre o ausencia de agua libre"

def _interpretar_evi(v, lang="es"):
    if v is None: return "Sin datos"
    if v > 0.5:  return "Vegetación densa — alta actividad fotosintética ribereña"
    if v > 0.2:  return "Vegetación moderada en la zona de influencia del cauce"
    if v > 0.0:  return "Vegetación escasa o suelo parcialmente cubierto"
    return "Sin vegetación — agua, suelo desnudo o área urbana"

_INTERPRETADORES = {
    "NDVI": _interpretar_ndvi, "NDWI": _interpretar_ndwi,
    "MNDWI": _interpretar_mndwi, "NDTI": _interpretar_ndti,
    "NDCI": _interpretar_ndci, "SABI": _interpretar_sabi,
    "CDOM": _interpretar_cdom, "AWEInsh": _interpretar_awei,
    "EVI": _interpretar_evi,
}

_COLORES_IDX = {
    "NDVI": "#22C55E", "NDWI": "#3B82F6", "MNDWI": "#06B6D4",
    "NDTI": "#F59E0B", "NDCI": "#8B5CF6", "SABI": "#10B981",
    "CDOM": "#F97316", "AWEInsh": "#0EA5E9", "EVI": "#84CC16",
    "LST":  "#EF4444",
}


def build_indices_stats_table(stats, indices_sel, styles, lang="es"):
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
    partes = [t("pdf_idx_interp_intro", lang)]
    for idx_name in indices_sel:
        s = stats.get(idx_name, {})
        mean_v = s.get("mean")
        if mean_v is None:
            continue
        interpretador = _INTERPRETADORES.get(idx_name)
        clase = interpretador(mean_v, lang) if interpretador else ""
        partes.append(
            f"<b>{idx_name}</b>: valor medio zonal = {mean_v:.3f} — {clase}."
        )
    partes.append(t("pdf_idx_interp_cierre", lang))
    return " ".join(partes)


# =============================================================================
# FUNCIÓN PRINCIPAL: PDF de índices espectrales con series temporales GEE
# =============================================================================
def generar_pdf_reporte_espectral(info, stats, thumbnails, indices_sel, bbox,
                                  fecha_ini, fecha_fin, logo_geo_path=None,
                                  lang="es", series_gee=None):
    """
    series_gee: dict opcional {indice: [(fecha_str, valor), ...]}
                Si se provee, se incluye una sección completa de series temporales GEE.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title="Spectral Indices Report — Water Quality Mapping"
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
        f"<b>Período de imagen:</b> {fecha_ini.strftime('%d %b %Y')} → {fecha_fin.strftime('%d %b %Y')}<br/>"
        f"<b>Fecha real imagen:</b> {info.get('fecha_real', 'N/D')} &nbsp;·&nbsp; "
        f"<b>Nubosidad:</b> {info.get('nubes_pct', '—')}%<br/>"
        f"<b>Área:</b> {info.get('area_km2', '—')} km² &nbsp;·&nbsp; "
        f"<b>Índices:</b> {', '.join(indices_sel)}<br/>"
        f"<b>Generado:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 0.7*cm))
    if "RGB" in thumbnails:
        thumbnails["RGB"].seek(0)
        story.append(RLImage(thumbnails["RGB"], width=13*cm, height=9*cm))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"<i>{t('pdf_fuente_copernicus', lang)}</i>", styles["FootnoteCentro"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(t("pdf_idx_nota_auto", lang), styles["FootnoteCentro"]))
    story.append(Spacer(1, 0.25*cm))
    story.append(HRFlowable(width="40%", thickness=0.5, color=colors.HexColor("#CBD5E1"), hAlign="CENTER"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Designed by Kevin Rodríguez González", styles["Credito"]))
    story.append(Paragraph("Departamento de Geomática · UANL · FIC", styles["Credito"]))
    story.append(PageBreak())

    # ── 1. INTRODUCCIÓN ────────────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "Los índices espectrales derivados de imágenes Sentinel-2 (ESA Copernicus) "
        "permiten caracterizar propiedades biofísicas y ópticas del agua superficial de forma "
        "espacialmente continua y repetible. Este reporte presenta los resultados del análisis "
        "multivariado de índices espectrales computados en Google Earth Engine (GEE) para el "
        "área de estudio definida por el shapefile cargado en la plataforma Water Quality Mapping. "
        "Los índices cubren aspectos de calidad del agua (NDCI, SABI, CDOM, NDTI), presencia de "
        "agua superficial (NDWI, MNDWI, AWEInsh), vegetación (NDVI, EVI) y temperatura de "
        "superficie (LST). El análisis temporal incluye el test de Mann-Kendall para detectar "
        "tendencias significativas en las series históricas.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 2. METODOLOGÍA ────────────────────────────────────────────────────────
    story.append(Paragraph("2. Metodología", styles["SeccionTitulo"]))
    met_rows = [
        ["Componente", "Detalle"],
        ["Sensor", "Sentinel-2 MSI (ESA Copernicus), 10 m / 20 m de resolución espacial"],
        ["Colección GEE", "COPERNICUS/S2_SR_HARMONIZED (reflectancia de superficie)"],
        ["Composición", "Mosaico ponderado por menor nubosidad (CLOUDY_PIXEL_PERCENTAGE)"],
        ["Clip espacial", "Recorte exacto al polígono del shapefile cargado (no rectangular)"],
        ["Estadísticas", "reduceRegion — media, desv. estándar, mín., máx., percentil 50 y 90"],
        ["Tendencias", "Mann-Kendall (τ de Kendall) + regresión lineal por mínimos cuadrados"],
        ["Plataforma", "Google Earth Engine · Python 3.11 · Streamlit · Geomática UANL"],
    ]
    met_tbl = Table(met_rows, colWidths=[4*cm, 12*cm])
    met_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_TEAL),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(met_tbl)

    # Fórmulas de los índices
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Fórmulas de los Índices Espectrales", styles["SubseccionTitulo"]))
    formulas = [
        ["Índice", "Fórmula", "Referencia"],
        ["NDVI",    "(B8−B4)/(B8+B4)",                          "Rouse et al., 1974"],
        ["NDWI",    "(B3−B8)/(B3+B8)",                          "McFeeters, 1996"],
        ["MNDWI",   "(B3−B11)/(B3+B11)",                        "Xu, 2006"],
        ["NDTI",    "(B11−B3)/(B11+B3)",                        "Lacaux et al., 2007"],
        ["NDCI",    "(B5−B4)/(B5+B4)",                          "Mishra & Mishra, 2012"],
        ["SABI",    "(B8−B4)/(B2+B3)",                          "Alawadi, 2010"],
        ["CDOM",    "B3/B4",                                     "Kirk, 1994"],
        ["AWEInsh", "4(B3−B11) − 0.25B8 − 2.75B12",            "Feyisa et al., 2014"],
        ["EVI",     "2.5(B8−B4)/(B8+6B4−7.5B2+1)",             "Huete et al., 2002"],
        ["LST",     "Landsat 8/9 ST_B10 (TsHARP 10m via S2)",  "Malakar et al., 2018"],
    ]
    ftbl = Table(formulas, colWidths=[2.4*cm, 8*cm, 5.6*cm])
    ftbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 7.8),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PDF_LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(ftbl)
    story.append(PageBreak())

    # ── 3. ÁREA DE ESTUDIO ────────────────────────────────────────────────────
    story.append(Paragraph("3. Área de Estudio", styles["SeccionTitulo"]))
    story.append(Paragraph(
        f"<b>Coordenadas:</b> Longitud {lon_min:.5f}° a {lon_max:.5f}° · "
        f"Latitud {lat_min:.5f}° a {lat_max:.5f}°<br/>"
        f"<b>Área estimada:</b> {info.get('area_km2', '—')} km²<br/>"
        f"<b>Resolución espacial:</b> 10 m (bandas visibles/NIR) — 20 m (SWIR/Red-Edge)",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 4. RESUMEN INTERPRETATIVO ─────────────────────────────────────────────
    story.append(Paragraph("4. Resumen Interpretativo", styles["SeccionTitulo"]))
    story.append(Paragraph(
        generar_interpretacion_espectral(stats, indices_sel, lang),
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 5. ESTADÍSTICAS ZONALES ───────────────────────────────────────────────
    story.append(Paragraph("5. Estadísticas Zonales por Índice", styles["SeccionTitulo"]))
    story.append(build_indices_stats_table(stats, indices_sel, styles, lang))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(t("pdf_idx_stats_nota", lang), styles["CuerpoTextoChico"]))
    story.append(PageBreak())

    # ── 6. MAPAS POR ÍNDICE ───────────────────────────────────────────────────
    story.append(Paragraph("6. Mapas Espectrales por Índice", styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_idx_sec5_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.3*cm))
    for idx_name in indices_sel:
        if idx_name not in thumbnails:
            continue
        s = stats.get(idx_name, {})
        mean_v = s.get("mean")
        interpretador = _INTERPRETADORES.get(idx_name)
        clase = interpretador(mean_v, lang) if interpretador and mean_v is not None else "—"
        thumbnails[idx_name].seek(0)
        story.append(KeepTogether([
            Paragraph(f"{idx_name}", styles["SubseccionTitulo"]),
            RLImage(thumbnails[idx_name], width=11*cm, height=7.7*cm),
            Spacer(1, 0.15*cm),
            Paragraph(
                f"Media zonal: <b>{mean_v:.3f}</b> (σ={s.get('std', 0):.3f}) — {clase}",
                styles["CuerpoTextoChico"]
            ),
            Spacer(1, 0.45*cm),
        ]))
    story.append(PageBreak())

    # ── 7. SERIES TEMPORALES GEE ──────────────────────────────────────────────
    if series_gee and any(len(v) >= 2 for v in series_gee.values()):
        story.append(Paragraph("7. Series Temporales (Google Earth Engine)", styles["SeccionTitulo"]))
        story.append(Paragraph(
            "Las series temporales se extrajeron mediante consultas mensuales a Google Earth Engine, "
            "calculando la media zonal de cada índice sobre el área de estudio. Se presentan la "
            "evolución temporal, la línea de tendencia lineal y el resultado del test de "
            "Mann-Kendall para evaluar la significancia estadística de la tendencia (α = 0.05).",
            styles["CuerpoTexto"]
        ))
        story.append(Spacer(1, 0.3*cm))

        # Tabla resumen Mann-Kendall
        story.append(Paragraph("Resumen de Tendencias (Mann-Kendall)", styles["SubseccionTitulo"]))
        story.append(_tabla_resumen_series(series_gee, indices_sel, styles))
        story.append(Spacer(1, 0.5*cm))

        # Gráficos individuales por índice
        for idx_name in indices_sel:
            serie = series_gee.get(idx_name, [])
            if len(serie) < 2:
                continue
            color = _COLORES_IDX.get(idx_name, "#22D3EE")
            fig_buf = _figura_serie_gee(serie, idx_name, color)
            if fig_buf:
                story.append(KeepTogether([
                    RLImage(fig_buf, width=15.5*cm, height=5.8*cm),
                    Spacer(1, 0.35*cm),
                ]))
        story.append(PageBreak())
        sec_aplic = "8"
    else:
        sec_aplic = "7"

    # ── APLICACIONES Y RECOMENDACIONES ────────────────────────────────────────
    story.append(Paragraph(f"{sec_aplic}. Aplicaciones y Recomendaciones", styles["SeccionTitulo"]))
    story.append(Paragraph(t("pdf_idx_sec6_texto", lang), styles["CuerpoTexto"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        f"<b>Cómo citar:</b> Rodríguez González, K.D. ({date.today().year}). "
        f"Water Quality &amp; Spectral Indices Mapping Tool. "
        f"Universidad Autónoma de Nuevo León, Facultad de Ingeniería Civil, "
        f"Departamento de Geomática. https://waterqualitygeomaticauanl.streamlit.app/",
        styles["CuerpoTextoChico"]
    ))

    from functools import partial
    header_fn3 = partial(_draw_header_footer, logo_geo_path=logo_geo_path, lang=lang,
                         titulo_corto="Spectral Indices Report — Water Quality Mapping")
    doc.build(story, onFirstPage=header_fn3, onLaterPages=header_fn3)
    buf.seek(0)
    return buf


# =============================================================================
# FUNCIÓN: PDF de análisis SST / ENSO
# =============================================================================
def generar_pdf_enso(anio, mes, serie_cache=None, logo_geo_path=None, lang="es"):
    """
    Genera un reporte PDF del análisis SST / Fenómeno ENSO.

    Parámetros
    ----------
    anio        : int  — Año del mapa SST analizado.
    mes         : int  — Mes (1-12) del mapa SST analizado.
    serie_cache : list[(str, float)] | None
        Serie histórica Niño 3.4 calculada por GEE;
        cada elemento es (fecha_str, anomalía_°C).
    logo_geo_path : str | None — Ruta al logo de Geomática.
    """
    _MESES = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
              7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
    mes_nombre = _MESES.get(mes, str(mes))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2.2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
        title=f"SST ENSO Report — {mes_nombre} {anio}"
    )
    styles = get_pdf_styles()
    story  = []

    # ── Barras de color matplotlib → BytesIO ──────────────────────────────────
    def _cbar(cmap_colors, lbl_min, lbl_max, title_str, w_cm=14.5, h_cm=0.7):
        fig, ax = plt.subplots(figsize=(w_cm/2.54, h_cm/2.54))
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        from matplotlib.colors import LinearSegmentedColormap as _LSCM
        cmap = _LSCM.from_list('_cb', cmap_colors)
        ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 1, 0, 1])
        ax.set_xticks([0, 1])
        ax.set_xticklabels([lbl_min, lbl_max], fontsize=7.5, color='#374151')
        ax.set_yticks([])
        ax.set_title(title_str, fontsize=7.5, color='#374151', pad=2.5)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        for sp in ax.spines.values():
            sp.set_edgecolor('#D1D5DB'); sp.set_linewidth(0.5)
        _b = io.BytesIO()
        fig.savefig(_b, format='png', dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close(fig)
        _b.seek(0)
        return _b

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph("Análisis SST / Fenómeno ENSO", styles["TituloPortada"]))
    story.append(Paragraph(
        "Temperatura Superficial del Mar · Anomalía · Región Niño 3.4",
        styles["SubtituloPortada"]
    ))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="60%", thickness=1.2, color=PDF_TEAL, hAlign="CENTER"))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        f"<b>Período analizado:</b> {mes_nombre} {anio}<br/>"
        f"<b>Dataset SST:</b> NOAA CDR OISST v2.1 · resolución 0.25°<br/>"
        f"<b>Dataset Clorofila-a:</b> NASA MODIS-Aqua L3SMI (2002–2024) / VIIRS-Snpp<br/>"
        f"<b>Procesamiento:</b> Google Earth Engine (GEE) Python API<br/>"
        f"<b>Generado:</b> {date.today().strftime('%d/%m/%Y')}",
        styles["MetaPortada"]
    ))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(
        "Reporte generado automáticamente por la plataforma Water Quality Mapping.",
        styles["FootnoteCentro"]
    ))
    story.append(Spacer(1, 0.25*cm))
    story.append(HRFlowable(width="40%", thickness=0.5,
                             color=colors.HexColor("#CBD5E1"), hAlign="CENTER"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Kevin Rodríguez González", styles["Credito"]))
    story.append(Paragraph("Departamento de Geomática · FIME · UANL", styles["Credito"]))
    story.append(PageBreak())

    # ── 1. INTRODUCCIÓN ────────────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", styles["SeccionTitulo"]))
    story.append(Paragraph(
        "El Fenómeno El Niño–Oscilación del Sur (ENSO) es el principal modo de variabilidad "
        "climática interanual del planeta. Se manifiesta como variaciones anómalas de la "
        "Temperatura Superficial del Mar (SST) en el Océano Pacífico Tropical, "
        "particularmente en la región Niño 3.4 (5°N–5°S · 170°W–120°W). "
        "Las anomalías positivas ≥+0.5°C (El Niño) y negativas ≤−0.5°C (La Niña) "
        "alteran los patrones de precipitación, temperatura y productividad biológica oceánica "
        "a escala global. En México el ENSO afecta directamente la disponibilidad hídrica, "
        "la frecuencia de eventos extremos y la calidad del agua en cuerpos continentales "
        "como el Río Pesquería, Nuevo León.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # ── 2. SST ─────────────────────────────────────────────────────────────────
    story.append(Paragraph(
        "2. Temperatura Superficial del Mar (SST)", styles["SeccionTitulo"]))
    story.append(Paragraph(
        f"El mapa de SST para <b>{mes_nombre} {anio}</b> proviene de la colección "
        f"NOAA OISST v2.1 (Optimum Interpolation Sea Surface Temperature), derivada de datos "
        f"AVHRR con resolución espacial de 0.25° (~28 km). "
        f"La escala de color cubre el rango típico 10°C–32°C.",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.2*cm))
    sst_cbar = _cbar(
        ['#313695','#4575b4','#74add1','#abd9e9','#e0f3f8',
         '#ffffbf','#fee090','#fdae61','#f46d43','#d73027','#a50026'],
        '10°C', '32°C',
        'SST (°C) — Escala RdYlBu · NOAA OISST v2.1'
    )
    story.append(RLImage(sst_cbar, width=14*cm, height=1.2*cm))
    story.append(Spacer(1, 0.4*cm))

    # ── 3. ANOMALÍA SST ────────────────────────────────────────────────────────
    story.append(Paragraph(
        "3. Anomalía SST — Región Niño 3.4", styles["SeccionTitulo"]))
    story.append(Paragraph(
        f"La anomalía es la diferencia entre la SST de <b>{mes_nombre} {anio}</b> "
        f"y la climatología mensual 1982–2025. Anomalía positiva (cálida) en Niño 3.4 → "
        f"El Niño; negativa (fría) → La Niña. Umbral operacional NOAA/CPC: ±0.5°C durante "
        f"cinco meses consecutivos. En El Niño la clorofila-a oceánica disminuye (menor "
        f"surgencia); en La Niña aumenta (mayor mezcla de aguas frías ricas en nutrientes).",
        styles["CuerpoTexto"]
    ))
    story.append(Spacer(1, 0.2*cm))
    anom_cbar = _cbar(
        ['#313695','#4575b4','#74add1','#abd9e9','#ffffbf',
         '#fdae61','#f46d43','#d73027','#a50026'],
        '−4°C', '+4°C',
        'Anomalía SST (°C) — Divergente azul-rojo · NOAA OISST v2.1'
    )
    story.append(RLImage(anom_cbar, width=14*cm, height=1.2*cm))
    story.append(Spacer(1, 0.3*cm))

    # Tabla de umbrales ENSO
    story.append(Paragraph(
        "Clasificación ENSO — Umbrales operacionales (NOAA/CPC):",
        styles["SubseccionTitulo"]
    ))
    umbral_rows = [
        ["Condición",  "Anomalía SST",        "Color en mapa", "Impacto Clorofila-a oceánica"],
        ["El Niño",    "≥ +0.5°C",            "Rojo",
         "Disminuye — aguas más cálidas, menor surgencia"],
        ["La Niña",    "≤ −0.5°C",            "Azul",
         "Aumenta — mayor surgencia de aguas frías"],
        ["Neutral",    "−0.5°C a +0.5°C",     "Blanco/amarillo",
         "Normal estacional"],
    ]
    umb_tbl = Table(umbral_rows, colWidths=[3.0*cm, 3.0*cm, 3.0*cm, 8.0*cm])
    umb_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PDF_BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("TEXTCOLOR",  (0,1), (0,1), colors.HexColor("#991B1B")),
        ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#FEF2F2")),
        ("TEXTCOLOR",  (0,2), (0,2), colors.HexColor("#1E40AF")),
        ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#F9FAFB")),
        ("FONTSIZE",   (0,0), (-1,-1), 8.5),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#D0D8E0")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(umb_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── 4. ESTADÍSTICAS HISTÓRICAS (si serie disponible) ──────────────────────
    if serie_cache and len(serie_cache) > 0:
        story.append(PageBreak())
        story.append(Paragraph(
            "4. Estadísticas Históricas ENSO — 1982–2025",
            styles["SeccionTitulo"]
        ))
        anoms = [a for _, a in serie_cache]
        total = len(anoms)
        nino_c = sum(1 for a in anoms if a >= 0.5)
        nina_c = sum(1 for a in anoms if a <= -0.5)
        neut_c = total - nino_c - nina_c
        max_nino = max((a for a in anoms if a >= 0.5), default=0.0)
        min_nina = min((a for a in anoms if a <= -0.5), default=0.0)
        f_max = next((f for f, a in serie_cache if abs(a - max_nino) < 0.001), '—')
        f_min = next((f for f, a in serie_cache if abs(a - min_nina) < 0.001), '—')

        story.append(Paragraph(
            f"La serie comprende <b>{total} meses</b> (1982–2025). "
            f"Media anomalía Niño 3.4: <b>{sum(anoms)/total:.3f}°C</b> · "
            f"Desviación estándar: <b>{float(np.std(anoms)):.3f}°C</b>.",
            styles["CuerpoTexto"]
        ))
        story.append(Spacer(1, 0.3*cm))

        stats_rows = [
            ["Condición", "N (meses)", "% período", "Pico anomalía", "Fecha pico"],
            ["El Niño",   str(nino_c),  f"{nino_c/total*100:.1f}%",
             f"+{max_nino:.2f}°C", f_max],
            ["La Niña",   str(nina_c),  f"{nina_c/total*100:.1f}%",
             f"{min_nina:.2f}°C",  f_min],
            ["Neutral",   str(neut_c),  f"{neut_c/total*100:.1f}%", "—", "—"],
            ["Total",     str(total),   "100%", "", "1982–2025"],
        ]
        stats_tbl = Table(stats_rows,
                          colWidths=[3.5*cm, 2.4*cm, 2.4*cm, 3.5*cm, 5.2*cm])
        stats_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), PDF_TEAL),
            ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 8.5),
            ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
            ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#FEF2F2")),
            ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#EFF6FF")),
            ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#F3F4F6")),
            ("ALIGN",      (1,0), (-1,-1), "CENTER"),
            ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
            ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#D0D8E0")),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))
        story.append(stats_tbl)
        story.append(Spacer(1, 0.4*cm))

        # Gráfico serie histórica
        story.append(Paragraph(
            "Serie Temporal Anomalía SST Niño 3.4 (1982–2025):",
            styles["SubseccionTitulo"]
        ))
        fechas_s = [f for f, _ in serie_cache]
        anoms_s  = [a for _, a in serie_cache]
        fig2, ax2 = plt.subplots(figsize=(15/2.54, 6/2.54))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('#FAFBFC')
        colores_s = ['#EF4444' if a >= 0.5 else '#3B82F6' if a <= -0.5 else '#9CA3AF'
                     for a in anoms_s]
        xnum2 = np.arange(len(anoms_s))
        ax2.axhspan(0.5, max(max(anoms_s)*1.1, 1.0),
                    color='#EF4444', alpha=0.05)
        ax2.axhspan(min(min(anoms_s)*1.1, -1.0), -0.5,
                    color='#3B82F6', alpha=0.05)
        ax2.plot(xnum2, anoms_s, '-', color='#9CA3AF', lw=0.7, alpha=0.4)
        ax2.scatter(xnum2, anoms_s, c=colores_s, s=6, zorder=3)
        ma3 = pd.Series(anoms_s).rolling(3, center=True).mean()
        ax2.plot(xnum2, ma3, '-', color='#1A4F7A', lw=2,
                 label='MM 3 meses', zorder=4)
        ax2.axhline(0.5,  color='#EF4444', lw=0.8, ls='--', alpha=0.6,
                    label='El Niño +0.5°C')
        ax2.axhline(-0.5, color='#3B82F6', lw=0.8, ls='--', alpha=0.6,
                    label='La Niña −0.5°C')
        ax2.axhline(0, color='#6B7280', lw=0.5, ls=':', alpha=0.4)
        _aplicar_eje_x(ax2, fechas_s, max_ticks=14)
        ax2.set_ylabel('Anomalía SST (°C)', fontsize=7.5)
        ax2.tick_params(axis='y', labelsize=7)
        ax2.legend(fontsize=6.5, loc='upper right', framealpha=0.7)
        ax2.grid(True, alpha=0.18, ls='--')
        ax2.set_title('Índice Niño 3.4 — NOAA OISST v2.1 · GEE',
                      fontsize=9, fontweight='bold', color='#1A4F7A')
        for sp in ax2.spines.values(): sp.set_edgecolor('#D0D8E0')
        plt.tight_layout()
        buf2 = io.BytesIO()
        fig2.savefig(buf2, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig2)
        buf2.seek(0)
        story.append(RLImage(buf2, width=15.5*cm, height=6.2*cm))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            "<i>Puntos rojos: El Niño (≥+0.5°C) · Azules: La Niña (≤−0.5°C) · "
            "Grises: Neutral · Línea azul: media móvil 3 meses.</i>",
            styles["FootnoteCentro"]
        ))
        sec_fuentes = "5."
    else:
        sec_fuentes = "4."

    # ── FUENTES DE DATOS ──────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        f"{sec_fuentes} Fuentes de Datos y Referencias", styles["SeccionTitulo"]))
    fuentes = [
        "<b>NOAA OISST v2.1:</b> Huang et al. (2021). Improvements of the Daily Optimum "
        "Interpolation SST Version 2.1. <i>Journal of Climate</i>, 34(8), 2923–2939.",
        "<b>NASA MODIS-Aqua L3SMI:</b> Ocean Biology Processing Group. "
        "Chlorophyll-a, 4 km Monthly. NASA GSFC.",
        "<b>Google Earth Engine:</b> Gorelick et al. (2017). "
        "<i>Remote Sensing of Environment</i>, 202, 18–27.",
        "<b>Plataforma:</b> Water Quality Mapping — Dpto. de Geomática · FIME · UANL · "
        "Kevin Rodríguez González.",
    ]
    for src in fuentes:
        story.append(Paragraph(f"• {src}", styles["CuerpoTextoChico"]))
        story.append(Spacer(1, 0.15*cm))

    from functools import partial
    hdr_fn = partial(
        _draw_header_footer,
        titulo_corto=f"SST / ENSO — {mes_nombre} {anio}",
        logo_geo_path=logo_geo_path, lang=lang
    )
    doc.build(story, onFirstPage=hdr_fn, onLaterPages=hdr_fn)
    buf.seek(0)
    return buf
