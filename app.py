import streamlit as st
import streamlit.components.v1 as components
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
import imageio.v2 as imageio
from datetime import date as date_cls
warnings.filterwarnings("ignore")
from i18n import t, IDIOMAS, get_param_label, get_param_desc, get_indice_nombre, get_indice_desc
from pdf_report_module import (generar_pdf_fecha_unica, generar_pdf_serie_temporal,
                               generar_pdf_reporte_espectral)

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

NOM_LIMITS = {
    "P_TOT":  {"lim": 5.0,  "ref": "NOM-001 Tabla 3"},
    "N_NH3":  {"lim": 25.0, "ref": "NOM-001 Tabla 3"},
    "N_TOT":  {"lim": 40.0, "ref": "Referencia"},
    "N_TOTK": {"lim": 40.0, "ref": "Referencia"},
}

COORDS = {
    "Punto_1": (-100.34495, 25.81193), "Punto_2": (-100.29269, 25.80148),
    "Punto_3": (-100.28059, 25.80205), "Punto_4": (-100.21237, 25.83095),
    "Punto_5": (-100.20026, 25.82832), "Punto_6": (-100.04244, 25.78160),
    "Punto_7": (-100.02404, 25.77480),
}

def zona_es_pesqueria(bbox, margen_factor=0.5):
    """
    Determina si un bbox (lon_min, lat_min, lon_max, lat_max) corresponde
    al área del Río Pesquería, verificando si al menos 3 de los 7 puntos
    de muestreo caen dentro (o cerca, con margen) del área subida.

    Esto permite habilitar los mapas de calidad de agua (que dependen del
    modelo RF entrenado solo con estos 7 puntos) únicamente cuando el
    usuario sube un wmask que realmente corresponde a esta zona — para
    cualquier otra área del mundo, solo se ofrecen RGB/índices/GIF/TIFF,
    que no dependen del modelo y sí funcionan en cualquier lugar.
    """
    lon_min, lat_min, lon_max, lat_max = bbox
    margen = max(lon_max - lon_min, lat_max - lat_min) * margen_factor
    n_dentro = 0
    for lon, lat in COORDS.values():
        if (lon_min - margen <= lon <= lon_max + margen and
            lat_min - margen <= lat <= lat_max + margen):
            n_dentro += 1
    return n_dentro >= 3

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

# ── Estado del idioma (debe inicializarse antes de cualquier texto) ──────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "es"
LANG = st.session_state["lang"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ══ TOKENS ══════════════════════════════════════════════════════════════ */
:root{
  --bg:#02060E;
  --t1:rgba(255,255,255,1); --t2:rgba(255,255,255,.7);
  --t3:rgba(255,255,255,.5); --t4:rgba(255,255,255,.35);
  --blue:#0EA5E9; --cyan:#22D3EE; --teal:#14B8A6;
  --ok:#10B981; --warn:#F59E0B; --err:#EF4444;
  --r:12px; --rl:20px;
  --f-sans:'Inter',system-ui,-apple-system,sans-serif;
  --f-mono:'JetBrains Mono',ui-monospace,monospace;
}

/* ── BASE ──────────────────────────────────────────────────────────────── */
html,body,.stApp,*:not(code):not(pre):not(.material-symbols-rounded):not(.material-symbols-outlined):not(.material-icons):not([data-testid="stIconMaterial"]){font-family:var(--f-sans)!important}
.material-symbols-rounded,.material-symbols-outlined,.material-icons,[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded','Material Symbols Outlined','Material Icons'!important}
code,pre,.stCode{font-family:var(--f-mono)!important}
body,.stApp{background:var(--bg)!important}

/* ── ANIMATED SATELLITE BACKGROUND ──────────────────────────────────────── */
.aurora-bg{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(ellipse 100% 80% at 50% 0%,#040C20 0%,#02060E 60%);
  overflow:hidden;
}
/* aurora color blobs */
.aurora-bg::before{
  content:'';position:absolute;inset:-35%;
  background:
    radial-gradient(ellipse 70% 55% at 18% 48%,rgba(14,165,233,.15) 0%,transparent 60%),
    radial-gradient(ellipse 60% 65% at 83% 18%,rgba(34,211,238,.1) 0%,transparent 55%),
    radial-gradient(ellipse 55% 50% at 52% 88%,rgba(20,184,166,.09) 0%,transparent 55%),
    radial-gradient(ellipse 35% 35% at 68% 60%,rgba(56,189,248,.07) 0%,transparent 50%);
  animation:auroraShift 24s ease-in-out infinite alternate;
}
/* coordinate grid + scan lines */
.aurora-bg::after{
  content:'';position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(34,211,238,.038) 1px,transparent 1px),
    linear-gradient(90deg,rgba(34,211,238,.038) 1px,transparent 1px),
    repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(14,165,233,.012) 3px,rgba(14,165,233,.012) 4px);
  background-size:55px 55px,55px 55px,100% 4px;
}

/* ── STARFIELD ───────────────────────────────────────────────────────────── */
.stars-layer{
  position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden;
}
.stars-layer::before{
  content:'';position:absolute;inset:0;
  background-image:
    radial-gradient(1px 1px at 8% 12%,rgba(255,255,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 23% 5%, rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 37% 19%,rgba(255,255,255,.8) 0%,transparent 100%),
    radial-gradient(1px 1px at 52% 8%, rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 68% 15%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 81% 3%, rgba(255,255,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 93% 22%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 14% 31%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(2px 2px at 29% 42%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 44% 35%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1px 1px at 57% 28%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 74% 38%,rgba(255,255,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 88% 44%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 6%  55%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(2px 2px at 19% 62%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 33% 58%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1px 1px at 48% 71%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 62% 65%,rgba(255,255,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 77% 52%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 91% 68%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 11% 78%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(2px 2px at 26% 85%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 41% 91%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 56% 82%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 71% 88%,rgba(255,255,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 85% 76%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 97% 83%,rgba(255,255,255,.4) 0%,transparent 100%),
    /* cyan-tinted stars */
    radial-gradient(1.5px 1.5px at 16% 46%,rgba(34,211,238,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 63% 14%,rgba(14,165,233,.4) 0%,transparent 100%),
    radial-gradient(2px 2px at 83% 59%,rgba(34,211,238,.35) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 40% 77%,rgba(20,184,166,.4) 0%,transparent 100%);
  animation:starsTwinkle 8s ease-in-out infinite alternate;
}
.stars-layer::after{
  content:'';position:absolute;inset:0;
  background-image:
    radial-gradient(1px 1px at 3%  17%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 18% 24%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 35% 9%, rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1px 1px at 49% 41%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 64% 33%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1px 1px at 79% 21%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1px 1px at 96% 14%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 7%  67%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 22% 73%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 39% 59%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(1px 1px at 54% 94%,rgba(255,255,255,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 69% 79%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 84% 86%,rgba(255,255,255,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 98% 95%,rgba(255,255,255,.6) 0%,transparent 100%);
  animation:starsTwinkle 12s ease-in-out infinite alternate-reverse;
}
@keyframes starsTwinkle{
  0%{opacity:.6} 50%{opacity:1} 100%{opacity:.7}
}

/* ── SATELLITE ────────────────────────────────────────────────────────────── */
.satellite{
  position:fixed;z-index:9999;pointer-events:none;
  width:58px;height:58px;
  animation:satellitePass 35s linear infinite;
  opacity:.75;
}
.satellite svg{width:100%;height:100%;filter:drop-shadow(0 0 8px rgba(34,211,238,.9)) drop-shadow(0 0 2px #fff);}
/* trail */
.satellite::after{
  content:'';position:absolute;top:50%;right:100%;
  width:40px;height:1px;margin-top:-.5px;
  background:linear-gradient(to left,rgba(34,211,238,.5),transparent);
}
@keyframes satellitePass{
  0%   {top:-5%;  left:-5%;  transform:rotate(35deg)}
  48%  {top:108%; left:108%; transform:rotate(35deg)}
  49%  {top:108%; left:108%; transform:rotate(215deg);opacity:0}
  50%  {top:-5%;  left:108%; transform:rotate(215deg);opacity:0}
  51%  {top:-5%;  left:108%; transform:rotate(215deg);opacity:.75}
  98%  {top:108%; left:-5%;  transform:rotate(215deg)}
  99%  {top:108%; left:-5%;  transform:rotate(35deg);opacity:0}
  100% {top:-5%;  left:-5%;  transform:rotate(35deg);opacity:0}
}

/* ── ANIMATIONS ──────────────────────────────────────────────────────────── */
@keyframes auroraShift{
  0%{transform:scale(1) translate(0,0);opacity:.8}
  25%{transform:scale(1.05) translate(2%,-2%)}
  50%{transform:scale(.97) translate(-2%,2%);opacity:1}
  75%{transform:scale(1.07) translate(1%,2%)}
  100%{transform:scale(1.01) translate(-1%,-1%);opacity:.82}
}
@keyframes scanSweep{
  0%{top:-2px;opacity:0} 5%{opacity:1} 92%{opacity:1} 100%{top:100%;opacity:0}
}
@keyframes bodyScan{
  0%{top:0;opacity:0} 3%{opacity:.8} 96%{opacity:.8} 100%{top:100vh;opacity:0}
}
@keyframes blink{
  0%,100%{opacity:1;box-shadow:0 0 8px var(--ok),0 0 16px rgba(16,185,129,.3)}
  50%{opacity:.2;box-shadow:none}
}
@keyframes fadeUp{
  from{opacity:0;transform:translateY(14px)}
  to{opacity:1;transform:translateY(0)}
}
@keyframes floatOrb{
  0%,100%{transform:translate(0,0) scale(1)}
  33%{transform:translate(20px,-16px) scale(1.05)}
  66%{transform:translate(-14px,12px) scale(.96)}
}
@keyframes glassShimmer{
  0%{background-position:-200% center}
  100%{background-position:200% center}
}
@keyframes pulseRing{
  0%{transform:scale(.95);opacity:1}
  100%{transform:scale(1.35);opacity:0}
}

/* ── LIQUID GLASS (light) ────────────────────────────────────────────────── */
.lqg{
  position:relative;overflow:hidden;
  background:rgba(255,255,255,.018);
  backdrop-filter:blur(4px);
  -webkit-backdrop-filter:blur(4px);
  box-shadow:inset 0 1px 1px rgba(255,255,255,.1);
}
.lqg::before{
  content:'';position:absolute;inset:0;
  padding:1.4px;
  background:linear-gradient(180deg,
    rgba(255,255,255,.45) 0%,rgba(255,255,255,.15) 20%,
    transparent 40%,transparent 60%,
    rgba(255,255,255,.15) 80%,rgba(255,255,255,.45) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;
  mask-composite:exclude;
  border-radius:inherit;
  pointer-events:none;
}

/* ── LIQUID GLASS (strong) ───────────────────────────────────────────────── */
.lqg-s{
  position:relative;overflow:hidden;
  background:rgba(255,255,255,.025);
  backdrop-filter:blur(50px);
  -webkit-backdrop-filter:blur(50px);
  box-shadow:4px 4px 4px rgba(0,0,0,.06),inset 0 1px 1px rgba(255,255,255,.15);
}
.lqg-s::before{
  content:'';position:absolute;inset:0;
  padding:1.4px;
  background:linear-gradient(180deg,
    rgba(255,255,255,.5) 0%,rgba(255,255,255,.2) 20%,
    transparent 40%,transparent 60%,
    rgba(255,255,255,.2) 80%,rgba(255,255,255,.5) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;
  mask-composite:exclude;
  border-radius:inherit;
  pointer-events:none;
}

/* ── SIDEBAR ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background:rgba(2,6,14,.97)!important;
  border-right:1px solid rgba(255,255,255,.06)!important;
  backdrop-filter:blur(20px)!important;
}

/* ── STREAMLIT NATIVE OVERRIDES ──────────────────────────────────────────── */
.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div{
  background:rgba(255,255,255,.018)!important;
  border:none!important;border-radius:var(--r)!important;
  backdrop-filter:blur(8px)!important;
  box-shadow:inset 0 1px 1px rgba(255,255,255,.08)!important;
}
.stTextInput>div>div>input,.stDateInput>div>div>input{
  background:rgba(255,255,255,.015)!important;
  border:1px solid rgba(255,255,255,.1)!important;
  color:rgba(255,255,255,.9)!important;border-radius:var(--r)!important;
  backdrop-filter:blur(8px)!important;
}
[data-testid="stFileUploader"]>div{
  background:rgba(255,255,255,.012)!important;
  border:1px dashed rgba(255,255,255,.14)!important;
  border-radius:var(--r)!important;backdrop-filter:blur(8px)!important;
}
.stSlider [role="slider"]{background:rgba(255,255,255,.9)!important}
[data-testid="stSliderTrackFill"]{background:rgba(255,255,255,.5)!important}
.stSlider [data-baseweb="slider"] [role="slider"]{background:rgba(255,255,255,.9)!important}
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrackFill"]{background:rgba(255,255,255,.4)!important}

/* Buttons — liquid glass with subtle white */
.stButton>button,.stDownloadButton>button{
  background:rgba(255,255,255,.1)!important;
  border:none!important;color:#fff!important;font-weight:600!important;
  font-size:.85rem!important;letter-spacing:.02em!important;
  border-radius:40px!important;padding:.55rem 1.4rem!important;
  transition:all .3s ease!important;
  backdrop-filter:blur(12px)!important;
  box-shadow:inset 0 1px 1px rgba(255,255,255,.15),0 2px 12px rgba(0,0,0,.2)!important;
  position:relative!important;overflow:hidden!important;
}
.stButton>button:hover,.stDownloadButton>button:hover{
  background:rgba(255,255,255,.18)!important;
  transform:scale(1.04) translateY(-1px)!important;
  box-shadow:inset 0 1px 1px rgba(255,255,255,.25),0 8px 28px rgba(14,165,233,.3)!important;
}
.stButton>button:disabled{
  background:rgba(255,255,255,.04)!important;color:rgba(255,255,255,.3)!important;
  box-shadow:none!important;transform:none!important;
}

/* ── HEADER HERO ──────────────────────────────────────────────────────────── */
.hdr{
  display:flex;align-items:stretch;gap:12px;
  margin-bottom:1.5rem;
  padding:8px 8px 8px 0;
  position:relative;overflow:hidden;
  animation:fadeUp .55s ease forwards;
  min-height:280px;
}
/* full-bg coordinate grid for whole header area */
.hdr::before{
  content:'';position:absolute;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(34,211,238,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(34,211,238,.04) 1px,transparent 1px);
  background-size:50px 50px;
}

/* LEFT PANEL */
.hdr-left{
  flex:0 0 58%;
  padding:1.6rem 1.8rem 1.4rem;
  display:flex;flex-direction:column;gap:0;
  border-radius:0 0 24px 24px;
  position:relative;z-index:1;
}
.hdr-left.lqg-s::before{border-radius:0 0 24px 24px}

/* floating orbs — only inside header */
.hdr-orb{position:absolute;border-radius:50%;pointer-events:none;filter:blur(48px)}
.hdr-orb-1{
  width:280px;height:280px;
  background:radial-gradient(circle,rgba(14,165,233,.2) 0%,transparent 70%);
  top:-100px;right:-30px;
  animation:floatOrb 12s ease-in-out infinite;
}
.hdr-orb-2{
  width:200px;height:200px;
  background:radial-gradient(circle,rgba(34,211,238,.14) 0%,transparent 70%);
  bottom:-60px;left:20%;
  animation:floatOrb 8s ease-in-out infinite reverse;
}
.hdr-orb-3{
  width:150px;height:150px;
  background:radial-gradient(circle,rgba(20,184,166,.11) 0%,transparent 70%);
  top:20px;left:5%;
  animation:floatOrb 15s ease-in-out infinite;
}
/* one-shot scan sweep */
.hdr-left::after{
  content:'';position:absolute;left:0;right:0;height:1.5px;top:0;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(34,211,238,.9) 40%,#fff 50%,rgba(34,211,238,.9) 60%,transparent);
  animation:scanSweep 2.4s ease-out .4s forwards;
  opacity:0;border-radius:0 0 0 0;
}

/* NAV ROW */
.hdr-logos{
  display:flex;align-items:center;gap:14px;margin-bottom:1.2rem;flex-wrap:wrap;
  position:relative;z-index:2;
}
.hdr-logo-img{height:46px;object-fit:contain;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))}
.hdr-sep{width:1px;height:38px;background:rgba(255,255,255,.12);flex-shrink:0}

/* LIVE badge in nav */
.hdr-live{
  display:inline-flex;align-items:center;gap:5px;margin-left:auto;
  background:rgba(255,255,255,.06);
  border-radius:40px;padding:4px 14px;
  font-family:var(--f-mono)!important;font-size:.6rem;
  color:rgba(255,255,255,.75);letter-spacing:.12em;
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.12);
}
.hdr-live::before{
  content:'';position:absolute;inset:0;padding:1px;
  background:linear-gradient(180deg,rgba(255,255,255,.35) 0%,rgba(255,255,255,.08) 50%,rgba(255,255,255,.35) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  border-radius:inherit;
}
.hdr-live-dot{
  width:6px;height:6px;background:var(--ok);border-radius:50%;
  animation:blink 2.2s ease infinite;flex-shrink:0;
}

/* HERO BODY */
.hdr-body{position:relative;z-index:2;flex:1;display:flex;flex-direction:column;justify-content:center}
.hdr-eyebrow{
  font-family:var(--f-mono)!important;font-size:.58rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;
  color:rgba(34,211,238,.65);margin-bottom:.7rem;
}

/* gradient title */
.app-title{
  font-size:2.4rem;font-weight:800;margin:0;letter-spacing:-.5px;line-height:1.1;
  font-family:var(--f-sans)!important;display:inline;
  background:linear-gradient(135deg,#fff 0%,rgba(255,255,255,.85) 40%,rgba(34,211,238,.9) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

.app-sub{
  font-size:.8rem;color:rgba(255,255,255,.55);margin:.55rem 0 0;
  font-family:var(--f-mono)!important;letter-spacing:.02em;
}

/* PILL TAGS */
.hdr-pills{display:flex;flex-wrap:wrap;gap:7px;margin-top:1rem;position:relative;z-index:2}
.hdr-pill{
  font-family:var(--f-mono)!important;font-size:.62rem;
  color:rgba(255,255,255,.75);
  background:rgba(255,255,255,.06);
  border-radius:40px;padding:4px 14px;
  transition:all .25s;cursor:default;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
  position:relative;overflow:hidden;
}
.hdr-pill::before{
  content:'';position:absolute;inset:0;padding:1px;
  background:linear-gradient(180deg,rgba(255,255,255,.3) 0%,rgba(255,255,255,.06) 50%,rgba(255,255,255,.3) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  border-radius:inherit;
}
.hdr-pill:hover{background:rgba(255,255,255,.12);transform:scale(1.04)}

/* META TAGS ROW */
.hdr-meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:.9rem;position:relative;z-index:2}
.hdr-tag{
  font-family:var(--f-mono)!important;font-size:.6rem;
  background:rgba(255,255,255,.04);
  color:rgba(255,255,255,.5);border-radius:5px;padding:3px 9px;letter-spacing:.05em;
  transition:background .2s;
}
.hdr-tag:hover{background:rgba(255,255,255,.09);color:rgba(255,255,255,.75)}
.hdr-tag b{color:rgba(34,211,238,.5);font-weight:500;margin-right:4px}

/* RIGHT PANEL */
.hdr-right{
  flex:0 0 42%;
  display:flex;flex-direction:column;gap:10px;
  padding:8px 0 8px 0;
  position:relative;z-index:1;
}
@media(max-width:768px){.hdr-right{display:none}}

/* feature cards grid */
.hdr-feat-grid{display:flex;gap:10px;flex:0 0 auto}
.hdr-feat-card{
  flex:1;
  background:rgba(255,255,255,.018);
  backdrop-filter:blur(4px);
  border-radius:20px;padding:1.1rem 1rem;
  display:flex;flex-direction:column;gap:8px;
  transition:all .25s;cursor:default;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
  position:relative;overflow:hidden;
}
.hdr-feat-card::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.45) 0%,rgba(255,255,255,.12) 25%,transparent 45%,transparent 55%,rgba(255,255,255,.12) 75%,rgba(255,255,255,.45) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  border-radius:inherit;
}
.hdr-feat-card:hover{background:rgba(255,255,255,.03);transform:scale(1.02)}
.hdr-feat-icon{
  width:36px;height:36px;border-radius:12px;
  background:rgba(255,255,255,.07);
  display:flex;align-items:center;justify-content:center;
  color:rgba(255,255,255,.7);
}
.hdr-feat-t{font-size:.78rem;font-weight:600;color:rgba(255,255,255,.85)}
.hdr-feat-s{font-family:var(--f-mono)!important;font-size:.58rem;color:rgba(255,255,255,.45);margin-top:2px}

/* bottom feature card (wide) */
.hdr-feat-bottom{
  flex:1;
  background:rgba(255,255,255,.025);
  backdrop-filter:blur(50px);
  border-radius:24px;padding:1.1rem 1.3rem;
  display:flex;gap:14px;align-items:center;
  transition:all .25s;
  box-shadow:4px 4px 4px rgba(0,0,0,.05),inset 0 1px rgba(255,255,255,.15);
  position:relative;overflow:hidden;
}
.hdr-feat-bottom::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.5) 0%,rgba(255,255,255,.18) 25%,transparent 45%,transparent 55%,rgba(255,255,255,.18) 75%,rgba(255,255,255,.5) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  border-radius:inherit;
}
.hdr-feat-thumb{
  width:56px;height:56px;border-radius:14px;
  background:linear-gradient(135deg,rgba(14,165,233,.3),rgba(34,211,238,.2));
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
  color:rgba(255,255,255,.8);font-size:1.4rem;
}
.hdr-feat-bt{font-size:.82rem;font-weight:600;color:rgba(255,255,255,.9);margin-bottom:3px}
.hdr-feat-bs{font-family:var(--f-mono)!important;font-size:.6rem;color:rgba(255,255,255,.45);line-height:1.6}
.hdr-feat-plus{
  margin-left:auto;width:32px;height:32px;border-radius:50%;
  background:rgba(255,255,255,.07);
  display:flex;align-items:center;justify-content:center;
  color:rgba(255,255,255,.6);font-size:1.1rem;flex-shrink:0;
  transition:all .2s;box-shadow:inset 0 1px rgba(255,255,255,.12);
}
.hdr-feat-plus:hover{background:rgba(255,255,255,.15);color:#fff}

/* ── LABELS ──────────────────────────────────────────────────────────────── */
.slabel{
  display:flex;align-items:center;gap:8px;
  font-family:var(--f-mono)!important;font-size:.6rem;
  color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.14em;font-weight:700;
  margin-bottom:.4rem;
}
.slabel::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.1),transparent)}
.sec-t{
  display:flex;align-items:center;gap:10px;
  font-family:var(--f-mono)!important;font-size:.63rem;
  color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.14em;font-weight:700;
  margin:1.3rem 0 .7rem;
}
.sec-t::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.08),transparent)}

/* ── METRIC CARDS ────────────────────────────────────────────────────────── */
.metric-row{display:flex;gap:10px;margin:1rem 0;flex-wrap:wrap}
.metric-card{
  flex:1;min-width:140px;
  background:rgba(255,255,255,.018);backdrop-filter:blur(12px);
  border-radius:var(--rl);padding:1.1rem 1.2rem;text-align:center;
  transition:all .25s;position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
}
.metric-card::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.4) 0%,rgba(255,255,255,.1) 25%,transparent 45%,transparent 55%,rgba(255,255,255,.1) 75%,rgba(255,255,255,.4) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.metric-card:hover{background:rgba(255,255,255,.032);transform:translateY(-2px);box-shadow:inset 0 1px rgba(255,255,255,.15),0 12px 32px rgba(0,0,0,.3)}
.metric-value{font-family:var(--f-mono)!important;font-size:2rem;font-weight:700;color:rgba(255,255,255,.92);line-height:1.1}
.metric-label{font-family:var(--f-mono)!important;font-size:.59rem;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.1em;margin-top:4px}
.badge-ok{
  display:inline-block;margin-top:8px;background:rgba(16,185,129,.08);
  color:rgba(16,185,129,.9);padding:2px 10px;border-radius:20px;
  font-size:.6rem;font-weight:600;font-family:var(--f-mono)!important;
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.08);
}

/* ── MAP PANELS ──────────────────────────────────────────────────────────── */
.map-panel{
  background:rgba(255,255,255,.018);backdrop-filter:blur(16px);
  border-radius:var(--rl);padding:.9rem 1.1rem;margin-bottom:1rem;
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
}
.map-panel::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.4) 0%,rgba(255,255,255,.08) 30%,transparent 50%,transparent 70%,rgba(255,255,255,.08) 85%,rgba(255,255,255,.4) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.map-title{
  font-family:var(--f-mono)!important;font-size:.62rem;font-weight:700;
  color:rgba(34,211,238,.8);letter-spacing:.14em;text-transform:uppercase;margin-bottom:.6rem;
}
.map-meta{font-size:.7rem;color:rgba(255,255,255,.5);margin-top:.5rem;line-height:1.65;font-family:var(--f-mono)!important}

/* ── CHIPS ───────────────────────────────────────────────────────────────── */
.chip{
  display:inline-block;background:rgba(255,255,255,.06);
  color:rgba(255,255,255,.7);font-size:.62rem;border-radius:40px;
  padding:3px 10px;margin:2px;font-family:var(--f-mono)!important;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
}
.chip-warn{background:rgba(245,158,11,.1);color:rgba(245,158,11,.9)}
.chip-bad{background:rgba(239,68,68,.08);color:rgba(239,68,68,.9)}

/* ── INFO PANELS ─────────────────────────────────────────────────────────── */
.info-panel{
  background:rgba(255,255,255,.016);backdrop-filter:blur(12px);
  border-radius:var(--rl);padding:.9rem 1.1rem;margin-bottom:1rem;
  position:relative;overflow:hidden;box-shadow:inset 0 1px rgba(255,255,255,.08);
}
.info-panel::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.35) 0%,rgba(255,255,255,.06) 30%,transparent 50%,transparent 70%,rgba(255,255,255,.06) 85%,rgba(255,255,255,.35) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.info-title{font-family:var(--f-mono)!important;font-size:.62rem;font-weight:700;color:rgba(255,255,255,.45);letter-spacing:.12em;text-transform:uppercase;margin-bottom:.6rem}

/* ── PARAM CARDS ─────────────────────────────────────────────────────────── */
.param-card{
  background:rgba(255,255,255,.016);backdrop-filter:blur(12px);
  border-radius:var(--rl);padding:1.1rem 1.4rem;margin-bottom:.7rem;
  transition:all .28s;position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.08);
}
.param-card::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.35) 0%,rgba(255,255,255,.06) 30%,transparent 50%,transparent 70%,rgba(255,255,255,.06) 85%,rgba(255,255,255,.35) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.param-card:hover{
  background:rgba(255,255,255,.028);transform:translateY(-1px);
  box-shadow:inset 0 1px rgba(255,255,255,.14),0 8px 28px rgba(0,0,0,.25);
}
.param-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;flex-wrap:wrap;gap:8px}
.param-name{font-size:.95rem;font-weight:700;color:rgba(255,255,255,.9)}
.param-oob{
  font-family:var(--f-mono)!important;font-size:.62rem;
  color:rgba(34,211,238,.8);background:rgba(34,211,238,.08);
  border-radius:40px;padding:2px 10px;
  box-shadow:inset 0 1px rgba(255,255,255,.08);
}
.param-desc{font-size:.77rem;color:rgba(255,255,255,.55);line-height:1.7;margin-bottom:.65rem}
.param-meta{display:flex;gap:20px;flex-wrap:wrap}
.pmi{font-size:.7rem;color:rgba(255,255,255,.45);font-family:var(--f-mono)!important}
.pmv{color:rgba(255,255,255,.8);font-weight:600}

/* ── STEP BOXES ──────────────────────────────────────────────────────────── */
.step-box{
  background:rgba(255,255,255,.018);backdrop-filter:blur(12px);
  border-radius:var(--rl);padding:1.3rem 1.4rem;
  position:relative;overflow:hidden;transition:all .3s;
  animation:fadeUp .5s ease forwards;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
}
.step-box::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.42) 0%,rgba(255,255,255,.12) 25%,transparent 45%,transparent 55%,rgba(255,255,255,.12) 75%,rgba(255,255,255,.42) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.step-box:hover{
  background:rgba(255,255,255,.03);transform:translateY(-3px);
  box-shadow:inset 0 1px rgba(255,255,255,.18),0 16px 40px rgba(0,0,0,.35);
}
.step-num{
  font-family:var(--f-mono)!important;font-size:.58rem;font-weight:700;
  color:rgba(34,211,238,.6);letter-spacing:.14em;text-transform:uppercase;
  margin-bottom:.6rem;
}
.step-t{font-size:.9rem;font-weight:700;color:rgba(255,255,255,.9);margin-bottom:.5rem}
.step-b{font-size:.76rem;color:rgba(255,255,255,.5);line-height:1.7}

