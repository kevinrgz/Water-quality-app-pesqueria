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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ══ TOKENS ══════════════════════════════════════════════════════════════ */
:root{
  --bg:#080B0D; --s1:#0C1015; --s2:#111820;
  --v:#7C5CFC; --vs:rgba(124,92,252,.15); --vg:rgba(124,92,252,.3);
  --cy:#00C8FF; --cys:rgba(0,200,255,.12);
  --ok:#00E59A; --warn:#FFB800; --err:#FF4D4D;
  --t1:#DDE6EE; --t2:#4E6272; --t3:#222E38;
  --r:10px; --rl:16px;
  --f-sans:'Space Grotesk',system-ui,sans-serif;
  --f-mono:'JetBrains Mono',ui-monospace,monospace;
}

/* ── BASE ──────────────────────────────────────────────────────────────── */
html,body,.stApp,*:not(code):not(pre){font-family:var(--f-sans)!important}
code,pre,.stCode{font-family:var(--f-mono)!important}

/* dot-grid bg */
body,.stApp{
  background-color:var(--bg)!important;
  background-image:radial-gradient(circle,rgba(124,92,252,.055) 1px,transparent 1px)!important;
  background-size:28px 28px!important;
}

/* ── ANIMATIONS ──────────────────────────────────────────────────────────── */
@keyframes scanSweep{
  0%{top:-2px;opacity:0} 5%{opacity:.85} 95%{opacity:.85} 100%{top:100%;opacity:0}
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes glowIn{from{box-shadow:none}to{box-shadow:0 0 24px var(--vg)}}

/* ── SIDEBAR ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#09090D 0%,#080B0D 100%)!important;
  border-right:1px solid rgba(124,92,252,.15)!important;
}

/* ── STREAMLIT NATIVE OVERRIDES ──────────────────────────────────────────── */
.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div{
  background:var(--s1)!important;border:1px solid rgba(124,92,252,.18)!important;border-radius:var(--r)!important}
.stTextInput>div>div>input,.stDateInput>div>div>input{
  background:var(--s1)!important;border:1px solid rgba(124,92,252,.18)!important;
  color:var(--t1)!important;border-radius:var(--r)!important}
[data-testid="stFileUploader"]>div{
  background:var(--s1)!important;border:1px dashed rgba(124,92,252,.28)!important;border-radius:var(--r)!important}
.stSlider [role="slider"]{background:var(--v)!important}
[data-testid="stSliderTrackFill"]{background:var(--v)!important}

.stButton>button,.stDownloadButton>button{
  background:linear-gradient(135deg,var(--v),#5438C4)!important;
  border:none!important;color:#fff!important;font-weight:600!important;
  font-size:.85rem!important;letter-spacing:.02em!important;
  border-radius:var(--r)!important;padding:.55rem 1.2rem!important;
  transition:all .2s!important;box-shadow:0 2px 16px rgba(124,92,252,.2)!important}
.stButton>button:hover,.stDownloadButton>button:hover{
  background:linear-gradient(135deg,#8F72FD,#6B4FE4)!important;
  box-shadow:0 6px 28px rgba(124,92,252,.5)!important;transform:translateY(-1px)!important}
.stButton>button:disabled{
  background:rgba(124,92,252,.06)!important;color:var(--t3)!important;
  border:1px solid rgba(124,92,252,.1)!important;box-shadow:none!important;transform:none!important}

/* ── HEADER ──────────────────────────────────────────────────────────────── */
.hdr{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,#1C0E47 0%,#10083A 35%,#080B0D 100%);
  border-bottom:1px solid rgba(124,92,252,.45);
  padding:1.6rem 2rem 1.3rem;
  margin-bottom:1.5rem;
  border-radius:0 0 20px 20px;
  animation:fadeUp .45s ease forwards;
}
/* coordinate grid overlay */
.hdr::before{
  content:'';position:absolute;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(124,92,252,.08) 1px,transparent 1px),
    linear-gradient(90deg,rgba(124,92,252,.08) 1px,transparent 1px);
  background-size:48px 48px;
}
/* one-shot radar sweep */
.hdr::after{
  content:'';position:absolute;left:0;right:0;height:2px;top:0;pointer-events:none;
  background:linear-gradient(90deg,transparent 0%,rgba(0,200,255,.9) 50%,transparent 100%);
  animation:scanSweep 2s ease-out .4s forwards;
}
.hdr-logos{display:flex;align-items:center;gap:16px;margin-bottom:1rem;flex-wrap:wrap;position:relative;z-index:1}
.hdr-logo-img{height:50px;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,.6))}
.hdr-sep{width:1px;height:42px;background:rgba(124,92,252,.28);flex-shrink:0}
.hdr-body{position:relative;z-index:1}
.app-title{
  font-size:2.25rem;font-weight:700;color:#fff;margin:0;letter-spacing:-.3px;line-height:1.1;
  font-family:var(--f-sans)!important;display:inline;
}
.app-title .hl{color:var(--v)}
.hdr-live{
  display:inline-flex;align-items:center;gap:5px;margin-left:12px;
  background:rgba(0,229,154,.08);border:1px solid rgba(0,229,154,.28);
  border-radius:20px;padding:2px 10px;vertical-align:middle;position:relative;top:-5px;
  font-family:var(--f-mono)!important;font-size:.6rem;color:var(--ok);letter-spacing:.12em;
}
.hdr-live-dot{width:6px;height:6px;background:var(--ok);border-radius:50%;animation:blink 1.8s ease infinite}
.app-sub{
  font-size:.8rem;color:var(--t2);margin:.45rem 0 0;
  font-family:var(--f-mono)!important;letter-spacing:.02em;
}
.hdr-meta{
  display:flex;flex-wrap:wrap;gap:6px;margin-top:.9rem;
}
.hdr-tag{
  font-family:var(--f-mono)!important;font-size:.62rem;
  background:rgba(0,200,255,.06);border:1px solid rgba(0,200,255,.18);
  color:rgba(0,200,255,.7);border-radius:4px;padding:3px 10px;letter-spacing:.05em;
}
.hdr-tag b{color:rgba(0,200,255,.45);font-weight:500;margin-right:4px}

