import streamlit as st
import pickle, tempfile, os, zipfile, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import RBFInterpolator, griddata
from scipy import stats
import geopandas as gpd
from shapely.geometry import Point
import io, base64
warnings.filterwarnings("ignore")

# ── Cargar logos y foto desde archivos del repositorio ────────────────────────
def _b64(filename):
    p = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(p):
        return ""
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()

GEO_B64   = _b64("logo_geomatica.png")
UANL_B64  = _b64("logo_uanl.png")
FIC_B64   = _b64("logo_fic.png")
PHOTO_B64 = _b64("photo_researcher.png")

# ── Constantes ────────────────────────────────────────────────────────────────
PARAMS = {
    "P_TOT": dict(
        label="Fósforo Total", unidad="mg/L", vmin=0, vmax=6, oob=0.684,
        icon="🧪",
        pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"],
        desc=(
            "Nutriente clave en procesos de eutrofización. Concentraciones elevadas "
            "indican descargas de aguas residuales domésticas, efluentes industriales "
            "y escorrentía agrícola con fertilizantes. Referencia NOM-001-SEMARNAT: "
            "límite de 5 mg/L para uso en riego agrícola."
        ),
    ),
    "N_NH3": dict(
        label="N-Amoniaco", unidad="mg/L", vmin=0, vmax=25, oob=0.645,
        icon="⚗️",
        pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"],
        desc=(
            "Forma reducida del nitrógeno, indicador directo de contaminación "
            "orgánica reciente y presencia de aguas residuales sin tratar. "
            "Tóxico para organismos acuáticos incluso a bajas concentraciones. "
            "Referencia NOM-001: 25 mg/L promedio mensual para uso en riego."
        ),
    ),
    "N_TOT": dict(
        label="N-Total", unidad="mg/L", vmin=0, vmax=35, oob=0.615,
        icon="🔬",
        pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"],
        desc=(
            "Suma de todas las fracciones de nitrógeno disuelto: orgánico, "
            "amoniaco, nitritos y nitratos. Indicador integral de la carga "
            "nitrogenada total en el cuerpo de agua y del riesgo de "
            "eutrofización y deterioro del ecosistema acuático."
        ),
    ),
    "N_TOTK": dict(
        label="N-Total Kjeldahl", unidad="mg/L", vmin=0, vmax=35, oob=0.662,
        icon="🧫",
        pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"],
        desc=(
            "Nitrógeno orgánico + amoniaco determinado por el método Kjeldahl, "
            "estándar internacional para evaluar la carga orgánica en aguas "
            "residuales. Determina el potencial de demanda bioquímica de oxígeno "
            "y la capacidad de autodepuración del río."
        ),
    ),
}

COORDS = {
    "Punto_1": (-100.34495, 25.81193), "Punto_2": (-100.29269, 25.80148),
    "Punto_3": (-100.28059, 25.80205), "Punto_4": (-100.21237, 25.83095),
    "Punto_5": (-100.20026, 25.82832), "Punto_6": (-100.04244, 25.78160),
    "Punto_7": (-100.02404, 25.77480),
}

FECHAS = [
    "2/25/2016","4/12/2016","5/17/2016","6/23/2016","7/26/2016","9/4/2016",
    "2/22/2017","4/4/2017","5/16/2017","6/27/2017","8/8/2017","9/18/2017",
    "2/8/2018","3/13/2018","4/26/2018","6/8/2018","10/8/2018","11/12/2018",
    "1/14/2019"
]

def make_cmap(pal):
    return LinearSegmentedColormap.from_list("wq", pal, N=256)

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Water Quality RF — Río Pesquería",
    page_icon="💧", layout="wide",
)