/* ── RESEARCHER CARD ─────────────────────────────────────────────────────── */
.researcher-card{
  background:rgba(255,255,255,.02);backdrop-filter:blur(20px);
  border-radius:var(--rl);padding:1.3rem 1.7rem;
  display:flex;gap:20px;align-items:center;
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.12),4px 4px 4px rgba(0,0,0,.06);
}
.researcher-card::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.45) 0%,rgba(255,255,255,.12) 25%,transparent 45%,transparent 55%,rgba(255,255,255,.12) 75%,rgba(255,255,255,.45) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.rphoto{
  width:88px;height:88px;border-radius:50%;object-fit:cover;flex-shrink:0;
  box-shadow:0 0 0 2px rgba(255,255,255,.2),0 0 0 6px rgba(255,255,255,.04),0 0 24px rgba(14,165,233,.25);
}
.rname{font-size:1rem;font-weight:700;color:rgba(255,255,255,.92);margin:0 0 2px}
.rtitle{font-size:.8rem;color:rgba(34,211,238,.8);font-weight:600;margin:0 0 3px}
.rdept{font-size:.75rem;color:rgba(255,255,255,.5);margin:0 0 10px}
.rlinks{display:flex;gap:8px;flex-wrap:wrap}
.rlink{
  font-size:.67rem;color:rgba(255,255,255,.55);
  background:rgba(255,255,255,.04);border-radius:40px;
  padding:3px 12px;text-decoration:none;font-family:var(--f-mono)!important;
  transition:all .2s;box-shadow:inset 0 1px rgba(255,255,255,.08);
  position:relative;overflow:hidden;
}
.rlink::before{
  content:'';position:absolute;inset:0;padding:1px;
  background:linear-gradient(180deg,rgba(255,255,255,.28) 0%,rgba(255,255,255,.05) 50%,rgba(255,255,255,.28) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.rlink:hover{background:rgba(255,255,255,.1);color:rgba(255,255,255,.9)}

/* ── MISC ────────────────────────────────────────────────────────────────── */
.divider{border:0;border-top:1px solid rgba(255,255,255,.06);margin:1.2rem 0}
.footer{text-align:center;font-family:var(--f-mono)!important;font-size:.62rem;color:rgba(255,255,255,.22);margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.05)}

/* ── STATUS ROW ──────────────────────────────────────────────────────────── */
.status-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  margin-bottom:1.2rem;
  padding:.7rem 1.1rem;
  border-radius:12px;
  background:rgba(255,255,255,.016);
  border:1px solid rgba(255,255,255,.06);
  backdrop-filter:blur(12px);
}
.status-item{
  display:flex;align-items:center;gap:6px;
  font-family:var(--f-mono)!important;font-size:.62rem;color:rgba(255,255,255,.55);
}
.status-item b{color:rgba(255,255,255,.85);font-weight:600}
.status-dot-ok{width:6px;height:6px;background:var(--ok);border-radius:50%;animation:blink 2.2s ease infinite;flex-shrink:0;box-shadow:0 0 6px var(--ok)}
.status-dot-warn{width:6px;height:6px;background:var(--warn);border-radius:50%;flex-shrink:0;box-shadow:0 0 6px var(--warn)}
.status-sep{width:1px;height:14px;background:rgba(255,255,255,.08);flex-shrink:0}
.status-badge{
  margin-left:auto;font-family:var(--f-mono)!important;font-size:.58rem;
  color:rgba(34,211,238,.8);background:rgba(34,211,238,.06);
  border:1px solid rgba(34,211,238,.12);border-radius:20px;padding:2px 10px;
}

/* ── STAT METRIC CARDS ───────────────────────────────────────────────────── */
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:1rem 0}
.stat-card{
  background:rgba(255,255,255,.018);backdrop-filter:blur(12px);
  border-radius:14px;padding:1.2rem 1.4rem;
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px rgba(255,255,255,.1);
  transition:all .25s;
}
.stat-card::before{
  content:'';position:absolute;inset:0;padding:1.4px;
  background:linear-gradient(180deg,rgba(255,255,255,.38) 0%,rgba(255,255,255,.08) 30%,transparent 50%,transparent 70%,rgba(255,255,255,.08) 85%,rgba(255,255,255,.38) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.stat-card:hover{background:rgba(255,255,255,.03);transform:translateY(-2px);box-shadow:inset 0 1px rgba(255,255,255,.18),0 12px 32px rgba(0,0,0,.3)}
.stat-card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.8rem}
.stat-card-label{font-size:.82rem;font-weight:700;color:rgba(255,255,255,.9)}
.stat-card-unit{font-family:var(--f-mono)!important;font-size:.6rem;color:rgba(255,255,255,.4);background:rgba(255,255,255,.05);border-radius:20px;padding:2px 8px}
.stat-row{display:flex;gap:18px;margin-top:.4rem}
.stat-item{display:flex;flex-direction:column;gap:3px}
.stat-val{font-family:var(--f-mono)!important;font-size:1.3rem;font-weight:700;line-height:1}
.stat-name{font-family:var(--f-mono)!important;font-size:.58rem;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.08em}
.stat-glow{position:absolute;bottom:-20px;left:20px;width:100px;height:50px;border-radius:50%;filter:blur(24px);opacity:.25;pointer-events:none}

/* ── DOWNLOAD ROW ────────────────────────────────────────────────────────── */
.dl-row{display:flex;gap:8px;margin:1rem 0;flex-wrap:wrap}
.dl-label{
  font-family:var(--f-mono)!important;font-size:.6rem;color:rgba(34,211,238,.7);
  letter-spacing:.12em;text-transform:uppercase;
  display:flex;align-items:center;gap:6px;margin-bottom:.5rem;
}
.dl-label::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(34,211,238,.15),transparent)}

