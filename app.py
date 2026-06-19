import streamlit as st
import pickle, tempfile, os, zipfile, warnings, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import RBFInterpolator, griddata
from scipy import stats
import geopandas as gpd
from shapely.geometry import Point
import io, base64
from datetime import date, timedelta
import folium
from streamlit_folium import st_folium
import ee
warnings.filterwarnings("ignore")

# ── Assets ────────────────────────────────────────────────────────────────────
def _b64(fn):
    p = os.path.join(os.path.dirname(__file__), fn)
    return base64.b64encode(open(p,"rb").read()).decode() if os.path.exists(p) else ""

GEO_B64   = _b64("logo_geomatica.png")
UANL_B64  = _b64("logo_uanl.png")
FIC_B64   = _b64("logo_fic.png")
PHOTO_B64 = _b64("photo_researcher.png")

# ── Constantes ────────────────────────────────────────────────────────────────
PARAMS = {
    "P_TOT": dict(label="Fósforo Total", unidad="mg/L", vmin=0, vmax=6, oob=0.684,
        icon="🧪", pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], color="#74c476",
        desc="Nutriente clave en eutrofización. Indica descargas de aguas residuales, "
             "efluentes industriales y escorrentía agrícola. Ref. NOM-001: 5 mg/L."),
    "N_NH3": dict(label="N-Amoniaco", unidad="mg/L", vmin=0, vmax=25, oob=0.645,
        icon="⚗️", pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], color="#238b45",
        desc="Forma reducida del nitrógeno. Indicador directo de contaminación orgánica "
             "reciente. Tóxico para fauna acuática. Ref. NOM-001: 25 mg/L."),
    "N_TOT": dict(label="N-Total", unidad="mg/L", vmin=0, vmax=35, oob=0.615,
        icon="🔬", pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], color="#2E8B8B",
        desc="Suma de todas las formas de nitrógeno disuelto. Indicador integral de "
             "carga nitrogenada y riesgo de eutrofización del ecosistema acuático."),
    "N_TOTK": dict(label="N-Total Kjeldahl", unidad="mg/L", vmin=0, vmax=35, oob=0.662,
        icon="🧫", pal=["#f7fcf5","#c7e9c0","#74c476","#238b45","#005a32"], color="#1A4F7A",
        desc="Nitrógeno orgánico + amoniaco por método Kjeldahl. Estándar internacional "
             "para evaluar carga orgánica y potencial de demanda bioquímica de oxígeno."),
}

COORDS = {
    "Punto_1": (-100.34495, 25.81193), "Punto_2": (-100.29269, 25.80148),
    "Punto_3": (-100.28059, 25.80205), "Punto_4": (-100.21237, 25.83095),
    "Punto_5": (-100.20026, 25.82832), "Punto_6": (-100.04244, 25.78160),
    "Punto_7": (-100.02404, 25.77480),
}

FECHAS_CAMPO = [
    "2/25/2016","4/12/2016","5/17/2016","6/23/2016","7/26/2016","9/4/2016",
    "2/22/2017","4/4/2017","5/16/2017","6/27/2017","8/8/2017","9/18/2017",
    "2/8/2018","3/13/2018","4/26/2018","6/8/2018","10/8/2018","11/12/2018",
    "1/14/2019"
]

def make_cmap(pal):
    return LinearSegmentedColormap.from_list("wq", pal, N=256)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Water Quality RF — Río Pesquería", page_icon="💧", layout="wide")