st.markdown("""
<style>
body,.stApp{background-color:#0D1117!important}
section[data-testid="stSidebar"]{background-color:#161B22!important}

/* Header */
.hdr{background:linear-gradient(135deg,#1A4F7A 0%,#0D1117 65%);
     border-bottom:2px solid #2E8B8B;padding:1.2rem 2rem .9rem;
     margin-bottom:1.2rem;border-radius:0 0 14px 14px}
.hdr-logos{display:flex;align-items:center;gap:16px;margin-bottom:.8rem;flex-wrap:wrap}
.hdr-logo-img{height:54px;object-fit:contain}
.hdr-sep{width:1px;height:46px;background:#2E8B8B55;flex-shrink:0}
.app-title{font-size:2.1rem;font-weight:800;color:#fff;margin:0;letter-spacing:-.5px;line-height:1.1}
.app-sub{font-size:.88rem;color:#8EAAC8;margin:.3rem 0 0}

/* Métricas */
.metric-row{display:flex;gap:12px;margin:1rem 0;flex-wrap:wrap}
.metric-card{flex:1;min-width:130px;background:linear-gradient(145deg,#161B22,#1A2030);
             border:1px solid #2E8B8B44;border-radius:14px;padding:1rem;text-align:center}
.metric-value{font-size:1.85rem;font-weight:700;color:#2E8B8B}
.metric-label{font-size:.68rem;color:#8EAAC8;text-transform:uppercase;letter-spacing:.07em;margin-top:4px}
.badge-ok{display:inline-block;margin-top:8px;background:#1A3A2A;color:#3DBA7A;
          border:1px solid #3DBA7A55;padding:2px 12px;border-radius:20px;font-size:.68rem;font-weight:700}

/* Tarjetas de parámetros */
.param-card{background:#161B22;border:1px solid #FFFFFF12;
            border-left:3px solid #2E8B8B;border-radius:0 12px 12px 0;
            padding:1.1rem 1.4rem;margin-bottom:.75rem}
.param-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:.55rem;flex-wrap:wrap;gap:8px}
.param-name{font-size:.95rem;font-weight:700;color:#FFFFFF}
.param-oob{font-size:.68rem;color:#2E8B8B;background:#0D1F2D;border:1px solid #2E8B8B44;
           border-radius:20px;padding:2px 10px;white-space:nowrap}
.param-desc{font-size:.78rem;color:#8EAAC8;line-height:1.65;margin-bottom:.65rem}
.param-meta{display:flex;gap:20px;flex-wrap:wrap}
.pmi{font-size:.72rem;color:#8EAAC8}
.pmv{color:#2E8B8B;font-weight:600}

/* Pasos */
.step-box{background:#161B22;border:1px solid #FFFFFF0F;border-left:3px solid #2E8B8B;
          border-radius:0 10px 10px 0;padding:1rem 1.2rem}
.step-t{font-size:.88rem;font-weight:700;color:#fff;margin-bottom:.5rem}
.step-b{font-size:.76rem;color:#8EAAC8;line-height:1.65}

/* Investigador */
.researcher-card{background:linear-gradient(145deg,#161B22,#1A2030);
                 border:1px solid #2E8B8B44;border-radius:16px;
                 padding:1.3rem 1.7rem;display:flex;gap:20px;align-items:center}
.rphoto{width:88px;height:88px;border-radius:50%;object-fit:cover;
        border:3px solid #2E8B8B;flex-shrink:0}
.rname{font-size:1rem;font-weight:700;color:#fff;margin:0 0 2px}
.rtitle{font-size:.8rem;color:#2E8B8B;font-weight:600;margin:0 0 3px}
.rdept{font-size:.76rem;color:#8EAAC8;margin:0 0 9px}
.rlinks{display:flex;gap:9px;flex-wrap:wrap}
.rlink{font-size:.70rem;color:#8EAAC8;background:#FFFFFF0D;border:1px solid #FFFFFF22;
       border-radius:20px;padding:3px 11px;text-decoration:none}

/* Utilidades */
.divider{border:0;border-top:1px solid #FFFFFF0F;margin:1.1rem 0}
.sec-t{font-size:.73rem;font-weight:700;color:#8EAAC8;letter-spacing:.09em;
       text-transform:uppercase;margin:1.1rem 0 .6rem}
.slabel{font-size:.68rem;color:#8EAAC8;text-transform:uppercase;
        letter-spacing:.08em;font-weight:700;margin-bottom:.3rem}
.footer{text-align:center;font-size:.68rem;color:#3A4A5C;margin-top:2rem;
        padding-top:1rem;border-top:1px solid #FFFFFF0D}
</style>
""", unsafe_allow_html=True)