/* ── STREAMLIT DEEP OVERRIDES ────────────────────────────────────────────── */
/* Selectbox + multiselect */
[data-testid="stSelectbox"] label,[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label,[data-testid="stDateInput"] label,
[data-testid="stFileUploader"] label,[data-testid="stNumberInput"] label{
  font-family:var(--f-mono)!important;font-size:.6rem!important;
  color:rgba(255,255,255,.38)!important;text-transform:uppercase!important;
  letter-spacing:.12em!important;font-weight:600!important;margin-bottom:4px!important;
}
/* Selectbox dropdown container */
[data-baseweb="select"] [data-baseweb="popover"] ul{
  background:rgba(4,10,22,.98)!important;
  border:1px solid rgba(255,255,255,.08)!important;
  border-radius:10px!important;
  backdrop-filter:blur(20px)!important;
}
[data-baseweb="select"] [data-baseweb="popover"] li{
  font-size:.78rem!important;color:rgba(255,255,255,.7)!important;
  padding:6px 12px!important;transition:background .15s!important;
}
[data-baseweb="select"] [data-baseweb="popover"] li:hover{
  background:rgba(14,165,233,.1)!important;color:#fff!important;
}
/* Selectbox selected value text */
[data-baseweb="select"] [data-baseweb="tag"],[data-baseweb="select"] span{
  color:rgba(255,255,255,.8)!important;font-size:.78rem!important;
}
/* Date inputs */
[data-testid="stDateInput"] input{
  background:rgba(255,255,255,.03)!important;
  border:1px solid rgba(255,255,255,.08)!important;
  color:rgba(255,255,255,.85)!important;
  font-family:var(--f-mono)!important;font-size:.72rem!important;
  border-radius:8px!important;padding:5px 10px!important;
}
[data-testid="stDateInput"] input:focus{
  border-color:rgba(14,165,233,.4)!important;
  box-shadow:0 0 0 2px rgba(14,165,233,.1)!important;
  outline:none!important;
}
/* Slider track */
[data-testid="stSlider"] [data-baseweb="slider"]{
  padding:0 4px!important;
}
[data-testid="stSlider"] div[data-baseweb="slider"]>div>div{
  background:rgba(255,255,255,.08)!important;height:3px!important;
}
[data-testid="stSliderTrackFill"]{
  background:linear-gradient(90deg,rgba(14,165,233,.6),rgba(34,211,238,.8))!important;
  height:3px!important;
}
[data-testid="stSlider"] [role="slider"]{
  background:#fff!important;width:14px!important;height:14px!important;
  box-shadow:0 0 0 3px rgba(14,165,233,.3),0 2px 8px rgba(0,0,0,.4)!important;
  border:none!important;top:-6px!important;
}
/* File uploader */
[data-testid="stFileUploader"]>section{
  background:rgba(255,255,255,.01)!important;
  border:1px dashed rgba(255,255,255,.1)!important;
  border-radius:10px!important;padding:12px!important;
  transition:all .2s!important;
}
[data-testid="stFileUploader"]>section:hover{
  border-color:rgba(14,165,233,.3)!important;
  background:rgba(14,165,233,.02)!important;
}
[data-testid="stFileUploader"] p,[data-testid="stFileUploader"] small{
  color:rgba(255,255,255,.45)!important;font-size:.72rem!important;
}
/* Captions */
[data-testid="stCaptionContainer"] p{
  color:rgba(255,255,255,.38)!important;font-size:.68rem!important;
  font-family:var(--f-mono)!important;letter-spacing:.02em!important;
}
/* Alert / info / success / warning boxes */
[data-testid="stAlert"]{
  border-radius:10px!important;border-width:1px!important;
  backdrop-filter:blur(8px)!important;
}
[data-testid="stAlert"][data-baseweb="notification"]{font-size:.78rem!important}
/* Progress bar */
[data-testid="stProgressBar"]>div>div{
  background:linear-gradient(90deg,rgba(14,165,233,.8),rgba(34,211,238,1))!important;
  border-radius:4px!important;
}
[data-testid="stProgressBar"]>div{
  background:rgba(255,255,255,.06)!important;border-radius:4px!important;height:4px!important;
}
/* Multiselect tags */
[data-baseweb="tag"]{
  background:rgba(14,165,233,.12)!important;
  border:1px solid rgba(14,165,233,.2)!important;
  border-radius:20px!important;
}
[data-baseweb="tag"] span{color:rgba(14,165,233,.9)!important;font-size:.68rem!important}
/* Columns gap */
[data-testid="column"]{padding:0 6px!important}
/* Dividers inside sidebar */
[data-testid="stSidebar"] hr{
  border-color:rgba(255,255,255,.05)!important;margin:.6rem 0!important;
}
/* Sidebar collapse button */
[data-testid="stSidebarCollapsedControl"] button,
button[kind="header"]{
  background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(255,255,255,.06)!important;
  border-radius:8px!important;
}
/* Main content padding */
[data-testid="stMainBlockContainer"]{
  padding-top:1rem!important;padding-bottom:2rem!important;
}
/* Image captions */
[data-testid="stImageCaption"]{
  font-family:var(--f-mono)!important;font-size:.62rem!important;
  color:rgba(255,255,255,.3)!important;text-align:center!important;
}
/* Select slider */
[data-testid="stSelectSlider"] [role="slider"]{
  background:#fff!important;
  box-shadow:0 0 0 3px rgba(14,165,233,.3)!important;
}

/* ── EMPTY STATE ─────────────────────────────────────────────────────────── */
.empty-state{
  display:flex;flex-direction:column;align-items:center;
  padding:3rem 2rem;text-align:center;
  border-radius:20px;margin:1rem 0;
  background:rgba(255,255,255,.012);
  border:1px dashed rgba(255,255,255,.08);
  position:relative;overflow:hidden;
}
.empty-state::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 50% at 50% 0%,rgba(14,165,233,.06),transparent);
  pointer-events:none;
}
.empty-icon{
  font-size:3.2rem;margin-bottom:1.2rem;
  filter:drop-shadow(0 0 24px rgba(14,165,233,.3));
}
.empty-title{
  font-size:1.1rem;font-weight:700;color:rgba(255,255,255,.85);
  margin-bottom:.5rem;letter-spacing:-.3px;
}
.empty-sub{
  font-size:.8rem;color:rgba(255,255,255,.45);line-height:1.7;
  max-width:520px;margin-bottom:1.5rem;
}
.empty-steps{
  display:flex;gap:12px;flex-wrap:wrap;justify-content:center;
  margin-bottom:1.5rem;
}
.empty-step{
  display:flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);
  border-radius:10px;padding:8px 14px;font-size:.75rem;color:rgba(255,255,255,.6);
}
.empty-step-num{
  width:20px;height:20px;border-radius:50%;
  background:rgba(14,165,233,.12);border:1px solid rgba(14,165,233,.2);
  font-family:var(--f-mono)!important;font-size:.6rem;font-weight:700;
  color:rgba(14,165,233,.8);display:flex;align-items:center;justify-content:center;
  flex-shrink:0;
}
.empty-coords{
  font-family:var(--f-mono)!important;font-size:.62rem;
  color:rgba(255,255,255,.25);margin-top:1rem;letter-spacing:.1em;
}

/* ── NOM-001 ALERT TABLE ─────────────────────────────────────────────────── */
.nom-wrap{
  border-radius:16px;overflow:hidden;margin:1rem 0;
  background:rgba(255,255,255,.015);
  border:1px solid rgba(255,255,255,.07);
}
.nom-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:.75rem 1.2rem;
  border-bottom:1px solid rgba(255,255,255,.06);
  background:rgba(255,255,255,.02);
}
.nom-title{
  font-family:var(--f-mono)!important;font-size:.62rem;font-weight:700;
  color:rgba(255,255,255,.5);letter-spacing:.14em;text-transform:uppercase;
}
.nom-legend{display:flex;gap:12px;align-items:center}
.nom-leg-item{display:flex;align-items:center;gap:5px;font-family:var(--f-mono)!important;font-size:.58rem;color:rgba(255,255,255,.4)}
.nom-leg-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
table.nom-table{width:100%;border-collapse:collapse;font-size:.72rem}
table.nom-table th{
  font-family:var(--f-mono)!important;font-size:.58rem;font-weight:700;
  color:rgba(255,255,255,.35);letter-spacing:.1em;text-transform:uppercase;
  padding:8px 14px;text-align:left;background:rgba(255,255,255,.01);
  border-bottom:1px solid rgba(255,255,255,.05);
}
table.nom-table td{
  padding:7px 14px;border-bottom:1px solid rgba(255,255,255,.04);
  color:rgba(255,255,255,.75);vertical-align:middle;
}
table.nom-table tr:last-child td{border-bottom:none}
table.nom-table tr:hover td{background:rgba(255,255,255,.02)}
.nom-point{font-family:var(--f-mono)!important;font-size:.7rem;color:rgba(34,211,238,.8);font-weight:600}
.nom-val{font-family:var(--f-mono)!important;font-weight:700}
.nom-val-ok{color:rgba(16,185,129,.9)}
.nom-val-warn{color:rgba(245,158,11,.9)}
.nom-val-err{color:rgba(239,68,68,.9)}
.nom-badge{
  display:inline-flex;align-items:center;gap:4px;
  font-family:var(--f-mono)!important;font-size:.6rem;font-weight:600;
  border-radius:20px;padding:2px 9px;
}
.nom-badge-ok{background:rgba(16,185,129,.08);color:rgba(16,185,129,.9);border:1px solid rgba(16,185,129,.15)}
.nom-badge-warn{background:rgba(245,158,11,.08);color:rgba(245,158,11,.9);border:1px solid rgba(245,158,11,.15)}
.nom-badge-err{background:rgba(239,68,68,.08);color:rgba(239,68,68,.9);border:1px solid rgba(239,68,68,.15)}

/* ── DATA TABLE ──────────────────────────────────────────────────────────── */
.data-table-wrap{
  border-radius:16px;overflow:hidden;margin:1rem 0;
  background:rgba(255,255,255,.012);
  border:1px solid rgba(255,255,255,.07);
}
.data-table-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:.7rem 1.2rem;border-bottom:1px solid rgba(255,255,255,.06);
  background:rgba(255,255,255,.02);
}
table.data-tbl{width:100%;border-collapse:collapse;font-size:.71rem}
table.data-tbl th{
  font-family:var(--f-mono)!important;font-size:.57rem;font-weight:700;
  color:rgba(255,255,255,.35);letter-spacing:.08em;text-transform:uppercase;
  padding:7px 12px;background:rgba(255,255,255,.01);
  border-bottom:1px solid rgba(255,255,255,.05);white-space:nowrap;
  position:sticky;top:0;
}
table.data-tbl td{
  padding:5px 12px;border-bottom:1px solid rgba(255,255,255,.03);
  color:rgba(255,255,255,.7);font-family:var(--f-mono)!important;white-space:nowrap;
}
table.data-tbl tr:last-child td{border-bottom:none}
table.data-tbl tr:hover td{background:rgba(255,255,255,.025);color:rgba(255,255,255,.9)}
table.data-tbl td.fecha-col{color:rgba(34,211,238,.7);font-weight:600}
table.data-tbl td.punto-col{color:rgba(255,255,255,.45)}
.data-tbl-scroll{max-height:320px;overflow-y:auto}
.data-tbl-scroll::-webkit-scrollbar{width:3px}
.data-tbl-scroll::-webkit-scrollbar-track{background:transparent}
.data-tbl-scroll::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px}

/* ── FOLIUM / LEAFLET ────────────────────────────────────────────────────── */
.leaflet-control-layers{
  font-family:var(--f-mono)!important;font-size:11px!important;
  background:rgba(2,6,14,.92)!important;
  border-radius:var(--r)!important;box-shadow:0 4px 20px rgba(0,0,0,.7)!important;
  backdrop-filter:blur(20px)!important;
  position:relative;overflow:hidden;
}
.leaflet-control-layers::before{
  content:'';position:absolute;inset:0;padding:1px;
  background:linear-gradient(180deg,rgba(255,255,255,.3) 0%,rgba(255,255,255,.06) 50%,rgba(255,255,255,.3) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;border-radius:inherit;
}
.leaflet-control-layers-list{padding:6px 8px!important}
.leaflet-control-layers label{color:rgba(255,255,255,.7)!important;font-size:11px!important;line-height:1.7!important;font-weight:500!important}
.leaflet-control-layers-separator{border-color:rgba(255,255,255,.08)!important;margin:4px 0!important}
.leaflet-control-layers-base label,.leaflet-control-layers-overlays label{display:flex!important;align-items:center!important;gap:5px!important}
.leaflet-control-layers-toggle{background:rgba(2,6,14,.92)!important;border-radius:var(--r)!important}

/* ── RADIO LABEL SIZE ── */
[data-testid="stRadio"] label p{font-size:.72rem!important;line-height:1.3!important}
[data-testid="stRadio"] label{gap:5px!important;padding:1px 0!important}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stars-layer"></div>
<div class="satellite" aria-hidden="true">
  <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- body -->
    <rect x="10" y="10" width="8" height="8" rx="1.5" fill="#0EA5E9" fill-opacity=".9"/>
    <!-- solar panels left -->
    <rect x="1" y="12" width="7" height="4" rx=".8" fill="#22D3EE" fill-opacity=".7"/>
    <line x1="8" y1="14" x2="10" y2="14" stroke="#22D3EE" stroke-width=".8" stroke-opacity=".6"/>
    <!-- solar panels right -->
    <rect x="20" y="12" width="7" height="4" rx=".8" fill="#22D3EE" fill-opacity=".7"/>
    <line x1="18" y1="14" x2="20" y2="14" stroke="#22D3EE" stroke-width=".8" stroke-opacity=".6"/>
    <!-- antenna -->
    <line x1="14" y1="10" x2="14" y2="6" stroke="#14B8A6" stroke-width=".8"/>
    <circle cx="14" cy="5.5" r="1.5" fill="#14B8A6" fill-opacity=".8"/>
    <!-- glow center -->
    <circle cx="14" cy="14" r="2" fill="white" fill-opacity=".15"/>
  </svg>
</div>
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
@st.cache_resource(show_spinner="Cargando modelo...")
def load_model():
    p = os.path.join(os.path.dirname(__file__), "modelos_rf_v3.pkl")
    if not os.path.exists(p):
        st.session_state["_model_load_error"] = f"Archivo no encontrado en: {p}"
        return None
    try:
        with open(p, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.session_state["_model_load_error"] = f"Error al cargar pickle: {type(e).__name__}: {e}"
        return None

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
        nombre="📷 RGB (Color natural)",
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
    "LST": dict(
        nombre="🌡️ LST (Temperatura Superficial)",
        desc="Temperatura superficial en °C desde Landsat 8/9 Collection 2 (ST_B10), "
             "con downscaling a 10 m vía TsHARP usando NDVI Sentinel-2.",
        vis={"min": 15, "max": 45,
             "palette": ["#313695","#4575b4","#abd9e9","#ffffbf","#fdae61","#d73027","#a50026"]},
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
def obtener_datos_reporte_espectral(bbox, fecha_ini_str, fecha_fin_str, max_nubes,
                                    geojson_poligono=None):
    """
    Construye el paquete de datos necesario para el reporte PDF de índices
    espectrales: estadísticas zonales reales (vía reduceRegion) y thumbnails
    de cada capa (RGB + 4 índices), válido para cualquier zona del mundo.

    geojson_poligono: dict __geo_interface__ del wmask (forma exacta, no el
        bbox rectangular). Si se provee, las imágenes y estadísticas se
        recortan a la silueta real del polígono subido por el usuario en
        lugar de a su rectángulo envolvente.

    Retorna: (info_dict, stats_por_indice, thumbnails_por_capa) o
             (None, {}, {}) si no hay imagen disponible.
    """
    if not GEE_OK:
        return None, {}, {}
    try:
        import requests as _requests
        lon_min, lat_min, lon_max, lat_max = bbox

        if geojson_poligono is not None:
            # Geometría exacta del polígono (recorta con la silueta real)
            geom = ee.Geometry(geojson_poligono, opt_geodesic=False)
        else:
            geom = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

        coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(geom)
                  .filterDate(fecha_ini_str, fecha_fin_str)
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                  .sort("CLOUDY_PIXEL_PERCENTAGE"))

        n_imgs = coll.size().getInfo()
        if n_imgs == 0:
            return {"n_imagenes": 0}, {}, {}

        img_ref = coll.first()
        props   = img_ref.getInfo().get("properties", {})
        fecha_real = props.get("PRODUCT_ID", "")[7:15] if "PRODUCT_ID" in props else "N/D"
        nubes_pct  = props.get("CLOUDY_PIXEL_PERCENTAGE", None)

        # Mosaico para cubrir el bbox completo (ver buscar_imagen_s2)
        img = coll.sort("CLOUDY_PIXEL_PERCENTAGE", False).mosaic().clip(geom)

        # Área real del bbox en km² (geodésica, no aproximada)
        area_km2 = geom.area(maxError=10).divide(1_000_000).getInfo()

        stats = {}
        thumbnails = {}

        # RGB: solo thumbnail, sin estadística de índice
        thumb_rgb_url = img.getThumbURL({
            **INDICES_VIZ["RGB"]["vis"], "dimensions": 500,
            "format": "png", "region": geom,
        })
        r = _requests.get(thumb_rgb_url, timeout=20)
        if r.status_code == 200:
            thumbnails["RGB"] = io.BytesIO(r.content)

        for idx_name in ["NDVI", "NDWI", "MNDWI", "NDTI"]:
            idx_img = calcular_indice_gee(img, idx_name)
            if idx_img is None:
                continue

            # Estadísticas zonales reales sobre el área del bbox completo
            reducer = (ee.Reducer.mean()
                      .combine(ee.Reducer.stdDev(), sharedInputs=True)
                      .combine(ee.Reducer.minMax(), sharedInputs=True)
                      .combine(ee.Reducer.percentile([10, 50, 90]), sharedInputs=True))
            stat_result = idx_img.reduceRegion(
                reducer=reducer, geometry=geom, scale=20,
                maxPixels=1e9, bestEffort=True
            ).getInfo()

            stats[idx_name] = {
                "mean":   stat_result.get(f"{idx_name}_mean"),
                "std":    stat_result.get(f"{idx_name}_stdDev"),
                "min":    stat_result.get(f"{idx_name}_min"),
                "max":    stat_result.get(f"{idx_name}_max"),
                "p10":    stat_result.get(f"{idx_name}_p10"),
                "p50":    stat_result.get(f"{idx_name}_p50"),
                "p90":    stat_result.get(f"{idx_name}_p90"),
            }

            cfg = INDICES_VIZ[idx_name]
            thumb_url = idx_img.getThumbURL({
                **cfg["vis"], "dimensions": 500, "format": "png", "region": geom,
            })
            r2 = _requests.get(thumb_url, timeout=20)
            if r2.status_code == 200:
                thumbnails[idx_name] = io.BytesIO(r2.content)

        info = {
            "n_imagenes": n_imgs,
            "nubes_pct": round(nubes_pct, 1) if nubes_pct is not None else None,
            "fecha_real": fecha_real,
            "area_km2": round(area_km2, 2),
        }
        return info, stats, thumbnails

    except Exception as e:
        return {"error": str(e)}, {}, {}


@st.cache_data(ttl=1800, show_spinner=False)
def buscar_imagen_s2(bbox, fecha_ini_str, fecha_fin_str, max_nubes,
                     geojson_poligono=None):
    """
    Busca y compone una imagen Sentinel-2 que cubra TODO el bbox solicitado.

    Una sola escena Sentinel-2 (.first()) puede no cubrir áreas grandes o
    que caen en el borde entre dos pasadas del satélite — eso deja zonas
    del bbox transparentes ("clip" sin datos). Por eso aquí se construye
    un MOSAICO (.mosaic()) combinando todas las escenas disponibles en el
    rango de fechas/nubes, asegurando cobertura completa del área subida,
    sea un río angosto o un municipio entero.

    geojson_poligono: dict __geo_interface__ del wmask. Si se provee, el
        clip final se hace con la silueta EXACTA del polígono (no su bbox
        rectangular), de modo que el tile mostrado en el mapa solo pinta
        dentro de la forma real que subió el usuario.
    """
    if not GEE_OK:
        return None, {}
    try:
        lon_min, lat_min, lon_max, lat_max = bbox
        geom_busqueda = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])
        # La búsqueda de escenas (filterBounds) siempre usa el bbox —
        # es más eficiente y no afecta qué imágenes se encuentran.
        # El recorte visual final sí usa la geometría exacta si está disponible.
        geom = (ee.Geometry(geojson_poligono, opt_geodesic=False)
               if geojson_poligono is not None else geom_busqueda)
        coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(geom)
                  .filterDate(fecha_ini_str, fecha_fin_str)
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                  .sort("CLOUDY_PIXEL_PERCENTAGE"))
        n_imgs = coll.size().getInfo()
        if n_imgs == 0:
            return {"n_imagenes": 0}, {}

        # Metadatos de referencia desde la imagen con menos nubes
        img_ref   = coll.first()
        props     = img_ref.getInfo().get("properties", {})
        fecha_real = props.get("PRODUCT_ID", "")[7:15] if "PRODUCT_ID" in props else "N/D"
        nubes_pct  = props.get("CLOUDY_PIXEL_PERCENTAGE", None)

        # Mosaico: combina todas las escenas del rango para cubrir el bbox
        # completo sin huecos, priorizando las de menor nubosidad (ya
        # vienen ordenadas por .sort() y mosaic() usa la última imagen
        # válida por píxel, así que invertimos el orden para que la mejor
        # quede "encima").
        coll_para_mosaico = coll.sort("CLOUDY_PIXEL_PERCENTAGE", False)
        img = coll_para_mosaico.mosaic().clip(geom)

        tile_urls = {}
        map_id_rgb = img.getMapId(INDICES_VIZ["RGB"]["vis"])
        tile_urls["RGB"] = map_id_rgb["tile_fetcher"].url_format

        for idx_name in ["NDVI", "NDWI", "MNDWI", "NDTI"]:
            idx_img = calcular_indice_gee(img, idx_name)
            if idx_img is not None:
                map_id  = idx_img.getMapId(INDICES_VIZ[idx_name]["vis"])
                tile_urls[idx_name] = map_id["tile_fetcher"].url_format

        # ── LST desde Landsat 8/9 Collection 2 con downscaling via NDVI S2 ──
        def _lst_to_celsius(image):
            return (image.select("ST_B10")
                    .multiply(0.00341802).add(149.0).subtract(273.15)
                    .rename("LST"))

        lst_merged = (
            ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
              .filterBounds(geom).filterDate(fecha_ini_str, fecha_fin_str)
              .filter(ee.Filter.lt("CLOUD_COVER", max_nubes))
            .merge(
            ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
              .filterBounds(geom).filterDate(fecha_ini_str, fecha_fin_str)
              .filter(ee.Filter.lt("CLOUD_COVER", max_nubes))
            )
        )
        if lst_merged.size().getInfo() > 0:
            lst_30m  = lst_merged.map(_lst_to_celsius).median().clip(geom)
            vis_lst  = INDICES_VIZ["LST"]["vis"]
            # Intenta TsHARP 10m; si falla usa 30m nativo
            try:
                ndvi_10m = img.normalizedDifference(["B8","B4"])
                proj_30m = ee.Projection("EPSG:4326").atScale(30)
                ndvi_30m = (ndvi_10m
                            .reduceResolution(ee.Reducer.mean(), maxPixels=1024)
                            .reproject(proj_30m))
                safe_30m = ndvi_30m.where(ndvi_30m.abs().lt(0.01), 0.01)
                lst_10m  = (lst_30m
                            .multiply(ndvi_10m.divide(safe_30m))
                            .reproject(ee.Projection("EPSG:4326").atScale(10)))
                tile_urls["LST"] = lst_10m.getMapId(vis_lst)["tile_fetcher"].url_format
            except Exception:
                # Fallback: LST a resolución nativa Landsat 30m
                tile_urls["LST"] = lst_30m.getMapId(vis_lst)["tile_fetcher"].url_format

        info = {"n_imagenes": n_imgs,
                "nubes_pct": round(nubes_pct, 1) if nubes_pct is not None else None,
                "fecha_real": fecha_real}
        return info, tile_urls
    except Exception as e:
        return {"error": str(e)}, {}