/* ── LABELS (sidebar + sections) ────────────────────────────────────────── */
.slabel{
  display:flex;align-items:center;gap:8px;
  font-family:var(--f-mono)!important;font-size:.6rem;
  color:var(--t2);text-transform:uppercase;letter-spacing:.14em;font-weight:700;
  margin-bottom:.4rem;
}
.slabel::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(124,92,252,.2),transparent)}
.sec-t{
  display:flex;align-items:center;gap:10px;
  font-family:var(--f-mono)!important;font-size:.63rem;
  color:var(--t2);text-transform:uppercase;letter-spacing:.14em;font-weight:700;
  margin:1.3rem 0 .7rem;
}
.sec-t::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(124,92,252,.15),transparent)}

/* ── METRIC CARDS ────────────────────────────────────────────────────────── */
.metric-row{display:flex;gap:10px;margin:1rem 0;flex-wrap:wrap}
.metric-card{
  flex:1;min-width:140px;background:var(--s1);
  border:1px solid rgba(124,92,252,.14);border-top:2px solid var(--v);
  border-radius:0 0 var(--r) var(--r);padding:1rem 1.2rem;text-align:center;
  transition:border-color .25s,box-shadow .25s;
}
.metric-card:hover{border-color:rgba(124,92,252,.4);box-shadow:0 4px 24px rgba(124,92,252,.12)}
.metric-value{font-family:var(--f-mono)!important;font-size:2rem;font-weight:700;color:var(--v);line-height:1.1}
.metric-label{font-family:var(--f-mono)!important;font-size:.59rem;color:var(--t2);text-transform:uppercase;letter-spacing:.1em;margin-top:4px}
.badge-ok{
  display:inline-block;margin-top:8px;background:rgba(0,229,154,.07);
  color:var(--ok);border:1px solid rgba(0,229,154,.22);
  padding:2px 10px;border-radius:20px;font-size:.6rem;font-weight:600;
  font-family:var(--f-mono)!important;
}

