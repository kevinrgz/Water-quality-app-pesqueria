import streamlit as st
import pickle, json, tempfile, os, zipfile, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import RBFInterpolator, griddata
from scipy import stats
import geopandas as gpd
from shapely.geometry import Point
import io
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# FOTO DEL INVESTIGADOR — leer desde archivo en el repo
# ─────────────────────────────────────────────────────────────────────────────
def get_photo_b64():
    p = os.path.join(os.path.dirname(__file__), "photo_researcher.png")
    if os.path.exists(p):
        import base64
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Water Quality RF — Río Pesquería",
    page_icon="💧",
    layout="wide",
)

st.markdown("""
<style>
body, .stApp { background-color: #0D1117 !important; }
section[data-testid="stSidebar"] { background-color: #161B22 !important; }

.header-banner {
    background: linear-gradient(135deg, #1A4F7A 0%, #0D1117 65%);
    border-bottom: 2px solid #2E8B8B;
    padding: 1.5rem 2rem 1rem 2rem;
    margin-bottom: 1.5rem;
    border-radius: 0 0 14px 14px;
}
.app-title {
    font-size: 2.2rem; font-weight: 800;
    color: #FFFFFF; letter-spacing: -0.5px;
    margin: 0; line-height: 1.1;
}
.app-subtitle { font-size: 0.92rem; color: #8EAAC8; margin: 0.3rem 0 0 0; }

.logo-row { display: flex; align-items: center; gap: 12px; margin-bottom: 0.7rem; flex-wrap: wrap; }
.logo-box {
    background: #FFFFFF10; border: 1px solid #2E8B8B55;
    border-radius: 8px; padding: 5px 14px;
    font-size: 0.72rem; color: #8EAAC8;
    font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
}

.metric-row { display: flex; gap: 12px; margin: 1rem 0; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 130px;
    background: linear-gradient(145deg, #161B22, #1A2030);
    border: 1px solid #2E8B8B44; border-radius: 14px; padding: 1rem;
    text-align: center;
}
.metric-value { font-size: 1.9rem; font-weight: 700; color: #2E8B8B; }
.metric-label { font-size: 0.70rem; color: #8EAAC8;
                text-transform: uppercase; letter-spacing: .06em; margin-top: 4px; }
.badge-good {
    display: inline-block; margin-top: 8px;
    background: #1A3A2A; color: #3DBA7A;
    border: 1px solid #3DBA7A55;
    padding: 2px 12px; border-radius: 20px;
    font-size: 0.70rem; font-weight: 700;
}

.researcher-card {
    background: linear-gradient(145deg, #161B22, #1A2030);
    border: 1px solid #2E8B8B55;
    border-radius: 16px; padding: 1.4rem 1.8rem;
    display: flex; gap: 22px; align-items: center;
    margin: 0.5rem 0 1rem 0;
}
.researcher-photo {
    width: 92px; height: 92px; border-radius: 50%;
    object-fit: cover; border: 3px solid #2E8B8B; flex-shrink: 0;
}
.researcher-name { font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin: 0 0 2px 0; }
.researcher-title { font-size: 0.82rem; color: #2E8B8B; font-weight: 600; margin: 0 0 3px 0; }
.researcher-dept  { font-size: 0.78rem; color: #8EAAC8; margin: 0 0 10px 0; }
.researcher-links { display: flex; gap: 10px; flex-wrap: wrap; }
.researcher-link {
    font-size: 0.72rem; color: #8EAAC8;
    background: #FFFFFF0D; border: 1px solid #FFFFFF22;
    border-radius: 20px; padding: 3px 12px; text-decoration: none;
}

.step-box {
    background: #161B22; border: 1px solid #FFFFFF12;
    border-left: 3px solid #2E8B8B;
    border-radius: 0 10px 10px 0; padding: 1rem 1.2rem;
}
.step-title { font-size: 0.9rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.5rem; }
.step-body  { font-size: 0.78rem; color: #8EAAC8; line-height: 1.6; }

.divider { border: 0; border-top: 1px solid #FFFFFF12; margin: 1.2rem 0; }
.section-title {
    font-size: 0.82rem; font-weight: 700; color: #8EAAC8;
    letter-spacing: .08em; text-transform: uppercase; margin: 1.2rem 0 0.6rem 0;
}
.sidebar-label {
    font-size: 0.70rem; color: #8EAAC8;
    text-transform: uppercase; letter-spacing: .08em;
    font-weight: 700; margin-bottom: 0.3rem;
}
.footer {
    text-align: center; font-size: 0.70rem; color: #3A4A5C;
    margin-top: 2rem; padding-top: 1rem;
    border-top: 1px solid #FFFFFF0D;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
PARAMS = {
    "P_TOT" : dict(label="Fósforo Total",   unidad="mg/L", vmin=0,  vmax=6,
                   pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], oob=0.684,
                   desc="Indicador de contaminación por aguas residuales y fertilizantes."),
    "N_NH3" : dict(label="N-Amoniaco",       unidad="mg/L", vmin=0,  vmax=25,
                   pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], oob=0.645,
                   desc="Indicador de descargas de aguas residuales domésticas e industriales."),
    "N_TOT" : dict(label="N-Total",          unidad="mg/L", vmin=0,  vmax=35,
                   pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], oob=0.615,
                   desc="Nitrógeno total disuelto, incluye todas las formas."),
    "N_TOTK": dict(label="N-Total Kjeldahl", unidad="mg/L", vmin=0,  vmax=35,
                   pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], oob=0.662,
                   desc="Nitrógeno orgánico + amoniaco, indicador de carga orgánica."),
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

def inv_transform(y_t, method, lam=None):
    if method == "none": return y_t.copy()
    if method == "log1": return np.expm1(y_t)
    if method == "sqrt": return np.clip(y_t, 0, None)**2
    if method == "yeoj": return stats.yeojohnson(y_t, lmbda=lam)

# ─────────────────────────────────────────────────────────────────────────────
# CARGAR MODELO Y CSV
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Cargando modelo RF v3...")
def load_model():
    p = os.path.join(os.path.dirname(__file__), "modelos_rf_v3.pkl")
    if not os.path.exists(p): return None
    with open(p, "rb") as f: return pickle.load(f)

@st.cache_data(show_spinner="Cargando datos de muestreo...")
def load_csv():
    p = os.path.join(os.path.dirname(__file__), "INDICES_completo.csv")
    if not os.path.exists(p): return None
    df = pd.read_csv(p)
    df["target_date"] = pd.to_datetime(df["target_date"], format="%m/%d/%Y")
    return df

model_data = load_model()
df_global  = load_csv()
photo_b64  = get_photo_b64()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="logo-row">
    <div class="logo-box">🎓 UANL</div>
    <div class="logo-box">🗺️ Depto. Geomática</div>
    <div class="logo-box">🛰️ Sentinel-2 SR</div>
    <div class="logo-box">🤖 Random Forest v3</div>
  </div>
  <div class="app-title">💧 Water Quality Mapping</div>
  <div class="app-subtitle">
    Río Pesquería, Nuevo León, México &nbsp;·&nbsp;
    Modelo entrenado con imágenes Sentinel-2 SR 2016–2019 &nbsp;·&nbsp;
    Universidad Autónoma de Nuevo León
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MÉTRICAS OOB
# ─────────────────────────────────────────────────────────────────────────────
metric_html = '<div class="metric-row">'
for col, cfg in PARAMS.items():
    metric_html += f"""
    <div class="metric-card">
      <div class="metric-value">{cfg["oob"]:.3f}</div>
      <div class="metric-label">OOB R² &nbsp;·&nbsp; {cfg["label"]}</div>
      <span class="badge-good">✓ Validado</span>
    </div>"""
metric_html += "</div>"
st.markdown(metric_html, unsafe_allow_html=True)

# Estado
if model_data is None:
    st.error("⚠️ Modelo `modelos_rf_v3.pkl` no encontrado."); st.stop()
if df_global is None:
    st.error("⚠️ Archivo `INDICES_completo.csv` no encontrado."); st.stop()

st.success("✅  Modelo RF v3 cargado  ·  Datos de muestreo 2016–2019 listos")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">📍 Área de estudio</div>', unsafe_allow_html=True)
    st.caption("Comprime tu shapefile: .shp + .dbf + .prj + .cpg → ZIP")
    wmask_zip = st.file_uploader("Sube wmask.zip", type=["zip"])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">📅 Fecha Sentinel-2</div>', unsafe_allow_html=True)
    fecha_sel = st.selectbox("", FECHAS, index=16,
        format_func=lambda f: pd.to_datetime(f, format="%m/%d/%Y").strftime("%d %b %Y"))
    mes = pd.to_datetime(fecha_sel, format="%m/%d/%Y").month
    st.info("🌵 Temporada Seca" if mes in [11, 12, 1, 2, 3] else "🌧️ Temporada Lluviosa")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">🔬 Parámetros</div>', unsafe_allow_html=True)
    params_sel = st.multiselect("", list(PARAMS.keys()), default=list(PARAMS.keys()),
        format_func=lambda p: f"{PARAMS[p]['label']} ({PARAMS[p]['unidad']})")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">🎯 Resolución de grilla</div>', unsafe_allow_html=True)
    resolucion = st.select_slider("", options=[200, 300, 400, 500], value=400,
        format_func=lambda v: f"{v}×{v} celdas")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    correr = st.button("🗺️  Generar Mapas", type="primary",
                       use_container_width=True,
                       disabled=(wmask_zip is None or not params_sel))
    if wmask_zip is None:
        st.warning("⬆️  Sube tu wmask.zip para continuar")

# ─────────────────────────────────────────────────────────────────────────────
# PANTALLA INICIAL
# ─────────────────────────────────────────────────────────────────────────────
if not correr:

    # Pasos
    c1, c2, c3 = st.columns(3)
    steps = [
        ("① Shapefile",
         "Comprime los 4 archivos de tu wmask en un ZIP y súbelos en el panel izquierdo.<br>"
         "<code>wmask.shp · .dbf · .prj · .cpg</code>"),
        ("② Configura",
         "Elige la fecha de la imagen Sentinel-2 y los parámetros a visualizar.<br>"
         "El modelo RF v3 está integrado — no necesitas subir nada más."),
        ("③ Descarga",
         "Clic en <b>Generar Mapas</b> y descarga:<br>"
         "📊 Panel PNG (tesis/artículo)<br>🗺️ Mapas individuales ZIP<br>📈 Estadísticas espaciales"),
    ]
    for col, (title, body) in zip([c1, c2, c3], steps):
        with col:
            st.markdown(
                f'<div class="step-box">'
                f'<div class="step-title">{title}</div>'
                f'<div class="step-body">{body}</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Tarjeta del investigador
    st.markdown('<div class="section-title">👨‍🔬 Investigador Principal</div>', unsafe_allow_html=True)

    if photo_b64:
        photo_src = f"data:image/png;base64,{photo_b64}"
    else:
        # Avatar placeholder si no hay foto
        photo_src = "https://via.placeholder.com/92/2E8B8B/FFFFFF?text=KR"

    st.markdown(f"""
    <div class="researcher-card">
      <img class="researcher-photo" src="{photo_src}" alt="Kevin Rodriguez">
      <div>
        <div class="researcher-name">Kevin David Rodríguez González</div>
        <div class="researcher-title">PhD Student · Environmental Water Quality &amp; Remote Sensing</div>
        <div class="researcher-dept">Departamento de Geomática · Universidad Autónoma de Nuevo León</div>
        <div class="researcher-links">
          <a class="researcher-link" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
          <a class="researcher-link" href="https://orcid.org/0009-0004-3060-8575" target="_blank">🔗 ORCID</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Parámetros disponibles
    st.markdown('<div class="section-title">📊 Parámetros del Modelo</div>', unsafe_allow_html=True)
    for param, cfg in PARAMS.items():
        with st.expander(f"🔬 {cfg['label']} — OOB R² = {cfg['oob']:.3f}"):
            col_e1, col_e2 = st.columns([2, 1])
            with col_e1:
                st.write(cfg["desc"])
                st.progress(cfg["oob"])
            with col_e2:
                st.metric("OOB R²", f"{cfg['oob']:.3f}")
                st.metric("Rango",  f"{cfg['vmin']}–{cfg['vmax']} {cfg['unidad']}")
                st.metric("Estado", "✅ Bueno")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📍 Puntos de Muestreo — Río Pesquería</div>', unsafe_allow_html=True)
    df_pts = pd.DataFrame([{"lat": c[1], "lon": c[0], "Punto": p} for p, c in COORDS.items()])
    st.map(df_pts)

    st.info("ℹ️ **pH y OD excluidos** — OOB R² negativo: Sentinel-2 no captura señal óptica suficiente para esos parámetros.")

    st.markdown("""
    <div class="footer">
      Kevin D. Rodríguez González · PhD Student · Depto. Geomática · UANL &nbsp;·&nbsp;
      RF v3 · Sentinel-2 SR · KFold-5 + OOB score &nbsp;·&nbsp;
      <a href="https://orcid.org/0009-0004-3060-8575" style="color:#3A4A5C">ORCID</a>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────────────────────────────────────
progress = st.progress(0)
status   = st.empty()

modelos   = model_data["models"]
transforms= model_data["transforms"]
lambdas   = model_data["lambdas"]

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
    bounds = wmask.total_bounds
progress.progress(30)

status.text("Generando grilla de interpolación...")
lon_min, lat_min, lon_max, lat_max = bounds
RES = resolucion
lon_vec  = np.linspace(lon_min, lon_max, RES)
lat_vec  = np.linspace(lat_min, lat_max, RES)
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
        rbf = RBFInterpolator(pts_known[ok], vals[ok], kernel="thin_plate_spline", smoothing=0.1)
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
if n == 1:   axes_flat = [axes]
elif nrows == 1: axes_flat = list(axes)
else:        axes_flat = axes.flatten().tolist()

buf_ind = {}
for i, (col, info) in enumerate(mapas.items()):
    ax = axes_flat[i]; ax.set_facecolor("#161B22")
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
    ax.set_title(f"{info['label']} | OOB R² = {info['oob']:.3f}",
                 color="white", fontsize=11, fontweight="bold")
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
            f"OOB R² = {info['oob']:.3f}  |  Kevin D. Rodríguez G. · UANL Geomática",
            transform=ai.transAxes, fontsize=7, color="#8EAAC8", ha="right", va="bottom")
    ai.tick_params(colors="#8EAAC8", labelsize=7)
    for sp in ai.spines.values(): sp.set_edgecolor("#2E8B8B44")
    plt.tight_layout()
    fi.savefig(bi, dpi=180, bbox_inches="tight", facecolor="#0D1117")
    buf_ind[col] = bi; plt.close(fi)

for k in range(n, len(axes_flat)): axes_flat[k].set_visible(False)
mes2 = fecha_dt.month
temp = "Temporada Seca 🌵" if mes2 in [11, 12, 1, 2, 3] else "Temporada Lluviosa 🌧️"
fig.suptitle(
    f"Calidad de Agua — Río Pesquería\n"
    f"{fecha_dt.strftime('%d/%m/%Y')} | {temp} | RF v3 | UANL Geomática",
    fontsize=14, fontweight="bold", color="white", y=1.01)
plt.tight_layout()
buf_panel = io.BytesIO()
fig.savefig(buf_panel, dpi=150, bbox_inches="tight", facecolor="#0D1117")
plt.close(fig)
progress.progress(100); status.empty()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────
st.success(f"✅  {n} mapas generados — {fecha_dt.strftime('%d/%m/%Y')} · {temp}")
st.image(buf_panel, caption="Panel de calidad de agua · Río Pesquería · UANL", use_column_width=True)

st.markdown('<div class="section-title">📥 Descargar resultados</div>', unsafe_allow_html=True)
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
st.markdown('<div class="section-title">📊 Estadísticas espaciales</div>', unsafe_allow_html=True)
cols_st = st.columns(len(mapas))
for cs, (param, info) in zip(cols_st, mapas.items()):
    d = info["data"][np.isfinite(info["data"])]
    with cs:
        st.markdown(f"**{info['label']}**")
        st.metric("Media",  f"{d.mean():.2f} {info['unidad']}")
        st.metric("Máximo", f"{d.max():.2f} {info['unidad']}")
        st.metric("Mínimo", f"{d.min():.2f} {info['unidad']}")
        st.metric("OOB R²", f"{info['oob']:.3f}")

st.markdown("""
<div class="footer">
  Kevin D. Rodríguez González · PhD Student · Depto. Geomática · UANL &nbsp;·&nbsp;
  Random Forest v3 · Sentinel-2 SR · KFold-5 + OOB score &nbsp;·&nbsp;
  <a href="https://orcid.org/0009-0004-3060-8575" style="color:#3A4A5C">ORCID: 0009-0004-3060-8575</a>
</div>
""", unsafe_allow_html=True)