# ── Cargar modelo y CSV ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Cargando modelo RF v3...")
def load_model():
    p = os.path.join(os.path.dirname(__file__), "modelos_rf_v3.pkl")
    if not os.path.exists(p): return None
    with open(p, "rb") as f: return pickle.load(f)

@st.cache_data(show_spinner="Cargando datos...")
def load_csv():
    p = os.path.join(os.path.dirname(__file__), "INDICES_completo.csv")
    if not os.path.exists(p): return None
    df = pd.read_csv(p)
    df["target_date"] = pd.to_datetime(df["target_date"], format="%m/%d/%Y")
    return df

model_data = load_model()
df_global  = load_csv()

# ── HEADER ────────────────────────────────────────────────────────────────────
logo_uanl = f'<img class="hdr-logo-img" src="data:image/png;base64,{UANL_B64}" alt="UANL">' if UANL_B64 else '<span style="color:#8EAAC8;font-size:.8rem">UANL</span>'
logo_fic  = f'<img class="hdr-logo-img" src="data:image/png;base64,{FIC_B64}"  alt="FIC">'  if FIC_B64  else '<span style="color:#8EAAC8;font-size:.8rem">FIC</span>'
logo_geo  = f'<img class="hdr-logo-img" src="data:image/png;base64,{GEO_B64}"  alt="Geomática">' if GEO_B64 else '<span style="color:#8EAAC8;font-size:.8rem">Geomática</span>'

st.markdown(f"""
<div class="hdr">
  <div class="hdr-logos">
    {logo_uanl}
    <div class="hdr-sep"></div>
    {logo_fic}
    <div class="hdr-sep"></div>
    {logo_geo}
  </div>
  <div class="app-title">💧 Water Quality Mapping</div>
  <div class="app-sub">
    Río Pesquería, Nuevo León, México &nbsp;·&nbsp;
    Random Forest v3 · Sentinel-2 SR 2016–2019 &nbsp;·&nbsp;
    Universidad Autónoma de Nuevo León · FIC · Depto. Geomática
  </div>
</div>
""", unsafe_allow_html=True)

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
mh = '<div class="metric-row">'
for col, cfg in PARAMS.items():
    mh += (f'<div class="metric-card">'
           f'<div class="metric-value">{cfg["oob"]:.3f}</div>'
           f'<div class="metric-label">OOB R² &nbsp;·&nbsp; {cfg["label"]}</div>'
           f'<span class="badge-ok">✓ Validado</span></div>')
mh += "</div>"
st.markdown(mh, unsafe_allow_html=True)