def generar_gif_animacion(param_key, fechas_lista, wmask_gdf, bounds, resolucion_gif=120):
    """
    Genera un GIF animado mostrando la evolución espacial de un parámetro
    fisicoquímico o índice espectral a lo largo de las fechas seleccionadas.

    param_key: clave del parámetro (ej. 'P_TOT') o índice ('NDVI', etc.)
    fechas_lista: lista de fechas en formato 'M/D/YYYY' (de FECHAS_CAMPO)
    Retorna: (BytesIO del GIF, n_frames_generados) o (None, 0) si falla
    """
    es_param_fisico = param_key in PARAMS
    es_indice = param_key in INDICES_VIZ and param_key != "RGB"

    if not es_param_fisico and not es_indice:
        return None, 0

    lon_min, lat_min, lon_max, lat_max = bounds
    RES_G = resolucion_gif
    lon_vec_g = np.linspace(lon_min, lon_max, RES_G)
    lat_vec_g = np.linspace(lat_min, lat_max, RES_G)
    lon_grid_g, lat_grid_g = np.meshgrid(lon_vec_g, lat_vec_g)
    pts_grid_g = np.column_stack([lon_grid_g.ravel(), lat_grid_g.ravel()])
    extent_g = [lon_min, lon_max, lat_min, lat_max]

    union_geom_g = wmask_gdf.geometry.unary_union
    mask_flat_g = np.array([union_geom_g.contains(Point(x,y)) for x,y in pts_grid_g])
    mask_2d_g = mask_flat_g.reshape(RES_G, RES_G)

    puntos_uniq_g = sorted(COORDS.keys())
    lons_g = np.array([COORDS[p][0] for p in puntos_uniq_g])
    lats_g = np.array([COORDS[p][1] for p in puntos_uniq_g])
    pts_known_g = np.column_stack([lons_g, lats_g])

    frames = []
    fechas_validas = []

    # Determinar config visual (paleta, rango, label, unidad)
    if es_param_fisico:
        cfg = PARAMS[param_key]
        vmin_g, vmax_g = cfg["vmin"], cfg["vmax"]
        pal_g = cfg["pal"]
        label_g = cfg["label"]
        unidad_g = cfg["unidad"]
    else:
        cfg = INDICES_VIZ[param_key]
        vmin_g, vmax_g = cfg["vis"]["min"], cfg["vis"]["max"]
        pal_g = cfg["vis"]["palette"]
        label_g = cfg["nombre"]
        unidad_g = ""

    cmap_g = make_cmap(pal_g)

    for fecha_str in fechas_lista:
        fecha_dt_g = pd.to_datetime(fecha_str, format="%m/%d/%Y")
        df_fecha_g = df_global[df_global["target_date"] == fecha_dt_g]
        if len(df_fecha_g) == 0:
            continue

        if es_param_fisico:
            if param_key not in model_data["models"]:
                continue
            vals_g = []
            for p in puntos_uniq_g:
                fila_g = df_fecha_g[df_fecha_g["nombre"]==p]
                vals_g.append(float(fila_g[param_key].values[0]) if len(fila_g)>0 else np.nan)
            vals_g = np.array(vals_g)
        else:
            # Para indices espectrales: usar valores espectrales de banda si estan en CSV
            # Como fallback, usar distribución simulada según orden temporal (no ideal)
            # Mejor: omitir indices espectrales del GIF si no hay banda cruda por fecha
            continue

        ok_g = np.isfinite(vals_g)
        if ok_g.sum() < 3:
            continue

        try:
            rbf_g = RBFInterpolator(pts_known_g[ok_g], vals_g[ok_g],
                                    kernel="thin_plate_spline", smoothing=0.1)
            z_flat_g = rbf_g(pts_grid_g)
        except Exception:
            z_flat_g = griddata(pts_known_g[ok_g], vals_g[ok_g], pts_grid_g, method="nearest")

        z_2d_g = np.where(mask_2d_g, z_flat_g.reshape(RES_G, RES_G), np.nan)

        fig_g, ax_g = plt.subplots(figsize=(7, 5))
        fig_g.patch.set_facecolor("#0D1117")
        ax_g.set_facecolor("#161B22")

        im_g = ax_g.imshow(np.clip(z_2d_g, vmin_g, vmax_g), cmap=cmap_g,
                           vmin=vmin_g, vmax=vmax_g, extent=extent_g,
                           aspect="auto", interpolation="bilinear", origin="upper")
        wmask_gdf.boundary.plot(ax=ax_g, color="#2E8B8B", linewidth=1.2, alpha=0.8)

        for j, p in enumerate(puntos_uniq_g):
            lon_p, lat_p = COORDS[p]
            ax_g.scatter(lon_p, lat_p, c="white", s=45, zorder=5,
                        edgecolors="#0D1117", linewidths=0.5)

        cbar_g = plt.colorbar(im_g, ax=ax_g, fraction=0.035, pad=0.02)
        cbar_g.set_label(f"{label_g} ({unidad_g})" if unidad_g else label_g,
                         color="white", fontsize=9)
        plt.setp(plt.getp(cbar_g.ax.axes, "yticklabels"), color="white", fontsize=8)

        ax_g.set_title(f"{label_g}\n{fecha_dt_g.strftime('%d %b %Y')}",
                       color="white", fontsize=12, fontweight="bold")
        ax_g.tick_params(colors="#8EAAC8", labelsize=7)
        for sp in ax_g.spines.values(): sp.set_edgecolor("#2E8B8B44")

        plt.tight_layout()
        buf_frame = io.BytesIO()
        fig_g.savefig(buf_frame, dpi=110, facecolor="#0D1117")
        plt.close(fig_g)
        buf_frame.seek(0)
        frames.append(imageio.v2.imread(buf_frame))
        fechas_validas.append(fecha_str)

    if len(frames) < 2:
        return None, 0

    # Repetir el último frame para pausa visual al final del loop
    frames.append(frames[-1])
    frames.append(frames[-1])

    gif_buf = io.BytesIO()
    imageio.mimsave(gif_buf, frames, format="GIF", duration=0.9, loop=0)
    gif_buf.seek(0)

    return gif_buf, len(fechas_validas)


@st.cache_data(ttl=1800, show_spinner=False)
def obtener_url_descarga_tiff(_bbox, fecha_ini_str, fecha_fin_str, max_nubes, indice):
    """
    Genera una URL de descarga directa GeoTIFF para una banda/indice especifico
    de la mejor imagen Sentinel-2 encontrada en el rango de fechas.
    """
    if not GEE_OK:
        return None
    try:
        lon_min, lat_min, lon_max, lat_max = _bbox
        geom = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])
        coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(geom)
                  .filterDate(fecha_ini_str, fecha_fin_str)
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                  .sort("CLOUDY_PIXEL_PERCENTAGE"))
        if coll.size().getInfo() == 0:
            return None
        img = coll.sort("CLOUDY_PIXEL_PERCENTAGE", False).mosaic().clip(geom)

        if indice == "RGB":
            img_export = img.select(["B4","B3","B2"]).toFloat()
        else:
            img_export = calcular_indice_gee(img, indice).toFloat()

        url = img_export.getDownloadURL({
            "scale": 10,
            "region": geom,
            "format": "GEO_TIFF",
            "crs": "EPSG:4326",
        })
        return url
    except Exception:
        return None


def generar_gif_sentinel2(capa_key, bbox, fecha_ini, fecha_fin, max_nubes,
                          n_frames_max=8, wmask_gdf=None):
    """
    Genera un GIF animado a partir de imágenes Sentinel-2 reales (RGB o índice
    espectral), descargando una imagen representativa por cada sub-período
    dentro del rango de fechas elegido por el usuario.

    capa_key: "RGB", "NDVI", "NDWI", "MNDWI" o "NDTI"
    bbox: (lon_min, lat_min, lon_max, lat_max)
    fecha_ini, fecha_fin: objetos date
    Retorna: (BytesIO del GIF, n_frames_generados, lista_fechas_usadas) o (None, 0, [])
    """
    if not GEE_OK:
        return None, 0, []

    import requests as _requests
    from PIL import Image as PILImage

    try:
        lon_min, lat_min, lon_max, lat_max = bbox
        geom = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

        dias_totales = (fecha_fin - fecha_ini).days
        if dias_totales < 1:
            return None, 0, []

        n_periodos = min(n_frames_max, max(2, dias_totales // 30 + 1))
        cortes = pd.date_range(fecha_ini, fecha_fin, periods=n_periodos + 1)

        cfg = INDICES_VIZ[capa_key]
        frames = []
        fechas_usadas = []

        for i in range(n_periodos):
            sub_ini = cortes[i].strftime("%Y-%m-%d")
            sub_fin = cortes[i+1].strftime("%Y-%m-%d")

            coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                      .filterBounds(geom)
                      .filterDate(sub_ini, sub_fin)
                      .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                      .sort("CLOUDY_PIXEL_PERCENTAGE"))

            if coll.size().getInfo() == 0:
                continue

            img_ref_gif  = coll.first()
            props        = img_ref_gif.getInfo().get("properties", {})
            fecha_real_str = props.get("PRODUCT_ID", "")[7:15]
            img = coll.sort("CLOUDY_PIXEL_PERCENTAGE", False).mosaic().clip(geom)
            try:
                fecha_legible = pd.to_datetime(fecha_real_str, format="%Y%m%d").strftime("%d %b %Y")
            except Exception:
                fecha_legible = f"{sub_ini} a {sub_fin}"

            if capa_key == "RGB":
                img_vis = img
                vis_params = cfg["vis"]
            else:
                img_vis = calcular_indice_gee(img, capa_key)
                vis_params = cfg["vis"]

            thumb_url = img_vis.getThumbURL({
                **vis_params, "dimensions": 500, "format": "png", "region": geom,
            })
            resp = _requests.get(thumb_url, timeout=20)
            if resp.status_code != 200:
                continue

            base_img = PILImage.open(io.BytesIO(resp.content)).convert("RGB")

            # Anotar fecha sobre el frame con matplotlib para overlay consistente
            fig_f, ax_f = plt.subplots(figsize=(6, 5))
            fig_f.patch.set_facecolor("#0D1117")
            ax_f.set_facecolor("#0D1117")
            ax_f.imshow(base_img, extent=[lon_min, lon_max, lat_min, lat_max], aspect="auto")

            if wmask_gdf is not None:
                wmask_gdf.boundary.plot(ax=ax_f, color="#00FFCC", linewidth=1.3, alpha=0.85)

            ax_f.set_title(f"{cfg['nombre']}\n{fecha_legible}",
                           color="white", fontsize=12, fontweight="bold")
            ax_f.set_xticks([]); ax_f.set_yticks([])
            for sp in ax_f.spines.values(): sp.set_edgecolor("#2E8B8B44")

            plt.tight_layout()
            buf_frame = io.BytesIO()
            fig_f.savefig(buf_frame, dpi=100, facecolor="#0D1117")
            plt.close(fig_f)
            buf_frame.seek(0)

            frames.append(PILImage.open(buf_frame).convert("RGB"))
            fechas_usadas.append(fecha_legible)

        if len(frames) < 2:
            return None, 0, []

        w0, h0 = frames[0].size
        frames = [f.resize((w0, h0)) for f in frames]

        buf_gif = io.BytesIO()
        frames[0].save(
            buf_gif, format="GIF", save_all=True,
            append_images=frames[1:], duration=1000,
            loop=0, optimize=True,
        )
        buf_gif.seek(0)
        return buf_gif, len(frames), fechas_usadas

    except Exception:
        return None, 0, []


def build_folium_map_s2(wmask_gdf, coords_dict, bbox, tile_urls=None, height=460):
    lon_min, lat_min, lon_max, lat_max = bbox
    cx, cy = (lon_min+lon_max)/2, (lat_min+lat_max)/2

    # location/zoom_start son solo un punto de partida; fit_bounds() (al final)
    # es lo que realmente encuadra el área sin importar su tamaño o ubicación
    # en el mundo — funciona igual de bien para un río chico que para un
    # municipio o una cuenca completa.
    m = folium.Map(location=[cy, cx], zoom_start=12, tiles=None,
                   width="100%", height=height)

    tile_urls = tile_urls or {}

    if "RGB" in tile_urls:
        folium.TileLayer(tiles=tile_urls["RGB"], attr="GEE — Sentinel-2 SR",
                         name="📷 RGB (Color natural)", overlay=False,
                         control=True, show=True).add_to(m)

    for idx_name in ["NDVI", "NDWI", "MNDWI", "NDTI", "LST"]:
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

    # Puntos de muestreo: solo se dibujan si caen dentro (o cerca) del bbox
    # del área de estudio. Si el usuario sube un wmask de otra parte del
    # mundo, los 7 puntos del Río Pesquería simplemente no aparecen.
    margen = max((lon_max - lon_min), (lat_max - lat_min)) * 0.5
    for j,(nombre,(lon,lat)) in enumerate(coords_dict.items()):
        dentro = (lon_min - margen <= lon <= lon_max + margen and
                 lat_min - margen <= lat <= lat_max + margen)
        if not dentro:
            continue
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

    # Encuadre robusto: ajusta el mapa exactamente a los límites del wmask
    # con un pequeño padding, sin importar el tamaño del área (metros o
    # cientos de kilómetros).
    m.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]], padding=(20, 20))

    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    return m