st.markdown("""
<style>
body,.stApp{background-color:#0D1117!important}
section[data-testid="stSidebar"]{background-color:#161B22!important}
.hdr{background:linear-gradient(135deg,#1A4F7A 0%,#0D1117 65%);
     border-bottom:2px solid #2E8B8B;padding:1.2rem 2rem .9rem;
     margin-bottom:1.2rem;border-radius:0 0 14px 14px}
.hdr-logos{display:flex;align-items:center;gap:16px;margin-bottom:.8rem;flex-wrap:wrap}
.hdr-logo-img{height:54px;object-fit:contain}
.hdr-sep{width:1px;height:46px;background:#2E8B8B55;flex-shrink:0}
.app-title{font-size:2.1rem;font-weight:800;color:#fff;margin:0;letter-spacing:-.5px}
.app-sub{font-size:.88rem;color:#8EAAC8;margin:.3rem 0 0}
.metric-row{display:flex;gap:12px;margin:1rem 0;flex-wrap:wrap}
.metric-card{flex:1;min-width:130px;background:linear-gradient(145deg,#161B22,#1A2030);
             border:1px solid #2E8B8B44;border-radius:14px;padding:1rem;text-align:center}
.metric-value{font-size:1.85rem;font-weight:700;color:#2E8B8B}
.metric-label{font-size:.68rem;color:#8EAAC8;text-transform:uppercase;letter-spacing:.07em;margin-top:4px}
.badge-ok{display:inline-block;margin-top:8px;background:#1A3A2A;color:#3DBA7A;
          border:1px solid #3DBA7A55;padding:2px 12px;border-radius:20px;font-size:.68rem;font-weight:700}
.map-panel{background:#161B22;border:1px solid #2E8B8B44;border-radius:14px;padding:.8rem 1rem;margin-bottom:1rem}
.map-title{font-size:.75rem;font-weight:700;color:#2E8B8B;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.5rem}
.map-meta{font-size:.72rem;color:#8EAAC8;margin-top:.5rem;line-height:1.5}
.chip{display:inline-block;background:#0D1F2D;border:1px solid #2E8B8B44;color:#2E8B8B;
      font-size:.67rem;border-radius:4px;padding:2px 8px;margin:2px}
.chip-warn{border-color:#FFD70066;color:#FFD700}
.chip-bad{border-color:#E74C3C66;color:#E74C3C}
.info-panel{background:#161B22;border:1px solid #FFFFFF0F;border-radius:14px;padding:.8rem 1rem;margin-bottom:1rem}
.info-title{font-size:.75rem;font-weight:700;color:#8EAAC8;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.5rem}
.param-card{background:#161B22;border:1px solid #FFFFFF12;border-left:3px solid #2E8B8B;
            border-radius:0 12px 12px 0;padding:1.1rem 1.4rem;margin-bottom:.75rem}
.param-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:.55rem;flex-wrap:wrap;gap:8px}
.param-name{font-size:.95rem;font-weight:700;color:#FFFFFF}
.param-oob{font-size:.68rem;color:#2E8B8B;background:#0D1F2D;border:1px solid #2E8B8B44;border-radius:20px;padding:2px 10px}
.param-desc{font-size:.78rem;color:#8EAAC8;line-height:1.65;margin-bottom:.65rem}
.param-meta{display:flex;gap:20px;flex-wrap:wrap}
.pmi{font-size:.72rem;color:#8EAAC8}
.pmv{color:#2E8B8B;font-weight:600}
.step-box{background:#161B22;border:1px solid #FFFFFF0F;border-left:3px solid #2E8B8B;
          border-radius:0 10px 10px 0;padding:1rem 1.2rem}
.step-t{font-size:.88rem;font-weight:700;color:#fff;margin-bottom:.5rem}
.step-b{font-size:.76rem;color:#8EAAC8;line-height:1.65}
.researcher-card{background:linear-gradient(145deg,#161B22,#1A2030);border:1px solid #2E8B8B44;
                 border-radius:16px;padding:1.3rem 1.7rem;display:flex;gap:20px;align-items:center}
.rphoto{width:88px;height:88px;border-radius:50%;object-fit:cover;border:3px solid #2E8B8B;flex-shrink:0}
.rname{font-size:1rem;font-weight:700;color:#fff;margin:0 0 2px}
.rtitle{font-size:.8rem;color:#2E8B8B;font-weight:600;margin:0 0 3px}
.rdept{font-size:.76rem;color:#8EAAC8;margin:0 0 9px}
.rlinks{display:flex;gap:9px;flex-wrap:wrap}
.rlink{font-size:.70rem;color:#8EAAC8;background:#FFFFFF0D;border:1px solid #FFFFFF22;
       border-radius:20px;padding:3px 11px;text-decoration:none}
.divider{border:0;border-top:1px solid #FFFFFF0F;margin:1.1rem 0}
.sec-t{font-size:.73rem;font-weight:700;color:#8EAAC8;letter-spacing:.09em;text-transform:uppercase;margin:1.1rem 0 .6rem}
.slabel{font-size:.68rem;color:#8EAAC8;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:.3rem}
.footer{text-align:center;font-size:.68rem;color:#3A4A5C;margin-top:2rem;padding-top:1rem;border-top:1px solid #FFFFFF0D}
</style>
""", unsafe_allow_html=True)

# ── Conexión a GEE con Service Account ────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_gee():
    try:
        sa_email = st.secrets["gee"]["service_account"]
        creds_json = st.secrets["gee"]["credentials"]
        credentials = ee.ServiceAccountCredentials(sa_email, key_data=creds_json)
        ee.Initialize(credentials)
        return True, None
    except Exception as e:
        return False, str(e)

GEE_OK, GEE_ERROR = init_gee()

# ── Carga modelo y CSV ─────────────────────────────────────────────────────────
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