/* ── MAP PANELS ──────────────────────────────────────────────────────────── */
.map-panel{
  background:var(--s1);
  border:1px solid rgba(124,92,252,.12);border-top:2px solid rgba(0,200,255,.38);
  border-radius:0 0 var(--rl) var(--rl);padding:.9rem 1.1rem;margin-bottom:1rem;
}
.map-title{
  font-family:var(--f-mono)!important;font-size:.62rem;font-weight:700;
  color:var(--cy);letter-spacing:.14em;text-transform:uppercase;margin-bottom:.6rem;
}
.map-meta{font-size:.7rem;color:var(--t2);margin-top:.5rem;line-height:1.65;font-family:var(--f-mono)!important}

/* ── CHIPS ───────────────────────────────────────────────────────────────── */
.chip{
  display:inline-block;background:rgba(124,92,252,.07);
  border:1px solid rgba(124,92,252,.22);color:#A78BFA;
  font-size:.62rem;border-radius:4px;padding:3px 8px;margin:2px;
  font-family:var(--f-mono)!important;
}
.chip-warn{background:rgba(255,184,0,.06);border-color:rgba(255,184,0,.28);color:var(--warn)}
.chip-bad{background:rgba(255,77,77,.06);border-color:rgba(255,77,77,.28);color:var(--err)}

/* ── INFO PANELS ─────────────────────────────────────────────────────────── */
.info-panel{background:var(--s1);border:1px solid rgba(255,255,255,.05);border-radius:var(--rl);padding:.9rem 1.1rem;margin-bottom:1rem}
.info-title{font-family:var(--f-mono)!important;font-size:.62rem;font-weight:700;color:var(--t2);letter-spacing:.12em;text-transform:uppercase;margin-bottom:.6rem}

/* ── PARAM CARDS ─────────────────────────────────────────────────────────── */
.param-card{
  background:var(--s1);border:1px solid rgba(255,255,255,.04);
  border-left:2px solid var(--v);border-radius:0 var(--rl) var(--rl) 0;
  padding:1.1rem 1.4rem;margin-bottom:.7rem;
  transition:all .2s;
}
.param-card:hover{background:#0E1318;border-left-color:#A78BFA;box-shadow:-4px 0 20px rgba(124,92,252,.12)}
.param-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;flex-wrap:wrap;gap:8px}
.param-name{font-size:.95rem;font-weight:700;color:var(--t1)}
.param-oob{font-family:var(--f-mono)!important;font-size:.62rem;color:var(--v);background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.18);border-radius:20px;padding:2px 10px}
.param-desc{font-size:.77rem;color:var(--t2);line-height:1.7;margin-bottom:.65rem}
.param-meta{display:flex;gap:20px;flex-wrap:wrap}
.pmi{font-size:.7rem;color:var(--t2);font-family:var(--f-mono)!important}
.pmv{color:var(--v);font-weight:600}

/* ── STEP BOXES ──────────────────────────────────────────────────────────── */
.step-box{
  background:var(--s1);border:1px solid rgba(255,255,255,.05);
  border-radius:var(--rl);padding:1.3rem 1.4rem;
  position:relative;overflow:hidden;
  transition:border-color .25s,box-shadow .25s;
  animation:fadeUp .5s ease forwards;
}
.step-num{
  font-family:var(--f-mono)!important;font-size:.6rem;font-weight:700;
  color:var(--v);letter-spacing:.1em;text-transform:uppercase;
  margin-bottom:.6rem;opacity:.7;
}
.step-box:hover{border-color:rgba(124,92,252,.22);box-shadow:0 4px 24px rgba(124,92,252,.08)}
.step-t{font-size:.9rem;font-weight:700;color:var(--t1);margin-bottom:.5rem}
.step-b{font-size:.76rem;color:var(--t2);line-height:1.7}

