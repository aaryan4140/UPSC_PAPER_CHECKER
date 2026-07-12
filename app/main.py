"""Main Streamlit application entry point."""

import streamlit as st
import sys
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.state.session import SessionStateManager
from core.config import get_settings
from core.logging_config import setup_logging


def get_logo_base64():
    """Load UPSC logo image as base64 for embedding in HTML."""
    logo_path = Path(__file__).parent / "assets" / "images" / "image.png"
    if logo_path.exists():
        data = logo_path.read_bytes()
        return base64.b64encode(data).decode()
    return None




def _get_logo_html():
    """Return HTML img tag with the UPSC logo (base64 or fallback emoji)."""
    b64 = get_logo_base64()
    if b64:
        return f'<img src="data:image/png;base64,{b64}" style="width:68px; height:68px; border-radius:12px; object-fit:contain;" />'
    return '<span style="font-size:2.8rem;">🏛️</span>'


def configure_page():
    st.set_page_config(
        page_title="UPSC Answer Evaluator",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def inject_css():
    st.markdown("""
    <style>
    /* ===== HIDE DEFAULTS ===== */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    header[data-testid="stHeader"] { display: none !important; }

    /* ===== ANIMATIONS ===== */
    @keyframes slideDown { from { opacity:0; transform:translateY(-25px); } to { opacity:1; transform:translateY(0); } }
    @keyframes fadeInUp { from { opacity:0; transform:translateY(15px); } to { opacity:1; transform:translateY(0); } }
    @keyframes shimmer { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
    @keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-3px); } }
    @keyframes gradientShift { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
    @keyframes scaleIn { from { opacity:0; transform:scale(0.94); } to { opacity:1; transform:scale(1); } }
    @keyframes glowPulse { 0%,100% { box-shadow:0 0 8px rgba(21,101,192,0.2); } 50% { box-shadow:0 0 20px rgba(21,101,192,0.4); } }
    @keyframes coinFlip {
        0% { transform: translate(-50%,-50%) perspective(800px) rotateY(0deg); }
        25% { transform: translate(-50%,-50%) perspective(800px) rotateY(90deg); }
        50% { transform: translate(-50%,-50%) perspective(800px) rotateY(180deg); }
        75% { transform: translate(-50%,-50%) perspective(800px) rotateY(270deg); }
        100% { transform: translate(-50%,-50%) perspective(800px) rotateY(360deg); }
    }

    /* ===== CENTRAL WATERMARK LOGO (pure CSS, no container) ===== */
    .stApp::after {
        content: '';
        position: fixed;
        top: 50%;
        left: 50%;
        width: 520px;
        height: 520px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.18;
        animation: coinFlip 14s ease-in-out infinite;
        transform-style: preserve-3d;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='200' cy='200' r='190' fill='none' stroke='rgba(144,202,249,0.6)' stroke-width='2' stroke-dasharray='8 4'/%3E%3Ccircle cx='200' cy='200' r='180' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1.5'/%3E%3Cpath d='M80 200 Q80 140 120 100 Q100 130 95 160 Q90 190 95 200 Q90 210 95 240 Q100 270 120 300 Q80 260 80 200Z' fill='rgba(144,202,249,0.3)' stroke='rgba(144,202,249,0.5)' stroke-width='1'/%3E%3Cpath d='M90 200 Q92 155 125 115 Q108 145 105 170 Q100 195 105 200 Q100 205 105 230 Q108 255 125 285 Q92 245 90 200Z' fill='rgba(144,202,249,0.2)'/%3E%3Cellipse cx='95' cy='150' rx='8' ry='18' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(-20 95 150)'/%3E%3Cellipse cx='88' cy='180' rx='7' ry='15' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(-10 88 180)'/%3E%3Cellipse cx='88' cy='220' rx='7' ry='15' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(10 88 220)'/%3E%3Cellipse cx='95' cy='250' rx='8' ry='18' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(20 95 250)'/%3E%3Cpath d='M320 200 Q320 140 280 100 Q300 130 305 160 Q310 190 305 200 Q310 210 305 240 Q300 270 280 300 Q320 260 320 200Z' fill='rgba(144,202,249,0.3)' stroke='rgba(144,202,249,0.5)' stroke-width='1'/%3E%3Cpath d='M310 200 Q308 155 275 115 Q292 145 295 170 Q300 195 295 200 Q300 205 295 230 Q292 255 275 285 Q308 245 310 200Z' fill='rgba(144,202,249,0.2)'/%3E%3Cellipse cx='305' cy='150' rx='8' ry='18' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(20 305 150)'/%3E%3Cellipse cx='312' cy='180' rx='7' ry='15' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(10 312 180)'/%3E%3Cellipse cx='312' cy='220' rx='7' ry='15' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(-10 312 220)'/%3E%3Cellipse cx='305' cy='250' rx='8' ry='18' fill='none' stroke='rgba(144,202,249,0.4)' stroke-width='1' transform='rotate(-20 305 250)'/%3E%3Ccircle cx='200' cy='200' r='65' fill='none' stroke='rgba(144,202,249,0.8)' stroke-width='3'/%3E%3Ccircle cx='200' cy='200' r='55' fill='none' stroke='rgba(144,202,249,0.5)' stroke-width='1.5'/%3E%3Ccircle cx='200' cy='200' r='12' fill='rgba(144,202,249,0.6)'/%3E%3Ccircle cx='200' cy='200' r='8' fill='rgba(144,202,249,0.4)'/%3E%3Cg stroke='rgba(144,202,249,0.7)' stroke-width='1.8' stroke-linecap='round'%3E%3Cline x1='200' y1='145' x2='200' y2='188'/%3E%3Cline x1='200' y1='255' x2='200' y2='212'/%3E%3Cline x1='145' y1='200' x2='188' y2='200'/%3E%3Cline x1='255' y1='200' x2='212' y2='200'/%3E%3Cline x1='161' y1='161' x2='191' y2='191'/%3E%3Cline x1='239' y1='239' x2='209' y2='209'/%3E%3Cline x1='239' y1='161' x2='209' y2='191'/%3E%3Cline x1='161' y1='239' x2='191' y2='209'/%3E%3Cline x1='181' y1='148' x2='194' y2='189'/%3E%3Cline x1='219' y1='252' x2='206' y2='211'/%3E%3Cline x1='219' y1='148' x2='206' y2='189'/%3E%3Cline x1='181' y1='252' x2='194' y2='211'/%3E%3Cline x1='148' y1='181' x2='189' y2='194'/%3E%3Cline x1='252' y1='219' x2='211' y2='206'/%3E%3Cline x1='148' y1='219' x2='189' y2='206'/%3E%3Cline x1='252' y1='181' x2='211' y2='194'/%3E%3Cline x1='155' y1='170' x2='190' y2='192'/%3E%3Cline x1='245' y1='230' x2='210' y2='208'/%3E%3Cline x1='245' y1='170' x2='210' y2='192'/%3E%3Cline x1='155' y1='230' x2='190' y2='208'/%3E%3Cline x1='170' y1='155' x2='192' y2='190'/%3E%3Cline x1='230' y1='245' x2='208' y2='210'/%3E%3Cline x1='230' y1='155' x2='208' y2='190'/%3E%3Cline x1='170' y1='245' x2='192' y2='210'/%3E%3C/g%3E%3Ctext x='200' y='310' text-anchor='middle' fill='rgba(144,202,249,0.8)' font-size='38' font-weight='900' font-family='serif' letter-spacing='6'%3EUPSC%3C/text%3E%3Ctext x='200' y='345' text-anchor='middle' fill='rgba(144,202,249,0.6)' font-size='14' font-weight='600'%3E%E0%A4%B8%E0%A4%82%E0%A4%98 %E0%A4%B2%E0%A5%8B%E0%A4%95 %E0%A4%B8%E0%A5%87%E0%A4%B5%E0%A4%BE %E0%A4%86%E0%A4%AF%E0%A5%8B%E0%A4%97%3C/text%3E%3Cpath d='M140 80 Q200 50 260 80' fill='none' stroke='rgba(144,202,249,0.5)' stroke-width='2'/%3E%3Ccircle cx='200' cy='10' r='3' fill='rgba(144,202,249,0.5)'/%3E%3Ccircle cx='200' cy='390' r='3' fill='rgba(144,202,249,0.5)'/%3E%3Ccircle cx='10' cy='200' r='3' fill='rgba(144,202,249,0.5)'/%3E%3Ccircle cx='390' cy='200' r='3' fill='rgba(144,202,249,0.5)'/%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }

    /* ===== BACKGROUND - GREY BLACK + BLUE ===== */
    .stApp {
        background: linear-gradient(160deg, #0f0f0f 0%, #1a1a2e 25%, #16213e 50%, #1a1a1a 75%, #0d0d0d 100%) !important;
        background-attachment: fixed !important;
    }
    .stApp::before {
        content: '';
        position: fixed; top:0; left:0; width:100%; height:100%;
        background-image:
            radial-gradient(ellipse at 30% 20%, rgba(21,101,192,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 80%, rgba(13,71,161,0.04) 0%, transparent 50%);
        pointer-events: none; z-index: 0;
    }

    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 0rem; max-width: 1300px;
        animation: fadeInUp 0.5s ease-out;
        position: relative; z-index: 1;
    }

    /* ===== HEADER BAR ===== */
    .upsc-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #1a237e 40%, #1565c0 80%, #0d47a1 100%);
        background-size: 300% 300%;
        animation: gradientShift 12s ease infinite, slideDown 0.5s ease-out;
        padding: 0.8rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 1.2rem -1rem;
        display: flex; align-items: center; gap: 16px;
        box-shadow: 0 6px 30px rgba(0,0,0,0.5), 0 0 40px rgba(21,101,192,0.08);
        position: relative; overflow: hidden;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .upsc-header::after {
        content:''; position:absolute; top:0; left:-50%; width:200%; height:100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.02), transparent);
        animation: shimmer 6s linear infinite;
    }
    .upsc-header .logo { animation: float 4s ease-in-out infinite; z-index:2; }
    .upsc-header .brand { flex:1; z-index:2; }
    .upsc-header .brand-title {
        font-size:1.4rem; font-weight:800; color:white;
        letter-spacing:1.5px; text-transform:uppercase;
        text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }
    .upsc-header .brand-sub {
        font-size:0.6rem; color:rgba(255,255,255,0.5);
        letter-spacing:2.5px; text-transform:uppercase; margin-top:1px;
    }

    /* ===== PAGE TEXT ===== */
    .page-header { font-size:1.6rem; font-weight:800; color:#e3f2fd; margin-bottom:0.2rem; animation: fadeInUp 0.4s ease-out 0.1s both; }
    .page-subtitle { font-size:0.9rem; color:rgba(160,180,200,0.7); margin-bottom:1rem; animation: fadeInUp 0.4s ease-out 0.2s both; }

    /* ===== SCORE HERO ===== */
    .score-hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #1a237e 40%, #1565c0 100%);
        background-size: 200% 200%; animation: gradientShift 6s ease infinite;
        border-radius: 18px; padding: 2rem; color:white; text-align:center; margin:1rem 0;
        box-shadow: 0 10px 35px rgba(0,0,0,0.4); border: 1px solid rgba(21,101,192,0.25);
        position:relative; overflow:hidden;
    }
    .score-hero::before { content:''; position:absolute; top:0; left:-100%; width:200%; height:100%; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.02),transparent); animation:shimmer 3s infinite; }
    .score-hero .big { font-size:3.2rem; font-weight:800; text-shadow:0 2px 8px rgba(0,0,0,0.4); }
    .score-hero .label { font-size:0.85rem; opacity:0.75; }

    /* ===== CARDS ===== */
    .metric-card {
        background: rgba(20,20,35,0.8); border-radius:14px; padding:1.2rem;
        border: 1px solid rgba(21,101,192,0.25); text-align:center;
        transition: all 0.3s ease; backdrop-filter:blur(6px);
    }
    .metric-card:hover { transform:translateY(-3px); border-color:rgba(21,101,192,0.5); box-shadow:0 6px 20px rgba(21,101,192,0.15); }
    .metric-card .label { font-size:0.75rem; color:rgba(160,180,200,0.6); text-transform:uppercase; letter-spacing:0.5px; }
    .metric-card .value { font-size:1.6rem; font-weight:700; color:#90caf9; margin:4px 0; }

    .question-card {
        background: rgba(20,20,35,0.7); border-radius:14px; padding:1.3rem;
        border: 1px solid rgba(21,101,192,0.2); margin:0.8rem 0;
        transition: all 0.3s ease; backdrop-filter:blur(6px);
    }
    .question-card:hover { border-color:rgba(21,101,192,0.4); }

    /* ===== RUBRIC BARS ===== */
    .rubric-bar { display:flex; align-items:center; margin:6px 0; }
    .rubric-bar .name { width:130px; font-size:0.8rem; color:#78909c; font-weight:500; }
    .rubric-bar .bar-bg { flex:1; height:8px; background:rgba(21,101,192,0.12); border-radius:4px; margin:0 10px; overflow:hidden; }
    .rubric-bar .bar-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#1a237e,#1565c0,#42a5f5); background-size:200% 100%; animation:shimmer 2.5s ease infinite; }
    .rubric-bar .score { font-size:0.8rem; color:#90caf9; width:55px; font-weight:700; }

    /* ===== BADGES ===== */
    .missing-high { background:rgba(198,40,40,0.2); color:#ef9a9a; padding:4px 10px; border-radius:16px; font-size:0.78rem; margin:2px; display:inline-block; border:1px solid rgba(198,40,40,0.35); }
    .missing-medium { background:rgba(230,81,0,0.2); color:#ffcc80; padding:4px 10px; border-radius:16px; font-size:0.78rem; margin:2px; display:inline-block; border:1px solid rgba(230,81,0,0.35); }
    .missing-low { background:rgba(21,101,192,0.2); color:#90caf9; padding:4px 10px; border-radius:16px; font-size:0.78rem; margin:2px; display:inline-block; border:1px solid rgba(21,101,192,0.35); }

    /* ===== FEEDBACK BOX ===== */
    .feedback-box {
        background:rgba(21,101,192,0.08); border-left:3px solid #42a5f5;
        padding:1rem 1.2rem; border-radius:0 10px 10px 0; margin:0.6rem 0; color:#b0bec5;
    }

    .low-confidence { background:#fbbf24; padding:1px 5px; border-radius:3px; font-weight:600; color:#1a1a2e; }

    /* ===== TABS - CLEAN, NO BLOCKING BOX ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: transparent !important;
        padding: 4px !important;
        border-radius: 0;
        border: none !important;
        border-bottom: 2px solid rgba(21,101,192,0.3) !important;
    }
    /* ALL tabs - active and inactive - look like buttons */
    .stTabs [data-baseweb="tab"],
    .stTabs [role="tab"],
    .stTabs [role="tab"][aria-selected="false"],
    .stTabs [data-baseweb="tab"][aria-selected="false"] {
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(66,165,245,0.5) !important;
        background: rgba(21,101,192,0.15) !important;
        transition: all 0.25s ease !important;
        opacity: 1 !important;
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [role="tab"] p,
    .stTabs [role="tab"] span,
    .stTabs [role="tab"][aria-selected="false"] p,
    .stTabs [role="tab"][aria-selected="false"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        opacity: 1 !important;
    }
    .stTabs [data-baseweb="tab"]:hover,
    .stTabs [role="tab"]:hover {
        color: #ffffff !important;
        background: rgba(21,101,192,0.3) !important;
        border-color: rgba(66,165,245,0.8) !important;
    }
    /* Active tab - slightly more prominent */
    .stTabs [aria-selected="true"],
    .stTabs [role="tab"][aria-selected="true"] {
        background: rgba(21,101,192,0.35) !important;
        color: #ffffff !important;
        border: 1.5px solid #42a5f5 !important;
        border-bottom: 3px solid #42a5f5 !important;
        box-shadow: 0 0 12px rgba(21,101,192,0.4) !important;
        opacity: 1 !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [role="tab"][aria-selected="true"] p,
    .stTabs [role="tab"][aria-selected="true"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    /* Remove tab highlight/border container */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] { color:#90caf9 !important; font-weight:700; }
    [data-testid="stMetricLabel"] { color:#78909c !important; }
    [data-testid="stMetric"] {
        background: rgba(20,20,35,0.7) !important; border-radius:12px; padding:10px;
        border: 1px solid rgba(21,101,192,0.2); transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover { transform:translateY(-2px); border-color:rgba(21,101,192,0.4); }

    /* ===== BUTTONS ===== */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.6px !important;
        padding: 0.85rem 1.6rem !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    /* Shrink file uploader box to match button height */
    [data-testid="stFileUploader"] section {
        padding: 0.8rem !important;
    }
    [data-testid="stFileUploader"] section > div {
        padding-top: 0.4rem !important;
        padding-bottom: 0.4rem !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1a237e 0%, #1565c0 100%) !important;
        border: 1px solid rgba(66,165,245,0.4) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(21,101,192,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 24px rgba(21,101,192,0.45) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(20,20,35,0.8) !important;
        color: #90caf9 !important;
        border: 1.5px solid rgba(21,101,192,0.35) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(21,101,192,0.15) !important;
        border-color: rgba(66,165,245,0.6) !important;
        transform: translateY(-2px) !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(21,101,192,0.35) !important;
        border-radius: 14px; padding: 1rem;
        background: rgba(13,27,62,0.3);
        transition: all 0.3s ease;
        max-width: 33%;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(66,165,245,0.6) !important;
        background: rgba(21,101,192,0.06);
    }

    /* ===== SELECTBOX & SLIDER ===== */
    [data-testid="stSelectbox"] label,
    .stSlider label {
        color: #90caf9 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background: rgba(20,20,35,0.9) !important;
        border: 1.5px solid rgba(21,101,192,0.3) !important;
        border-radius: 10px !important;
        color: #e3f2fd !important;
    }
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: rgba(66,165,245,0.6) !important;
    }
    .stSlider > div > div > div > div {
        background: #1565c0 !important;
    }

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: rgba(25, 35, 60, 0.9) !important;
        border-radius: 10px !important;
        border: 1.5px solid rgba(21,101,192,0.35) !important;
        color: #ffffff !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(66,165,245,0.6) !important;
        background: rgba(30, 45, 75, 0.95) !important;
    }
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }

    /* Expander content area - lighter background for readability */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: rgba(22, 30, 50, 0.95) !important;
        border: 1px solid rgba(21,101,192,0.2) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1.2rem !important;
    }

    /* Text areas (model/candidate answers) - HIGH CONTRAST */
    textarea {
        background: rgba(240, 245, 255, 0.95) !important;
        color: #1a1a2e !important;
        border: 1.5px solid rgba(21,101,192,0.4) !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        line-height: 1.5 !important;
    }

    /* Info boxes (Improvement Suggestions) - make text bright */
    [data-testid="stAlert"] {
        background: rgba(21, 40, 80, 0.85) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(21,101,192,0.35) !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {
        color: #e0e8f0 !important;
        font-size: 0.9rem !important;
    }

    /* ===== TEXT COLORS ===== */
    .stMarkdown p, .stMarkdown li, .stText, label { color: #cfd8dc !important; }
    h1, h2, h3, h4, h5 { color: #e3f2fd !important; }
    strong, b { color: #90caf9 !important; }
    hr { border-color: rgba(21,101,192,0.15) !important; }
    .stCaption, caption { color: #78909c !important; }

    /* ===== ALERTS ===== */
    [data-testid="stAlert"] {
        background: rgba(20,20,35,0.8) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(21,101,192,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header_and_nav(session: SessionStateManager):
    """Render header with UPSC logo and navigation (Settings as icon at right)."""
    current_page = session.get("current_page", "Dashboard")

    logo_html = _get_logo_html()
    header_html = f"""
    <div class="upsc-header">
        <div class="logo">{logo_html}</div>
        <div class="brand">
            <div class="brand-title">UPSC Evaluator</div>
            <div class="brand-sub">AI-Powered Answer Assessment</div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # Navigation: Dashboard + Analytics as tabs, Settings as small gear icon at right
    col_dash, col_analytics, col_spacer, col_gear = st.columns([1.2, 1.2, 4, 0.6])
    with col_dash:
        if st.button("📋  Dashboard", key="btn_dashboard", use_container_width=True,
                     type="primary" if current_page == "Dashboard" else "secondary"):
            session.set("current_page", "Dashboard")
            st.rerun()
    with col_analytics:
        if st.button("📊  Analytics", key="btn_analytics", use_container_width=True,
                     type="primary" if current_page == "Analytics" else "secondary"):
            session.set("current_page", "Analytics")
            st.rerun()
    with col_gear:
        if st.button("⚙️", key="btn_settings", use_container_width=True,
                     type="primary" if current_page == "Settings" else "secondary"):
            session.set("current_page", "Settings")
            st.rerun()


def main():
    """Application entry point."""
    configure_page()
    inject_css()

    settings = get_settings()
    setup_logging(settings.app.log_level, settings.app.log_dir)

    session = SessionStateManager()
    session.initialize()

    if "current_page" not in st.session_state:
        session.set("current_page", "Dashboard")
    if session.get("selected_subject") is None:
        session.set("selected_subject", "Polity")

    render_header_and_nav(session)

    page = session.get("current_page", "Dashboard")

    if page == "Dashboard":
        from app.pages.dashboard import render_dashboard_page
        render_dashboard_page(session)
    elif page == "Analytics":
        from app.pages.analytics import render_analytics_page
        render_analytics_page(session)
    elif page == "Settings":
        from app.pages.settings import render_settings_page
        render_settings_page(session)


if __name__ == "__main__":
    main()