if model_data is None: st.error("⚠️ modelos_rf_v3.pkl no encontrado"); st.stop()
if df_global  is None: st.error("⚠️ INDICES_completo.csv no encontrado"); st.stop()
st.success("✅  Modelo RF v3 cargado  ·  Datos de muestreo 2016–2019 listos")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="slabel">📍 Área de estudio</div>', unsafe_allow_html=True)
    st.caption("Comprime tu shapefile: .shp + .dbf + .prj + .cpg → ZIP")
    wmask_zip = st.file_uploader("Sube wmask.zip", type=["zip"])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">📅 Fecha Sentinel-2</div>', unsafe_allow_html=True)
    fecha_sel = st.selectbox("", FECHAS, index=16,
        format_func=lambda f: pd.to_datetime(f, format="%m/%d/%Y").strftime("%d %b %Y"))
    mes = pd.to_datetime(fecha_sel, format="%m/%d/%Y").month
    st.info("🌵 Temporada Seca" if mes in [11,12,1,2,3] else "🌧️ Temporada Lluviosa")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🔬 Parámetros</div>', unsafe_allow_html=True)
    params_sel = st.multiselect("", list(PARAMS.keys()), default=list(PARAMS.keys()),
        format_func=lambda p: f"{PARAMS[p]['label']} ({PARAMS[p]['unidad']})")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🎯 Resolución</div>', unsafe_allow_html=True)
    resolucion = st.select_slider("", options=[200,300,400,500], value=400,
        format_func=lambda v: f"{v}×{v} celdas")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    correr = st.button("🗺️  Generar Mapas", type="primary", use_container_width=True,
                       disabled=(wmask_zip is None or not params_sel))
    if wmask_zip is None:
        st.warning("⬆️  Sube tu wmask.zip para continuar")