/* ── RESEARCHER CARD ─────────────────────────────────────────────────────── */
.researcher-card{
  background:var(--s1);border:1px solid rgba(124,92,252,.14);border-radius:var(--rl);
  padding:1.3rem 1.7rem;display:flex;gap:20px;align-items:center;
}
.rphoto{width:88px;height:88px;border-radius:50%;object-fit:cover;border:2px solid var(--v);flex-shrink:0;box-shadow:0 0 0 5px rgba(124,92,252,.1)}
.rname{font-size:1rem;font-weight:700;color:var(--t1);margin:0 0 2px}
.rtitle{font-size:.8rem;color:var(--v);font-weight:600;margin:0 0 3px}
.rdept{font-size:.75rem;color:var(--t2);margin:0 0 10px}
.rlinks{display:flex;gap:8px;flex-wrap:wrap}
.rlink{font-size:.67rem;color:var(--t2);background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:3px 12px;text-decoration:none;font-family:var(--f-mono)!important;transition:border-color .2s,color .2s}
.rlink:hover{border-color:rgba(124,92,252,.4);color:#A78BFA}

/* ── MISC ────────────────────────────────────────────────────────────────── */
.divider{border:0;border-top:1px solid rgba(255,255,255,.05);margin:1.2rem 0}
.footer{text-align:center;font-family:var(--f-mono)!important;font-size:.62rem;color:var(--t3);margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.04)}