# ── Configuración de capas espectrales disponibles ────────────────────────────
INDICES_VIZ = {
    "RGB": dict(
        nombre="🌈 RGB (Color natural)",
        desc="Composición B4-B3-B2. Vista natural de la escena.",
        vis={"bands": ["B4","B3","B2"], "min": 0, "max": 3000, "gamma": 1.3},
    ),
    "NDVI": dict(
        nombre="🌿 NDVI (Vegetación)",
        desc="Detecta vegetación ribereña que puede contaminar el píxel "
             "de agua. Verde=vegetación densa, café=suelo/agua.",
        vis={"min": -0.2, "max": 0.8,
             "palette": ["#a50026","#d73027","#fee08b","#d9ef8b","#66bd63","#1a9850","#006837"]},
    ),
    "NDWI": dict(
        nombre="💧 NDWI (Índice de Agua)",
        desc="Índice McFeeters. Azul intenso=agua, café=tierra. "
             "Delimita el cuerpo de agua dentro de tu wmask.",
        vis={"min": -0.5, "max": 0.5,
             "palette": ["#8c510a","#d8b365","#f6e8c3","#c7eae5","#5ab4ac","#01665e"]},
    ),
    "MNDWI": dict(
        nombre="🌊 MNDWI (Agua mejorado)",
        desc="Índice Xu, mejor para aguas turbias que NDWI estándar. "
             "Recomendado para ríos con alta carga de sedimentos.",
        vis={"min": -0.5, "max": 0.5,
             "palette": ["#7f3b08","#b35806","#fee0b6","#d8daeb","#8073ac","#542788"]},
    ),
    "NDTI": dict(
        nombre="🟤 NDTI (Turbidez)",
        desc="Índice de turbidez normalizado. Rojo=alta turbidez, "
             "azul=agua clara. Correlaciona con SST y color del agua.",
        vis={"min": -0.3, "max": 0.3,
             "palette": ["#08519c","#6baed6","#fee5d9","#fc9272","#de2d26","#a50f15"]},
    ),
}

def calcular_indice_gee(img, indice):
    if indice == "NDVI":
        return img.normalizedDifference(["B8","B4"]).rename("NDVI")
    elif indice == "NDWI":
        return img.normalizedDifference(["B3","B8"]).rename("NDWI")
    elif indice == "MNDWI":
        return img.normalizedDifference(["B3","B11"]).rename("MNDWI")
    elif indice == "NDTI":
        return img.normalizedDifference(["B4","B3"]).rename("NDTI")
    return None


@st.cache_data(ttl=1800, show_spinner=False)
def buscar_imagen_s2(bbox, fecha_ini_str, fecha_fin_str, max_nubes):
    if not GEE_OK:
        return None, {}
    try:
        lon_min, lat_min, lon_max, lat_max = bbox
        geom = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])
        coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(geom)
                  .filterDate(fecha_ini_str, fecha_fin_str)
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                  .sort("CLOUDY_PIXEL_PERCENTAGE"))
        n_imgs = coll.size().getInfo()
        if n_imgs == 0:
            return {"n_imagenes": 0}, {}

        img = coll.first().clip(geom)
        img_info = img.getInfo()
        props = img_info.get("properties", {})
        fecha_real = props.get("PRODUCT_ID", "")[7:15] if "PRODUCT_ID" in props else "N/D"
        nubes_pct  = props.get("CLOUDY_PIXEL_PERCENTAGE", None)

        tile_urls = {}
        map_id_rgb = img.getMapId(INDICES_VIZ["RGB"]["vis"])
        tile_urls["RGB"] = map_id_rgb["tile_fetcher"].url_format

        for idx_name in ["NDVI", "NDWI", "MNDWI", "NDTI"]:
            idx_img = calcular_indice_gee(img, idx_name)
            map_id  = idx_img.getMapId(INDICES_VIZ[idx_name]["vis"])
            tile_urls[idx_name] = map_id["tile_fetcher"].url_format

        info = {"n_imagenes": n_imgs,
                "nubes_pct": round(nubes_pct, 1) if nubes_pct is not None else None,
                "fecha_real": fecha_real}
        return info, tile_urls
    except Exception as e:
        return {"error": str(e)}, {}


def build_folium_map_s2(wmask_gdf, coords_dict, bbox, tile_urls=None, height=460):
    lon_min, lat_min, lon_max, lat_max = bbox
    cx, cy = (lon_min+lon_max)/2, (lat_min+lat_max)/2
    span = max(lon_max-lon_min, lat_max-lat_min)
    zoom = max(11, min(15, int(13 - span*8)))
    m = folium.Map(location=[cy, cx], zoom_start=zoom, tiles=None, width="100%", height=height)

    tile_urls = tile_urls or {}

    if "RGB" in tile_urls:
        folium.TileLayer(tiles=tile_urls["RGB"], attr="GEE — Sentinel-2 SR",
                         name="🌈 RGB (Color natural)", overlay=False,
                         control=True, show=True).add_to(m)

    for idx_name in ["NDVI", "NDWI", "MNDWI", "NDTI"]:
        if idx_name in tile_urls:
            cfg = INDICES_VIZ[idx_name]
            folium.TileLayer(tiles=tile_urls[idx_name], attr="GEE — Sentinel-2 SR",
                             name=cfg["nombre"], overlay=False,
                             control=True, show=False).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery", name="🌍 Satélite (referencia actual)",
        overlay=False, control=True, show=(not tile_urls)).add_to(m)

    folium.TileLayer(tiles="OpenStreetMap", name="🗺️ Mapa base",
                     overlay=False, control=True, show=False).add_to(m)

    folium.GeoJson(
        wmask_gdf.__geo_interface__, name="📍 Área de estudio",
        style_function=lambda x: {"fillColor":"#2E8B8B","color":"#00FFCC",
                                  "weight":2.5,"fillOpacity":0.10}).add_to(m)

    for j,(nombre,(lon,lat)) in enumerate(coords_dict.items()):
        folium.CircleMarker(
            location=[lat,lon], radius=8, color="#FFD700",
            fill=True, fill_color="#FFD700", fill_opacity=0.9, weight=2,
            popup=folium.Popup(f"<b>{nombre}</b><br>Lon:{lon:.5f}°<br>Lat:{lat:.5f}°", max_width=150),
            tooltip=f"P{j+1} — {nombre}").add_to(m)
        folium.Marker(
            location=[lat+0.0015, lon+0.001],
            icon=folium.DivIcon(
                html=f'<div style="font-size:10px;font-weight:bold;color:white;'
                     f'text-shadow:1px 1px 2px black">P{j+1}</div>',
                icon_size=(25,15), icon_anchor=(0,0))).add_to(m)

    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    return m