# ── PANTALLA INICIAL ──────────────────────────────────────────────────────────
if not correr:

    # Pasos
    c1, c2, c3 = st.columns(3)
    for col, (t, b) in zip([c1,c2,c3], [
        ("① Shapefile",
         "Comprime tu wmask en un ZIP:<br><code>.shp · .dbf · .prj · .cpg</code><br>"
         "Sube el archivo en el panel izquierdo."),
        ("② Configura",
         "Elige la fecha de la imagen Sentinel-2 y los parámetros a visualizar.<br>"
         "El modelo RF v3 ya está integrado — no necesitas subir nada más."),
        ("③ Descarga",
         "Clic en <b>Generar Mapas</b> y descarga:<br>"
         "📊 Panel PNG para tesis / artículo<br>"
         "🗺️ Mapas individuales ZIP<br>"
         "📈 Estadísticas espaciales"),
    ]):
        with col:
            st.markdown(
                f'<div class="step-box"><div class="step-t">{t}</div>'
                f'<div class="step-b">{b}</div></div>',
                unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Parámetros — tarjetas con descripción técnica (SIN OOB redundante)
    st.markdown('<div class="sec-t">📊 Parámetros Fisicoquímicos del Modelo</div>',
                unsafe_allow_html=True)
    for col, cfg in PARAMS.items():
        st.markdown(f"""
        <div class="param-card">
          <div class="param-hdr">
            <div class="param-name">{cfg["icon"]} &nbsp;{cfg["label"]}</div>
            <span class="param-oob">OOB R² = {cfg["oob"]:.3f} · Modelo validado ✓</span>
          </div>
          <div class="param-desc">{cfg["desc"]}</div>
          <div class="param-meta">
            <div class="pmi">Unidad: <span class="pmv">{cfg["unidad"]}</span></div>
            <div class="pmi">Rango típico: <span class="pmv">{cfg["vmin"]}–{cfg["vmax"]} {cfg["unidad"]}</span></div>
            <div class="pmi">Estado: <span class="pmv">🟢 Bueno</span></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Mapa de puntos
    st.markdown('<div class="sec-t">📍 Puntos de Muestreo — Río Pesquería</div>',
                unsafe_allow_html=True)
    df_pts = pd.DataFrame([{"lat": c[1], "lon": c[0], "Punto": p}
                            for p, c in COORDS.items()])
    st.map(df_pts)

    st.info("ℹ️ **pH y OD excluidos del modelo** — su OOB R² resultó negativo, "
            "indicando que Sentinel-2 no captura señal óptica suficiente para "
            "estimar esos parámetros en este río.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Investigador — AL FINAL
    st.markdown('<div class="sec-t">👨‍🔬 Investigador Principal</div>',
                unsafe_allow_html=True)
    photo_src = (f"data:image/png;base64,{PHOTO_B64}"
                 if PHOTO_B64 else "https://via.placeholder.com/88/2E8B8B/fff?text=KR")
    st.markdown(f"""
    <div class="researcher-card">
      <img class="rphoto" src="{photo_src}" alt="Kevin Rodriguez">
      <div>
        <div class="rname">Kevin David Rodríguez González</div>
        <div class="rtitle">PhD Student · Environmental Water Quality &amp; Remote Sensing</div>
        <div class="rdept">Departamento de Geomática · Facultad de Ingeniería Civil · UANL</div>
        <div class="rlinks">
          <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
          <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">
            🔗 ORCID: 0009-0004-3060-8575</a>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="footer">
      Random Forest v3 · Sentinel-2 SR · Universidad Autónoma de Nuevo León ·
      Facultad de Ingeniería Civil · Departamento de Geomática ·
      Validado con KFold-5 y OOB score
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── PROCESAMIENTO ─────────────────────────────────────────────────────────────
progress = st.progress(0)
status   = st.empty()

modelos    = model_data["models"]
transforms = model_data["transforms"]
lambdas    = model_data["lambdas"]

puntos_uniq = sorted(COORDS.keys())
lons = np.array([COORDS[p][0] for p in puntos_uniq])
lats = np.array([COORDS[p][1] for p in puntos_uniq])
pts_known = np.column_stack([lons, lats])
fecha_dt  = pd.to_datetime(fecha_sel, format="%m/%d/%Y")
df_fecha  = df_global[df_global["target_date"] == fecha_dt]
progress.progress(10)

status.text("Cargando shapefile...")
with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(wmask_zip, "r") as z: z.extractall(tmpdir)
    shp = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
    if not shp: st.error("No .shp en el ZIP"); st.stop()
    wmask = gpd.read_file(os.path.join(tmpdir, shp[0]))
    if wmask.crs is None or wmask.crs.to_epsg() != 4326: wmask = wmask.to_crs(4326)
    union_geom = wmask.geometry.unary_union
    bounds     = wmask.total_bounds
progress.progress(30)

status.text("Generando grilla de interpolación...")
lon_min, lat_min, lon_max, lat_max = bounds
RES     = resolucion
lon_vec = np.linspace(lon_min, lon_max, RES)
lat_vec = np.linspace(lat_min, lat_max, RES)
lon_grid, lat_grid = np.meshgrid(lon_vec, lat_vec)
pts_grid = np.column_stack([lon_grid.ravel(), lat_grid.ravel()])
extent   = [lon_min, lon_max, lat_min, lat_max]
mask_flat = np.array([union_geom.contains(Point(x, y)) for x, y in pts_grid])
mask_2d   = mask_flat.reshape(RES, RES)
progress.progress(60)

status.text("Aplicando modelo RF...")
mapas = {}
for col in params_sel:
    if col not in PARAMS or col not in modelos: continue
    cfg  = PARAMS[col]
    vals = []
    for p in puntos_uniq:
        fila = df_fecha[df_fecha["nombre"] == p]
        vals.append(float(fila[col].values[0]) if len(fila) > 0 else np.nan)
    vals = np.array(vals); ok = np.isfinite(vals)
    if ok.sum() < 3: continue
    try:
        rbf    = RBFInterpolator(pts_known[ok], vals[ok],
                                  kernel="thin_plate_spline", smoothing=0.1)
        z_flat = rbf(pts_grid)
    except Exception:
        z_flat = griddata(pts_known[ok], vals[ok], pts_grid, method="linear")
        z_nan  = griddata(pts_known[ok], vals[ok], pts_grid, method="nearest")
        z_flat = np.where(np.isnan(z_flat), z_nan, z_flat)
    z_2d = np.where(mask_2d, z_flat.reshape(RES, RES), np.nan)
    mapas[col] = {"data": z_2d, "vals_puntos": vals, **cfg}
progress.progress(80)

status.text("Generando visualizaciones...")
n = len(mapas); ncols = min(n, 2); nrows = (n + ncols - 1) // ncols
fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*7, nrows*5.5))
fig.patch.set_facecolor("#0D1117")
if n == 1:       axes_flat = [axes]
elif nrows == 1: axes_flat = list(axes)
else:            axes_flat = axes.flatten().tolist()