/* ── FOLIUM / LEAFLET ────────────────────────────────────────────────────── */
.leaflet-control-layers{
  font-family:var(--f-mono)!important;font-size:11px!important;
  background:var(--s1)!important;border:1px solid rgba(124,92,252,.3)!important;
  border-radius:var(--r)!important;box-shadow:0 4px 20px rgba(0,0,0,.6)!important;
}
.leaflet-control-layers-list{padding:6px 8px!important}
.leaflet-control-layers label{color:#C0CCD8!important;font-size:11px!important;line-height:1.7!important;font-weight:500!important}
.leaflet-control-layers-separator{border-color:rgba(124,92,252,.14)!important;margin:4px 0!important}
.leaflet-control-layers-base label,.leaflet-control-layers-overlays label{display:flex!important;align-items:center!important;gap:5px!important}
.leaflet-control-layers-toggle{background-color:var(--s1)!important;border-radius:var(--r)!important}

/* ── KEEP FONT FAMILY OUT OF CODE ───────────────────────────────────────── */

body,.stApp{background-color:#0B0C0E!important}
section[data-testid="stSidebar"]{background-color:#0E0F11!important;border-right:1px solid rgba(124,92,252,.12)!important}

/* Streamlit native element overrides */
.stSelectbox>div>div>div,.stMultiSelect>div>div{
    background:#111214!important;border-color:rgba(124,92,252,.2)!important}
.stTextInput>div>div>input,.stDateInput>div>div>input{
    background:#111214!important;border-color:rgba(124,92,252,.2)!important;color:#e8e6f0!important}
.stSlider [data-baseweb="slider"] [role="slider"]{background:#7C5CFC!important}
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrackFill"]{background:#7C5CFC!important}

/* Primary buttons — violet gradient */
.stButton>button,.stDownloadButton>button{
    background:linear-gradient(135deg,#7C5CFC 0%,#5B3FD4 100%)!important;
    border:none!important;color:#fff!important;font-weight:600!important;
    letter-spacing:.01em!important;border-radius:8px!important;
    transition:all .2s ease!important}
.stButton>button:hover,.stDownloadButton>button:hover{
    background:linear-gradient(135deg,#8F72FD 0%,#6B4FE4 100%)!important;
    box-shadow:0 4px 24px rgba(124,92,252,.4)!important;transform:translateY(-1px)!important}
.stButton>button:disabled{background:#1a1a2e!important;color:#4a4a6a!important;border:1px solid rgba(124,92,252,.15)!important}

/* ── Header ─────────────────────────────────────────────────────────────── */
.hdr{background:linear-gradient(135deg,#2D1B69 0%,#0B0C0E 68%);
     border-bottom:1px solid rgba(124,92,252,.35);
     padding:1.4rem 2rem 1.1rem;margin-bottom:1.2rem;
     border-radius:0 0 16px 16px;
     box-shadow:0 8px 48px rgba(124,92,252,.1)}
.hdr-logos{display:flex;align-items:center;gap:16px;margin-bottom:.9rem;flex-wrap:wrap}
.hdr-logo-img{height:54px;object-fit:contain}
.hdr-sep{width:1px;height:46px;background:rgba(124,92,252,.3);flex-shrink:0}
.app-title{font-size:2.1rem;font-weight:800;color:#fff;margin:0;letter-spacing:-.5px;line-height:1.15}
.app-sub{font-size:.87rem;color:#9D94C4;margin:.35rem 0 0;font-weight:400;letter-spacing:.01em}

/* ── Metric cards ────────────────────────────────────────────────────────── */
.metric-row{display:flex;gap:12px;margin:1rem 0;flex-wrap:wrap}
.metric-card{flex:1;min-width:130px;background:linear-gradient(145deg,#111214,#0E0F11);
             border:1px solid rgba(124,92,252,.18);border-radius:14px;padding:1rem;
             text-align:center;transition:border-color .25s,box-shadow .25s}
.metric-card:hover{border-color:rgba(124,92,252,.4);box-shadow:0 4px 20px rgba(124,92,252,.1)}
.metric-value{font-size:1.85rem;font-weight:700;color:#7C5CFC;font-family:'JetBrains Mono',monospace!important}
.metric-label{font-size:.67rem;color:#9D94C4;text-transform:uppercase;letter-spacing:.09em;margin-top:4px;font-family:'JetBrains Mono',monospace!important}
.badge-ok{display:inline-block;margin-top:8px;background:rgba(61,186,122,.1);color:#3DBA7A;
          border:1px solid rgba(61,186,122,.3);padding:2px 12px;border-radius:20px;
          font-size:.67rem;font-weight:700;font-family:'JetBrains Mono',monospace!important}

/* ── Map panels ──────────────────────────────────────────────────────────── */
.map-panel{background:#111214;border:1px solid rgba(124,92,252,.15);border-radius:14px;padding:.85rem 1rem;margin-bottom:1rem}
.map-title{font-size:.7rem;font-weight:700;color:#7C5CFC;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.5rem;font-family:'JetBrains Mono',monospace!important}
.map-meta{font-size:.72rem;color:#9D94C4;margin-top:.5rem;line-height:1.6}

/* ── Chips ───────────────────────────────────────────────────────────────── */
.chip{display:inline-block;background:#160E30;border:1px solid rgba(124,92,252,.28);
      color:#A78BFA;font-size:.67rem;border-radius:4px;padding:2px 8px;margin:2px;font-family:'JetBrains Mono',monospace!important}
.chip-warn{background:#1a1200;border-color:rgba(255,215,0,.35);color:#FFD700}
.chip-bad{background:#1a0808;border-color:rgba(231,76,60,.35);color:#E74C3C}

/* ── Info panels ─────────────────────────────────────────────────────────── */
.info-panel{background:#111214;border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:.85rem 1rem;margin-bottom:1rem}
.info-title{font-size:.7rem;font-weight:700;color:#9D94C4;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.5rem;font-family:'JetBrains Mono',monospace!important}

/* ── Param cards ─────────────────────────────────────────────────────────── */
.param-card{background:#111214;border:1px solid rgba(255,255,255,.07);border-left:2px solid #7C5CFC;
            border-radius:0 12px 12px 0;padding:1.1rem 1.4rem;margin-bottom:.75rem;
            transition:border-left-color .2s,background .2s}
.param-card:hover{background:#131416;border-left-color:#A78BFA}
.param-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:.55rem;flex-wrap:wrap;gap:8px}
.param-name{font-size:.95rem;font-weight:700;color:#fff}
.param-oob{font-size:.67rem;color:#7C5CFC;background:#160E30;border:1px solid rgba(124,92,252,.22);border-radius:20px;padding:2px 10px;font-family:'JetBrains Mono',monospace!important}
.param-desc{font-size:.78rem;color:#9D94C4;line-height:1.65;margin-bottom:.65rem}
.param-meta{display:flex;gap:20px;flex-wrap:wrap}
.pmi{font-size:.72rem;color:#9D94C4}
.pmv{color:#7C5CFC;font-weight:600;font-family:'JetBrains Mono',monospace!important}

/* ── Step boxes ──────────────────────────────────────────────────────────── */
.step-box{background:#111214;border:1px solid rgba(255,255,255,.06);border-left:2px solid #7C5CFC;
          border-radius:0 10px 10px 0;padding:1rem 1.2rem}
.step-t{font-size:.88rem;font-weight:700;color:#fff;margin-bottom:.5rem}
.step-b{font-size:.76rem;color:#9D94C4;line-height:1.65}

/* ── Researcher card ─────────────────────────────────────────────────────── */
.researcher-card{background:linear-gradient(145deg,#111214,#0E0F11);border:1px solid rgba(124,92,252,.18);
                 border-radius:16px;padding:1.3rem 1.7rem;display:flex;gap:20px;align-items:center}
.rphoto{width:88px;height:88px;border-radius:50%;object-fit:cover;border:2px solid #7C5CFC;flex-shrink:0;box-shadow:0 0 0 4px rgba(124,92,252,.15)}
.rname{font-size:1rem;font-weight:700;color:#fff;margin:0 0 2px}
.rtitle{font-size:.8rem;color:#7C5CFC;font-weight:600;margin:0 0 3px}
.rdept{font-size:.76rem;color:#9D94C4;margin:0 0 9px}
.rlinks{display:flex;gap:9px;flex-wrap:wrap}
.rlink{font-size:.70rem;color:#9D94C4;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
       border-radius:20px;padding:3px 11px;text-decoration:none;transition:border-color .2s,color .2s}
.rlink:hover{border-color:rgba(124,92,252,.45);color:#A78BFA}

/* ── Misc ────────────────────────────────────────────────────────────────── */
.divider{border:0;border-top:1px solid rgba(255,255,255,.05);margin:1.1rem 0}
.sec-t{font-size:.7rem;font-weight:700;color:#9D94C4;letter-spacing:.12em;text-transform:uppercase;margin:1.1rem 0 .6rem;font-family:'JetBrains Mono',monospace!important}
.slabel{font-size:.67rem;color:#9D94C4;text-transform:uppercase;letter-spacing:.12em;font-weight:700;margin-bottom:.3rem;font-family:'JetBrains Mono',monospace!important}
.footer{text-align:center;font-size:.67rem;color:#3A3560;margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.04);font-family:'JetBrains Mono',monospace!important}

/* ── Folium / Leaflet controls ───────────────────────────────────────────── */
.leaflet-control-layers{
    font-family:'Inter',sans-serif!important;font-size:11px!important;
    background:#111214!important;border:1px solid rgba(124,92,252,.35)!important;
    border-radius:10px!important;box-shadow:0 4px 16px rgba(0,0,0,.5)!important}
.leaflet-control-layers-list{padding:6px 8px!important}
.leaflet-control-layers label{
    color:#D0CCEC!important;font-size:11px!important;line-height:1.6!important;
    font-weight:500!important;margin-bottom:2px!important}
.leaflet-control-layers-separator{border-color:rgba(124,92,252,.18)!important;margin:4px 0!important}
.leaflet-control-layers-base label,.leaflet-control-layers-overlays label{
    display:flex!important;align-items:center!important;gap:4px!important}
.leaflet-control-layers-toggle{background-color:#111214!important;border-radius:10px!important}
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
            map_id  = idx_img.getMapId(INDICES_VIZ[idx_name]["vis"])
            tile_urls[idx_name] = map_id["tile_fetcher"].url_format

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

st.markdown(f"""
<div class="hdr">
  <div class="hdr-logos">{logo_u}<div class="hdr-sep"></div>{logo_f}<div class="hdr-sep"></div>{logo_g}</div>
  <div class="hdr-body">
    <div>
      <span class="app-title">{t("app_title", LANG)}</span>
      <span class="hdr-live"><span class="hdr-live-dot"></span>LIVE</span>
    </div>
    <div class="app-sub">{t("app_subtitle", LANG)}</div>
    <div class="hdr-meta">
      <span class="hdr-tag"><b>SAT</b> Sentinel-2 SR · 10 m</span>
      <span class="hdr-tag"><b>MDL</b> Random Forest · 4 params</span>
      <span class="hdr-tag"><b>LAT</b> 25.77° – 25.83° N</span>
      <span class="hdr-tag"><b>LON</b> 100.34° – 100.02° W</span>
      <span class="hdr-tag"><b>EPSG</b> 4326</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if model_data is None:
    _err = st.session_state.get("_model_load_error", "Unknown")
    st.error(f'{t("error_modelo", LANG)} {_err}')
    st.stop()
if df_global is None:
    st.error(t("error_csv", LANG)); st.stop()

col_status1, col_status2 = st.columns(2)
with col_status1:
    st.success(t("modelo_cargado", LANG))
with col_status2:
    if GEE_OK:
        st.success(t("gee_activo", LANG))
    else:
        st.warning(t("gee_no_disponible", LANG))

st.markdown('<hr class="divider">', unsafe_allow_html=True)

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
    valid = (wmask_zip is not None and params_sel and fecha_ini < fecha_fin
            and es_zona_pesqueria)
    correr = st.button(t("sidebar_generar_mapas", LANG), type="primary",
                       use_container_width=True, disabled=not valid)
    if wmask_zip is None:
        st.warning(t("sidebar_sube_wmask_warn", LANG))
    elif not es_zona_pesqueria:
        st.caption(t("zona_pesqueria_boton_disabled", LANG))

# ── PANTALLA INICIAL ──────────────────────────────────────────────────────────
if not correr:
    c1,c2,c3 = st.columns(3)
    for col, paso_num, paso_titulo, paso_texto in zip(
        [c1,c2,c3],
        ["01", "02", "03"],
        [t("paso1_titulo",LANG), t("paso2_titulo",LANG), t("paso3_titulo",LANG)],
        [t("paso1_texto",LANG), t("paso2_texto",LANG), t("paso3_texto",LANG)],
    ):
        with col:
            st.markdown(f'<div class="step-box">'
                       f'<div class="step-num">STEP {paso_num}</div>'
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
                for ic, idx_key in zip(idx_cols, ["RGB","NDVI","NDWI","MNDWI","NDTI"]):
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
                    for tc, idx_key in zip(tiff_cols, ["RGB","NDVI","NDWI","MNDWI","NDTI"]):
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
                            options=["RGB","NDVI","NDWI","MNDWI","NDTI"],
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
        st.markdown(f'<div class="sec-t">{t("puntos_titulo", LANG)}</div>', unsafe_allow_html=True)
        st.map(pd.DataFrame([{"lat":c[1],"lon":c[0]} for c in COORDS.values()]))
        st.info(t("sube_wmask_para_ver", LANG))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-t">{t("parametros_seccion_titulo", LANG)}</div>', unsafe_allow_html=True)
    for col,cfg in PARAMS.items():
        label_t = get_param_label(col, LANG)
        desc_t  = get_param_desc(col, LANG)
        st.markdown(f"""<div class="param-card">
          <div class="param-hdr"><div class="param-name">{cfg["icon"]} &nbsp;{label_t}</div>
          <span class="param-oob">OOB R² = {cfg["oob"]:.3f} · {t("param_validado", LANG)}</span></div>
          <div class="param-desc">{desc_t}</div>
          <div class="param-meta">
            <div class="pmi">{t("param_unidad", LANG)}: <span class="pmv">{cfg["unidad"]}</span></div>
            <div class="pmi">{t("param_rango", LANG)}: <span class="pmv">{cfg["vmin"]}–{cfg["vmax"]} {cfg["unidad"]}</span></div>
            <div class="pmi">{t("param_estado", LANG)}: <span class="pmv">{t("param_bueno", LANG)}</span></div>
          </div></div>""", unsafe_allow_html=True)

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

st.success(f'✅  {n} {t("mapas_generados", LANG)} {fecha_campo_dt.strftime("%d/%m/%Y")} · {temp}')
st.image(buf_panel,caption=t("panel_caption", LANG),use_column_width=True)

st.markdown(f'<div class="sec-t">{t("descargar_resultados", LANG)}</div>',unsafe_allow_html=True)
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
cols_st=st.columns(len(mapas))
for cs,(param,info) in zip(cols_st,mapas.items()):
    d=info["data"][np.isfinite(info["data"])]
    label_stat_t = get_param_label(param, LANG)
    with cs:
        st.markdown(f"**{label_stat_t}**")
        st.metric(t("stat_media", LANG),f"{d.mean():.2f} {info['unidad']}")
        st.metric(t("stat_maximo", LANG),f"{d.max():.2f} {info['unidad']}")
        st.metric(t("stat_minimo", LANG),f"{d.min():.2f} {info['unidad']}")

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