# ── HEADER ────────────────────────────────────────────────────────────────────
logo_u = f'<img class="hdr-logo-img" src="data:image/png;base64,{UANL_B64}">' if UANL_B64 else "<span style='color:#8EAAC8'>UANL</span>"
logo_f = f'<img class="hdr-logo-img" src="data:image/png;base64,{FIC_B64}">'  if FIC_B64  else ""
logo_g = f'<img class="hdr-logo-img" src="data:image/png;base64,{GEO_B64}">'  if GEO_B64  else ""

_hero_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Source+Serif+4:ital,opsz,wght@1,8..60,400;1,8..60,500&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

body{
  font-family:'Poppins',system-ui,sans-serif;
  background:#020A14;
  height:100vh;
  overflow:hidden;
  color:#fff;
}

.bg-wrap{position:fixed;inset:0;z-index:0}

.bg-base{
  position:absolute;inset:0;
  background:#020A14;
}

.bg-aurora{
  position:absolute;inset:-40%;
  background:
    radial-gradient(ellipse 70% 55% at 18% 48%,rgba(14,165,233,.24) 0%,transparent 55%),
    radial-gradient(ellipse 65% 70% at 82% 18%,rgba(34,211,238,.17) 0%,transparent 50%),
    radial-gradient(ellipse 55% 50% at 52% 86%,rgba(20,184,166,.14) 0%,transparent 50%),
    radial-gradient(ellipse 38% 38% at 68% 58%,rgba(56,189,248,.09) 0%,transparent 50%);
  animation:aurora 22s ease-in-out infinite alternate;
}

.bg-grid{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(34,211,238,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(34,211,238,.05) 1px,transparent 1px);
  background-size:55px 55px;
}

.bg-scan{
  position:absolute;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(34,211,238,.7) 40%,rgba(255,255,255,.9) 50%,rgba(34,211,238,.7) 60%,transparent);
  animation:scanLine 10s linear infinite;
  opacity:0;
}

@keyframes aurora{
  0%{transform:scale(1) translate(0,0);opacity:.85}
  33%{transform:scale(1.05) translate(2%,-2.5%)}
  66%{transform:scale(.97) translate(-2.5%,2%);opacity:1}
  100%{transform:scale(1.03) translate(1%,-1%);opacity:.88}
}

@keyframes scanLine{
  0%{top:0;opacity:0} 3%{opacity:.9} 96%{opacity:.9} 100%{top:100vh;opacity:0}
}

@keyframes fadeUp{
  from{opacity:0;transform:translateY(16px)}
  to{opacity:1;transform:translateY(0)}
}