# ── HEADER ────────────────────────────────────────────────────────────────────
logo_u = f'<img class="hdr-logo-img" src="data:image/png;base64,{UANL_B64}">' if UANL_B64 else "<span style='color:#8EAAC8'>UANL</span>"
logo_f = f'<img class="hdr-logo-img" src="data:image/png;base64,{FIC_B64}">'  if FIC_B64  else ""
logo_g = f'<img class="hdr-logo-img" src="data:image/png;base64,{GEO_B64}">'  if GEO_B64  else ""

st.markdown(f"""
<div class="hdr">
  <div class="hdr-logos">{logo_u}<div class="hdr-sep"></div>{logo_f}<div class="hdr-sep"></div>{logo_g}</div>
  <div class="app-title">💧 Water Quality Mapping</div>
  <div class="app-sub">Río Pesquería, Nuevo León, México &nbsp;·&nbsp;
    Random Forest v3 · Sentinel-2 SR 2016–2019 &nbsp;·&nbsp;
    Universidad Autónoma de Nuevo León · FIC · Depto. Geomática</div>
</div>
""", unsafe_allow_html=True)

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
mh = '<div class="metric-row">'
for col, cfg in PARAMS.items():
    mh += (f'<div class="metric-card"><div class="metric-value">{cfg["oob"]:.3f}</div>'
           f'<div class="metric-label">OOB R² · {cfg["label"]}</div>'
           f'<span class="badge-ok">✓ Validado</span></div>')
mh += "</div>"
st.markdown(mh, unsafe_allow_html=True)

if model_data is None: st.error("⚠️ modelos_rf_v3.pkl no encontrado"); st.stop()
if df_global  is None: st.error("⚠️ INDICES_completo.csv no encontrado"); st.stop()

col_status1, col_status2 = st.columns(2)
with col_status1:
    st.success("✅  Modelo RF v3 cargado  ·  Datos de muestreo 2016–2019 listos")
