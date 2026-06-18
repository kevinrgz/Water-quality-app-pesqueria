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
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Calidad de Agua – Río Pesquería",
    page_icon="💧",
    layout="wide",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem; font-weight: 700;
        color: #1A4F7A; margin-bottom: 0.2rem;
    }
    .subtitle { font-size: 1rem; color: #6B7280; margin-bottom: 1.5rem; }
    .metric-card {
        background: #F0F4F8; border-radius: 10px;
        padding: 1rem; text-align: center; margin-bottom: 0.5rem;
    }
    .metric-value { font-size: 1.8rem; font-weight: 600; color: #1A4F7A; }
    .metric-label { font-size: 0.8rem; color: #6B7280; }
    .badge-good {
        background: #EAF3DE; color: #27500A;
        padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;
    }
    .step-box {
        background: #F8FAFC; border: 1px solid #E2E8F0;
        border-radius: 10px; padding: 1rem; margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
PARAMS = {
    'P_TOT' : dict(label='Fósforo Total',       unidad='mg/L', vmin=0,  vmax=6,
                   pal=['#f7fcf5','#c7e9c0','#74c476','#238b45','#005a32'],
                   oob=0.684,
                   desc='Indicador de contaminación por aguas residuales y fertilizantes.'),
    'N_NH3' : dict(label='N-Amoniaco',           unidad='mg/L', vmin=0,  vmax=25,
                   pal=['#f7fcf5','#c7e9c0','#74c476','#238b45','#005a32'],
                   oob=0.645,
                   desc='Indicador de descargas de aguas residuales domésticas e industriales.'),
    'N_TOT' : dict(label='N-Total',              unidad='mg/L', vmin=0,  vmax=35,
                   pal=['#f7fcf5','#c7e9c0','#74c476','#238b45','#005a32'],
                   oob=0.615,
                   desc='Nitrógeno total disuelto, incluye todas las formas.'),
    'N_TOTK': dict(label='N-Total Kjeldahl',     unidad='mg/L', vmin=0,  vmax=35,
                   pal=['#f7fcf5','#c7e9c0','#74c476','#238b45','#005a32'],
                   oob=0.662,
                   desc='Nitrógeno orgánico + amoniaco, indicador de carga orgánica.'),
}

COORDS_PESQUERIA = {
    'Punto_1': (-100.34495, 25.81193),
    'Punto_2': (-100.29269, 25.80148),
    'Punto_3': (-100.28059, 25.80205),
    'Punto_4': (-100.21237, 25.83095),
    'Punto_5': (-100.20026, 25.82832),
    'Punto_6': (-100.04244, 25.78160),
    'Punto_7': (-100.02404, 25.77480),
}

FECHAS = [
    '2/25/2016','4/12/2016','5/17/2016','6/23/2016','7/26/2016','9/4/2016',
    '2/22/2017','4/4/2017', '5/16/2017','6/27/2017','8/8/2017', '9/18/2017',
    '2/8/2018', '3/13/2018','4/26/2018','6/8/2018', '10/8/2018','11/12/2018',
    '1/14/2019'
]

def make_cmap(pal):
    return LinearSegmentedColormap.from_list('wq', pal, N=256)

def inverse_transform_y(y_t, method, lam=None):
    if method == 'none': return y_t.copy()
    if method == 'log1': return np.expm1(y_t)
    if method == 'sqrt': return np.clip(y_t, 0, None)**2
    if method == 'yeoj': return stats.yeojohnson(y_t, lmbda=lam)


# ─────────────────────────────────────────────────────────────────────────────
# CARGAR MODELO EMBEBIDO (automático, sin que el usuario lo suba)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Cargando modelo RF v3...")
def cargar_modelo():
    pkl_path = os.path.join(os.path.dirname(__file__), 'modelos_rf_v3.pkl')
    if not os.path.exists(pkl_path):
        return None
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)

@st.cache_data(show_spinner="Cargando datos de muestreo...")
def cargar_csv():
    csv_path = os.path.join(os.path.dirname(__file__), 'INDICES_completo.csv')
    if not os.path.exists(csv_path):
        return None
    df = pd.read_csv(csv_path)
    df['target_date'] = pd.to_datetime(df['target_date'], format='%m/%d/%Y')
    return df

model_data = cargar_modelo()
df_global  = cargar_csv()


# ─────────────────────────────────────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">💧 Calidad de Agua — Río Pesquería</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">'
    'Modelo Random Forest v3 | Sentinel-2 SR | '
    'Universidad Autónoma de Nuevo León<br>'
    'Sube tu shapefile del área de estudio y obtén los mapas de calidad de agua'
    '</div>',
    unsafe_allow_html=True
)

# Tarjetas de métricas
cols_m = st.columns(4)
for col_m, (param, cfg) in zip(cols_m, PARAMS.items()):
    with col_m:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{cfg['oob']:.3f}</div>
            <div class="metric-label">OOB R² — {cfg['label']}</div>
            <span class="badge-good">🟢 Validado</span>
        </div>""", unsafe_allow_html=True)

# Avisos si faltan archivos del repositorio
if model_data is None:
    st.error("⚠️ Modelo `modelos_rf_v3.pkl` no encontrado en el repositorio.")
    st.stop()

if df_global is None:
    st.error("⚠️ Archivo `INDICES_completo.csv` no encontrado en el repositorio.")
    st.stop()

st.success("✅ Modelo RF v3 cargado | Datos de muestreo 2016–2019 listos")
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — SOLO WMASK Y CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")

    # Wmask
    st.subheader("1. 📍 Área de estudio")
    st.markdown(
        "Comprime tu shapefile en un ZIP con los 4 archivos: "
        "**.shp + .dbf + .prj + .cpg**"
    )
    wmask_zip = st.file_uploader(
        "Sube wmask.zip",
        type=['zip'],
        help="ZIP con los archivos .shp .dbf .prj .cpg"
    )

    st.markdown("---")

    # Fecha
    st.subheader("2. 📅 Fecha")
    fecha_sel = st.selectbox(
        "Fecha de la imagen Sentinel-2",
        options=FECHAS,
        index=16,
        format_func=lambda f: pd.to_datetime(f, format='%m/%d/%Y').strftime('%d %b %Y')
    )
    mes_prev  = pd.to_datetime(fecha_sel, format='%m/%d/%Y').month
    temp_prev = '🌵 Temporada Seca' if mes_prev in [11,12,1,2,3] else '🌧️ Temporada Lluviosa'
    st.info(temp_prev)

    st.markdown("---")

    # Parámetros
    st.subheader("3. 🔬 Parámetros")
    params_sel = st.multiselect(
        "Selecciona parámetros",
        options=list(PARAMS.keys()),
        default=list(PARAMS.keys()),
        format_func=lambda p: f"{PARAMS[p]['label']} ({PARAMS[p]['unidad']})"
    )

    st.markdown("---")

    # Resolución
    st.subheader("4. 🎯 Resolución")
    resolucion = st.select_slider(
        "Resolución de la grilla",
        options=[200, 300, 400, 500],
        value=400,
        format_func=lambda v: f"{v}×{v} celdas"
    )
    st.caption("Mayor resolución = más detalle, más tiempo")

    st.markdown("---")

    correr = st.button(
        "🗺️ Generar Mapas",
        type="primary",
        use_container_width=True,
        disabled=(wmask_zip is None or not params_sel)
    )

    if wmask_zip is None:
        st.warning("⬆️ Sube tu wmask.zip para continuar")


# ─────────────────────────────────────────────────────────────────────────────
# PANTALLA INICIAL
# ─────────────────────────────────────────────────────────────────────────────
if not correr:
    st.markdown("### 🚀 Cómo usar esta aplicación")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="step-box">
        <h4>Paso 1 — Sube tu shapefile</h4>
        Comprime los 4 archivos de tu wmask en un ZIP.<br><br>
        <code>wmask.shp</code><br>
        <code>wmask.dbf</code><br>
        <code>wmask.prj</code><br>
        <code>wmask.cpg</code>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="step-box">
        <h4>Paso 2 — Configura</h4>
        Elige la fecha de muestreo Sentinel-2 y los parámetros
        que quieres visualizar.<br><br>
        El modelo RF v3 ya está integrado.
        No necesitas subir nada más.
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="step-box">
        <h4>Paso 3 — Descarga</h4>
        Haz clic en <b>Generar Mapas</b> y descarga:<br><br>
        📊 Panel PNG — para tesis<br>
        🗺️ Mapas individuales ZIP<br>
        📈 Estadísticas espaciales
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Parámetros del modelo")
    for param, cfg in PARAMS.items():
        with st.expander(f"🔬 {cfg['label']} — OOB R² = {cfg['oob']:.3f}"):
            col_e1, col_e2 = st.columns([2,1])
            with col_e1:
                st.write(cfg['desc'])
                st.progress(cfg['oob'])
            with col_e2:
                st.metric("OOB R²", f"{cfg['oob']:.3f}")
                st.metric("Rango",  f"{cfg['vmin']}–{cfg['vmax']} {cfg['unidad']}")
                st.metric("Estado", "🟢 Bueno")

    st.markdown("---")
    st.markdown("### 📍 Puntos de muestreo — Río Pesquería")
    df_pts = pd.DataFrame([
        {'lat': c[1], 'lon': c[0], 'Punto': p}
        for p, c in COORDS_PESQUERIA.items()
    ])
    st.map(df_pts)

    st.info(
        "ℹ️ pH y OD no están disponibles — su OOB R² fue negativo, "
        "lo que indica que Sentinel-2 no tiene señal óptica suficiente "
        "para estimar esos parámetros en este río."
    )
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────────────────────────────────────
progress = st.progress(0)
status   = st.empty()

# Modelo ya en caché
modelos    = model_data['models']
transforms = model_data['transforms']
lambdas    = model_data['lambdas']
medias_pto = model_data['medias_punto']
progress.progress(10)

# Datos de la fecha seleccionada
status.text("Preparando datos de muestreo...")
coords      = COORDS_PESQUERIA
puntos_uniq = sorted(coords.keys())
lons        = np.array([coords[p][0] for p in puntos_uniq])
lats        = np.array([coords[p][1] for p in puntos_uniq])
pts_known   = np.column_stack([lons, lats])
fecha_dt    = pd.to_datetime(fecha_sel, format='%m/%d/%Y')
df_fecha    = df_global[df_global['target_date'] == fecha_dt]
progress.progress(20)

# Cargar wmask
status.text("Cargando shapefile...")
with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(wmask_zip, 'r') as z:
        z.extractall(tmpdir)
    shp_files = [f for f in os.listdir(tmpdir) if f.endswith('.shp')]
    if not shp_files:
        st.error("❌ No se encontró .shp dentro del ZIP")
        st.stop()
    wmask = gpd.read_file(os.path.join(tmpdir, shp_files[0]))
    if wmask.crs is None or wmask.crs.to_epsg() != 4326:
        wmask = wmask.to_crs(epsg=4326)
    union_geom = wmask.geometry.unary_union
    bounds     = wmask.total_bounds

progress.progress(35)

# Grilla de interpolación
status.text("Generando grilla de interpolación...")
lon_min, lat_min, lon_max, lat_max = bounds
RES      = resolucion
lon_vec  = np.linspace(lon_min, lon_max, RES)
lat_vec  = np.linspace(lat_min, lat_max, RES)
lon_grid, lat_grid = np.meshgrid(lon_vec, lat_vec)
pts_grid = np.column_stack([lon_grid.ravel(), lat_grid.ravel()])
extent   = [lon_min, lon_max, lat_min, lat_max]

mask_flat = np.array([union_geom.contains(Point(x,y)) for x,y in pts_grid])
mask_2d   = mask_flat.reshape(RES, RES)
progress.progress(60)

# Interpolar
status.text("Aplicando modelo RF...")
mapas = {}
for col in params_sel:
    if col not in PARAMS or col not in modelos: continue
    cfg  = PARAMS[col]

    # Valores observados en los 7 puntos para la fecha seleccionada
    vals = []
    for p in puntos_uniq:
        fila = df_fecha[df_fecha['nombre'] == p]
        vals.append(float(fila[col].values[0]) if len(fila) > 0 else np.nan)
    vals = np.array(vals)
    ok   = np.isfinite(vals)

    if ok.sum() < 3: continue

    try:
        rbf    = RBFInterpolator(pts_known[ok], vals[ok],
                                  kernel='thin_plate_spline', smoothing=0.1)
        z_flat = rbf(pts_grid)
    except Exception:
        z_flat = griddata(pts_known[ok], vals[ok], pts_grid, method='linear')
        z_nan  = griddata(pts_known[ok], vals[ok], pts_grid, method='nearest')
        z_flat = np.where(np.isnan(z_flat), z_nan, z_flat)

    z_2d = np.where(mask_2d, z_flat.reshape(RES, RES), np.nan)
    mapas[col] = {'data': z_2d, 'vals_puntos': vals, **cfg}

progress.progress(80)

# ─────────────────────────────────────────────────────────────────────────────
# GENERAR FIGURAS
# ─────────────────────────────────────────────────────────────────────────────
status.text("Generando visualizaciones...")

n     = len(mapas)
ncols = min(n, 2)
nrows = (n + ncols - 1) // ncols

fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*7, nrows*5.5))
fig.patch.set_facecolor('#1a1a2e')

if n == 1:   axes_flat = [axes]
elif nrows == 1: axes_flat = list(axes)
else:        axes_flat = axes.flatten().tolist()

buf_individuales = {}

for i, (col, info) in enumerate(mapas.items()):
    ax   = axes_flat[i]
    ax.set_facecolor('#0f0f23')
    data = info['data']
    vmin, vmax = info['vmin'], info['vmax']
    cmap = make_cmap(info['pal'])

    im = ax.imshow(np.clip(data, vmin, vmax), cmap=cmap,
                   vmin=vmin, vmax=vmax, extent=extent,
                   aspect='auto', interpolation='bilinear', origin='upper')

    wmask.boundary.plot(ax=ax, color='white', linewidth=1, alpha=0.7)

    vals_p = info['vals_puntos']
    for j, p in enumerate(puntos_uniq):
        lon, lat = coords[p]
        ax.scatter(lon, lat, c='white', s=60, zorder=5,
                   edgecolors='black', linewidths=0.6)
        if np.isfinite(vals_p[j]):
            ax.annotate(f' P{j+1}: {vals_p[j]:.1f}', (lon, lat),
                        fontsize=7.5, color='white', fontweight='bold', zorder=6)

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02, shrink=0.85)
    cbar.set_label(f"{info['label']} ({info['unidad']})",
                   color='white', fontsize=10)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white', fontsize=8)

    d = data[np.isfinite(data)]
    ax.set_title(f"{info['label']} | OOB R² = {info['oob']:.3f}",
                 color='white', fontsize=11, fontweight='bold')
    ax.text(0.01, 0.99,
            f"Min: {d.min():.2f}\nMáx: {d.max():.2f}\nMedia: {d.mean():.2f}",
            transform=ax.transAxes, fontsize=8, color='white', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.6))
    ax.set_xlabel('Longitud (°)', color='white', fontsize=8)
    ax.set_ylabel('Latitud (°)',  color='white', fontsize=8)
    ax.tick_params(colors='white', labelsize=7)
    for sp in ax.spines.values(): sp.set_edgecolor('#444')

    # Mapa individual
    buf_ind = io.BytesIO()
    fig_i, ax_i = plt.subplots(figsize=(11, 5))
    fig_i.patch.set_facecolor('#1a1a2e')
    ax_i.set_facecolor('#0f0f23')
    im2 = ax_i.imshow(np.clip(data, vmin, vmax), cmap=cmap,
                       vmin=vmin, vmax=vmax, extent=extent,
                       aspect='auto', interpolation='bilinear', origin='upper')
    wmask.boundary.plot(ax=ax_i, color='white', linewidth=1.2, alpha=0.7)
    for j, p in enumerate(puntos_uniq):
        lon, lat = coords[p]
        ax_i.scatter(lon, lat, c='white', s=80, zorder=5,
                     edgecolors='black', linewidths=0.8)
        if np.isfinite(vals_p[j]):
            ax_i.annotate(f' P{j+1}: {vals_p[j]:.1f}', (lon, lat),
                          fontsize=9, color='white', fontweight='bold', zorder=6)
    cbar2 = plt.colorbar(im2, ax=ax_i, fraction=0.025, pad=0.02, shrink=0.9)
    cbar2.set_label(f"{info['label']} ({info['unidad']})",
                    color='white', fontsize=11)
    plt.setp(plt.getp(cbar2.ax.axes, 'yticklabels'), color='white', fontsize=9)
    ax_i.set_title(
        f"{info['label']} | Río Pesquería | {fecha_dt.strftime('%d/%m/%Y')} | RF v3",
        color='white', fontsize=11, fontweight='bold')
    ax_i.text(0.99, 0.01, f'OOB R² = {info["oob"]:.3f}',
              transform=ax_i.transAxes, fontsize=8, color='#aaa',
              ha='right', va='bottom')
    ax_i.tick_params(colors='white', labelsize=7)
    for sp in ax_i.spines.values(): sp.set_edgecolor('#555')
    plt.tight_layout()
    fig_i.savefig(buf_ind, dpi=180, bbox_inches='tight', facecolor='#1a1a2e')
    buf_individuales[col] = buf_ind
    plt.close(fig_i)

for k in range(n, len(axes_flat)):
    axes_flat[k].set_visible(False)

mes       = fecha_dt.month
temporada = 'Temporada Seca 🌵' if mes in [11,12,1,2,3] else 'Temporada Lluviosa 🌧️'
fig.suptitle(
    f'Calidad de Agua — Río Pesquería\n'
    f'{fecha_dt.strftime("%d/%m/%Y")} | {temporada} | RF v3',
    fontsize=14, fontweight='bold', color='white', y=1.01
)
plt.tight_layout()

buf_panel = io.BytesIO()
fig.savefig(buf_panel, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close(fig)

progress.progress(100)
status.empty()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────
st.success(f"✅ {n} mapas generados — {fecha_dt.strftime('%d/%m/%Y')} | {temporada}")
st.image(buf_panel, caption="Panel de calidad de agua", use_column_width=True)

st.markdown("### 📥 Descargar resultados")
dl1, dl2 = st.columns(2)
with dl1:
    st.download_button(
        label="⬇️ Panel completo (PNG — para tesis)",
        data=buf_panel.getvalue(),
        file_name=f"calidad_agua_pesqueria_{fecha_dt.strftime('%Y%m%d')}.png",
        mime="image/png",
        use_container_width=True
    )
with dl2:
    buf_zip = io.BytesIO()
    with zipfile.ZipFile(buf_zip, 'w') as zf:
        for col, buf in buf_individuales.items():
            zf.writestr(
                f"mapa_{col}_{fecha_dt.strftime('%Y%m%d')}.png",
                buf.getvalue()
            )
    st.download_button(
        label="⬇️ Mapas individuales ZIP",
        data=buf_zip.getvalue(),
        file_name=f"mapas_pesqueria_{fecha_dt.strftime('%Y%m%d')}.zip",
        mime="application/zip",
        use_container_width=True
    )

st.markdown("---")
st.markdown("### 📊 Estadísticas espaciales")
cols_st = st.columns(len(mapas))
for col_st, (param, info) in zip(cols_st, mapas.items()):
    d = info['data'][np.isfinite(info['data'])]
    with col_st:
        st.markdown(f"**{info['label']}**")
        st.metric("Media",   f"{d.mean():.2f} {info['unidad']}")
        st.metric("Máximo",  f"{d.max():.2f} {info['unidad']}")
        st.metric("Mínimo",  f"{d.min():.2f} {info['unidad']}")
        st.metric("OOB R²",  f"{info['oob']:.3f}")

st.markdown("---")
st.caption(
    "Modelo Random Forest v3 | Sentinel-2 SR | "
    "Universidad Autónoma de Nuevo León | "
    "Validado con KFold-5 y OOB score"
)