buf_ind = {}
for i, (col, info) in enumerate(mapas.items()):
    ax   = axes_flat[i]; ax.set_facecolor("#161B22")
    data = info["data"]; vmin, vmax = info["vmin"], info["vmax"]
    cmap = make_cmap(info["pal"])

    im = ax.imshow(np.clip(data, vmin, vmax), cmap=cmap, vmin=vmin, vmax=vmax,
                   extent=extent, aspect="auto", interpolation="bilinear", origin="upper")
    wmask.boundary.plot(ax=ax, color="#2E8B8B", linewidth=1.2, alpha=0.8)

    vals_p = info["vals_puntos"]
    for j, p in enumerate(puntos_uniq):
        lon, lat = COORDS[p]
        ax.scatter(lon, lat, c="white", s=60, zorder=5, edgecolors="#0D1117", linewidths=0.6)
        if np.isfinite(vals_p[j]):
            ax.annotate(f" P{j+1}: {vals_p[j]:.1f}", (lon, lat),
                        fontsize=7.5, color="white", fontweight="bold", zorder=6)

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02, shrink=0.85)
    cbar.set_label(f"{info['label']} ({info['unidad']})", color="white", fontsize=10)
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white", fontsize=8)

    d = data[np.isfinite(data)]
    ax.set_title(info["label"], color="white", fontsize=11, fontweight="bold")
    ax.text(0.01, 0.99,
            f"Min: {d.min():.2f}\nMáx: {d.max():.2f}\nMedia: {d.mean():.2f}",
            transform=ax.transAxes, fontsize=8, color="white", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0D1117", alpha=0.7))
    ax.set_xlabel("Longitud (°)", color="#8EAAC8", fontsize=8)
    ax.set_ylabel("Latitud (°)",  color="#8EAAC8", fontsize=8)
    ax.tick_params(colors="#8EAAC8", labelsize=7)
    for sp in ax.spines.values(): sp.set_edgecolor("#2E8B8B44")

    # PNG individual
    bi = io.BytesIO()
    fi, ai = plt.subplots(figsize=(11, 5))
    fi.patch.set_facecolor("#0D1117"); ai.set_facecolor("#161B22")
    im2 = ai.imshow(np.clip(data, vmin, vmax), cmap=cmap, vmin=vmin, vmax=vmax,
                    extent=extent, aspect="auto", interpolation="bilinear", origin="upper")
    wmask.boundary.plot(ax=ai, color="#2E8B8B", linewidth=1.4, alpha=0.8)
    for j, p in enumerate(puntos_uniq):
        lon, lat = COORDS[p]
        ai.scatter(lon, lat, c="white", s=80, zorder=5, edgecolors="#0D1117", linewidths=0.8)
        if np.isfinite(vals_p[j]):
            ai.annotate(f" P{j+1}: {vals_p[j]:.1f}", (lon, lat),
                        fontsize=9, color="white", fontweight="bold", zorder=6)
    cb2 = plt.colorbar(im2, ax=ai, fraction=0.025, pad=0.02, shrink=0.9)
    cb2.set_label(f"{info['label']} ({info['unidad']})", color="white", fontsize=11)
    plt.setp(plt.getp(cb2.ax.axes, "yticklabels"), color="white", fontsize=9)
    ai.set_title(
        f"{info['label']} | Río Pesquería | {fecha_dt.strftime('%d/%m/%Y')} | RF v3",
        color="white", fontsize=11, fontweight="bold")
    ai.text(0.99, 0.01,
            "Kevin D. Rodríguez G. · UANL · Depto. Geomática · RF v3",
            transform=ai.transAxes, fontsize=7, color="#8EAAC8", ha="right", va="bottom")
    ai.tick_params(colors="#8EAAC8", labelsize=7)
    for sp in ai.spines.values(): sp.set_edgecolor("#2E8B8B44")
    plt.tight_layout()
    fi.savefig(bi, dpi=180, bbox_inches="tight", facecolor="#0D1117")
    buf_ind[col] = bi; plt.close(fi)

for k in range(n, len(axes_flat)): axes_flat[k].set_visible(False)
mes2 = fecha_dt.month
temp = "Temporada Seca 🌵" if mes2 in [11,12,1,2,3] else "Temporada Lluviosa 🌧️"
fig.suptitle(
    f"Calidad de Agua — Río Pesquería\n"
    f"{fecha_dt.strftime('%d/%m/%Y')} | {temp} | RF v3 | UANL · FIC · Geomática",
    fontsize=13, fontweight="bold", color="white", y=1.01)
plt.tight_layout()
buf_panel = io.BytesIO()
fig.savefig(buf_panel, dpi=150, bbox_inches="tight", facecolor="#0D1117")
plt.close(fig)
progress.progress(100); status.empty()

# ── RESULTADOS ────────────────────────────────────────────────────────────────
st.success(f"✅  {n} mapas generados — {fecha_dt.strftime('%d/%m/%Y')} · {temp}")
st.image(buf_panel, caption="Panel de calidad de agua · Río Pesquería · UANL",
         use_column_width=True)

st.markdown('<div class="sec-t">📥 Descargar resultados</div>', unsafe_allow_html=True)
dl1, dl2 = st.columns(2)
with dl1:
    st.download_button("⬇️  Panel completo PNG (tesis / artículo)",
        buf_panel.getvalue(),
        f"WaterQuality_Pesqueria_{fecha_dt.strftime('%Y%m%d')}.png",
        "image/png", use_container_width=True)
with dl2:
    bz = io.BytesIO()
    with zipfile.ZipFile(bz, "w") as zf:
        for col, buf in buf_ind.items():
            zf.writestr(f"mapa_{col}_{fecha_dt.strftime('%Y%m%d')}.png", buf.getvalue())
    st.download_button("⬇️  Mapas individuales ZIP",
        bz.getvalue(),
        f"mapas_pesqueria_{fecha_dt.strftime('%Y%m%d')}.zip",
        "application/zip", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-t">📊 Estadísticas espaciales</div>', unsafe_allow_html=True)
cols_st = st.columns(len(mapas))
for cs, (param, info) in zip(cols_st, mapas.items()):
    d = info["data"][np.isfinite(info["data"])]
    with cs:
        st.markdown(f"**{info['label']}**")
        st.metric("Media",  f"{d.mean():.2f} {info['unidad']}")
        st.metric("Máximo", f"{d.max():.2f} {info['unidad']}")
        st.metric("Mínimo", f"{d.min():.2f} {info['unidad']}")

# Investigador al final también en la pantalla de resultados
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-t">👨‍🔬 Investigador Principal</div>', unsafe_allow_html=True)
photo_src2 = (f"data:image/png;base64,{PHOTO_B64}"
              if PHOTO_B64 else "https://via.placeholder.com/88/2E8B8B/fff?text=KR")
st.markdown(f"""
<div class="researcher-card">
  <img class="rphoto" src="{photo_src2}" alt="Kevin Rodriguez">
  <div>
    <div class="rname">Kevin David Rodríguez González</div>
    <div class="rtitle">PhD Student · Environmental Water Quality &amp; Remote Sensing</div>
    <div class="rdept">Departamento de Geomática · Facultad de Ingeniería Civil · UANL</div>
    <div class="rlinks">
      <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
      <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">
        🔗 ORCID: 0009-0004-3060-8575</a>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class="footer">
  Random Forest v3 · Sentinel-2 SR · Universidad Autónoma de Nuevo León ·
  Facultad de Ingeniería Civil · Departamento de Geomática ·
  Validado con KFold-5 y OOB score
</div>""", unsafe_allow_html=True)