@keyframes blink{
  0%,100%{opacity:1;box-shadow:0 0 8px #10B981,0 0 16px rgba(16,185,129,.3)}
  50%{opacity:.15;box-shadow:none}
}

@keyframes floatOrb{
  0%,100%{transform:translate(0,0) scale(1)}
  33%{transform:translate(20px,-18px) scale(1.06)}
  66%{transform:translate(-15px,14px) scale(.95)}
}

/* ── LAYOUT ── */
.hero{
  position:relative;z-index:10;
  display:flex;height:100%;min-height:540px;
  overflow:hidden;
}

/* ── LIQUID GLASS LIGHT ── */
.lg{
  position:relative;overflow:hidden;
  background:rgba(255,255,255,.01);
  background-blend-mode:luminosity;
  backdrop-filter:blur(4px);
  -webkit-backdrop-filter:blur(4px);
  box-shadow:inset 0 1px 1px rgba(255,255,255,.1);
}

.lg::before{
  content:'';position:absolute;inset:0;
  padding:1.4px;
  background:linear-gradient(180deg,
    rgba(255,255,255,.45) 0%,rgba(255,255,255,.15) 20%,
    transparent 40%,transparent 60%,
    rgba(255,255,255,.15) 80%,rgba(255,255,255,.45) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;
  mask-composite:exclude;
  border-radius:inherit;
  pointer-events:none;
}

/* ── LIQUID GLASS STRONG ── */
.lg-s{
  position:relative;overflow:hidden;
  background:rgba(255,255,255,.015);
  background-blend-mode:luminosity;
  backdrop-filter:blur(50px);
  -webkit-backdrop-filter:blur(50px);
  box-shadow:4px 4px 4px rgba(0,0,0,.05),inset 0 1px 1px rgba(255,255,255,.15);
}

.lg-s::before{
  content:'';position:absolute;inset:0;
  padding:1.4px;
  background:linear-gradient(180deg,
    rgba(255,255,255,.5) 0%,rgba(255,255,255,.2) 20%,
    transparent 40%,transparent 60%,
    rgba(255,255,255,.2) 80%,rgba(255,255,255,.5) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;
  mask-composite:exclude;
  border-radius:inherit;
  pointer-events:none;
}

/* ── LEFT PANEL ── */
.panel-l{
  flex:1 1 100%;
  position:relative;
  padding:20px;
  overflow:visible;
}

.panel-glass{
  position:absolute;inset:16px;
  border-radius:28px;
}

.left-inner{
  position:relative;z-index:2;
  height:100%;
  display:flex;flex-direction:column;
  padding:26px 30px 22px;
}

/* floating orbs inside left panel */
.orb{
  position:absolute;border-radius:50%;
  pointer-events:none;filter:blur(50px);
}
.orb1{
  width:280px;height:280px;top:-90px;right:-40px;
  background:radial-gradient(circle,rgba(14,165,233,.22) 0%,transparent 70%);
  animation:floatOrb 12s ease-in-out infinite;
}
.orb2{
  width:200px;height:200px;bottom:-60px;left:20%;
  background:radial-gradient(circle,rgba(34,211,238,.16) 0%,transparent 70%);
  animation:floatOrb 8s ease-in-out infinite reverse;
}
.orb3{
  width:160px;height:160px;top:10px;left:5%;
  background:radial-gradient(circle,rgba(20,184,166,.12) 0%,transparent 70%);
  animation:floatOrb 15s ease-in-out infinite;
}

/* one-shot scan on left panel */
.panel-l-scan{
  position:absolute;left:16px;right:16px;height:1.5px;top:16px;
  border-radius:28px 28px 0 0;
  background:linear-gradient(90deg,transparent,rgba(34,211,238,.8) 40%,rgba(255,255,255,.95) 50%,rgba(34,211,238,.8) 60%,transparent);
  animation:scanLine 2.5s ease-out .3s forwards;
  opacity:0;
}

/* NAV */
.nav{
  display:flex;align-items:center;
  justify-content:space-between;
  flex-shrink:0;margin-bottom:4px;
  flex-wrap:nowrap;gap:8px;
}

.brand{display:flex;align-items:center;gap:10px;min-width:0;flex:1}

.brand-logos{
  display:flex;align-items:center;gap:6px;flex-wrap:nowrap;
}

.brand-logos img{height:28px;object-fit:contain;opacity:.9;flex-shrink:0}
.brand-sep{width:1px;height:22px;background:rgba(255,255,255,.12);flex-shrink:0}
.brand-meta{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:rgba(255,255,255,.35);letter-spacing:.06em;white-space:nowrap;padding-left:10px;border-left:1px solid rgba(255,255,255,.08);margin-left:4px}

.live-badge{
  display:flex;align-items:center;gap:7px;
  padding:7px 16px;border-radius:40px;
  font-size:.68rem;font-weight:500;
  color:rgba(255,255,255,.7);letter-spacing:.1em;
}

.live-dot{
  width:6px;height:6px;border-radius:50%;
  background:#10B981;flex-shrink:0;
  animation:blink 2.2s ease infinite;
}

/* HERO CENTER */
.hero-center{
  flex:1;display:flex;flex-direction:column;
  justify-content:center;gap:18px;
  padding:20px 0;
  animation:fadeUp .7s ease forwards;
}

.eyebrow{
  font-family:'JetBrains Mono',monospace;
  font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(34,211,238,.65);
}

.hero-h1{
  font-size:clamp(2.4rem,5.5vw,4.8rem);
  font-weight:500;line-height:1.08;letter-spacing:-.04em;
  color:rgba(255,255,255,.95);
  max-width:720px;
}

.hero-h1 em{
  font-family:inherit;
  font-style:normal;font-weight:300;
  font-size:.52em;
  color:rgba(255,255,255,.55);
  display:block;margin-top:.3em;letter-spacing:-.01em;
}

.hero-sub{
  font-family:'JetBrains Mono',monospace;
  font-size:.72rem;color:rgba(255,255,255,.45);
  line-height:1.7;max-width:520px;
}

/* CTA */
.cta-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}

.cta-btn{
  display:inline-flex;align-items:center;gap:10px;
  padding:11px 22px;border-radius:40px;
  font-size:.78rem;font-weight:600;color:#fff;
  cursor:pointer;transition:transform .3s ease;
  border:none;font-family:'Poppins',sans-serif;
  background:none;
}

.cta-btn:hover{transform:scale(1.05)}
.cta-btn:active{transform:scale(.95)}

.cta-ic{
  width:28px;height:28px;border-radius:50%;
  background:rgba(255,255,255,.15);
  display:flex;align-items:center;justify-content:center;
  font-size:.85rem;
}

/* PILLS */
.pills{display:flex;flex-wrap:wrap;gap:7px}

.pill{
  padding:5px 14px;border-radius:40px;
  font-size:.68rem;color:rgba(255,255,255,.72);
}

/* BOTTOM */
.bottom{
  border-top:1px solid rgba(255,255,255,.07);
  padding-top:15px;flex-shrink:0;
}

.q-label{
  font-size:.56rem;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(255,255,255,.36);margin-bottom:7px;
}

.q-text{
  font-size:.78rem;color:rgba(255,255,255,.62);line-height:1.65;
}

.q-text em{
  font-family:'Source Serif 4',Georgia,serif;
  font-style:italic;color:rgba(255,255,255,.42);
}

.q-author{display:flex;align-items:center;gap:12px;margin-top:9px}

.ql{flex:1;height:1px;background:rgba(255,255,255,.1)}

.qname{
  font-size:.56rem;letter-spacing:.14em;text-transform:uppercase;
  color:rgba(255,255,255,.32);flex-shrink:0;
}

/* ── RIGHT PANEL ── */
.panel-r{
  flex:1;display:flex;flex-direction:column;gap:10px;
  padding:20px 20px 20px 0;
  animation:fadeUp .85s ease .12s both;
}

.r-top{
  display:flex;align-items:center;
  justify-content:space-between;flex-shrink:0;
}

.band-pill{
  display:flex;align-items:center;gap:5px;
  padding:8px 14px;border-radius:40px;
}

.band-tag{
  font-family:'JetBrains Mono',monospace;
  font-size:.63rem;font-weight:500;
  color:rgba(255,255,255,.65);
  padding:3px 8px;border-radius:6px;
  background:rgba(255,255,255,.06);
}

.arr{font-size:.75rem;color:rgba(255,255,255,.38);margin-left:2px}

.sparkle{
  width:36px;height:36px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.95rem;cursor:pointer;
  transition:transform .2s;
}

.sparkle:hover{transform:scale(1.1)}

/* COMMUNITY CARD */
.comm{
  border-radius:18px;padding:16px 18px;flex-shrink:0;
}

.comm-t{font-size:.78rem;font-weight:600;color:rgba(255,255,255,.9);margin-bottom:5px}
.comm-d{font-size:.66rem;color:rgba(255,255,255,.46);line-height:1.55}

/* FEATURE SECTION */
.feat-outer{
  flex:1;border-radius:26px;padding:12px;
  display:flex;flex-direction:column;gap:8px;min-height:0;
}

.feat-row{display:flex;gap:8px;flex:0 0 auto}

.feat-card{
  flex:1;border-radius:18px;padding:14px;
  display:flex;flex-direction:column;gap:8px;
  transition:transform .25s;
}

.feat-card:hover{transform:scale(1.02)}

.feat-ic{
  width:32px;height:32px;border-radius:10px;
  background:rgba(255,255,255,.07);
  display:flex;align-items:center;justify-content:center;
  font-size:.85rem;
}

.feat-t{font-size:.74rem;font-weight:600;color:rgba(255,255,255,.88)}
.feat-s{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:rgba(255,255,255,.4)}

.feat-bot{
  border-radius:18px;padding:13px 16px;
  display:flex;align-items:center;gap:13px;flex:1;
  transition:transform .25s;
}

.feat-bot:hover{transform:scale(1.01)}

.thumb{
  width:52px;height:46px;border-radius:12px;
  background:linear-gradient(135deg,rgba(14,165,233,.3),rgba(34,211,238,.18));
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;flex-shrink:0;
}

.bt{font-size:.76rem;font-weight:600;color:rgba(255,255,255,.9);margin-bottom:3px}
.bs{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:rgba(255,255,255,.4);line-height:1.55}

.plus{
  margin-left:auto;width:28px;height:28px;border-radius:50%;
  background:rgba(255,255,255,.07);
  display:flex;align-items:center;justify-content:center;
  color:rgba(255,255,255,.55);font-size:.9rem;cursor:pointer;
  transition:all .2s;flex-shrink:0;
}

/* ── GLOBE ── */
.globe-wrap{
  position:absolute;right:20px;top:50%;transform:translateY(-50%);
  width:380px;height:380px;pointer-events:none;z-index:1;
  overflow:visible;
}
.globe{
  width:100%;height:100%;border-radius:50%;
  background:
    radial-gradient(circle at 32% 36%, rgba(34,211,238,.18) 0%, transparent 55%),
    radial-gradient(circle at 68% 65%, rgba(14,165,233,.14) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, #051824 0%, #031018 60%, #020c14 100%);
  box-shadow:
    0 0 0 1px rgba(34,211,238,.12),
    0 0 60px rgba(14,165,233,.18),
    0 0 120px rgba(14,165,233,.08),
    inset 0 0 80px rgba(0,0,0,.6);
  position:relative;overflow:hidden;
}
/* atmosphere glow ring */
.globe::after{
  content:'';position:absolute;inset:-8px;border-radius:50%;
  background:radial-gradient(circle at 50% 50%,transparent 46%,rgba(34,211,238,.07) 52%,rgba(14,165,233,.12) 58%,transparent 66%);
  pointer-events:none;
}
/* continent patches */
.globe::before{
  content:'';position:absolute;inset:0;border-radius:50%;
  background:
    radial-gradient(ellipse 28% 18% at 38% 42%, rgba(20,184,166,.22) 0%, transparent 100%),
    radial-gradient(ellipse 20% 12% at 62% 35%, rgba(16,185,129,.16) 0%, transparent 100%),
    radial-gradient(ellipse 16% 22% at 72% 58%, rgba(20,184,166,.14) 0%, transparent 100%),
    radial-gradient(ellipse 12% 10% at 28% 62%, rgba(16,185,129,.12) 0%, transparent 100%),
    radial-gradient(ellipse 10% 8%  at 50% 72%, rgba(20,184,166,.10) 0%, transparent 100%);
  animation:globeRotate 28s linear infinite;
}
.globe-grid{
  position:absolute;inset:0;border-radius:50%;overflow:hidden;
}
.globe-grid svg{width:100%;height:100%;opacity:.18;animation:globeRotate 28s linear infinite;}
/* pin dot */
.globe-pin{
  position:absolute;width:8px;height:8px;border-radius:50%;
  background:#22D3EE;top:38%;left:44%;
  box-shadow:0 0 0 3px rgba(34,211,238,.25),0 0 12px rgba(34,211,238,.6);
  animation:pinPulse 2.5s ease-in-out infinite;
}
.globe-pin::after{
  content:'';position:absolute;bottom:100%;left:50%;transform:translateX(-50%);
  width:1px;height:18px;background:linear-gradient(to top,rgba(34,211,238,.7),transparent);
}
/* orbit ring */
.globe-orbit{
  position:absolute;inset:-18px;border-radius:50%;
  border:1px solid rgba(34,211,238,.08);
  animation:orbitSpin 18s linear infinite;
}
.globe-orbit::before{
  content:'';position:absolute;width:6px;height:6px;border-radius:50%;
  background:#0EA5E9;top:-3px;left:50%;transform:translateX(-50%);
  box-shadow:0 0 8px rgba(14,165,233,.8);
}
.globe-orbit2{
  position:absolute;inset:-36px;border-radius:50%;
  border:1px solid rgba(14,165,233,.05);
  animation:orbitSpin 32s linear infinite reverse;
}
.globe-orbit2::before{
  content:'';position:absolute;width:4px;height:4px;border-radius:50%;
  background:#14B8A6;bottom:-2px;right:20%;
  box-shadow:0 0 6px rgba(20,184,166,.8);
}
@keyframes globeRotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes orbitSpin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes pinPulse{0%,100%{box-shadow:0 0 0 3px rgba(34,211,238,.25),0 0 12px rgba(34,211,238,.6)}50%{box-shadow:0 0 0 6px rgba(34,211,238,.1),0 0 20px rgba(34,211,238,.8)}}

.plus:hover{background:rgba(255,255,255,.15);color:#fff}
</style>"""

_title = t("app_title", LANG)
_sub   = t("app_subtitle", LANG)

_hero_body = f"""<div class="bg-wrap">
<div class="bg-base"></div><div class="bg-aurora"></div><div class="bg-grid"></div><div class="bg-scan"></div>
</div>
<div class="hero">
<div class="panel-l">
<div class="panel-glass lg-s"></div>
<div class="panel-l-scan"></div>
<div class="orb orb1"></div><div class="orb orb2"></div><div class="orb orb3"></div>
<div class="left-inner">
<nav class="nav">
<div class="brand">
<div class="brand-logos">{logo_u}<div class="brand-sep"></div>{logo_f}<div class="brand-sep"></div>{logo_g}</div>
<div class="brand-meta">UANL &middot; Geom&aacute;tica &middot; NL, M&eacute;xico</div>
</div>
<div class="live-badge lg" style="border-radius:40px"><div class="live-dot"></div>GEE</div>
</nav>
<div class="hero-center">
<div class="eyebrow">TELEDETECCION &middot; NL, MEXICO &middot; UANL</div>
<h1 class="hero-h1">{_title}<br><em>{_sub}</em></h1>
<p class="hero-sub">Sentinel-2 SR Harmonized &middot; 10 m &middot; EPSG:4326<br>Sube cualquier shapefile &middot; An&aacute;lisis global</p>
<div class="cta-row">
<button class="cta-btn lg-s" style="border-radius:40px" onclick="
  var btn=this;
  btn.style.transform='scale(0.95)';
  btn.style.opacity='0.7';
  setTimeout(function(){{
    btn.style.transition='transform 0.3s,opacity 0.3s';
    btn.style.transform='scale(1)';
    btn.style.opacity='1';
  }},200);
  try{{window.parent.scrollBy({{top:620,behavior:'smooth'}})}}catch(e){{}}
  try{{window.top.scrollBy({{top:620,behavior:'smooth'}})}}catch(e){{}}
"><span class="cta-ic">&#8594;</span>Explorar Ahora</button>
</div>
<div class="pills">
<span class="pill lg" style="border-radius:40px">Sentinel-2 SR</span>
<span class="pill lg" style="border-radius:40px">Calidad del Agua</span>
<span class="pill lg" style="border-radius:40px">&Iacute;ndices Espectrales</span>
<span class="pill lg" style="border-radius:40px">Random Forest</span>
</div>
</div>
<div class="bottom">
<div class="q-label">MONITOREO REMOTO SATELITAL</div>
<div class="q-text"><em>Observar el planeta desde el espacio,</em> para comprender el agua que habitamos.</div>
<div class="q-author"><div class="ql"></div><div class="qname">SENTINEL-2 SR &middot; GEE CLOUD API &middot; RANDOM FOREST</div><div class="ql"></div></div>
</div>
</div>

<!-- GLOBE -->
<div class="globe-wrap">
  <div class="globe-orbit2"></div>
  <div class="globe-orbit"></div>
  <div class="globe">
    <div class="globe-grid">
      <svg viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="210" cy="210" rx="200" ry="40"  fill="none" stroke="#22D3EE" stroke-width=".7"/>
        <ellipse cx="210" cy="210" rx="200" ry="90"  fill="none" stroke="#22D3EE" stroke-width=".6"/>
        <ellipse cx="210" cy="210" rx="200" ry="148" fill="none" stroke="#22D3EE" stroke-width=".6"/>
        <ellipse cx="210" cy="210" rx="200" ry="185" fill="none" stroke="#22D3EE" stroke-width=".5"/>
        <ellipse cx="210" cy="210" rx="40"  ry="200" fill="none" stroke="#22D3EE" stroke-width=".7"/>
        <ellipse cx="210" cy="210" rx="100" ry="200" fill="none" stroke="#22D3EE" stroke-width=".6"/>
        <ellipse cx="210" cy="210" rx="160" ry="200" fill="none" stroke="#22D3EE" stroke-width=".5"/>
        <circle  cx="210" cy="210" r="200"  fill="none" stroke="#22D3EE" stroke-width=".8"/>
      </svg>
    </div>
    <div class="globe-pin"></div>
  </div>
</div>
</div>
</div>
</div>
</div>"""

components.html(
    f"<!DOCTYPE html><html><head><meta charset='utf-8'>{_hero_css}</head><body>{_hero_body}</body></html>",
    height=720,
    scrolling=False
)


if model_data is None:
    _err = st.session_state.get("_model_load_error", "Unknown")
    st.error(f'{t("error_modelo", LANG)} {_err}')
    st.stop()
if df_global is None:
    st.error(t("error_csv", LANG)); st.stop()

_gee_dot  = '<span class="status-dot-ok"></span>'  if GEE_OK else '<span class="status-dot-warn"></span>'
_gee_txt  = t("gee_activo", LANG) if GEE_OK else t("gee_no_disponible", LANG)
_mod_txt  = t("modelo_cargado", LANG)
st.markdown(f"""<div class="status-row">
  <div class="status-item"><span class="status-dot-ok"></span><span><b>RF v3</b> {_mod_txt}</span></div>
  <div class="status-sep"></div>
  <div class="status-item">{_gee_dot}<span><b>GEE</b> {_gee_txt}</span></div>
  <div class="status-sep"></div>
  <div class="status-item"><span class="status-dot-ok"></span><span><b>Sentinel-2</b> SR Harmonized · 10 m</span></div>
  <div class="status-sep"></div>
  <div class="status-item"><span class="status-dot-ok"></span><span><b>19</b> campañas · <b>7</b> puntos · EPSG:4326</span></div>
  <div class="status-badge">SISTEMA ACTIVO</div>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div class="slabel">{t("sidebar_idioma", LANG)}</div>', unsafe_allow_html=True)
    lang_sel = st.selectbox(
        "", options=list(IDIOMAS.keys()),
        index=list(IDIOMAS.keys()).index(LANG),
        format_func=lambda k: IDIOMAS[k],
        key="lang_selectbox", label_visibility="collapsed"
    )
    if lang_sel != st.session_state["lang"]:
        st.session_state["lang"] = lang_sel
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_area", LANG)}</div>', unsafe_allow_html=True)
    st.caption(t("sidebar_area_caption", LANG))
    wmask_zip = st.file_uploader(t("sidebar_upload", LANG), type=["zip"])

    # Detectar si el wmask subido corresponde al Río Pesquería (única zona
    # con modelo RF entrenado) o es otra zona del mundo (solo RGB/índices)
    es_zona_pesqueria = False
    if wmask_zip is not None:
        try:
            with tempfile.TemporaryDirectory() as _tmp_zone:
                with zipfile.ZipFile(wmask_zip, "r") as _z: _z.extractall(_tmp_zone)
                _shp = [f for f in os.listdir(_tmp_zone) if f.endswith(".shp")]
                if _shp:
                    _w_check = gpd.read_file(os.path.join(_tmp_zone, _shp[0]))
                    if _w_check.crs is None or _w_check.crs.to_epsg() != 4326:
                        _w_check = _w_check.to_crs(4326)
                    es_zona_pesqueria = zona_es_pesqueria(tuple(_w_check.total_bounds))
            wmask_zip.seek(0)  # reset para usos posteriores del mismo archivo
        except Exception:
            es_zona_pesqueria = False

        if es_zona_pesqueria:
            st.success(t("zona_pesqueria_si", LANG))
        else:
            st.info(t("zona_pesqueria_no", LANG))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_fecha_muestreo", LANG)}</div>', unsafe_allow_html=True)
    fecha_campo = st.selectbox("", FECHAS_CAMPO, index=16,
        format_func=lambda f: pd.to_datetime(f, format="%m/%d/%Y").strftime("%d %b %Y"))
    fecha_dt = pd.to_datetime(fecha_campo, format="%m/%d/%Y")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_rango_s2", LANG)}</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fecha_ini = st.date_input(t("sidebar_desde", LANG), value=fecha_dt.date()-timedelta(days=8),
                                  min_value=date(2015,6,1), max_value=date(2025,12,31))
    with col_d2:
        fecha_fin = st.date_input(t("sidebar_hasta", LANG), value=fecha_dt.date()+timedelta(days=8),
                                  min_value=date(2015,6,1), max_value=date(2025,12,31))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_filtro_nubes", LANG)}</div>', unsafe_allow_html=True)
    max_nubes = st.slider(t("sidebar_max_nubes", LANG), 0, 50, 15, 5)

    if fecha_ini >= fecha_fin:
        st.error(t("sidebar_fecha_error", LANG))
    else:
        dias = (fecha_fin - fecha_ini).days
        mid  = fecha_ini + (fecha_fin - fecha_ini)/2
        des  = abs((fecha_dt.date() - mid).days)
        _d_word = t("sidebar_dias", LANG)
        if des <= 5:   st.success(f"✅ {t('sidebar_desfase', LANG)}: {des} {_d_word}")
        elif des <= 12: st.warning(f"⚠️ {t('sidebar_desfase', LANG)}: {des} {_d_word}")
        else:           st.error(f"❌ {t('sidebar_desfase', LANG)}: {des} {_d_word}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_parametros", LANG)}</div>', unsafe_allow_html=True)
    params_sel = st.multiselect("", list(PARAMS.keys()), default=list(PARAMS.keys()),
        format_func=lambda p: f"{get_param_label(p, LANG)} ({PARAMS[p]['unidad']})")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="slabel">{t("sidebar_resolucion", LANG)}</div>', unsafe_allow_html=True)
    resolucion = st.select_slider("", options=[200,300,400,500], value=400,
        format_func=lambda v: f"{v}×{v}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    valid = (wmask_zip is not None and params_sel and fecha_ini < fecha_fin)
    correr = st.button(t("sidebar_generar_mapas", LANG), type="primary",
                       use_container_width=True, disabled=not valid)
    if wmask_zip is None:
        st.warning(t("sidebar_sube_wmask_warn", LANG))

# ── PANTALLA INICIAL ──────────────────────────────────────────────────────────
if not correr:
    _step_icons = ["📁", "⚙️", "🗺"]
    c1,c2,c3 = st.columns(3)
    for col, paso_num, paso_titulo, paso_texto, paso_icon in zip(
        [c1,c2,c3],
        ["01", "02", "03"],
        [t("paso1_titulo",LANG), t("paso2_titulo",LANG), t("paso3_titulo",LANG)],
        [t("paso1_texto",LANG), t("paso2_texto",LANG), t("paso3_texto",LANG)],
        _step_icons,
    ):
        with col:
            st.markdown(
                f'<div class="step-box">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:.7rem">'
                f'<div style="width:34px;height:34px;border-radius:10px;background:rgba(14,165,233,.1);'
                f'border:1px solid rgba(14,165,233,.2);display:flex;align-items:center;'
                f'justify-content:center;font-size:16px;flex-shrink:0">{paso_icon}</div>'
                f'<div class="step-num" style="margin:0">STEP {paso_num}</div>'
                f'</div>'
                f'<div class="step-t">{paso_titulo}</div>'
                f'<div class="step-b">{paso_texto}</div></div>',
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
            st.markdown(f'<div class="sec-t">{t("previsualizacion_titulo", LANG)}</div>', unsafe_allow_html=True)

            tile_urls, s2_info = {}, {}
            if GEE_OK:
                with st.spinner(t("buscando_imagen", LANG)):
                    s2_info, tile_urls = buscar_imagen_s2(
                        bbox_prev, fecha_ini.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d"), max_nubes,
                        geojson_poligono=wmask_prev.geometry.union_all().__geo_interface__)

            st.markdown('<div class="map-panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="map-title">{t("imagen_satelital_titulo", LANG)}</div>', unsafe_allow_html=True)

            mapa_f = build_folium_map_s2(wmask_prev, COORDS, bbox_prev, tile_urls=tile_urls, height=460)
            st_folium(mapa_f, width="100%", height=460, returned_objects=[])

            if s2_info.get("n_imagenes", 0) == 0:
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip chip-bad">{t("sin_imagenes", LANG)} (&lt;{max_nubes}%)</span>
                  <br>{t("amplia_rango", LANG)}
                </div></div>""", unsafe_allow_html=True)
            elif "error" in s2_info:
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip chip-warn">{t("capa_referencia", LANG)}</span>
                  <br>{t("no_conexion_gee", LANG)}
                </div></div>""", unsafe_allow_html=True)
            else:
                n_imgs   = s2_info.get("n_imagenes", 0)
                nubes_real = s2_info.get("nubes_pct", "N/D")
                st.markdown(f"""
                <div class="map-meta">
                  <span class="chip">✅ {n_imgs} {t("imagenes_encontradas", LANG)}</span>
                  <span class="chip">☁️ {t("nubes_reales", LANG)}: {nubes_real}%</span>
                  <span class="chip">📅 {fecha_ini.strftime('%d %b')} → {fecha_fin.strftime('%d %b %Y')}</span>
                  <span class="chip">🧪 {t("muestreo", LANG)}: {fecha_dt.strftime('%d %b %Y')}</span><br>
                  {t("capas_disponibles", LANG)}
                </div></div>""", unsafe_allow_html=True)

                # Leyenda de indices espectrales disponibles
                st.markdown('<div class="map-panel" style="margin-top:.6rem">', unsafe_allow_html=True)
                st.markdown(f'<div class="map-title">{t("indices_disponibles_titulo", LANG)}</div>',
                           unsafe_allow_html=True)
                idx_cols = st.columns(5)
                for ic, idx_key in zip(idx_cols, ["RGB","NDVI","NDWI","MNDWI","NDTI","LST"]):
                    cfg = INDICES_VIZ[idx_key]
                    idx_nombre_t = get_indice_nombre(idx_key, LANG)
                    idx_desc_t = get_indice_desc(idx_key, LANG) if idx_key != "RGB" else ""
                    with ic:
                        st.markdown(f"""
                        <div style="font-size:.72rem;color:#8EAAC8;line-height:1.5;
                                    border-left:2px solid #2E8B8B;padding-left:8px">
                          <b style="color:#fff;font-size:.78rem">{idx_nombre_t}</b><br>
                          {idx_desc_t}
                        </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # ── Descarga de GeoTIFFs ─────────────────────────────────────
                if GEE_OK and s2_info.get("n_imagenes", 0) > 0:
                    st.markdown('<div class="map-panel" style="margin-top:.6rem">',
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="map-title">{t("tiff_titulo", LANG)}</div>',
                               unsafe_allow_html=True)
                    st.caption(t("tiff_caption", LANG))

                    tiff_cols = st.columns(5)
                    for tc, idx_key in zip(tiff_cols, ["RGB","NDVI","NDWI","MNDWI","NDTI","LST"]):
                        with tc:
                            if st.button(f"📥 {idx_key}", key=f"tiff_{idx_key}",
                                        use_container_width=True):
                                with st.spinner(f'{t("tiff_generando", LANG)} {idx_key}...'):
                                    url_tiff = obtener_url_descarga_tiff(
                                        bbox_prev, fecha_ini.strftime("%Y-%m-%d"),
                                        fecha_fin.strftime("%Y-%m-%d"), max_nubes, idx_key
                                    )
                                if url_tiff:
                                    st.success(t("tiff_listo", LANG))
                                    st.markdown(f"[{t('tiff_descargar', LANG)} {idx_key}.tif]({url_tiff})")
                                else:
                                    st.error(t("tiff_error", LANG))
                    st.markdown("</div>", unsafe_allow_html=True)

                # ── Animación GIF Sentinel-2 (RGB e índices reales) ──────────
                if GEE_OK and s2_info.get("n_imagenes", 0) > 0:
                    st.markdown('<div class="map-panel" style="margin-top:.6rem">',
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="map-title">{t("gif_titulo", LANG)}</div>',
                               unsafe_allow_html=True)
                    st.caption(t("gif_caption", LANG))

                    col_gifc1, col_gifc2 = st.columns([2,1])
                    with col_gifc1:
                        capa_gif_sel = st.selectbox(
                            t("gif_capa_animar", LANG),
                            options=["RGB","NDVI","NDWI","MNDWI","NDTI","LST"],
                            format_func=lambda k: get_indice_nombre(k, LANG),
                            key="capa_gif_select"
                        )
                    with col_gifc2:
                        n_frames_sel = st.slider(t("gif_max_fotogramas", LANG), 2, 10, 6,
                                                 key="n_frames_gif")

                    dias_rango = (fecha_fin - fecha_ini).days
                    st.caption(f'📅 {t("gif_rango_actual", LANG)}: {fecha_ini.strftime("%d %b %Y")} → '
                              f'{fecha_fin.strftime("%d %b %Y")} ({dias_rango} {t("sidebar_dias", LANG)}) · '
                              f'☁️ {t("gif_nubes", LANG)} < {max_nubes}%')

                    if dias_rango < 30:
                        st.warning(t("gif_rango_corto_warn", LANG))

                    gen_gif_s2 = st.button(
                        t("gif_generar_btn", LANG), use_container_width=True,
                        type="primary", key="btn_gif_s2"
                    )

                    if gen_gif_s2:
                        with st.spinner(t("gif_generando", LANG)):
                            buf_gif_s2, n_frames_ok, fechas_usadas_gif = generar_gif_sentinel2(
                                capa_gif_sel, bbox_prev, fecha_ini, fecha_fin, max_nubes,
                                n_frames_max=n_frames_sel, wmask_gdf=wmask_prev
                            )

                        if buf_gif_s2 is not None:
                            st.success(f'{t("gif_exito", LANG)} {n_frames_ok} {t("gif_fotogramas", LANG)}: '
                                      f'{", ".join(fechas_usadas_gif)}')
                            st.image(buf_gif_s2.getvalue(),
                                    caption=f"{get_indice_nombre(capa_gif_sel, LANG)}")
                            st.download_button(
                                t("gif_descargar_btn", LANG),
                                buf_gif_s2.getvalue(),
                                f"Animacion_S2_{capa_gif_sel}_"
                                f"{fecha_ini.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.gif",
                                "image/gif", use_container_width=True
                            )
                        else:
                            st.warning(t("gif_sin_imagenes", LANG))
                    st.markdown("</div>", unsafe_allow_html=True)

                # ── Reportes PDF: Calidad de Agua vs Índices Espectrales ─────
                if GEE_OK and s2_info.get("n_imagenes", 0) > 0:
                    st.markdown('<div class="map-panel" style="margin-top:.6rem">',
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="map-title">{t("reportes_titulo", LANG)}</div>',
                               unsafe_allow_html=True)
                    st.caption(t("reportes_caption", LANG))

                    col_rep1, col_rep2 = st.columns(2)

                    # ── Reporte 1: Calidad de Agua (solo zona Pesquería) ──────
                    with col_rep1:
                        st.markdown(f"**{t('reporte_calidad_titulo', LANG)}**")
                        if es_zona_pesqueria:
                            st.caption(t("reporte_calidad_disponible", LANG))
                            if st.button(t("reporte_calidad_btn", LANG),
                                        use_container_width=True, key="btn_rep_calidad"):
                                st.info(t("reporte_calidad_redirigir", LANG))
                        else:
                            st.caption(t("reporte_calidad_no_disponible", LANG))
                            st.button(t("reporte_calidad_btn", LANG),
                                     use_container_width=True, disabled=True,
                                     key="btn_rep_calidad_disabled")

                    # ── Reporte 2: Índices Espectrales (cualquier zona) ───────
                    with col_rep2:
                        st.markdown(f"**{t('reporte_espectral_titulo', LANG)}**")
                        st.caption(t("reporte_espectral_disponible", LANG))
                        gen_rep_espectral = st.button(
                            t("reporte_espectral_btn", LANG),
                            use_container_width=True, type="primary",
                            key="btn_rep_espectral"
                        )

                        if gen_rep_espectral:
                            with st.spinner(t("reporte_espectral_generando", LANG)):
                                rep_info, rep_stats, rep_thumbs = obtener_datos_reporte_espectral(
                                    bbox_prev, fecha_ini.strftime("%Y-%m-%d"),
                                    fecha_fin.strftime("%Y-%m-%d"), max_nubes,
                                    geojson_poligono=wmask_prev.geometry.union_all().__geo_interface__
                                )

                            if rep_info and rep_info.get("n_imagenes", 0) > 0 and rep_thumbs:
                                try:
                                    _logo_path_rep = os.path.join(
                                        os.path.dirname(__file__), "logo_geomatica.png")
                                    if not os.path.exists(_logo_path_rep):
                                        _logo_path_rep = None

                                    pdf_espectral_buf = generar_pdf_reporte_espectral(
                                        rep_info, rep_stats, rep_thumbs,
                                        ["NDVI","NDWI","MNDWI","NDTI"],
                                        bbox_prev, fecha_ini, fecha_fin,
                                        logo_geo_path=_logo_path_rep, lang=LANG
                                    )
                                    st.success(t("reporte_espectral_exito", LANG))
                                    st.download_button(
                                        t("reporte_espectral_descargar", LANG),
                                        pdf_espectral_buf.getvalue(),
                                        f"Reporte_Espectral_{fecha_ini.strftime('%Y%m%d')}_"
                                        f"{fecha_fin.strftime('%Y%m%d')}.pdf",
                                        "application/pdf", use_container_width=True,
                                        key="dl_rep_espectral"
                                    )
                                except Exception as e:
                                    st.error(f'{t("reporte_espectral_error", LANG)} {e}')
                            else:
                                st.warning(t("reporte_espectral_sin_datos", LANG))

                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            ci1,ci2,ci3 = st.columns(3)
            with ci1:
                st.markdown(f'<div class="info-panel"><div class="info-title">{t("bbox_titulo", LANG)}</div>', unsafe_allow_html=True)
                st.markdown(f"""<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">
                  <b style="color:#fff">Lon</b>: {lon_min:.5f}° → {lon_max:.5f}°<br>
                  <b style="color:#fff">Lat</b>: {lat_min:.5f}° → {lat_max:.5f}°<br>
                  <b style="color:#fff">{t("bbox_poligonos", LANG)}</b>: {len(wmask_prev)}
                </div></div>""", unsafe_allow_html=True)
            with ci2:
                st.markdown(f'<div class="info-panel"><div class="info-title">{t("s2_titulo", LANG)}</div>', unsafe_allow_html=True)
                dias=(fecha_fin-fecha_ini).days
                st.markdown(f"""<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">
                  <b style="color:#fff">{t("s2_coleccion", LANG)}</b>: S2_SR_HARMONIZED<br>
                  <b style="color:#fff">RGB</b>: B4·B3·B2 (10m)<br>
                  <b style="color:#fff">{t("s2_rango", LANG)}</b>: {dias} {t("sidebar_dias", LANG)} · Clouds&lt;{max_nubes}%
                </div></div>""", unsafe_allow_html=True)
            with ci3:
                st.markdown(f'<div class="info-panel"><div class="info-title">{t("parametros_titulo_corto", LANG)}</div>', unsafe_allow_html=True)
                ph = "".join(f'<div style="font-size:.76rem;color:#8EAAC8;line-height:1.9">'
                            f'<span style="color:{PARAMS[p]["color"]}">{PARAMS[p]["icon"]}</span> '
                            f'<b style="color:#fff">{get_param_label(p, LANG)}</b></div>' for p in params_sel)
                st.markdown(ph + "</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="empty-state">
          <div class="empty-icon">🗺️</div>
          <div class="empty-title">{t("puntos_titulo", LANG)}</div>
          <div class="empty-sub">{t("sube_wmask_para_ver", LANG)}</div>
          <div class="empty-steps">
            <div class="empty-step"><div class="empty-step-num">1</div>Sube un <b>wmask.zip</b> con tu shapefile (.shp + .dbf + .prj + .cpg) de cualquier zona</div>
            <div class="empty-step"><div class="empty-step-num">2</div>Selecciona el rango de fechas Sentinel-2 y la cobertura de nubes</div>
            <div class="empty-step"><div class="empty-step-num">3</div>Obtén índices espectrales, animaciones GIF y reportes PDF para cualquier área del mundo</div>
          </div>
          <div class="empty-coords">Río Pesquería · 7 puntos · 25.77°N – 25.83°N · 100.02°W – 100.35°W · EPSG:4326 · Modelo RF activo solo para esta zona</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="sec-t">{t("puntos_titulo", LANG)}</div>', unsafe_allow_html=True)
        # Mapa Folium con marcadores animados
        _pts = list(COORDS.items())
        _lats = [c[1] for _,c in _pts]; _lons = [c[0] for _,c in _pts]
        _center = [sum(_lats)/len(_lats), sum(_lons)/len(_lons)]
        _mapa_pts = folium.Map(location=_center, zoom_start=11, tiles=None,
                               width="100%", height=320)
        folium.TileLayer("CartoDB dark_matter", name="Dark", attr="CARTO").add_to(_mapa_pts)
        # Línea del río (conecta puntos ordenados por longitud)
        _sorted_pts = sorted(_pts, key=lambda x: x[1][0])
        folium.PolyLine(
            locations=[[c[1], c[0]] for _,c in _sorted_pts],
            color="#22D3EE", weight=2.5, opacity=0.6, dash_array="6 4"
        ).add_to(_mapa_pts)
        # Marcadores con pulso CSS + popup
        _pulse_css = """
        <style>
        .pulse-marker{width:16px;height:16px;position:relative}
        .pulse-dot{width:10px;height:10px;border-radius:50%;background:#EF4444;
          position:absolute;top:3px;left:3px;
          box-shadow:0 0 0 0 rgba(239,68,68,.6)}
        .pulse-dot::after{content:'';position:absolute;inset:-4px;border-radius:50%;
          border:2px solid rgba(239,68,68,.5);
          animation:pulseRing 1.8s ease-out infinite}
        @keyframes pulseRing{0%{transform:scale(.8);opacity:1}100%{transform:scale(2.2);opacity:0}}
        </style>"""
        for i, (nombre, (lon, lat)) in enumerate(_pts):
            icon_html = f"""{_pulse_css}
            <div class="pulse-marker"><div class="pulse-dot"></div></div>"""
            folium.Marker(
                location=[lat, lon],
                icon=folium.DivIcon(html=icon_html, icon_size=(16,16), icon_anchor=(8,8)),
                popup=folium.Popup(
                    f"<b style='font-family:monospace;font-size:11px'>{nombre}</b><br>"
                    f"<span style='font-family:monospace;font-size:10px;color:#666'>"
                    f"Lat: {lat:.5f}°N<br>Lon: {lon:.5f}°W</span>",
                    max_width=160
                ),
                tooltip=f"📍 {nombre}"
            ).add_to(_mapa_pts)
        # Badge número de punto
        for i, (nombre, (lon, lat)) in enumerate(_pts):
            folium.Marker(
                location=[lat+0.003, lon],
                icon=folium.DivIcon(
                    html=f"<div style='font-family:monospace;font-size:9px;font-weight:700;"
                         f"color:#22D3EE;background:rgba(2,6,14,.75);padding:1px 4px;"
                         f"border-radius:3px;border:1px solid rgba(34,211,238,.3);white-space:nowrap'>"
                         f"P{i+1}</div>",
                    icon_size=(24, 14), icon_anchor=(12, 14)
                )
            ).add_to(_mapa_pts)
        st_folium(_mapa_pts, width="100%", height=320, returned_objects=[])

        # ── Formulario de contribución de puntos ──────────────────────────
        _SHEETS_URL = "https://script.google.com/macros/s/AKfycbyuloqzC9EwW_FxvqKZq1Q7ihWkmGdsPJnalwgXDCJF8kCNYS8n-Ul_uzUrH1VjkLRppg/exec"

        with st.expander("➕  Contribuir un punto de muestreo", expanded=False):
            st.markdown("""<div style="font-size:.8rem;color:rgba(255,255,255,.5);margin-bottom:12px">
            Ayuda a expandir el modelo aportando datos de campo verificados.
            Cada contribución es revisada antes de ser incluida.
            </div>""", unsafe_allow_html=True)

            with st.form("form_contribucion", clear_on_submit=True):
                fc1, fc2 = st.columns(2)
                with fc1:
                    _rio      = st.text_input("Nombre del río *", placeholder="Ej. Río Bravo")
                    _estado   = st.text_input("Estado / Municipio *", placeholder="Ej. Tamaulipas")
                    _contrib  = st.text_input("Tu nombre *", placeholder="Ej. Juan Pérez")
                    _inst     = st.text_input("Institución / Organización", placeholder="Ej. UANL, CONAGUA, IMTA")
                with fc2:
                    _lat      = st.number_input("Latitud *", min_value=14.0, max_value=33.0, value=25.80, format="%.5f")
                    _lon      = st.number_input("Longitud *", min_value=-118.0, max_value=-86.0, value=-100.20, format="%.5f")
                    _fecha    = st.date_input("Fecha de muestreo *")
                    _fuente   = st.selectbox("Fuente de los datos *",
                        ["CONAGUA", "IMTA", "SEMARNAT", "Tesis/Artículo científico", "Reporte institucional", "Otra"])

                st.markdown("**Parámetros fisicoquímicos** (al menos uno requerido)")
                pp1, pp2, pp3, pp4 = st.columns(4)
                with pp1: _ptot  = st.number_input("P_TOT (mg/L)",  min_value=0.0, value=0.0, format="%.3f")
                with pp2: _nnh3  = st.number_input("N_NH3 (mg/L)",  min_value=0.0, value=0.0, format="%.3f")
                with pp3: _ntot  = st.number_input("N_TOT (mg/L)",  min_value=0.0, value=0.0, format="%.3f")
                with pp4: _ntotk = st.number_input("N_TOTK (mg/L)", min_value=0.0, value=0.0, format="%.3f")

                _url_ev = st.text_input("URL o referencia de la evidencia *",
                    placeholder="https://... o cita bibliográfica completa")
                _notas  = st.text_area("Notas adicionales (opcional)", height=70,
                    placeholder="Método de análisis, condiciones del muestreo, etc.")

                _submitted = st.form_submit_button("📤  Enviar contribución", use_container_width=True, type="primary")

            if _submitted:
                # Validaciones
                _errores = []
                if not _rio.strip():    _errores.append("Nombre del río")
                if not _estado.strip(): _errores.append("Estado/Municipio")
                if not _contrib.strip():_errores.append("Tu nombre")
                if not _url_ev.strip(): _errores.append("URL/referencia de evidencia")
                if _ptot == 0 and _nnh3 == 0 and _ntot == 0 and _ntotk == 0:
                    _errores.append("Al menos un parámetro fisicoquímico (> 0)")

                if _errores:
                    st.error(f"Campos requeridos: {', '.join(_errores)}")
                else:
                    import requests as _req, datetime as _dt, json as _json
                    _payload = {
                        "timestamp":      _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "rio":            _rio.strip(),
                        "estado":         _estado.strip(),
                        "lat":            str(_lat),
                        "lon":            str(_lon),
                        "fecha_muestreo": str(_fecha),
                        "P_TOT":          str(_ptot)  if _ptot  > 0 else "",
                        "N_NH3":          str(_nnh3)  if _nnh3  > 0 else "",
                        "N_TOT":          str(_ntot)  if _ntot  > 0 else "",
                        "N_TOTK":         str(_ntotk) if _ntotk > 0 else "",
                        "fuente":         _fuente,
                        "url_evidencia":  _url_ev.strip(),
                        "contribuidor":   _contrib.strip(),
                        "institucion":    _inst.strip() or "No especificada",
                        "notas":          _notas.strip(),
                    }
                    try:
                        _r = _req.post(_SHEETS_URL, data=_json.dumps(_payload),
                                       headers={"Content-Type": "application/json"}, timeout=15)
                        if _r.status_code == 200:
                            st.success("✅ Contribución enviada. Será revisada antes de incluirse en el modelo. ¡Gracias!")
                        else:
                            st.error(f"Error al enviar ({_r.status_code}). Intenta de nuevo.")
                    except Exception as _ex:
                        st.error(f"Error de conexión: {_ex}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-t">🔬&nbsp; {t("parametros_seccion_titulo", LANG)}</div>', unsafe_allow_html=True)
    for col,cfg in PARAMS.items():
        label_t = get_param_label(col, LANG)
        desc_t  = get_param_desc(col, LANG)
        st.markdown(f"""<div class="param-card" style="border-left:3px solid {cfg['color']}22">
          <div style="position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,{cfg['color']},transparent);border-radius:3px 0 0 3px"></div>
          <div class="param-hdr">
            <div style="display:flex;align-items:center;gap:10px">
              <div style="width:36px;height:36px;border-radius:10px;background:{cfg['color']}18;border:1px solid {cfg['color']}30;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">{cfg["icon"]}</div>
              <div class="param-name" style="color:{cfg['color']}">{label_t}</div>
            </div>
            <span class="param-oob">OOB R² = {cfg["oob"]:.3f}</span>
          </div>
          <div class="param-desc">{desc_t}</div>
          <div class="param-meta">
            <div class="pmi">{t("param_unidad", LANG)}: <span class="pmv">{cfg["unidad"]}</span></div>
            <div class="pmi">{t("param_rango", LANG)}: <span class="pmv">{cfg["vmin"]}–{cfg["vmax"]} {cfg["unidad"]}</span></div>
            <div class="pmi">{t("param_estado", LANG)}: <span class="pmv" style="color:rgba(16,185,129,.9)">✓ {t("param_bueno", LANG)}</span></div>
          </div></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── TABLA DE DATOS HISTÓRICOS EXPORTABLE ──────────────────────────────────
    if df_global is not None:
        st.markdown('<div class="sec-t">📊&nbsp; Datos históricos de campo · Serie completa</div>', unsafe_allow_html=True)
        _param_cols = [c for c in ["P_TOT","N_NH3","N_TOT","N_TOTK"] if c in df_global.columns]
        _df_show = df_global[["target_date","nombre"] + _param_cols].copy()
        _df_show["target_date"] = pd.to_datetime(_df_show["target_date"]).dt.strftime("%Y-%m-%d")
        _df_show = _df_show.sort_values(["target_date","nombre"])
        _th = "".join(f'<th>{c}</th>' for c in (["Fecha","Punto"] + _param_cols))
        _rows_html = ""
        for _, row in _df_show.iterrows():
            _cells = f'<td class="fecha-col">{row["target_date"]}</td><td class="punto-col">{row["nombre"]}</td>'
            for c in _param_cols:
                v = row[c]
                _nom_lim = NOM_LIMITS.get(c, {}).get("lim", None)
                if pd.isna(v):
                    _cells += '<td style="color:rgba(255,255,255,.2)">—</td>'
                elif _nom_lim and v > _nom_lim * 0.9:
                    _css = "nom-val-err" if v > _nom_lim else "nom-val-warn"
                    _cells += f'<td class="nom-val {_css}">{v:.2f}</td>'
                else:
                    _cells += f'<td class="nom-val nom-val-ok">{v:.2f}</td>'
            _rows_html += f"<tr>{_cells}</tr>"
        st.markdown(f"""<div class="data-table-wrap">
          <div class="data-table-header">
            <div class="nom-title">📋 {len(_df_show)} registros · 19 campañas · 7 puntos</div>
            <div style="display:flex;gap:6px">
              <span class="nom-badge nom-badge-ok">● OK</span>
              <span class="nom-badge nom-badge-warn">● ≥90% límite</span>
              <span class="nom-badge nom-badge-err">● Excede NOM</span>
            </div>
          </div>
          <div class="data-tbl-scroll">
          <table class="data-tbl"><thead><tr>{_th}</tr></thead><tbody>{_rows_html}</tbody></table>
          </div></div>""", unsafe_allow_html=True)
        _csv_buf = _df_show.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Descargar CSV histórico completo", _csv_buf,
            "datos_campo_pesqueria.csv", "text/csv", use_container_width=True, key="dl_hist_csv")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Reporte de Serie Temporal Completa (opcional) ──────────────────────────
    st.markdown(f'<div class="sec-t">{t("serie_titulo", LANG)}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="step-box"><div class="step-b">{t("serie_caption", LANG)}</div></div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    gen_serie = st.button(t("serie_generar_btn", LANG),
                          use_container_width=True,
                          disabled=(wmask_zip is None or not params_sel))

    if gen_serie and wmask_zip is not None:
        with st.spinner(t("serie_calculando", LANG)):
            try:
                with tempfile.TemporaryDirectory() as tmpdir2:
                    with zipfile.ZipFile(wmask_zip, "r") as z: z.extractall(tmpdir2)
                    shp2 = [f for f in os.listdir(tmpdir2) if f.endswith(".shp")]
                    wmask_serie = gpd.read_file(os.path.join(tmpdir2, shp2[0]))
                    if wmask_serie.crs is None or wmask_serie.crs.to_epsg()!=4326:
                        wmask_serie = wmask_serie.to_crs(4326)
                    union_serie = wmask_serie.geometry.unary_union
                    bounds_serie = wmask_serie.total_bounds

                lon_min_s, lat_min_s, lon_max_s, lat_max_s = bounds_serie
                RES_S = 150  # resolucion reducida para velocidad en serie temporal
                lon_vec_s = np.linspace(lon_min_s, lon_max_s, RES_S)
                lat_vec_s = np.linspace(lat_min_s, lat_max_s, RES_S)
                lon_grid_s, lat_grid_s = np.meshgrid(lon_vec_s, lat_vec_s)
                pts_grid_s = np.column_stack([lon_grid_s.ravel(), lat_grid_s.ravel()])
                mask_flat_s = np.array([union_serie.contains(Point(x,y)) for x,y in pts_grid_s])
                mask_2d_s = mask_flat_s.reshape(RES_S, RES_S)

                puntos_uniq_s = sorted(COORDS.keys())
                lons_s = np.array([COORDS[p][0] for p in puntos_uniq_s])
                lats_s = np.array([COORDS[p][1] for p in puntos_uniq_s])
                pts_known_s = np.column_stack([lons_s, lats_s])

                resultados_por_fecha = {}
                pbar = st.progress(0)
                for i_f, fecha_str in enumerate(FECHAS_CAMPO):
                    fecha_dt_s = pd.to_datetime(fecha_str, format="%m/%d/%Y")
                    df_fecha_s = df_global[df_global["target_date"] == fecha_dt_s]
                    if len(df_fecha_s) == 0:
                        continue

                    resultados_por_fecha[fecha_str] = {}
                    for col_s in params_sel:
                        if col_s not in PARAMS or col_s not in model_data["models"]:
                            continue
                        vals_s = []
                        for p in puntos_uniq_s:
                            fila_s = df_fecha_s[df_fecha_s["nombre"]==p]
                            vals_s.append(float(fila_s[col_s].values[0]) if len(fila_s)>0 else np.nan)
                        vals_s = np.array(vals_s); ok_s = np.isfinite(vals_s)
                        if ok_s.sum() < 3: continue

                        try:
                            rbf_s = RBFInterpolator(pts_known_s[ok_s], vals_s[ok_s],
                                                    kernel="thin_plate_spline", smoothing=0.1)
                            z_flat_s = rbf_s(pts_grid_s)
                        except Exception:
                            z_flat_s = griddata(pts_known_s[ok_s], vals_s[ok_s],
                                                pts_grid_s, method="nearest")

                        z_2d_s = np.where(mask_2d_s, z_flat_s.reshape(RES_S,RES_S), np.nan)
                        d_s = z_2d_s[np.isfinite(z_2d_s)]
                        if len(d_s) > 0:
                            resultados_por_fecha[fecha_str][col_s] = {
                                "mean": float(d_s.mean()),
                                "max": float(d_s.max()),
                                "min": float(d_s.min()),
                            }
                    pbar.progress((i_f+1)/len(FECHAS_CAMPO))

                pbar.empty()

                if len(resultados_por_fecha) >= 2:
                    _logo_geo_path_s = os.path.join(os.path.dirname(__file__), "logo_geomatica.png")
                    if not os.path.exists(_logo_geo_path_s):
                        _logo_geo_path_s = None
                    pdf_serie_buf = generar_pdf_serie_temporal(
                        resultados_por_fecha, params_sel, bounds_serie,
                        len(puntos_uniq_s), PARAMS, logo_geo_path=_logo_geo_path_s
                    )
                    st.success(f'{t("serie_exito", LANG)} {len(resultados_por_fecha)} {t("serie_fechas", LANG)}')
                    st.download_button(
                        t("serie_descargar_btn", LANG),
                        pdf_serie_buf.getvalue(),
                        f"Reporte_SerieTemporal_Pesqueria_{date_cls.today().strftime('%Y%m%d')}.pdf",
                        "application/pdf", use_container_width=True, type="primary"
                    )
                else:
                    st.warning(t("serie_sin_datos", LANG))

            except Exception as e:
                st.error(f'{t("serie_error", LANG)} {e}')

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown(f'<div class="sec-t">{t("investigador_titulo", LANG)}</div>', unsafe_allow_html=True)
    photo_src = f"data:image/png;base64,{PHOTO_B64}" if PHOTO_B64 else ""
    st.markdown(f"""<div class="researcher-card">
      <img class="rphoto" src="{photo_src}">
      <div><div class="rname">Kevin David Rodríguez González</div>
      <div class="rtitle">{t("investigador_cargo", LANG)}</div>
      <div class="rdept">{t("investigador_depto", LANG)}</div>
      <div class="rlinks">
        <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
        <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">🔗 ORCID</a>
      </div></div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="footer">{t("footer_texto", LANG)}</div>""",
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

status.text(t("cargando_shapefile", LANG))
with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(wmask_zip,"r") as z: z.extractall(tmpdir)
    shp=[f for f in os.listdir(tmpdir) if f.endswith(".shp")]
    if not shp: st.error("No .shp"); st.stop()
    wmask = gpd.read_file(os.path.join(tmpdir, shp[0]))
    if wmask.crs is None or wmask.crs.to_epsg()!=4326: wmask=wmask.to_crs(4326)
    union_geom = wmask.geometry.unary_union
    bounds = wmask.total_bounds
progress.progress(25)

# Capturar imagen RGB satelital del area de estudio para el reporte PDF
rgb_satelital_buf = None
if GEE_OK:
    status.text(t("obteniendo_imagen", LANG))
    try:
        _wmask_geojson = wmask.geometry.union_all().__geo_interface__
        _, tile_urls_pdf = buscar_imagen_s2(
            tuple(bounds), fecha_ini.strftime("%Y-%m-%d"),
            fecha_fin.strftime("%Y-%m-%d"), max_nubes,
            geojson_poligono=_wmask_geojson
        )
        if tile_urls_pdf and "RGB" in tile_urls_pdf:
            # Geometría exacta del polígono (no el bbox rectangular) para
            # que el thumbnail del reporte PDF se recorte con la silueta
            # real del área de estudio subida por el usuario.
            geom_r = ee.Geometry(_wmask_geojson, opt_geodesic=False)
            coll_r = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                        .filterBounds(geom_r)
                        .filterDate(fecha_ini.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"))
                        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_nubes))
                        .sort("CLOUDY_PIXEL_PERCENTAGE"))
            if coll_r.size().getInfo() > 0:
                # Mosaico (no .first()) para cubrir el área completa sin huecos
                img_r = coll_r.sort("CLOUDY_PIXEL_PERCENTAGE", False).mosaic().clip(geom_r)
                thumb_url = img_r.getThumbURL({
                    "bands": ["B4","B3","B2"], "min": 0, "max": 3000,
                    "gamma": 1.3, "dimensions": 800, "format": "png",
                    "region": geom_r,
                })
                import requests as _req
                resp_r = _req.get(thumb_url, timeout=15)
                if resp_r.status_code == 200:
                    rgb_satelital_buf = io.BytesIO(resp_r.content)
    except Exception:
        rgb_satelital_buf = None
progress.progress(35)

status.text(t("generando_grilla", LANG))
lon_min,lat_min,lon_max,lat_max = bounds
RES = resolucion
lon_vec=np.linspace(lon_min,lon_max,RES); lat_vec=np.linspace(lat_min,lat_max,RES)
lon_grid,lat_grid=np.meshgrid(lon_vec,lat_vec)
pts_grid=np.column_stack([lon_grid.ravel(),lat_grid.ravel()])
extent=[lon_min,lon_max,lat_min,lat_max]
mask_flat=np.array([union_geom.contains(Point(x,y)) for x,y in pts_grid])
mask_2d=mask_flat.reshape(RES,RES)
progress.progress(60)

status.text(t("aplicando_modelo", LANG))
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

status.text(t("generando_visualizaciones", LANG))
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
    ai.set_title(f"{info['label']} | Río Pesquería | {fecha_campo_dt.strftime('%d/%m/%Y')}",
                color="white",fontsize=11,fontweight="bold")
    ai.text(0.99,0.01,"Kevin D. Rodríguez G. · UANL · Depto. Geomática",
           transform=ai.transAxes,fontsize=7,color="#8EAAC8",ha="right",va="bottom")
    ai.tick_params(colors="#8EAAC8",labelsize=7)
    for sp in ai.spines.values(): sp.set_edgecolor("#2E8B8B44")
    plt.tight_layout(); fi.savefig(bi,dpi=180,bbox_inches="tight",facecolor="#0D1117")
    buf_ind[col]=bi; plt.close(fi)
    mapas[col]["individual_buf"] = bi

for k in range(n,len(axes_flat)): axes_flat[k].set_visible(False)
mes2=fecha_campo_dt.month
temp="Temporada Seca 🌵" if mes2 in [11,12,1,2,3] else "Temporada Lluviosa 🌧️"
fig.suptitle(f"Calidad de Agua — Río Pesquería\n{fecha_campo_dt.strftime('%d/%m/%Y')} | {temp} | UANL·FIC·Geomática",
            fontsize=13,fontweight="bold",color="white",y=1.01)
plt.tight_layout()
buf_panel=io.BytesIO()
fig.savefig(buf_panel,dpi=150,bbox_inches="tight",facecolor="#0D1117")
plt.close(fig); progress.progress(100); status.empty()

st.markdown(f"""<div class="status-row" style="margin-bottom:.8rem">
  <div class="status-item"><span class="status-dot-ok"></span><b>{n} {t("mapas_generados", LANG)}</b></div>
  <div class="status-sep"></div>
  <div class="status-item"><b>Fecha:</b> {fecha_campo_dt.strftime("%d/%m/%Y")}</div>
  <div class="status-sep"></div>
  <div class="status-item"><b>Temporada:</b> {temp}</div>
  <div class="status-badge">RF v3 · OOB ≥ 0.61</div>
</div>""", unsafe_allow_html=True)
st.image(buf_panel,caption=t("panel_caption", LANG),use_column_width=True)

# ── NOM-001 ALERT TABLE ──────────────────────────────────────────────────────
st.markdown('<div class="sec-t">⚠️&nbsp; Semáforo NOM-001-SEMARNAT-1996 · Valores por punto de muestreo</div>', unsafe_allow_html=True)
_nom_cols_active = [c for c in params_sel if c in mapas]
_leg = '<div class="nom-legend"><div class="nom-leg-item"><div class="nom-leg-dot" style="background:rgba(16,185,129,.8)"></div>OK</div><div class="nom-leg-item"><div class="nom-leg-dot" style="background:rgba(245,158,11,.8)"></div>≥90% límite</div><div class="nom-leg-item"><div class="nom-leg-dot" style="background:rgba(239,68,68,.8)"></div>Excede NOM</div></div>'
_nom_th = '<th>Punto</th><th>Coordenadas</th>' + "".join(
    f'<th>{PARAMS[c]["icon"]} {get_param_label(c, LANG)}<br><span style="font-weight:400;color:rgba(255,255,255,.3)">lím. {NOM_LIMITS[c]["lim"]} {PARAMS[c]["unidad"]}</span></th>'
    for c in _nom_cols_active
)
_nom_rows = ""
for j, punto in enumerate(puntos_uniq):
    lon_p, lat_p = COORDS[punto]
    _cells = f'<td class="nom-point">P{j+1} · {punto.replace("_"," ")}</td><td style="font-family:var(--f-mono);font-size:.65rem;color:rgba(255,255,255,.35)">{lat_p:.4f}°N · {abs(lon_p):.4f}°W</td>'
    _has_exc = False
    for c in _nom_cols_active:
        v = mapas[c]["vals_puntos"][j] if j < len(mapas[c]["vals_puntos"]) else float("nan")
        lim = NOM_LIMITS[c]["lim"]
        if np.isnan(v):
            _cells += '<td style="color:rgba(255,255,255,.2)">—</td>'
        elif v > lim:
            _cells += f'<td><div class="nom-badge nom-badge-err">● {v:.2f}</div></td>'
            _has_exc = True
        elif v > lim * 0.9:
            _cells += f'<td><div class="nom-badge nom-badge-warn">● {v:.2f}</div></td>'
        else:
            _cells += f'<td><div class="nom-badge nom-badge-ok">● {v:.2f}</div></td>'
    _nom_rows += f"<tr>{_cells}</tr>"

st.markdown(f"""<div class="nom-wrap">
  <div class="nom-header"><div class="nom-title">⚠ Norma Oficial Mexicana NOM-001-SEMARNAT-1996 · {fecha_campo_dt.strftime("%d/%m/%Y")}</div>{_leg}</div>
  <table class="nom-table"><thead><tr>{_nom_th}</tr></thead><tbody>{_nom_rows}</tbody></table>
</div>""", unsafe_allow_html=True)

st.markdown(f'<div class="dl-label">⬇&nbsp; {t("descargar_resultados", LANG)}</div>',unsafe_allow_html=True)
dl1,dl2,dl3=st.columns(3)
with dl1:
    st.download_button(t("descargar_panel_png", LANG),buf_panel.getvalue(),
        f"WaterQuality_{fecha_campo_dt.strftime('%Y%m%d')}.png","image/png",use_container_width=True)
with dl2:
    bz=io.BytesIO()
    with zipfile.ZipFile(bz,"w") as zf:
        for col,buf in buf_ind.items(): zf.writestr(f"mapa_{col}_{fecha_campo_dt.strftime('%Y%m%d')}.png",buf.getvalue())
    st.download_button(t("descargar_mapas_zip", LANG),bz.getvalue(),
        f"mapas_{fecha_campo_dt.strftime('%Y%m%d')}.zip","application/zip",use_container_width=True)
with dl3:
    with st.spinner(t("generando_pdf", LANG)):
        try:
            _logo_geo_path = os.path.join(os.path.dirname(__file__), "logo_geomatica.png")
            if not os.path.exists(_logo_geo_path):
                _logo_geo_path = None
            pdf_buf = generar_pdf_fecha_unica(
                mapas, fecha_campo_dt, temp, buf_panel,
                bounds, len(puntos_uniq), PARAMS,
                rgb_buf=rgb_satelital_buf, logo_geo_path=_logo_geo_path,
                lang=LANG
            )
            st.download_button(t("descargar_pdf_btn", LANG), pdf_buf.getvalue(),
                f"Reporte_CalidadAgua_{fecha_campo_dt.strftime('%Y%m%d')}.pdf",
                "application/pdf", use_container_width=True, type="primary")
        except Exception as e:
            st.error(f'{t("error_pdf", LANG)} {e}')

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown(f'<div class="sec-t">{t("estadisticas_espaciales", LANG)}</div>',unsafe_allow_html=True)
_stat_cards_html = '<div class="stat-grid">'
for param, info in mapas.items():
    d = info["data"][np.isfinite(info["data"])]
    label_stat_t = get_param_label(param, LANG)
    _col = info.get("color", PARAMS[param]["color"])
    _icon = PARAMS[param]["icon"]
    _unit = info["unidad"]
    _stat_cards_html += f"""<div class="stat-card">
      <div class="stat-glow" style="background:{_col}"></div>
      <div class="stat-card-header">
        <div class="stat-card-label">{_icon}&nbsp; {label_stat_t}</div>
        <div class="stat-card-unit">{_unit}</div>
      </div>
      <div class="stat-row">
        <div class="stat-item">
          <div class="stat-val" style="color:{_col}">{d.mean():.2f}</div>
          <div class="stat-name">{t("stat_media", LANG)}</div>
        </div>
        <div class="stat-item">
          <div class="stat-val" style="color:rgba(239,68,68,.85)">{d.max():.2f}</div>
          <div class="stat-name">{t("stat_maximo", LANG)}</div>
        </div>
        <div class="stat-item">
          <div class="stat-val" style="color:rgba(16,185,129,.85)">{d.min():.2f}</div>
          <div class="stat-name">{t("stat_minimo", LANG)}</div>
        </div>
      </div>
    </div>"""
_stat_cards_html += '</div>'
st.markdown(_stat_cards_html, unsafe_allow_html=True)

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown(f'<div class="sec-t">{t("investigador_titulo", LANG)}</div>',unsafe_allow_html=True)
st.markdown(f"""<div class="researcher-card">
  <img class="rphoto" src="data:image/png;base64,{PHOTO_B64}">
  <div><div class="rname">Kevin David Rodríguez González</div>
  <div class="rtitle">{t("investigador_cargo", LANG)}</div>
  <div class="rdept">{t("investigador_depto", LANG)}</div>
  <div class="rlinks">
    <a class="rlink" href="mailto:krodriguezge@uanl.edu.mx">✉ krodriguezge@uanl.edu.mx</a>
    <a class="rlink" href="https://orcid.org/0009-0004-3060-8575" target="_blank">🔗 ORCID</a>
  </div></div></div>""",unsafe_allow_html=True)

st.markdown(f"""<div class="footer">{t("footer_texto", LANG)}</div>""",
           unsafe_allow_html=True)