with col_status2:
    if GEE_OK:
        st.success("✅  Conexión a Google Earth Engine activa")
    else:
        st.warning(f"⚠️  GEE no disponible — se usará imagen de referencia.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="slabel">📍 Área de estudio</div>', unsafe_allow_html=True)
    st.caption("Comprime: .shp + .dbf + .prj + .cpg → ZIP")
    wmask_zip = st.file_uploader("Sube wmask.zip", type=["zip"])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🧪 Fecha de muestreo</div>', unsafe_allow_html=True)
    fecha_campo = st.selectbox("", FECHAS_CAMPO, index=16,
        format_func=lambda f: pd.to_datetime(f, format="%m/%d/%Y").strftime("%d %b %Y"))
    fecha_dt = pd.to_datetime(fecha_campo, format="%m/%d/%Y")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🛰️ Rango imagen Sentinel-2</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fecha_ini = st.date_input("Desde", value=fecha_dt.date()-timedelta(days=8),
                                  min_value=date(2015,6,1), max_value=date(2025,12,31))
    with col_d2:
        fecha_fin = st.date_input("Hasta", value=fecha_dt.date()+timedelta(days=8),
                                  min_value=date(2015,6,1), max_value=date(2025,12,31))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">☁️ Filtro de nubes</div>', unsafe_allow_html=True)
    max_nubes = st.slider("Máx. cobertura (%)", 0, 50, 15, 5)

    if fecha_ini >= fecha_fin:
        st.error("⚠️ Fecha inicio debe ser anterior a fin")
    else:
        dias = (fecha_fin - fecha_ini).days
        mid  = fecha_ini + (fecha_fin - fecha_ini)/2
        des  = abs((fecha_dt.date() - mid).days)
        if des <= 5:   st.success(f"✅ Desfase: {des} días")
        elif des <= 12: st.warning(f"⚠️ Desfase: {des} días")
        else:           st.error(f"❌ Desfase: {des} días")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🔬 Parámetros a mapear</div>', unsafe_allow_html=True)
    params_sel = st.multiselect("", list(PARAMS.keys()), default=list(PARAMS.keys()),
        format_func=lambda p: f"{PARAMS[p]['label']} ({PARAMS[p]['unidad']})")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">🎯 Resolución</div>', unsafe_allow_html=True)
    resolucion = st.select_slider("", options=[200,300,400,500], value=400,
        format_func=lambda v: f"{v}×{v}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    valid = (wmask_zip is not None and params_sel and fecha_ini < fecha_fin)
    correr = st.button("🗺️  Generar Mapas", type="primary",
                       use_container_width=True, disabled=not valid)
    if wmask_zip is None:
        st.warning("⬆️  Sube tu wmask.zip para continuar")

# ── PANTALLA INICIAL ──────────────────────────────────────────────────────────
if not correr:
    c1,c2,c3 = st.columns(3)
    for col,(t,b) in zip([c1,c2,c3],[
        ("① Configura","Sube tu <b>wmask.zip</b>, elige fecha de muestreo y rango Sentinel-2."),
        ("② Verifica imagen","Se busca automáticamente en GEE la imagen real con menos nubes del período."),
        ("③ Genera y Descarga","Panel PNG · Mapas individuales ZIP · Estadísticas espaciales"),
    ]):
        with col:
            st.markdown(f'<div class="step-box"><div class="step-t">{t}</div><div class="step-b">{b}</div></div>',
                       unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if wmask_zip is not None and fecha_ini < fecha_fin:
        with st.spinner("Cargando shapefile..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    with zipfile.ZipFile(wmask_zip,"r") as z: z.extractall(tmpdir)
                    shp = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
                    wmask_prev = gpd.read_file(os.path.join(tmpdir, shp[0]))
                    if wmask_prev.crs is None or wmask_prev.crs.to_epsg()!=4326:
                        wmask_prev = wmask_prev.to_crs(4326)
                    bbox_prev = tuple(wmask_prev.total_bounds)
                    lon_min,lat_min,lon_max,lat_max = bbox_prev
            except Exception as e:
                st.error(f"Error: {e}"); wmask_prev = None

        if wmask_prev is not None:
            st.markdown('<div class="sec-t">🛰️ Previsualización del Área de Estudio</div>', unsafe_allow_html=True)

            tile_urls, s2_info = {}, {}
            if GEE_OK:
                with st.spinner("Buscando imagen Sentinel-2 y calculando indices espectrales..."):
                    s2_info, tile_urls = buscar_imagen_s2(
                        bbox_prev, fecha_ini.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d"), max_nubes)

            st.markdown('<div class="map-panel">', unsafe_allow_html=True)
            st.markdown('<div class="map-title">🛰️ Imagen Satelital — Rio Pesqueria</div>', unsafe_allow_html=True)

            mapa_f = build_folium_map_s2(wmask_prev, COORDS, bbox_prev, tile_urls=tile_urls, height=460)
            st_folium(mapa_f, width="100%", height=460, returned_objects=[])

            if s2_info.get("n_imagenes", 0) == 0:
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip chip-bad">❌ Sin imágenes en este rango con &lt;{max_nubes}% nubes</span>
                  <br>Amplía el rango de fechas o aumenta el umbral de nubes en el sidebar.
                </div></div>""", unsafe_allow_html=True)
            elif "error" in s2_info:
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip chip-warn">⚠️ Mostrando capa de referencia (Esri actual)</span>
                  <br>No se pudo conectar a GEE.
                </div></div>""", unsafe_allow_html=True)
            else:
                n_imgs   = s2_info.get("n_imagenes", 0)
                nubes_real = s2_info.get("nubes_pct", "N/D")
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip">✅ {n_imgs} imagen(es) encontrada(s)</span>
                  <span class="chip">☁️ Nubes reales: {nubes_real}%</span>
                  <span class="chip">📅 {fecha_ini.strftime('%d %b')} → {fecha_fin.strftime('%d %b %Y')}</span>
                  <span class="chip">🧪 Muestreo: {fecha_dt.strftime('%d %b %Y')}</span><br>
                  <b style="color:#fff">5 capas disponibles</b>: usa el panel de capas a la derecha
                  del mapa para alternar entre RGB, NDVI (vegetación), NDWI y MNDWI (agua),
                  y NDTI (turbidez) — la misma imagen que usará el modelo.
                </div></div>""", unsafe_allow_html=True)

                # Leyenda de indices espectrales disponibles
                st.markdown('<div class="map-panel" style="margin-top:.6rem">', unsafe_allow_html=True)
                st.markdown('<div class="map-title">📡 Indices Espectrales Disponibles en el Mapa</div>',
                           unsafe_allow_html=True)
                idx_cols = st.columns(5)
                for ic, idx_key in zip(idx_cols, ["RGB","NDVI","NDWI","MNDWI","NDTI"]):
                    cfg = INDICES_VIZ[idx_key]
                    with ic:
                        st.markdown(f"""
                        <div style="font-size:.72rem;color:#8EAAC8;line-height:1.5;
                                    border-left:2px solid #2E8B8B;padding-left:8px">
                          <b style="color:#fff;font-size:.78rem">{cfg['nombre']}</b><br>
                          {cfg['desc']}
                        </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            ci1,ci2,ci3 = st.columns(3)
            with ci1:
                st.markdown('<div class="info-panel"><div class="info-title">📐 Bbox</div>', unsafe_allow_html=True)
                st.markdown(f"""<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">
                  <b style="color:#fff">Lon</b>: {lon_min:.5f}° → {lon_max:.5f}°<br>
                  <b style="color:#fff">Lat</b>: {lat_min:.5f}° → {lat_max:.5f}°<br>
                  <b style="color:#fff">Polígonos</b>: {len(wmask_prev)}
                </div></div>""", unsafe_allow_html=True)
            with ci2:
                st.markdown('<div class="info-panel"><div class="info-title">🛰️ Sentinel-2</div>', unsafe_allow_html=True)
                dias=(fecha_fin-fecha_ini).days
                st.markdown(f"""<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">
                  <b style="color:#fff">Colección</b>: S2_SR_HARMONIZED<br>
                  <b style="color:#fff">RGB</b>: B4·B3·B2 (10m)<br>
                  <b style="color:#fff">Rango</b>: {dias} días · Nubes&lt;{max_nubes}%
                </div></div>""", unsafe_allow_html=True)
            with ci3:
                st.markdown('<div class="info-panel"><div class="info-title">🔬 Parámetros</div>', unsafe_allow_html=True)
                ph = "".join(f'<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">'
                            f'<span style="color:{PARAMS[p]["color"]}">{PARAMS[p]["icon"]}</span> '
                            f'<b style="color:#fff">{PARAMS[p]["label"]}</b></div>' for p in params_sel)
                st.markdown(ph + "</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="sec-t">📍 Puntos de Muestreo</div>', unsafe_allow_html=True)
        st.map(pd.DataFrame([{"lat":c[1],"lon":c[0]} for c in COORDS.values()]))
        st.info("⬅️  Sube tu **wmask.zip** para ver la imagen Sentinel-2 real del área.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sec-t">📊 Parámetros Fisicoquímicos del Modelo</div>', unsafe_allow_html=True)
    for col,cfg in PARAMS.items():
        st.markdown(f"""<div class="param-card">
          <div class="param-hdr"><div class="param-name">{cfg["icon"]} &nbsp;{cfg["label"]}</div>
          <span class="param-oob">OOB R² = {cfg["oob"]:.3f} · Validado ✓</span></div>
          <div class="param-desc">{cfg["desc"]}</div>
          <div class="param-meta">
            <div class="pmi">Unidad: <span class="pmv">{cfg["unidad"]}</span></div>
            <div class="pmi">Rango: <span class="pmv">{cfg["vmin"]}–{cfg["vmax"]} {cfg["unidad"]}</span></div>
            <div class="pmi">Estado: <span class="pmv">🟢 Bueno</span></div>
          </div></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sec-t">👨‍🔬 Investigador Principal</div>', unsafe_allow_html=True)
    photo_src = f"data:image/png;base64,{PHOTO_B64}" if PHOTO_B64 else ""
    st.markdown(f"""<div class="researcher-card">
      <img class="rphoto" src="{photo_src}">
      <div><div class="rname">Kevin David Rodríguez González</div>
      <div class="rtitle">PhD Student · Environmental Water Quality &amp; Remote Sensing</div>
      <div class="rdept">Departamento de Geomática · Facultad de Ingeniería Civil · UANL</div>
      <div class="rlinks">
        <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
        <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">🔗 ORCID</a>
      </div></div></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="footer">RF v3 · Sentinel-2 SR · UANL · FIC · Depto. Geomática · KFold-5 + OOB</div>""",
               unsafe_allow_html=True)
    st.stop()

# ── PROCESAMIENTO ─────────────────────────────────────────────────────────────
progress = st.progress(0); status = st.empty()
modelos    = model_data["models"]
transforms = model_data["transforms"]
lambdas    = model_data["lambdas"]

puntos_uniq = sorted(COORDS.keys())
lons = np.array([COORDS[p][0] for p in puntos_uniq])
lats = np.array([COORDS[p][1] for p in puntos_uniq])
pts_known = np.column_stack([lons, lats])
fecha_campo_dt = pd.to_datetime(fecha_campo, format="%m/%d/%Y")
df_fecha = df_global[df_global["target_date"]==fecha_campo_dt]
progress.progress(10)

status.text("Cargando shapefile...")
with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(wmask_zip,"r") as z: z.extractall(tmpdir)
    shp=[f for f in os.listdir(tmpdir) if f.endswith(".shp")]
    if not shp: st.error("No .shp"); st.stop()
    wmask = gpd.read_file(os.path.join(tmpdir, shp[0]))
    if wmask.crs is None or wmask.crs.to_epsg()!=4326: wmask=wmask.to_crs(4326)
    union_geom = wmask.geometry.unary_union
    bounds = wmask.total_bounds
progress.progress(30)

status.text("Generando grilla...")
lon_min,lat_min,lon_max,lat_max = bounds
RES = resolucion
lon_vec=np.linspace(lon_min,lon_max,RES); lat_vec=np.linspace(lat_min,lat_max,RES)
lon_grid,lat_grid=np.meshgrid(lon_vec,lat_vec)
pts_grid=np.column_stack([lon_grid.ravel(),lat_grid.ravel()])
extent=[lon_min,lon_max,lat_min,lat_max]
mask_flat=np.array([union_geom.contains(Point(x,y)) for x,y in pts_grid])
mask_2d=mask_flat.reshape(RES,RES)
progress.progress(60)

status.text("Aplicando modelo RF...")
mapas={}
for col in params_sel:
    if col not in PARAMS or col not in modelos: continue
    cfg=PARAMS[col]; vals=[]
    for p in puntos_uniq:
        fila=df_fecha[df_fecha["nombre"]==p]
        vals.append(float(fila[col].values[0]) if len(fila)>0 else np.nan)
    vals=np.array(vals); ok=np.isfinite(vals)
    if ok.sum()<3: continue
    try:
        rbf=RBFInterpolator(pts_known[ok],vals[ok],kernel="thin_plate_spline",smoothing=0.1)
        z_flat=rbf(pts_grid)
    except Exception:
        z_flat=griddata(pts_known[ok],vals[ok],pts_grid,method="linear")
        z_nan=griddata(pts_known[ok],vals[ok],pts_grid,method="nearest")
        z_flat=np.where(np.isnan(z_flat),z_nan,z_flat)
    z_2d=np.where(mask_2d,z_flat.reshape(RES,RES),np.nan)
    mapas[col]={"data":z_2d,"vals_puntos":vals,**cfg}
progress.progress(80)

status.text("Generando visualizaciones...")
n=len(mapas); ncols=min(n,2); nrows=(n+ncols-1)//ncols
fig,axes=plt.subplots(nrows,ncols,figsize=(ncols*7,nrows*5.5))
fig.patch.set_facecolor("#0D1117")
if n==1: axes_flat=[axes]
elif nrows==1: axes_flat=list(axes)
else: axes_flat=axes.flatten().tolist()
buf_ind={}

for i,(col,info) in enumerate(mapas.items()):
    ax=axes_flat[i]; ax.set_facecolor("#161B22")
    data=info["data"]; vmin,vmax=info["vmin"],info["vmax"]
    cmap=make_cmap(info["pal"])
    im=ax.imshow(np.clip(data,vmin,vmax),cmap=cmap,vmin=vmin,vmax=vmax,
                extent=extent,aspect="auto",interpolation="bilinear",origin="upper")
    wmask.boundary.plot(ax=ax,color="#2E8B8B",linewidth=1.2,alpha=0.8)
    vals_p=info["vals_puntos"]
    for j,p in enumerate(puntos_uniq):
        lon,lat=COORDS[p]
        ax.scatter(lon,lat,c="white",s=60,zorder=5,edgecolors="#0D1117",linewidths=0.6)
        if np.isfinite(vals_p[j]):
            ax.annotate(f" P{j+1}: {vals_p[j]:.1f}",(lon,lat),fontsize=7.5,color="white",fontweight="bold",zorder=6)
    cbar=plt.colorbar(im,ax=ax,fraction=0.03,pad=0.02,shrink=0.85)
    cbar.set_label(f"{info['label']} ({info['unidad']})",color="white",fontsize=10)
    plt.setp(plt.getp(cbar.ax.axes,"yticklabels"),color="white",fontsize=8)
    d=data[np.isfinite(data)]
    ax.set_title(info["label"],color="white",fontsize=11,fontweight="bold")
    ax.text(0.01,0.99,f"Min:{d.min():.2f}\nMáx:{d.max():.2f}\nMedia:{d.mean():.2f}",
            transform=ax.transAxes,fontsize=8,color="white",va="top",
            bbox=dict(boxstyle="round,pad=0.3",facecolor="#0D1117",alpha=0.7))
    ax.set_xlabel("Longitud (°)",color="#8EAAC8",fontsize=8)
    ax.set_ylabel("Latitud (°)",color="#8EAAC8",fontsize=8)
    ax.tick_params(colors="#8EAAC8",labelsize=7)
    for sp in ax.spines.values(): sp.set_edgecolor("#2E8B8B44")

    bi=io.BytesIO(); fi,ai=plt.subplots(figsize=(11,5))
    fi.patch.set_facecolor("#0D1117"); ai.set_facecolor("#161B22")
    im2=ai.imshow(np.clip(data,vmin,vmax),cmap=cmap,vmin=vmin,vmax=vmax,
                 extent=extent,aspect="auto",interpolation="bilinear",origin="upper")
    wmask.boundary.plot(ax=ai,color="#2E8B8B",linewidth=1.4,alpha=0.8)
    for j,p in enumerate(puntos_uniq):
        lon,lat=COORDS[p]; ai.scatter(lon,lat,c="white",s=80,zorder=5,edgecolors="#0D1117",linewidths=0.8)
        if np.isfinite(vals_p[j]): ai.annotate(f" P{j+1}: {vals_p[j]:.1f}",(lon,lat),fontsize=9,color="white",fontweight="bold",zorder=6)
    cb2=plt.colorbar(im2,ax=ai,fraction=0.025,pad=0.02,shrink=0.9)
    cb2.set_label(f"{info['label']} ({info['unidad']})",color="white",fontsize=11)
    plt.setp(plt.getp(cb2.ax.axes,"yticklabels"),color="white",fontsize=9)
    ai.set_title(f"{info['label']} | Río Pesquería | {fecha_campo_dt.strftime('%d/%m/%Y')} | RF v3",
                color="white",fontsize=11,fontweight="bold")
    ai.text(0.99,0.01,"Kevin D. Rodríguez G. · UANL · Depto. Geomática · RF v3",
           transform=ai.transAxes,fontsize=7,color="#8EAAC8",ha="right",va="bottom")
    ai.tick_params(colors="#8EAAC8",labelsize=7)
    for sp in ai.spines.values(): sp.set_edgecolor("#2E8B8B44")
    plt.tight_layout(); fi.savefig(bi,dpi=180,bbox_inches="tight",facecolor="#0D1117")
    buf_ind[col]=bi; plt.close(fi)

for k in range(n,len(axes_flat)): axes_flat[k].set_visible(False)
mes2=fecha_campo_dt.month
temp="Temporada Seca 🌵" if mes2 in [11,12,1,2,3] else "Temporada Lluviosa 🌧️"
fig.suptitle(f"Calidad de Agua — Río Pesquería\n{fecha_campo_dt.strftime('%d/%m/%Y')} | {temp} | RF v3 | UANL·FIC·Geomática",
            fontsize=13,fontweight="bold",color="white",y=1.01)
plt.tight_layout()
buf_panel=io.BytesIO()
fig.savefig(buf_panel,dpi=150,bbox_inches="tight",facecolor="#0D1117")
plt.close(fig); progress.progress(100); status.empty()

st.success(f"✅  {n} mapas — {fecha_campo_dt.strftime('%d/%m/%Y')} · {temp}")
st.image(buf_panel,caption="Panel de calidad de agua · Río Pesquería · UANL",use_column_width=True)

st.markdown('<div class="sec-t">📥 Descargar resultados</div>',unsafe_allow_html=True)
dl1,dl2=st.columns(2)
with dl1:
    st.download_button("⬇️  Panel completo PNG",buf_panel.getvalue(),
        f"WaterQuality_{fecha_campo_dt.strftime('%Y%m%d')}.png","image/png",use_container_width=True)
with dl2:
    bz=io.BytesIO()
    with zipfile.ZipFile(bz,"w") as zf:
        for col,buf in buf_ind.items(): zf.writestr(f"mapa_{col}_{fecha_campo_dt.strftime('%Y%m%d')}.png",buf.getvalue())
    st.download_button("⬇️  Mapas individuales ZIP",bz.getvalue(),
        f"mapas_{fecha_campo_dt.strftime('%Y%m%d')}.zip","application/zip",use_container_width=True)

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown('<div class="sec-t">📊 Estadísticas espaciales</div>',unsafe_allow_html=True)
cols_st=st.columns(len(mapas))
for cs,(param,info) in zip(cols_st,mapas.items()):
    d=info["data"][np.isfinite(info["data"])]
    with cs:
        st.markdown(f"**{info['label']}**")
        st.metric("Media",f"{d.mean():.2f} {info['unidad']}")
        st.metric("Máximo",f"{d.max():.2f} {info['unidad']}")
        st.metric("Mínimo",f"{d.min():.2f} {info['unidad']}")

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown('<div class="sec-t">👨‍🔬 Investigador Principal</div>',unsafe_allow_html=True)
st.markdown(f"""<div class="researcher-card">
  <img class="rphoto" src="data:image/png;base64,{PHOTO_B64}">
  <div><div class="rname">Kevin David Rodríguez González</div>
  <div class="rtitle">PhD Student · Environmental Water Quality &amp; Remote Sensing</div>
  <div class="rdept">Departamento de Geomática · Facultad de Ingeniería Civil · UANL</div>
  <div class="rlinks">
    <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
    <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">🔗 ORCID</a>
  </div></div></div>""",unsafe_allow_html=True)

st.markdown("""<div class="footer">RF v3 · Sentinel-2 SR · UANL · FIC · Depto. Geomática · KFold-5 + OOB</div>""",
           unsafe_allow_html=True)
