# ============================================================
# HOUSEHOLD RISK INTELLIGENCE
# Interactive Research Presentation
# OPENING → MODEL LAB → EXPLAIN
# ============================================================
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from pathlib import Path


# ============================================================
# GRAPH ANIMATION
# ============================================================

def animated_gain_card(value, steps=20, delay=0.025):
    placeholder = st.empty()

    for step in range(1, steps + 1):
        progress = step / steps
        progress = 1 - (1 - progress) ** 3
        current_value = value * progress

        placeholder.markdown(
            f"""
            <div style="
                font-size:76px;
                font-weight:900;
                line-height:.95;
                letter-spacing:-4px;
                color:#FF704D;
                text-shadow:0 0 32px rgba(255,112,77,.34);
                margin:3px 0 8px 0;
            ">
                {current_value:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(delay)


def animated_bar_chart(fig, key, steps=14, delay=0.035):
    """Render a Plotly bar chart with bars growing from zero to final values."""
    placeholder = st.empty()
    final_fig = go.Figure(fig)

    for step in range(1, steps + 1):
        progress = step / steps
        progress = 1 - (1 - progress) ** 3
        frame = go.Figure(final_fig)

        for i, trace in enumerate(frame.data):
            original = final_fig.data[i]

            if getattr(trace, "type", None) != "bar":
                continue

            if getattr(trace, "orientation", None) == "h":
                values = list(original.x)
                trace.x = [
                    float(v) * progress if v is not None else 0
                    for v in values
                ]
            else:
                values = list(original.y)
                trace.y = [
                    float(v) * progress if v is not None else 0
                    for v in values
                ]

            # Keep value labels hidden while the bars are moving.
            if step < steps:
                trace.text = None

        placeholder.plotly_chart(
            frame,
            use_container_width=True,
            key=f"{key}_{step}",
            config={"displaylogo": False}
        )
        time.sleep(delay)

    placeholder.plotly_chart(
        final_fig,
        use_container_width=True,
        key=f"{key}_final",
        config={"displaylogo": False}
    )


# ============================================================
# 01. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="가계 연체위험 예측",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 02. SESSION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "OPENING"


# ============================================================
# 03. DESIGN SYSTEM
# BRIGHT FINTECH NAVY · COBALT / CYAN
# ============================================================

st.markdown("""
<style>

:root {
    --bg: #08182B;
    --bg2: #0B2038;

    --panel: #102B49;
    --panel2: #123252;
    --panel3: #153A5E;

    --cobalt: #4385FF;
    --cobalt2: #6DA4FF;

    --cyan: #32C8FF;
    --aqua: #2FE0D0;
    --orange: #FF704D;

    --white: #F8FBFF;
    --text: #D9E8F7;
    --muted: #A8BED4;
}


/* ==========================================================
   APP BACKGROUND
   ========================================================== */

.stApp {

    background:

        radial-gradient(
            circle at 83% 10%,
            rgba(67,133,255,.30),
            transparent 30%
        ),

        radial-gradient(
            circle at 55% 48%,
            rgba(50,200,255,.075),
            transparent 35%
        ),

        radial-gradient(
            circle at 20% 88%,
            rgba(47,224,208,.055),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #08182B 0%,
            #0A1D33 42%,
            #0D2744 100%
        ) !important;

    color: var(--white);
}


/* technical grid */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background-image:

        linear-gradient(
            rgba(120,175,230,.040) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(120,175,230,.040) 1px,
            transparent 1px
        );

    background-size: 64px 64px;
}


/* ==========================================================
   CLEANUP
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


.block-container {

    max-width: 1600px;

    padding-top: 1.1rem;
    padding-left: 3.1rem;
    padding-right: 3.1rem;
    padding-bottom: 2rem;

    animation: pageEnter .38s ease;
}


/* ==========================================================
   TYPOGRAPHY
   ========================================================== */

h1 {

    color: #FFFFFF !important;

    font-size: 64px !important;
    line-height: .98 !important;

    font-weight: 850 !important;
    letter-spacing: -3px !important;

    margin-top: -2px !important;
    margin-bottom: 5px !important;

    text-shadow:
        0 0 22px rgba(67,133,255,.18),
        0 5px 18px rgba(0,0,0,.20);
}


h2 {

    color: #FFFFFF !important;

    font-weight: 800 !important;

    letter-spacing: -1.2px !important;

    text-shadow:
        0 0 20px rgba(67,133,255,.16),
        0 4px 12px rgba(0,0,0,.20);
}


h3 {

    color: #F8FBFF !important;

    font-weight: 760 !important;

    letter-spacing: -.5px !important;

    text-shadow:
        0 0 15px rgba(50,200,255,.10);
}


h4 {

    color: #F8FBFF !important;
}


p {

    color: #C9D9E9;

    font-weight: 450;

    line-height: 1.65;
}


strong {

    color: #F8FBFF;

    font-weight: 750;

    text-shadow:
        0 0 10px rgba(67,133,255,.10);
}


div[data-testid="stCaptionContainer"] {

    color: #9DB4CC !important;

    font-weight: 550 !important;

    letter-spacing: .15px;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background:

        radial-gradient(
            circle at 50% 8%,
            rgba(67,133,255,.11),
            transparent 28%
        ),

        linear-gradient(
            180deg,
            #091B30,
            #071525
        ) !important;

    border-right:
        1px solid rgba(105,165,225,.25);

    box-shadow:
        10px 0 35px rgba(0,0,0,.10);
}


section[data-testid="stSidebar"] button {

    background:
        rgba(13,38,65,.62) !important;

    color:
        #BED0E3 !important;

    border:
        1px solid rgba(115,170,225,.23) !important;

    border-radius:
        8px !important;

    min-height:
        44px !important;

    font-size:
        12px !important;

    font-weight:
        700 !important;

    transition:
        all .18s ease !important;
}


section[data-testid="stSidebar"] button:hover {

    background:
        linear-gradient(
            90deg,
            rgba(67,133,255,.20),
            rgba(50,200,255,.09)
        ) !important;

    color:
        #FFFFFF !important;

    border-color:
        rgba(67,133,255,.85) !important;

    box-shadow:
        0 0 18px rgba(67,133,255,.13);

    transform:
        translateX(3px);
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

div[data-testid="stMetric"] {

    position: relative;

    overflow: hidden;

    background:

        radial-gradient(
            circle at 90% 0%,
            rgba(67,133,255,.14),
            transparent 40%
        ),

        linear-gradient(
            145deg,
            rgba(18,50,82,.98),
            rgba(12,38,65,.98)
        );

    border:
        1px solid rgba(100,170,235,.35);

    border-radius:
        10px;

    padding:
        17px 18px;

    min-height:
        105px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.035),
        0 9px 25px rgba(0,0,0,.10);

    transition:
        transform .18s ease,
        border-color .18s ease,
        box-shadow .18s ease;
}


/* luminous top line */

div[data-testid="stMetric"]::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            #4385FF,
            #32C8FF,
            rgba(50,200,255,.05)
        );
}


div[data-testid="stMetric"]:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(67,160,255,.80);

    box-shadow:
        0 14px 34px rgba(67,133,255,.16),
        inset 0 1px 0 rgba(255,255,255,.06);
}


div[data-testid="stMetricLabel"] p {

    color:
        #C5D8EA !important;

    font-size:
        11px !important;

    font-weight:
        750 !important;

    letter-spacing:
        .35px;
}


div[data-testid="stMetricValue"] {

    color:
        #FFFFFF !important;

    font-size:
        30px !important;

    font-weight:
        850 !important;

    letter-spacing:
        -.8px;

    text-shadow:
        0 0 18px rgba(50,200,255,.22),
        0 4px 12px rgba(0,0,0,.16);
}


/* ==========================================================
   SELECTBOX
   ========================================================== */

div[data-baseweb="select"] > div {

    background:

        linear-gradient(
            90deg,
            rgba(17,48,80,.98),
            rgba(13,40,68,.98)
        ) !important;

    border:
        1px solid rgba(50,200,255,.50) !important;

    border-radius:
        8px !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 0 18px rgba(50,200,255,.055);
}


div[data-baseweb="select"] > div:hover {

    border-color:
        #32C8FF !important;

    box-shadow:
        0 0 20px rgba(50,200,255,.13);
}


/* ==========================================================
   SEGMENTED CONTROL
   ========================================================== */

div[data-testid="stSegmentedControl"] button {

    background:
        rgba(16,45,75,.88) !important;

    color:
        #C4D4E4 !important;

    border-color:
        rgba(105,165,225,.30) !important;

    font-weight:
        650 !important;

    transition:
        all .18s ease !important;
}


div[data-testid="stSegmentedControl"] button:hover {

    border-color:
        #4385FF !important;

    background:
        rgba(67,133,255,.17) !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 0 15px rgba(67,133,255,.10);
}


/* ==========================================================
   BUTTON
   ========================================================== */

div[data-testid="stButton"] button {

    border-radius:
        8px;

    font-weight:
        720;

    transition:
        all .18s ease;
}


div[data-testid="stButton"] button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 28px rgba(67,133,255,.20);
}


/* ==========================================================
   WARNING / INFO
   ========================================================== */

div[data-testid="stAlert"] {

    background:
        rgba(17,48,80,.82) !important;

    border:
        1px solid rgba(50,200,255,.28) !important;

    border-radius:
        9px !important;

    color:
        #DCEBFA !important;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border-color:
        rgba(115,175,230,.21) !important;
}


/* ==========================================================
   PAGE ENTRY
   ========================================================== */

@keyframes pageEnter {

    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}



/* ==========================================================
   EVERY GRAPH / TABLE · UNIVERSAL VISUAL MOTION
   ========================================================== */

/* Plotly titles, legends, axes come in after the plot itself */
[data-testid="stPlotlyChart"] .gtitle,
[data-testid="stPlotlyChart"] .legend,
[data-testid="stPlotlyChart"] .infolayer,
[data-testid="stPlotlyChart"] .annotation {
    opacity:0;
    animation:hriPlotTextIn .55s .62s ease forwards;
}

/* Bars: fade + slight rise, preserving their true geometry */
[data-testid="stPlotlyChart"] .barlayer .trace {
    opacity:0;
    animation:hriTraceRise .72s .34s cubic-bezier(.16,.84,.24,1) forwards;
}
[data-testid="stPlotlyChart"] .barlayer .trace:nth-child(2){animation-delay:.44s}
[data-testid="stPlotlyChart"] .barlayer .trace:nth-child(3){animation-delay:.54s}
[data-testid="stPlotlyChart"] .barlayer .trace:nth-child(4){animation-delay:.64s}

/* Scatter/line geometry must remain untouched.
   SVG transforms on Plotly trace/point nodes can move markers away from their
   data coordinates. Motion is applied to the chart container instead. */
[data-testid="stPlotlyChart"] .scatterlayer .trace,
[data-testid="stPlotlyChart"] .scatterlayer path.point,
[data-testid="stPlotlyChart"] .scatterlayer path.js-line {
    opacity:1;
    animation:none;
}

/* Plotly table / heatmap / image-like layers */
[data-testid="stPlotlyChart"] .table,
[data-testid="stPlotlyChart"] .heatmaplayer,
[data-testid="stPlotlyChart"] .imagelayer {
    opacity:0;
    animation:hriTablePlotIn .78s .32s cubic-bezier(.16,.84,.24,1) forwards;
}

/* Axis tick labels are delayed slightly */
[data-testid="stPlotlyChart"] .xtick,
[data-testid="stPlotlyChart"] .ytick {
    opacity:0;
    animation:hriPlotTextIn .42s .70s ease forwards;
}

/* Plotly hover remains responsive and visually alive */
[data-testid="stPlotlyChart"] .hoverlayer {
    transition:opacity .15s ease;
}

/* Native Streamlit tables if added later */
[data-testid="stTable"],
[data-testid="stDataFrame"] {
    opacity:0;
    animation:hriTableReveal .82s .18s cubic-bezier(.16,.84,.24,1) forwards;
    transition:transform .20s ease, filter .20s ease;
}
[data-testid="stTable"]:hover,
[data-testid="stDataFrame"]:hover {
    transform:translateY(-2px);
    filter:brightness(1.025);
}

/* Images / HTML visual blocks also enter with the same language */
[data-testid="stImage"],
[data-testid="stHtml"] {
    animation:hriCardIn .66s .10s cubic-bezier(.16,.84,.24,1) both;
}

/* Every successive chart on a page gets a small stagger */
[data-testid="stPlotlyChart"]:nth-of-type(2){animation-delay:.18s}
[data-testid="stPlotlyChart"]:nth-of-type(3){animation-delay:.24s}
[data-testid="stPlotlyChart"]:nth-of-type(4){animation-delay:.30s}

/* Keyframes */
@keyframes hriTraceRise {
    0%   {opacity:0; transform:translateY(9px)}
    100% {opacity:1; transform:translateY(0)}
}
@keyframes hriPointPop {
    0%   {opacity:0; transform:scale(.45)}
    70%  {opacity:1; transform:scale(1.08)}
    100% {opacity:1; transform:scale(1)}
}
@keyframes hriLineGlow {
    0%   {opacity:.10; filter:drop-shadow(0 0 0 rgba(50,200,255,0))}
    55%  {opacity:1; filter:drop-shadow(0 0 5px rgba(50,200,255,.32))}
    100% {opacity:1; filter:drop-shadow(0 0 0 rgba(50,200,255,0))}
}
@keyframes hriTablePlotIn {
    0%   {opacity:0; transform:translateY(8px)}
    100% {opacity:1; transform:translateY(0)}
}
@keyframes hriPlotTextIn {
    from {opacity:0; transform:translateY(4px)}
    to   {opacity:1; transform:translateY(0)}
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# GLOBAL MOTION SYSTEM · PRESENTATION SAFE
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   HRI MOTION SYSTEM — visible on presentation, still restrained
   ========================================================== */

@keyframes hriTitleIn {
  0%   {opacity:0; transform:translateY(20px); filter:blur(5px);}
  100% {opacity:1; transform:translateY(0); filter:blur(0);}
}
@keyframes hriCardIn {
  0%   {opacity:0; transform:translateY(18px) scale(.975);}
  100% {opacity:1; transform:translateY(0) scale(1);}
}
@keyframes hriChartReveal {
  0%   {opacity:0; transform:translateY(12px); clip-path:inset(0 100% 0 0);}
  35%  {opacity:1;}
  100% {opacity:1; transform:translateY(0); clip-path:inset(0 0 0 0);}
}
@keyframes hriTableReveal {
  0%   {opacity:0; transform:translateY(10px); clip-path:inset(0 0 100% 0);}
  100% {opacity:1; transform:translateY(0); clip-path:inset(0 0 0 0);}
}
@keyframes hriPulse {
  0%,100% {box-shadow:0 0 0 rgba(67,133,255,0);}
  50% {box-shadow:0 0 26px rgba(67,133,255,.18);}
}
@keyframes hriAccentSweep {
  0% {background-position:200% 0;}
  100% {background-position:-200% 0;}
}

/* Page headings */
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3 {
  animation:hriTitleIn .72s cubic-bezier(.16,.84,.24,1) both;
}

/* KPI cards — visible stagger */
[data-testid="stMetric"] {
  opacity:0;
  animation:hriCardIn .68s cubic-bezier(.16,.84,.24,1) forwards;
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
[data-testid="column"]:nth-child(1) [data-testid="stMetric"] {animation-delay:.05s}
[data-testid="column"]:nth-child(2) [data-testid="stMetric"] {animation-delay:.14s}
[data-testid="column"]:nth-child(3) [data-testid="stMetric"] {animation-delay:.23s}
[data-testid="column"]:nth-child(4) [data-testid="stMetric"] {animation-delay:.32s}
[data-testid="stMetric"]:hover {
  transform:translateY(-5px) scale(1.015);
  box-shadow:0 16px 34px rgba(67,133,255,.16);
}

/* Plotly: obvious left→right reveal on page/section render */
[data-testid="stPlotlyChart"] {
  opacity:0;
  animation:hriChartReveal 1.05s cubic-bezier(.16,.84,.24,1) .12s forwards;
  transform-origin:left center;
  transition:transform .24s ease, filter .24s ease;
}
[data-testid="stPlotlyChart"]:hover {
  transform:translateY(-3px);
  filter:brightness(1.06);
}

/* Tables reveal vertically */
[data-testid="stDataFrame"] {
  opacity:0;
  animation:hriTableReveal .85s cubic-bezier(.16,.84,.24,1) .12s forwards;
}

/* Cards / bordered containers */
[data-testid="stVerticalBlockBorderWrapper"] {
  opacity:0;
  animation:hriCardIn .68s cubic-bezier(.16,.84,.24,1) .10s forwards;
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  transform:translateY(-4px);
  box-shadow:0 15px 34px rgba(50,200,255,.11);
}

/* Inputs and buttons */
[data-testid="stSelectbox"],
[data-testid="stSegmentedControl"] {
  animation:hriCardIn .60s cubic-bezier(.16,.84,.24,1) both;
}
.stButton > button {
  transition:transform .18s ease, box-shadow .18s ease,
             border-color .18s ease, background .18s ease !important;
}
.stButton > button:hover {
  transform:translateY(-3px);
  box-shadow:0 10px 28px rgba(67,133,255,.20);
}

/* Important blue/orange emphasis gets a very subtle living glow */
[data-testid="stMainBlockContainer"] strong {
  text-shadow:0 0 18px rgba(67,133,255,.07);
}

/* accessibility */
@media (prefers-reduced-motion: reduce) {
  *,*::before,*::after {
    animation-duration:.001ms !important;
    animation-delay:0ms !important;
    animation-iteration-count:1 !important;
    transition-duration:.001ms !important;
  }
  [data-testid="stPlotlyChart"],
  [data-testid="stMetric"],
  [data-testid="stDataFrame"],
  [data-testid="stVerticalBlockBorderWrapper"] {
    opacity:1 !important;
    clip-path:none !important;
    transform:none !important;
  }
}
</style>
""", unsafe_allow_html=True)


def apply_motion(fig, duration=850):
    """Apply consistent, restrained Plotly transition behavior."""
    try:
        fig.update_layout(
            transition=dict(
                duration=duration,
                easing="cubic-in-out"
            )
        )
    except Exception:
        pass
    return fig

def motion_signal(label="LIVE ANALYTICS"):
    st.markdown(
        f"""
        <div class="hri-motion-signal">
            <span class="hri-motion-dot"></span>
            <span>{label}</span>
            <span class="hri-motion-line"></span>
        </div>
        <style>
        .hri-motion-signal {{
            display:flex;align-items:center;gap:8px;
            margin:2px 0 12px 0;
            color:#6F8FAE;font-size:9px;font-weight:800;letter-spacing:.75px;
            opacity:0;animation:hriCardIn .65s .18s ease forwards;
        }}
        .hri-motion-dot {{
            width:6px;height:6px;border-radius:50%;
            background:#32C8FF;
            box-shadow:0 0 0 rgba(50,200,255,0);
            animation:hriSignalPulse 1.8s ease-in-out infinite;
        }}
        .hri-motion-line {{
            height:1px;flex:1;max-width:150px;
            background:linear-gradient(90deg,#4385FF,#32C8FF,transparent);
            background-size:200% 100%;
            animation:hriSignalSweep 2.6s linear infinite;
        }}
        @keyframes hriSignalPulse {{
            0%,100%{{box-shadow:0 0 0 rgba(50,200,255,0)}}
            50%{{box-shadow:0 0 14px rgba(50,200,255,.75)}}
        }}
        @keyframes hriSignalSweep {{
            from{{background-position:100% 0}}
            to{{background-position:-100% 0}}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



# ============================================================
# 04. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("##### HRI / 2026")

    st.markdown("## HOUSEHOLD")

    st.caption(
        "RISK INTELLIGENCE\n\n"
        "가계 금융 취약성 분석\n\n"
        "MICRO PANEL DATA"
    )

    st.write("")

    if st.button(
        "01   OPENING",
        use_container_width=True
    ):
        st.session_state.page = "OPENING"
        st.rerun()


    if st.button(
        "02   DATA & VARIABLES",
        use_container_width=True
    ):
        st.session_state.page = "DATA"
        st.rerun()


    if st.button("03   VALIDATION MAP", use_container_width=True):
        st.session_state.page = "VALIDATION_MAP"
        st.rerun()

    if st.button("04   MODEL LAB", use_container_width=True):
        st.session_state.page = "MODEL"
        st.rerun()

    if st.button("05   EXPLAIN", use_container_width=True):
        st.session_state.page = "EXPLAIN"
        st.rerun()

    if st.button("06   PROFILE", use_container_width=True):
        st.session_state.page = "PROFILE"
        st.rerun()

    if st.button("07   OOT VALIDATE", use_container_width=True):
        st.session_state.page = "VALIDATE"
        st.rerun()

    if st.button("08   SCREEN", use_container_width=True):
        st.session_state.page = "SCREEN"
        st.rerun()

    if st.button("09   CONCLUSION", use_container_width=True):
        st.session_state.page = "CONCLUSION"
        st.rerun()

    st.write("")
    st.write("")

    st.caption(
        "PRESENTATION × ANALYTICS\n\n"
        "2021 — 2025"
    )


# ============================================================
# 05. OPENING
# ============================================================

if st.session_state.page == "OPENING":

    top_left, top_right = st.columns([1, 1])

    with top_left:
        st.markdown(
            "**:blue[HOUSEHOLD FINANCIAL RISK · RESEARCH INTERFACE]**"
        )

    with top_right:
        st.caption(
            "MICRO PANEL DATA · ML/DL · OUT-OF-TIME VALIDATION"
        )

    st.write("")


    hero_left, hero_right = st.columns(
        [1.03, .97],
        gap="large"
    )


    # ========================================================
    # OPENING LEFT
    # ========================================================

    with hero_left:

        st.caption(
            "HOUSEHOLD DELINQUENCY RISK · 가계 금융 취약성 분석"
        )

        st.markdown("# 가계 연체위험")
        st.markdown("# 예측")

        st.write("")

        st.markdown(
            """
### 미시 패널자료를 기반으로
### :orange[30일 이상 원리금 연체위험]을 예측
"""
        )

        st.markdown(
            """
현재 가구의 **소득 · 자산 · 유동성 · 소비 · 부채구조**를 활용해  
다음 해 연체위험을 분류합니다.
"""
        )

        st.caption(
            "2021–2023 DEVELOPMENT  ·  "
            "2024 INPUT  ·  "
            "2025 OOT VALIDATION"
        )

        st.write("")


        # ====================================================
        # ANIMATED KPI STRIP
        # ====================================================

        components.html(
            """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background: transparent;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    overflow: hidden;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);

    gap: 9px;
    width: 100%;

    padding: 4px 1px 7px 1px;
}

.card {
    position: relative;

    min-width: 0;
    height: 117px;

    overflow: hidden;

    border-radius: 10px;

    padding: 16px 14px 12px 14px;

    background:
        linear-gradient(
            145deg,
            rgba(15,35,59,.96),
            rgba(8,25,43,.98)
        );

    transition:
        transform .22s ease,
        box-shadow .22s ease,
        border-color .22s ease;

    opacity: 0;

    animation:
        cardEnter .45s ease forwards;
}

.card::after {
    content: "";

    position: absolute;

    width: 95px;
    height: 95px;

    right: -45px;
    top: -48px;

    border-radius: 50%;

    opacity: .12;

    filter: blur(18px);
}

.card:hover {
    transform: translateY(-4px);
}

.card:hover::after {
    opacity: .25;
}


/* SAMPLE */

.sample {
    border:
        1px solid rgba(50,200,255,.35);

    box-shadow:
        inset 0 1px 0 rgba(50,200,255,.08),
        0 8px 22px rgba(0,0,0,.10);
}

.sample::before {
    content: "";

    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            #32C8FF,
            rgba(50,200,255,.10)
        );
}

.sample::after {
    background: #32C8FF;
}

.sample:hover {
    border-color:
        rgba(50,200,255,.75);

    box-shadow:
        0 10px 30px rgba(50,200,255,.11);
}


/* EVENT */

.event {
    border:
        1px solid rgba(255,112,77,.42);
}

.event::before {
    content: "";

    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            #FF704D,
            rgba(255,112,77,.10)
        );
}

.event::after {
    background: #FF704D;
}

.event:hover {
    border-color:
        rgba(255,112,77,.80);

    box-shadow:
        0 10px 32px rgba(255,112,77,.15);
}


/* FEATURES */

.features {
    border:
        1px solid rgba(47,224,208,.36);
}

.features::before {
    content: "";

    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            #2FE0D0,
            rgba(47,224,208,.10)
        );
}

.features::after {
    background: #2FE0D0;
}

.features:hover {
    border-color:
        rgba(47,224,208,.75);

    box-shadow:
        0 10px 30px rgba(47,224,208,.11);
}


/* MODELS */

.models {
    border:
        1px solid rgba(67,133,255,.42);
}

.models::before {
    content: "";

    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            #4385FF,
            rgba(67,133,255,.10)
        );
}

.models::after {
    background: #4385FF;
}

.models:hover {
    border-color:
        rgba(67,133,255,.80);

    box-shadow:
        0 10px 30px rgba(67,133,255,.14);
}


/* TEXT */

.label {
    position: relative;
    z-index: 2;

    white-space: nowrap;

    font-size: 10px;
    font-weight: 700;
    letter-spacing: .55px;

    color: #B7C8DA;
}

.value {
    position: relative;
    z-index: 2;

    margin-top: 8px;

    font-size: 27px;
    line-height: 1;

    font-weight: 800;
    letter-spacing: -1px;

    color: #F7FAFF;

    font-variant-numeric:
        tabular-nums;
}

.sample .value {
    text-shadow:
        0 0 18px rgba(50,200,255,.22);
}

.event .value {
    color: #FFF7F4;

    text-shadow:
        0 0 21px rgba(255,112,77,.28);
}

.features .value {
    text-shadow:
        0 0 18px rgba(47,224,208,.21);
}

.models .value {
    text-shadow:
        0 0 18px rgba(67,133,255,.23);
}

.meta {
    position: absolute;

    left: 14px;
    bottom: 11px;

    z-index: 2;

    font-size: 8.5px;
    font-weight: 600;

    letter-spacing: .25px;

    color: #738BA5;

    white-space: nowrap;
}

.event .meta {
    color: #A88178;
}


/* ENTRY */

.card:nth-child(1) {
    animation-delay: .03s;
}

.card:nth-child(2) {
    animation-delay: .09s;
}

.card:nth-child(3) {
    animation-delay: .15s;
}

.card:nth-child(4) {
    animation-delay: .21s;
}

@keyframes cardEnter {
    from {
        opacity: 0;
        transform: translateY(9px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
</head>


<body>

<div class="kpi-grid">

    <div class="card sample">

        <div class="label">
            DEV SAMPLE
        </div>

        <div
            class="value"
            id="sampleValue"
        >
            0
        </div>

        <div class="meta">
            2021–2023
        </div>

    </div>


    <div class="card event">

        <div class="label">
            30D+ EVENT
        </div>

        <div
            class="value"
            id="eventValue"
        >
            0.00%
        </div>

        <div class="meta">
            605 OBS.
        </div>

    </div>


    <div class="card features">

        <div class="label">
            FEATURES
        </div>

        <div
            class="value"
            id="featureValue"
        >
            0
        </div>

        <div class="meta">
            COMMON SET
        </div>

    </div>


    <div class="card models">

        <div class="label">
            MODELS
        </div>

        <div
            class="value"
            id="modelValue"
        >
            0
        </div>

        <div class="meta">
            ML · DL
        </div>

    </div>

</div>


<script>

function animateValue(
    elementId,
    start,
    end,
    duration,
    formatter
) {

    const element =
        document.getElementById(elementId);

    const startTime =
        performance.now();


    function update(currentTime) {

        const elapsed =
            currentTime - startTime;

        const progress =
            Math.min(
                elapsed / duration,
                1
            );

        const eased =
            1 - Math.pow(
                1 - progress,
                3
            );

        const current =
            start +
            (end - start) *
            eased;

        element.textContent =
            formatter(current);

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}


setTimeout(
    function() {

        animateValue(
            "sampleValue",
            0,
            20554,
            900,
            function(v) {
                return Math.round(v)
                    .toLocaleString();
            }
        );

        animateValue(
            "eventValue",
            0,
            2.94,
            900,
            function(v) {
                return v.toFixed(2) + "%";
            }
        );

        animateValue(
            "featureValue",
            0,
            12,
            760,
            function(v) {
                return Math.round(v);
            }
        );

        animateValue(
            "modelValue",
            0,
            4,
            700,
            function(v) {
                return Math.round(v);
            }
        );

    },
    160
);

</script>

</body>
</html>
""",
            height=132,
            scrolling=False
        )


    # ========================================================
    # OPENING RIGHT · REFINED VISUAL
    # ========================================================

    with hero_right:
        st.caption("MICRO PANEL DATA · ML/DL · OUT-OF-TIME VALIDATION")

        left_y = np.array([7.9,7.2,6.6,6.0,5.4,4.8,4.2,3.6,3.0,2.4])
        left_x = np.array([1.20,1.58,1.34,1.72,1.48,1.18,1.66,1.39,1.76,1.30])
        right_y = np.array([7.9,7.2,6.6,6.0,5.4,4.8,4.2,3.6,3.0,2.4])
        right_x = np.array([8.42,8.70,8.30,8.78,8.48,8.22,8.66,8.38,8.76,8.28])
        risk_idx = np.array([0, 3, 6])
        normal_idx = np.array([i for i in range(10) if i not in risk_idx])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[2.15,4.25], y=[5.15,5.15], mode="lines",
            line=dict(width=3, color="rgba(67,133,255,.58)"),
            hoverinfo="skip", showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[5.75,7.82], y=[5.15,5.15], mode="lines",
            line=dict(width=3, color="rgba(50,200,255,.58)"),
            hoverinfo="skip", showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=left_x, y=left_y, mode="markers", name="2024 INPUT",
            marker=dict(size=10, color="#4385FF", opacity=.82,
                        line=dict(width=1, color="rgba(210,230,255,.62)")),
            hovertemplate="<b>2024 INPUT</b><br>가구 재무정보<extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=right_x[normal_idx], y=right_y[normal_idx],
            mode="markers", name="2025 OOT",
            marker=dict(size=10, color="#32C8FF", opacity=.72,
                        line=dict(width=1, color="rgba(210,245,255,.55)")),
            hovertemplate="<b>2025 OOT</b><br>관측 결과<extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=right_x[risk_idx], y=right_y[risk_idx],
            mode="markers", name="30D+ RISK",
            marker=dict(size=15, color="#FF704D", opacity=1,
                        line=dict(width=2, color="#FFD7CD")),
            hovertemplate="<b>30D+ DELINQUENCY</b><br>장기연체 관측<extra></extra>"
        ))

        fig.add_shape(
            type="circle", x0=4.35, x1=5.65, y0=4.10, y1=6.20,
            fillcolor="rgba(67,133,255,.14)",
            line=dict(color="#6DA4FF", width=2)
        )
        fig.add_annotation(
            x=5, y=5.38, text="<b>MODEL</b>",
            showarrow=False, font=dict(size=17, color="#FFFFFF")
        )
        fig.add_annotation(
            x=5, y=4.90, text="t → t+1",
            showarrow=False, font=dict(size=10, color="#9FB8D2")
        )
        fig.add_annotation(
            x=1.48, y=8.85,
            text="<b>2024</b><br><span style='font-size:9px'>HOUSEHOLD INPUT</span>",
            showarrow=False, align="center",
            font=dict(size=24, color="#6DA4FF")
        )
        fig.add_annotation(
            x=8.50, y=8.85,
            text="<b>2025</b><br><span style='font-size:9px'>OOT OUTCOME</span>",
            showarrow=False, align="center",
            font=dict(size=24, color="#F7FAFF")
        )
        fig.add_annotation(
            x=5, y=7.65,
            text="<b>NEXT-YEAR RISK</b><br><span style='font-size:9px'>CURRENT FINANCIAL STATE → FUTURE DELINQUENCY</span>",
            showarrow=False, align="center",
            font=dict(size=11, color="#C7D9EA")
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(7,22,39,.34)",
            margin=dict(l=8, r=8, t=12, b=8),
            xaxis=dict(visible=False, range=[.45,9.55], fixedrange=True),
            yaxis=dict(visible=False, range=[1.0,9.65], fixedrange=True),
            legend=dict(
                orientation="h", x=.5, xanchor="center", y=.015,
                font=dict(size=10, color="#BFD1E4"),
                bgcolor="rgba(0,0,0,0)"
            ),
            hoverlabel=dict(
                bgcolor="#0A192B",
                bordercolor="#4385FF",
                font_color="#FFFFFF"
            )
        )

        st.plotly_chart(
            apply_motion(fig),
            use_container_width=True,
            config={"displaylogo": False, "displayModeBar": False},
            key="opening_refined_flow"
        )

        st.caption("MODEL INPUT · 가구 재무정보")
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.markdown("**소득**")
            st.caption("INCOME")
        with c2:
            st.markdown("**자산**")
            st.caption("ASSET")
        with c3:
            st.markdown("**유동성**")
            st.caption("LIQUIDITY")
        with c4:
            st.markdown("**소비**")
            st.caption("SPENDING")
        with c5:
            st.markdown("**:orange[부채구조]**")
            st.caption("DEBT STRUCTURE")

        st.caption(
            "Conceptual interface · 위 점들은 실제 개별가구의 예측점수를 의미하지 않습니다."
        )


    # OPENING BOTTOM
    # ========================================================

    st.divider()


    b1, b2, b3, b4 = st.columns(4)


    with b1:
        st.caption("01 / DEVELOPMENT")
        st.markdown("**2021–2023 DEV**")


    with b2:
        st.caption("02 / INPUT")
        st.markdown("**2024 가구 재무정보**")


    with b3:
        st.caption("03 / TARGET")
        st.markdown("**2025년 30일+ 연체**")


    with b4:
        st.caption("04 / VALIDATION")
        st.markdown("**2025 OOT 검증**")


    st.write("")


    empty, next_col = st.columns(
        [4.3, 1]
    )


    with next_col:

        if st.button(
            "DATA & VARIABLES  →",
            use_container_width=True
        ):
            st.session_state.page = "DATA"
            st.rerun()


# ============================================================
# 06. MODEL LAB
# ============================================================


# ============================================================
# 06. DATA & VARIABLES · TEAM PART
# ============================================================

elif st.session_state.page == "DATA":

    motion_signal("DATA ARCHITECTURE · LIVE")
    st.caption("HOVER · SELECT · ZOOM  |  주요 시각화는 진입·선택 시 부드럽게 반응합니다.")

    st.markdown(":blue[**02 / DATA ARCHITECTURE**]")
    st.markdown("## 데이터 구성과 설명변수")
    st.caption(
        "MICRO PANEL DATA · SAMPLE STRUCTURE · VARIABLE DIAGNOSTICS · EVALUATION METRICS"
    )
    st.write("")

    # ========================================================
    # 01 · ANNUAL SAMPLE STRUCTURE
    # ========================================================
    st.markdown(":blue[**01 · ANNUAL SAMPLE STRUCTURE**]")
    st.markdown("### 연도별 표본은 어떻게 구성되었는가?")
    st.write(
        "가계금융복지조사의 연도별 표본에서 금융부채 보유가구와 "
        "30일 이상 장기연체가구의 규모를 확인했습니다."
    )

    sample_df = pd.DataFrame({
        "연도": ["2021", "2022", "2023", "2024"],
        "총 가구": [13760, 13648, 13828, 14078],
        "금융부채 가구": [7043, 6809, 6702, 6607],
        "30D+ 연체가구": [217, 205, 183, 173],
        "연체율": [3.08, 3.01, 2.73, 2.62],
    })

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("DEV WINDOW", "2021–2023", "MODEL DEVELOPMENT")
    with k2:
        st.metric("OOT INPUT", "2024", "→ 2025 TARGET")
    with k3:
        st.metric("2024 DEBT SAMPLE", "6,607", "금융부채 보유가구")
    with k4:
        st.metric("2024 30D+ RATE", "2.62%", "173 households")

    st.write("")

    trend_col, table_col = st.columns([1.08, .92], gap="large")

    with trend_col:
        fig_sample = go.Figure()

        fig_sample.add_trace(
            go.Scatter(
                x=sample_df["연도"],
                y=sample_df["금융부채 가구"],
                mode="lines+markers",
                name="금융부채 가구",
                line=dict(color="#4385FF", width=3),
                marker=dict(size=9, color="#4385FF"),
                hovertemplate=(
                    "<b>%{x}년</b><br>"
                    "금융부채 가구 %{y:,}가구"
                    "<extra></extra>"
                ),
            )
        )

        # 연체율은 시각적 추세 비교를 위해 보조축 사용
        fig_sample.add_trace(
            go.Scatter(
                x=sample_df["연도"],
                y=sample_df["연체율"],
                mode="lines+markers",
                name="30D+ 연체율",
                yaxis="y2",
                line=dict(color="#FF704D", width=3),
                marker=dict(size=10, color="#FF704D"),
                hovertemplate=(
                    "<b>%{x}년</b><br>"
                    "30D+ 연체율 %{y:.2f}%"
                    "<extra></extra>"
                ),
            )
        )

        fig_sample.update_layout(
            height=390,
            title=dict(
                text=(
                    "<b>Annual Sample Signal</b><br>"
                    "<span style='font-size:10px;'>"
                    "FINANCIAL-DEBT HOUSEHOLDS × 30D+ DELINQUENCY RATE"
                    "</span>"
                ),
                x=.01,
                font=dict(size=16, color="#F7FAFF"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(7,22,39,.38)",
            margin=dict(l=10, r=55, t=72, b=40),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color="#A8BED4"),
            ),
            yaxis=dict(
                range=[6200, 7300],
                gridcolor="rgba(130,160,200,.10)",
                zeroline=False,
                tickfont=dict(color="#91A6BF"),
                title=dict(text="금융부채 가구", font=dict(color="#91A6BF")),
            ),
            yaxis2=dict(
                overlaying="y",
                side="right",
                range=[2.4, 3.2],
                showgrid=False,
                tickfont=dict(color="#FF9E87"),
                title=dict(text="30D+ 연체율 (%)", font=dict(color="#FF9E87")),
            ),
            legend=dict(
                orientation="h",
                x=.01,
                y=1.03,
                font=dict(size=10, color="#C5D3E2"),
                bgcolor="rgba(0,0,0,0)",
            ),
            hoverlabel=dict(
                bgcolor="#0A192B",
                bordercolor="#4385FF",
                font_color="#FFFFFF",
            ),
        )

        st.plotly_chart(
        apply_motion(fig_sample),
            width="stretch",
            config={"displaylogo": False, "displayModeBar": False},
        )

    with table_col:
        fig_sample_table = go.Figure(
            data=[
                go.Table(
                    columnwidth=[.7, 1.05, 1.15, 1.15, .8],
                    header=dict(
                        values=[
                            "<b>YEAR</b>",
                            "<b>전체 표본</b>",
                            "<b>금융부채 가구</b>",
                            "<b>30D+ 연체</b>",
                            "<b>RATE</b>",
                        ],
                        fill_color="#123A61",
                        line_color="rgba(90,165,230,.38)",
                        font=dict(color="#DDEEFF", size=11),
                        align=["left", "right", "right", "right", "right"],
                        height=38,
                    ),
                    cells=dict(
                        values=[
                            [f"<b>{v}</b>" for v in sample_df["연도"]],
                            [f"{v:,}" for v in sample_df["총 가구"]],
                            [f"{v:,}" for v in sample_df["금융부채 가구"]],
                            [f"{v:,}" for v in sample_df["30D+ 연체가구"]],
                            [f"<b>{v:.2f}%</b>" for v in sample_df["연체율"]],
                        ],
                        fill_color=[
                            ["#102B49"] * 4,
                            ["#0D263F"] * 4,
                            ["#0D263F"] * 4,
                            ["#0D263F", "#0D263F", "#0D263F", "#2B2330"],
                            ["#102B49", "#102B49", "#102B49", "#332337"],
                        ],
                        line_color="rgba(100,160,215,.18)",
                        font=dict(color="#D9E8F7", size=11),
                        align=["left", "right", "right", "right", "right"],
                        height=47,
                    ),
                )
            ]
        )

        fig_sample_table.update_layout(
            height=390,
            title=dict(
                text=(
                    "<b>Sample Structure</b><br>"
                    "<span style='font-size:10px;'>ANNUAL OBSERVATION TABLE</span>"
                ),
                x=.01,
                font=dict(size=16, color="#F7FAFF"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=72, b=10),
        )

        st.plotly_chart(
        apply_motion(fig_sample_table),
            width="stretch",
            config={"displaylogo": False, "displayModeBar": False},
        )

    st.markdown(
        ":blue[**DATA FLOW · 2021–2023 DEV → 2024 INPUT → 2025 OOT VALIDATION**]"
    )
    st.caption(
        "2024년 금융부채 보유가구 6,607가구를 입력으로 사용해 "
        "2025년 30일 이상 장기연체 여부를 OOT에서 평가합니다."
    )

    st.divider()

    # ========================================================
    # 02 · VARIABLE DIAGNOSTICS
    # ========================================================
    st.markdown(":blue[**02 · VARIABLE DIAGNOSTICS**]")
    st.markdown("### 최종 12개 설명변수 · OLS & VIF")
    st.write(
        "최종 설명변수의 기본적인 관계와 다중공선성을 점검했습니다. "
        "표를 단순히 나열하기보다 VIF 구조와 회귀 진단값을 함께 확인할 수 있도록 구성했습니다."
    )

    ols_df = pd.DataFrame([
        ["const", 0.0295, 0.001, 22.964, 0.000, None],
        ["처분가능소득(보완)", -0.0054, 0.002, -3.225, 0.001, 1.715],
        ["지출_소비지출비", -0.0123, 0.002, -6.060, 0.000, 2.523],
        ["자산", -0.0060, 0.002, -2.753, 0.006, 2.871],
        ["금융자산_저축금액", -0.0082, 0.003, 2.930, 0.003, 4.737],
        ["유동자산(추정)", -0.0092, 0.003, -3.339, 0.001, 4.578],
        ["부채", 0.0041, 0.002, 2.013, 0.044, 2.540],
        ["금융부채_신용대출", 0.0033, 0.001, 2.254, 0.024, 1.267],
        ["금융부채_신용카드", 0.0274, 0.001, 21.114, 0.000, 1.027],
        ["금융부채_개인·직장", 0.0152, 0.001, 11.607, 0.000, 1.040],
        ["무담보위험부채비중", 0.0073, 0.001, 5.090, 0.000, 1.241],
        ["지출_주거비", 0.0066, 0.001, 4.626, 0.000, 1.239],
        ["가구원", -0.0006, 0.002, -0.359, 0.720, 1.601],
    ], columns=["변수", "coef", "std err", "t", "P>|t|", "VIF"])

    diag_left, diag_right = st.columns([1.18, .82], gap="large")

    with diag_left:
        plot_vif = ols_df.dropna(subset=["VIF"]).sort_values("VIF", ascending=True)

        vif_colors = [
            "#FF704D" if v >= 4.5
            else "#32C8FF" if v >= 2.5
            else "#4385FF"
            for v in plot_vif["VIF"]
        ]

        fig_vif = go.Figure(
            go.Bar(
                x=plot_vif["VIF"],
                y=plot_vif["변수"],
                orientation="h",
                marker=dict(color=vif_colors),
                text=[f"{v:.3f}" for v in plot_vif["VIF"]],
                textposition="outside",
                cliponaxis=False,
                customdata=np.stack(
                    [
                        plot_vif["coef"],
                        plot_vif["P>|t|"],
                        plot_vif["t"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "VIF %{x:.3f}<br>"
                    "coef %{customdata[0]:.4f}<br>"
                    "p-value %{customdata[1]:.3f}<br>"
                    "t %{customdata[2]:.3f}"
                    "<extra></extra>"
                ),
            )
        )

        fig_vif.add_vline(
            x=5,
            line_width=1.5,
            line_dash="dash",
            line_color="rgba(255,112,77,.70)",
            annotation_text="VIF 5",
            annotation_font_color="#FF9E87",
        )

        fig_vif.update_layout(
            margin=dict(l=165, r=65, t=72, b=45),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(7,22,39,.38)",

            xaxis=dict(
                title="Variance Inflation Factor",
                range=[0, 5.45],
                gridcolor="rgba(130,160,200,.10)",
                zeroline=False,
                tickfont=dict(color="#91A6BF"),
            ),

            yaxis=dict(
                tickfont=dict(
                    size=10,
                    color="#C5D3E2"
                ),
                automargin=True,
                ticklabelposition="outside",
            ),

            showlegend=False,

            hoverlabel=dict(
                bgcolor="#0A192B",
                font_size=12,
                font_color="white",
            ),
        )

        animated_bar_chart(
            fig_vif,
            key="vif_animation",
            steps=14,
            delay=0.035
        )

    with diag_right:
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric("FEATURES", "12")
        with d2:
            st.metric("MAX VIF", "4.737")
        with d3:
            st.metric("VIF ≥ 5", "0")

        fig_ols_table = go.Figure(
            data=[
                go.Table(
                    columnwidth=[1.65, .65, .7, .65, .7, .65],
                    header=dict(
                        values=[
                            "<b>VARIABLE</b>",
                            "<b>COEF</b>",
                            "<b>STD ERR</b>",
                            "<b>t</b>",
                            "<b>p</b>",
                            "<b>VIF</b>",
                        ],
                        fill_color="#123A61",
                        line_color="rgba(90,165,230,.38)",
                        font=dict(color="#DDEEFF", size=10),
                        align=["left", "right", "right", "right", "right", "right"],
                        height=31,
                    ),
                    cells=dict(
                        values=[
                            ols_df["변수"],
                            [f"{v:.4f}" for v in ols_df["coef"]],
                            [f"{v:.3f}" for v in ols_df["std err"]],
                            [f"{v:.3f}" for v in ols_df["t"]],
                            [f"{v:.3f}" for v in ols_df["P>|t|"]],
                            ["–" if pd.isna(v) else f"{v:.3f}" for v in ols_df["VIF"]],
                        ],
                        fill_color=[
                            ["#102B49"] * len(ols_df),
                            ["#0D263F"] * len(ols_df),
                            ["#0D263F"] * len(ols_df),
                            ["#0D263F"] * len(ols_df),
                            [
                                "#332337" if v >= .05 else "#0D263F"
                                for v in ols_df["P>|t|"]
                            ],
                            [
                                "#30293A" if (not pd.isna(v) and v >= 4.5)
                                else "#0D263F"
                                for v in ols_df["VIF"]
                            ],
                        ],
                        line_color="rgba(100,160,215,.16)",
                        font=dict(color="#D9E8F7", size=9),
                        align=["left", "right", "right", "right", "right", "right"],
                        height=29,
                    ),
                )
            ]
        )

        fig_ols_table.update_layout(
            height=445,
            title=dict(
                text=(
                    "<b>OLS Diagnostic Table</b><br>"
                    "<span style='font-size:10px;'>COEFFICIENT · SIGNIFICANCE · VIF</span>"
                ),
                x=.01,
                font=dict(size=15, color="#F7FAFF"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=62, b=0),
        )

        st.plotly_chart(
        apply_motion(fig_ols_table),
            width="stretch",
            config={"displaylogo": False, "displayModeBar": False},
        )

        st.markdown(":blue[**DIAGNOSTIC RESULT**]")
        st.caption(
            "최대 VIF는 4.737이며 12개 설명변수 모두 VIF 5 미만입니다. "
            "OLS/VIF는 변수 제거의 단독 기준이 아니라 최종 변수구조를 확인하는 보조 진단으로 사용했습니다."
        )

    st.divider()

    # ========================================================
    # 03 · EVALUATION METRICS
    # ========================================================
    st.markdown(":blue[**03 · EVALUATION METRICS**]")
    st.markdown("### 분류모형은 어떤 기준으로 평가했는가?")
    st.write(
        "혼동행렬에서 출발하는 핵심 분류지표와 ROC-AUC를 함께 확인했습니다. "
        "각 공식은 뒤의 후보모형 비교에서 사용되는 성능지표의 기준입니다."
    )
    st.write("")

    m1, m2, m3 = st.columns(3, gap="medium")

    with m1:
        with st.container(border=True):
            st.caption("01 / OVERALL CORRECTNESS")
            st.markdown("#### Accuracy")
            st.latex(r"\frac{TN+TP}{TN+TP+FN+FP}")
            st.caption("전체 예측 중 올바르게 분류한 비율")

        with st.container(border=True):
            st.caption("02 / POSITIVE RELIABILITY")
            st.markdown("#### Precision")
            st.latex(r"\frac{TP}{TP+FP}")
            st.caption("위험가구 예측 중 실제 위험가구의 비율")

    with m2:
        with st.container(border=True):
            st.caption("03 / EVENT CAPTURE")
            st.markdown("#### Recall · TPR")
            st.latex(r"\frac{TP}{TP+FN}")
            st.caption("실제 위험가구 중 모델이 찾아낸 비율")

        with st.container(border=True):
            st.caption("04 / BALANCE")
            st.markdown("#### F1-score")
            st.latex(r"2\times\frac{Precision\times Recall}{Precision+Recall}")
            st.caption("Precision과 Recall의 조화평균")

    with m3:
        with st.container(border=True):
            st.caption("05 / RANKING POWER")
            st.markdown("#### ROC-AUC")
            st.latex(r"\int_{0}^{1}TPR(FPR^{-1}(x))\,dx")
            st.caption("여러 임계값에서 양성과 음성을 구분하는 능력")

        with st.container(border=True):
            st.caption("PRIMARY METRIC · NEXT SECTION")
            st.markdown("#### :blue[PR-AUC]")
            st.markdown("**희소한 30D+ 연체가구의 선별력을 중심으로 비교**")
            st.caption(
                "장기연체 비율이 약 3%인 불균형 데이터이므로 "
                "다음 MODEL LAB에서는 PR-AUC를 주요 선정지표로 사용합니다."
            )

    st.write("")
    st.markdown(
        ":blue[**NEXT · SAME 12 FEATURES → LOGISTIC · RANDOM FOREST · XGBOOST · TABNET**]"
    )

    st.write("")
    back_col, empty_col, next_col = st.columns([1, 4, 1])

    with back_col:
        if st.button("← OPENING", width="stretch"):
            st.session_state.page = "OPENING"
            st.rerun()

    with next_col:
        if st.button("VALIDATION MAP →", width="stretch"):
            st.session_state.page = "VALIDATION_MAP"
            st.rerun()

# ============================================================
# 07. VALIDATION MAP · MODEL FITNESS REVIEW
# ============================================================

elif st.session_state.page == "VALIDATION_MAP":

    motion_signal("MODEL FITNESS REVIEW · VALIDATION FRAMEWORK")
    st.markdown(":blue[**03 / MODEL VALIDATION FRAMEWORK**]")
    st.markdown("## 분석결과를 해석하기에 앞서, 모형의 :orange[적합성 검증 결과]를 살펴보겠습니다")
    st.caption("MODEL FITNESS REVIEW · 12 VALIDATION DOMAINS · COMPREHENSIVE ASSESSMENT")
    st.write(
        "모델링 이후 수행한 적합성 검증 결과를 발표 흐름상 먼저 제시합니다. "
        "타깃의 목적 부합성부터 표본, 변수, 모델링 방법, 검증방법과 예측 활용 가능성까지 "
        "총 12개 영역을 종합적으로 점검했습니다."
    )
    st.write("")

    v1, v2, v3 = st.columns(3)
    with v1:
        st.metric("충족", "2 / 12", "독립성 · 다중공선성")
    with v2:
        st.metric("조건부 충족", "9 / 12", "추가 보완 필요")
    with v3:
        st.metric("미확인", "1 / 12", "대안 대비 통계적 우월성")

    validation_rows = [
        ("종속변수의 목적 부합성", "조건부 충족", "30일 이상 연체 타깃 · 차기연도 연결"),
        ("표본 충분성·대표성", "조건부 충족", "DEV/OOT 표본 구성 · 전국 단위 조사자료"),
        ("모델링 방법의 타당성", "조건부 충족", "동일 조건 후보모형 비교 · Group CV"),
        ("정보의 충분성", "조건부 충족", "재무·가구 특성 포함 · 세부 신용정보 부재"),
        ("설명변수의 유의성", "조건부 충족", "순열 중요도 · SHAP 분석"),
        ("변수 방향의 합리성", "조건부 충족", "SHAP 방향 · 실제 연체집단 비교"),
        ("기본가정·관측치 독립성", "충족", "가구 단위 분할 · fold 간 가구 중복 방지"),
        ("이상치·영향력 관측치", "조건부 충족", "윈저라이징 민감도 분석"),
        ("다중공선성", "충족", "VIF 점검"),
        ("검증방법의 타당성", "조건부 충족", "DEV OOF · 시간 OOT 검증"),
        ("예측력·활용 가능성", "조건부 충족", "OOT AUC · KS · Lift · 상위 10% 포착률"),
        ("대안 대비 통계적 우월성", "미확인", "일부 신뢰구간 0 포함 · 대안모형 우월성 미확정"),
    ]

    def validation_badge(verdict):
        if verdict == "충족":
            return '<span class="vb vb-ok">충족</span>'
        if verdict == "미확인":
            return '<span class="vb vb-na">미확인</span>'
        return '<span class="vb vb-cond">조건부 충족</span>'

    rows_html = ""
    for idx, (area, verdict, evidence) in enumerate(validation_rows, 1):
        rows_html += (
            f'<div class="vt-row"><div class="vt-num">{idx:02d}</div>'
            f'<div class="vt-area">{area}</div><div class="vt-status">{validation_badge(verdict)}</div>'
            f'<div class="vt-evidence">{evidence}</div></div>'
        )

    st.markdown(
        f"""
        <style>
        .vt-wrap{{margin-top:8px;border:1px solid rgba(67,133,255,.25);border-radius:12px;overflow:hidden;background:rgba(8,29,51,.72);}}
        .vt-head,.vt-row{{display:grid;grid-template-columns:46px minmax(210px,.9fr) 126px minmax(360px,1.55fr);align-items:center;column-gap:12px;}}
        .vt-head{{padding:11px 16px;background:rgba(67,133,255,.12);font-size:10px;font-weight:900;letter-spacing:.08em;color:#83A7CE;}}
        .vt-row{{padding:9px 16px;border-top:1px solid rgba(130,170,210,.085);min-height:44px;}}
        .vt-row:hover{{background:rgba(67,133,255,.055);}}
        .vt-num{{font-size:10px;color:#577797;font-weight:800;}}
        .vt-area{{font-size:13px;color:#F1F7FF;font-weight:750;white-space:nowrap;}}
        .vt-status{{text-align:left;}}
        .vt-evidence{{font-size:12px;color:#B8CBDE;line-height:1.35;white-space:nowrap;}}
        .vb{{display:inline-block;min-width:94px;text-align:center;padding:4px 8px;border-radius:999px;font-size:11px;font-weight:850;}}
        .vb-ok{{color:#55E8D8;background:rgba(47,224,208,.09);border:1px solid rgba(47,224,208,.30);}}
        .vb-cond{{color:#82B2FF;background:rgba(67,133,255,.09);border:1px solid rgba(67,133,255,.30);}}
        .vb-na{{color:#FF9E87;background:rgba(255,112,77,.09);border:1px solid rgba(255,112,77,.30);}}
        @media(max-width:1100px){{.vt-head,.vt-row{{grid-template-columns:36px minmax(170px,.9fr) 112px minmax(260px,1.4fr);column-gap:8px;}}.vt-area,.vt-evidence{{white-space:normal;}}}}
        </style>
        <div class="vt-wrap">
          <div class="vt-head"><div>NO.</div><div>검증 영역</div><div>최종 판정</div><div>판정 근거</div></div>
          {rows_html}
        </div>
        """, unsafe_allow_html=True
    )

    st.write("")
    st.markdown(
        '<div style="padding:14px 18px;border-left:3px solid #4385FF;background:rgba(67,133,255,.065);border-radius:0 9px 9px 0;">'
        '<b style="color:#F7FAFF;">VALIDATION TAKEAWAY</b>&nbsp;&nbsp;'
        '<span style="color:#BFD0E2;">가구 단위 누수 통제와 다중공선성 점검은 충족했으며, 나머지 영역은 데이터·검증 범위를 고려해 조건부로 해석했습니다. 대안모형 대비 통계적 우월성은 확정하지 않았습니다.</span>'
        '</div>', unsafe_allow_html=True
    )

    st.write("")
    back_col, empty_col, next_col = st.columns([1, 4, 1])
    with back_col:
        if st.button("← DATA", use_container_width=True):
            st.session_state.page = "DATA"
            st.rerun()
    with next_col:
        if st.button("MODEL LAB →", use_container_width=True):
            st.session_state.page = "MODEL"
            st.rerun()

# ============================================================
# 07. EXPLAIN · SHAP
# ============================================================


elif st.session_state.page == "MODEL":

    motion_signal("MODEL COMPARISON · LIVE")

    st.markdown(
        ":blue[**02 / MODEL PERFORMANCE**]"
    )

    st.markdown(
        "## 후보모형 성능 비교 및 최종모형 선정"
    )

    st.caption(
        "Candidate Model Evaluation · DEV OOF Performance"
    )

    st.write("")


    # --------------------------------------------------------
    # MODEL DATA
    # --------------------------------------------------------

    model_data = {

        "Logistic": {
            "PR-AUC": .1723,
            "ROC-AUC": .8041,
            "Precision": .1819,
            "Recall": .4083,
            "F1": .2517,
            "Threshold": .6908
        },

        "Random Forest": {
            "PR-AUC": .1900,
            "ROC-AUC": .7997,
            "Precision": .2472,
            "Recall": .3289,
            "F1": .2823,
            "Threshold": .1400
        },

        "TabNet": {
            "PR-AUC": .1874,
            "ROC-AUC": .8166,
            "Precision": .2210,
            "Recall": .3587,
            "F1": .2735,
            "Threshold": .7599
        },

        "XGBoost": {
            "PR-AUC": .2203,
            "ROC-AUC": .8034,
            "Precision": .2630,
            "Recall": .3438,
            "F1": .2980,
            "Threshold": .7786
        }
    }


    selected_model = st.segmented_control(
        "모형 선택 · SELECT MODEL",

        options=[
            "Logistic",
            "Random Forest",
            "TabNet",
            "XGBoost"
        ],

        default="XGBoost"
    )


    if selected_model is None:
        selected_model = "XGBoost"


    selected = model_data[
        selected_model
    ]


    chart_col, metric_col = st.columns(
        [1.35, .65],
        gap="large"
    )


    # ========================================================
    # MODEL CHART
    # ========================================================

    with chart_col:

        model_order = [
            "Logistic",
            "TabNet",
            "Random Forest",
            "XGBoost"
        ]


        scores = [
            model_data[m]["PR-AUC"]
            for m in model_order
        ]


        colors = []


        for model in model_order:

            if model == "XGBoost":
                colors.append("#4385FF")

            elif model == selected_model:
                colors.append("#32C8FF")

            else:
                colors.append(
                    "rgba(126,151,181,.34)"
                )


        fig2 = go.Figure()


        fig2.add_trace(
            go.Bar(
                x=scores,
                y=model_order,

                orientation="h",

                marker=dict(
                    color=colors
                ),

                text=[
                    f"{v:.4f}"
                    for v in scores
                ],

                textposition=[
                    "outside",
                    "outside",
                    "outside",
                    "inside"
                ],

                insidetextanchor="end",

                textfont=dict(
                    size=12,
                    color="#F7FAFF"
                ),

                cliponaxis=False,

                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>"
                    "DEV OOF PR-AUC %{x:.4f}"
                    "<extra></extra>"
                )
            )
        )


        fig2.add_annotation(
            x=.232,
            y="XGBoost",

            text="<b>BEST · SELECTED</b>",

            showarrow=False,

            xanchor="left",
            yanchor="middle",

            bgcolor="rgba(67,133,255,.14)",

            bordercolor="rgba(67,133,255,.72)",

            borderwidth=1,
            borderpad=5,

            font=dict(
                size=9,
                color="#9AB9FF"
            )
        )


        fig2.update_layout(
            height=475,

            title=dict(
                text=(
                    "<b>모형별 DEV OOF PR-AUC</b>"
                    "<br>"
                    "<span style='font-size:10px;'>"
                    "PRIMARY MODEL SELECTION METRIC"
                    "</span>"
                ),

                x=.01,

                font=dict(
                    size=15,
                    color="#F7FAFF"
                )
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(7,22,39,.38)",

            margin=dict(
                l=10,
                r=105,
                t=80,
                b=45
            ),

            xaxis=dict(
                range=[0, .27],

                title="PR-AUC",

                gridcolor="rgba(130,160,200,.10)",

                zeroline=False,

                tickfont=dict(
                    color="#91A6BF"
                )
            ),

            yaxis=dict(
                tickfont=dict(
                    size=12,
                    color="#C5D3E2"
                )
            ),

            showlegend=False,

            hoverlabel=dict(
                bgcolor="#0A192B",
                bordercolor="#4385FF",
                font_color="#FFFFFF"
            )
        )

        animated_bar_chart(
            fig2,
            key="model_pr_auc_animation",
            steps=16,
            delay=0.04
        )

        # --------------------------------------------------------
        # PRECISION - RECALL TRADE-OFF
        # --------------------------------------------------------

        st.markdown(
            '<div style="margin:14px 0 20px 0;padding:16px 20px;border:1px solid rgba(67,133,255,.55);border-radius:10px;background:rgba(67,133,255,.10);">'
            '<div style="font-size:13px;font-weight:800;letter-spacing:.08em;color:#6DA4FF;margin-bottom:8px;">PRECISION ↔ RECALL · TRADE-OFF</div>'
            '<div style="font-size:16px;font-weight:600;line-height:1.6;color:#F2F7FF;">위험가구 포착 범위를 넓힐수록 <span style="color:#32C8FF;font-weight:800;">Recall ↑</span>, 오탐 증가로 <span style="color:#FF8A70;font-weight:800;">Precision ↓</span>할 수 있습니다.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            ":blue[**KEY FINDING · 핵심 결과**]"
        )


        st.write(
            "XGBoost가 DEV OOF PR-AUC 0.2203으로 "
            "가장 높은 성능을 기록했습니다."
        )


        st.write(
            "30일 이상 연체가 DEV 표본의 약 2.94%에 불과하므로 "
            "Accuracy보다 PR-AUC를 주요 모형 선정지표로 사용했습니다."
        )


    # ========================================================
    # MODEL METRICS
    # ========================================================

    with metric_col:

        st.caption(
            "SELECTED VIEW · 현재 선택"
        )

        st.markdown(
            f"## {selected_model}"
        )


        m1, m2 = st.columns(2)

        with m1:
            st.metric(
                "PR-AUC",
                f'{selected["PR-AUC"]:.4f}'
            )

        with m2:
            st.metric(
                "ROC-AUC",
                f'{selected["ROC-AUC"]:.4f}'
            )


        m3, m4 = st.columns(2)

        with m3:
            st.metric(
                "Precision",
                f'{selected["Precision"]:.4f}'
            )

        with m4:
            st.metric(
                "Recall",
                f'{selected["Recall"]:.4f}'
            )


        m5, m6 = st.columns(2)

        with m5:
            st.metric(
                "F1",
                f'{selected["F1"]:.4f}'
            )

        with m6:
            st.metric(
                "Threshold",
                f'{selected["Threshold"]:.4f}'
            )


        st.write("")


        if selected_model == "XGBoost":

            st.markdown(
                "### :blue[XGBoost · FINAL MODEL]"
            )

            st.write(
                "PR-AUC 0.2203 · BEST"
            )

            st.write(
                "Precision 0.2630 · BEST"
            )

            st.write(
                "F1 0.2980 · BEST"
            )

            st.markdown(
                "**DEV 성능기준에 따라 "
                "XGBoost를 최종모형으로 선정했습니다.**"
            )

            st.caption(
                "2025 OOT 결과는 모형 선정에 사용하지 않았습니다."
            )


        elif selected_model == "Logistic":

            st.markdown(
                "### Logistic Regression"
            )

            st.write(
                "Recall 0.4083으로 가장 높지만 "
                "Precision은 상대적으로 낮았습니다."
            )


        elif selected_model == "Random Forest":

            st.markdown(
                "### Random Forest"
            )

            st.write(
                "PR-AUC 0.1900, F1 0.2823으로 "
                "중간 수준의 균형 잡힌 성능을 보였습니다."
            )


        else:

            st.markdown(
                "### TabNet"
            )

            st.write(
                "ROC-AUC 0.8166으로 가장 높았지만 "
                "주요 선정지표인 PR-AUC는 XGBoost보다 낮았습니다."
            )


    # ========================================================
    # PERFORMANCE MATRIX · ALL MODEL METRICS
    # ========================================================

    st.write("")
    st.markdown(":blue[**MODEL PERFORMANCE MATRIX · 지표별 성능 비교**]")
    st.markdown("### 각 모델은 어떤 지표에서 강점을 보였는가?")
    st.caption(
        "셀의 밝기는 각 지표 내 상대적 성능을 나타내며, 숫자는 실제 DEV OOF 성능값입니다. "
        "★는 해당 지표의 최고값입니다."
    )

    perf_models = ["Logistic", "Random Forest", "TabNet", "XGBoost"]
    perf_metrics = [
        "PR-AUC", "ROC-AUC", "Precision", "Recall",
        "Balanced Acc.", "F1", "KS", "Gini"
    ]

    perf_values = np.array([
        [0.1723, 0.8041, 0.1819, 0.4083, 0.6763, 0.2517, 0.4804, 0.6082],
        [0.1900, 0.7997, 0.2472, 0.3289, 0.6493, 0.2823, 0.4840, 0.5993],
        [0.1874, 0.8166, 0.2210, 0.3587, 0.6602, 0.2735, 0.5153, 0.6332],
        [0.2203, 0.8034, 0.2630, 0.3438, 0.6573, 0.2980, 0.4877, 0.6067],
    ])

    # Normalize within each metric so the color intensity communicates
    # relative performance without mixing metrics with different scales.
    col_min = perf_values.min(axis=0)
    col_max = perf_values.max(axis=0)
    perf_norm = (perf_values - col_min) / np.where(
        (col_max - col_min) == 0, 1, (col_max - col_min)
    )

    best_rows = perf_values.argmax(axis=0)
    perf_text = []
    for r in range(len(perf_models)):
        row_text = []
        for c in range(len(perf_metrics)):
            prefix = "★  " if best_rows[c] == r else ""
            row_text.append(f"{prefix}{perf_values[r, c]:.4f}")
        perf_text.append(row_text)

    fig_perf = go.Figure(
        data=go.Heatmap(
            z=perf_norm,
            x=perf_metrics,
            y=perf_models,
            text=perf_text,
            texttemplate="%{text}",
            textfont=dict(size=16, color="#FFFFFF"),
            colorscale=[
                [0.00, "#0D2946"],
                [0.74, "#173A5C"],
                [0.94, "#245A86"],
                [1.00, "#32C8FF"],
            ],
            showscale=False,
            xgap=4,
            ygap=4,
            customdata=perf_values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x}<br>"
                "DEV OOF = %{customdata:.4f}"
                "<extra></extra>"
            ),
        )
    )

    fig_perf.update_layout(
        height=455,
        margin=dict(l=25, r=15, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            side="top",
            tickfont=dict(size=15, color="#F2F7FC", family="Arial Black"),
            fixedrange=True,
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=15, color="#F2F7FC", family="Arial Black"),
            fixedrange=True,
        ),
        hoverlabel=dict(
            bgcolor="#0A192B",
            bordercolor="#4385FF",
            font_color="#FFFFFF",
        ),
    )

    st.plotly_chart(
        apply_motion(fig_perf),
        use_container_width=True,
        config={"displaylogo": False, "displayModeBar": False},
    )

    st.markdown(
        "**PRIMARY METRIC · PR-AUC → :blue[XGBoost 0.2203 · BEST]**  "
        "· XGBoost: PR-AUC · Precision · F1 최고  "
        "· TabNet: ROC-AUC · KS · Gini 최고  "
        "· Logistic: Recall · Balanced Accuracy 최고"
    )


    # ========================================================
    # MODEL BOTTOM
    # ========================================================

    st.divider()


    v1, v2, v3 = st.columns(3)


    with v1:
        st.caption("01 / COMMON INPUT")
        st.markdown("**12개 공통 설명변수**")

        st.write(
            "모든 후보모형에 동일한 변수 세트를 적용했습니다."
        )


    with v2:
        st.caption("02 / CROSS VALIDATION")

        st.markdown(
            "**5-Fold Stratified Group CV**"
        )

        st.write(
            "동일 가구의 반복관측으로 인한 "
            "데이터 누수를 방지했습니다."
        )


    with v3:
        st.caption("03 / FINAL DECISION")

        st.markdown(
            "**XGBoost → 2025 OOT**"
        )

        st.write(
            "DEV에서 선정한 모형과 Threshold를 "
            "고정하여 미래 시점 성능을 검증합니다."
        )


    st.write("")


    back_col, empty_col, next_col = st.columns(
        [1, 4, 1]
    )


    with back_col:

        if st.button(
            "← VALIDATION MAP",
            use_container_width=True
        ):
            st.session_state.page = "VALIDATION_MAP"
            st.rerun()


    with next_col:

        if st.button(
            "EXPLAIN  →",
            use_container_width=True
        ):
            st.session_state.page = "EXPLAIN"
            st.rerun()


# ============================================================
# 07. EXPLAIN · SHAP
# ============================================================



elif st.session_state.page == "EXPLAIN":

    motion_signal("MODEL EXPLAINABILITY · LIVE")

    st.markdown(":blue[**03 / MODEL EXPLAINABILITY**]")
    st.markdown("## XGBoost는 어떤 재무정보를 중요하게 보았는가?")
    st.caption("SHAP FEATURE IMPORTANCE · FINAL XGBOOST MODEL · DEV 2021–2023")
    st.write("")

    # --------------------------------------------------------
    # SHAP IMPORTANCE DATA
    # --------------------------------------------------------
    shap_data = {
        "자산": (0.8466, 25.29),
        "처분가능소득": (0.3380, 10.10),
        "유동자산": (0.3327, 9.94),
        "소비지출": (0.3189, 9.53),
        "부채": (0.3184, 9.51),
        "신용대출": (0.2778, 8.30),
        "저축금액": (0.2225, 6.65),
        "개인·직장차입": (0.1828, 5.46),
        "가구원수": (0.1680, 5.02),
        "주거비": (0.1571, 4.69),
        "카드관련대출": (0.1083, 3.23),
        "무담보위험부채비율": (0.0768, 2.30),
    }

    top6_share = sum(v[1] for v in list(shap_data.values())[:6])

    k1, k2, k3 = st.columns([1.15, 1, 1])
    with k1:
        st.metric("#1 FEATURE · 자산", "25.29%", "Mean |SHAP| 0.8466")
    with k2:
        st.metric("TOP 6 CONCENTRATION", f"{top6_share:.2f}%", "전체 SHAP 중요도")
    with k3:
        st.metric("FINAL MODEL", "XGBoost", "12 common features")

    st.write("")

    # --------------------------------------------------------
    # IMPORTANCE RANKING
    # --------------------------------------------------------
    names = list(shap_data.keys())
    shares = [shap_data[n][1] for n in names]
    means = [shap_data[n][0] for n in names]
    order = list(range(len(names)-1, -1, -1))

    colors = [
        "#4385FF" if names[i] == "자산"
        else "#32C8FF" if i < 6
        else "rgba(126,151,181,.38)"
        for i in order
    ]

    fig_imp = go.Figure(go.Bar(
        x=[shares[i] for i in order],
        y=[names[i] for i in order],
        orientation="h",
        marker=dict(color=colors),
        text=[f"{shares[i]:.2f}%" for i in order],
        textposition="outside",
        cliponaxis=False,
        customdata=[[means[i]] for i in order],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Importance share %{x:.2f}%<br>"
            "Mean |SHAP| %{customdata[0]:.4f}"
            "<extra></extra>"
        )
    ))
    fig_imp.update_layout(
        height=440,
        title=dict(
            text="<b>SHAP Feature Importance</b><br><span style='font-size:10px;'>WHAT MATTERS MOST TO THE MODEL?</span>",
            x=.01, font=dict(size=16, color="#F7FAFF")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,22,39,.38)",
        margin=dict(l=10, r=70, t=72, b=35),
        xaxis=dict(title="Importance share (%)", gridcolor="rgba(130,160,200,.10)", zeroline=False, tickfont=dict(color="#91A6BF")),
        yaxis=dict(tickfont=dict(size=11, color="#C5D3E2")),
        showlegend=False,
        hoverlabel=dict(bgcolor="#0A192B", bordercolor="#4385FF", font_color="#FFFFFF")
    )
    animated_bar_chart(
        fig_imp,
        key="shap_importance_animation",
        steps=16,
        delay=0.04
    )

    st.markdown(":blue[**KEY FINDING · 모델은 부채 규모만 보지 않았습니다.**]")
    st.write(
        "자산이 전체 SHAP 중요도의 25.29%로 가장 큰 비중을 차지했고, "
        "상위 6개 변수에는 자산·소득·유동성·소비·부채·신용대출이 함께 포함되었습니다. "
        "즉 XGBoost는 가구의 재무여력과 부채구조를 복합적으로 활용해 위험을 구분했습니다."
    )

    st.divider()

    # --------------------------------------------------------
    # INTERACTIVE SHAP DEPENDENCE
    # --------------------------------------------------------
    st.markdown(":blue[**HOW DOES RISK CHANGE? · 변수 수준에 따라 모델 반응은 어떻게 달라지는가**]")
    st.markdown("### SHAP Dependence Explorer")
    st.caption("점 하나는 DEV 관측치 1개 · SHAP > 0은 모델 위험점수를 높이는 방향, SHAP < 0은 낮추는 방향")

    csv_path = Path(__file__).resolve().parent / "shap_dependence_6features.csv"

    if not csv_path.exists():
        st.error("shap_dependence_6features.csv 파일을 hybrid.py와 같은 폴더에 넣어주세요.")
    else:
        @st.cache_data
        def load_shap_dependence(path_str):
            return pd.read_csv(path_str, encoding="utf-8-sig")

        dep_df = load_shap_dependence(str(csv_path))

        feature_options = ["자산", "부채", "신용대출", "개인·직장차입", "카드관련대출", "가구원수"]
        selected_feature = st.segmented_control(
            "변수 선택 · SELECT FEATURE",
            options=feature_options,
            default="자산",
            key="shap_dependence_feature"
        )
        if selected_feature is None:
            selected_feature = "자산"

        plot_df = dep_df.loc[dep_df["feature"] == selected_feature, ["value", "shap_value"]].dropna().copy()

        # 20,554개 점을 모두 그리되 WebGL로 렌더링
        point_colors = np.where(plot_df["shap_value"].to_numpy() >= 0, "#FF704D", "#4385FF")

        fig_dep = go.Figure()
        fig_dep.add_trace(go.Scattergl(
            x=plot_df["value"],
            y=plot_df["shap_value"],
            mode="markers",
            marker=dict(size=5.5, color=point_colors, opacity=.42),
            hovertemplate=(
                f"<b>{selected_feature}</b><br>"
                "변수값 %{x:,.2f}<br>"
                "SHAP %{y:.4f}<extra></extra>"
            ),
            showlegend=False
        ))
        fig_dep.add_hline(y=0, line_width=1.5, line_dash="dash", line_color="rgba(230,240,250,.70)")

        fig_dep.add_annotation(
            xref="paper", yref="paper", x=.99, y=.97,
            text="RISK SCORE ↑", showarrow=False,
            font=dict(size=10, color="#FF9E87"),
            bgcolor="rgba(255,112,77,.10)", bordercolor="rgba(255,112,77,.35)", borderpad=5
        )
        fig_dep.add_annotation(
            xref="paper", yref="paper", x=.99, y=.05,
            text="RISK SCORE ↓", showarrow=False,
            font=dict(size=10, color="#82B2FF"),
            bgcolor="rgba(67,133,255,.10)", bordercolor="rgba(67,133,255,.35)", borderpad=5
        )

        fig_dep.update_layout(
            height=570,
            title=dict(
                text=f"<b>{selected_feature}</b> · Feature Value × SHAP Value",
                x=.01, font=dict(size=18, color="#F7FAFF")
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(7,22,39,.48)",
            margin=dict(l=25, r=25, t=65, b=50),
            xaxis=dict(
                title=f"{selected_feature} · 실제 변수값",
                gridcolor="rgba(130,160,200,.09)",
                zeroline=False, tickfont=dict(color="#9FB5CB")
            ),
            yaxis=dict(
                title="SHAP value · 모델 위험점수 기여",
                gridcolor="rgba(130,160,200,.09)",
                zeroline=False, tickfont=dict(color="#9FB5CB")
            ),
            hovermode="closest",
            dragmode="zoom",
            hoverlabel=dict(bgcolor="#0A192B", bordercolor="#4385FF", font_color="#FFFFFF")
        )

        st.plotly_chart(
        apply_motion(fig_dep),
            use_container_width=True,
            config={
                "displaylogo": False,
                "scrollZoom": True,
                "modeBarButtonsToRemove": ["lasso2d"],
                "toImageButtonOptions": {"format": "png", "scale": 2}
            }
        )

        interpretations = {
            "자산": "낮은 자산 구간에서 양(+)의 SHAP 값이 상대적으로 크게 나타나고, 자산이 증가하면서 SHAP 값이 빠르게 낮아지는 비선형 패턴이 관찰됩니다.",
            "부채": "부채 수준에 따라 SHAP 값이 비선형적으로 달라집니다. 전체 부채 규모 하나만으로 위험이 결정되는 것이 아니라 다른 재무변수와 함께 활용됩니다.",
            "신용대출": "신용대출 수준에 따라 모델의 위험 기여도가 달라지며, 부채구조를 구분하는 신호로 사용됩니다.",
            "개인·직장차입": "개인·직장 차입 수준에 따라 위험점수 기여가 달라지는 구간이 나타납니다. 이는 해당 차입 변수가 부채구조의 보조 신호로 활용됐음을 보여줍니다.",
            "카드관련대출": "카드관련대출 값의 변화에 따라 SHAP 기여도가 달라집니다. 중요도 자체는 상위 변수보다 낮지만 특정 관측치의 위험점수에는 영향을 줄 수 있습니다.",
            "가구원수": "가구원수별로 SHAP 값이 서로 다른 수준에 형성되어, 가구구조가 다른 재무정보와 함께 위험 분류의 보조 정보로 사용됐음을 보여줍니다."
        }

        left_info, right_info = st.columns([1.45, .55], gap="large")
        with left_info:
            st.markdown(f"### :blue[{selected_feature}] · MODEL RESPONSE")
            st.write(interpretations[selected_feature])
            st.caption("SHAP은 예측모형의 기여도를 설명하며 인과효과를 의미하지 않습니다.")
        with right_info:
            pos_share = (plot_df["shap_value"] > 0).mean() * 100
            median_shap = plot_df["shap_value"].median()
            st.metric("OBSERVATIONS", f"{len(plot_df):,}")
            st.metric("SHAP > 0", f"{pos_share:.1f}%")
            st.metric("MEDIAN SHAP", f"{median_shap:.3f}")

    st.divider()
    st.markdown("### MODEL SIGNAL FLOW")
    st.write("**ASSET → INCOME → LIQUIDITY → CONSUMPTION → DEBT → CREDIT**")
    st.caption("SHAP 중요도는 예측 기여도를 나타냅니다. 실제 장기연체가구의 관측 특성은 다음 PROFILE에서 별도로 비교합니다.")

    st.write("")
    back_col, empty_col, next_col = st.columns([1, 4, 1])
    with back_col:
        if st.button("← MODEL LAB", use_container_width=True):
            st.session_state.page = "MODEL"
            st.rerun()
    with next_col:
        if st.button("PROFILE →", use_container_width=True):
            st.session_state.page = "PROFILE"
            st.rerun()


# ============================================================
# 08. PROFILE
# ============================================================


elif st.session_state.page == "PROFILE":

    motion_signal("HOUSEHOLD PROFILE · LIVE")

    st.markdown(":orange[**04 / HOUSEHOLD RISK PROFILE**]")

    st.markdown(
        "## 실제 30일 이상 연체가구는 어떤 특성을 보였는가?"
    )

    st.caption(
        "OBSERVED CHARACTERISTICS · "
        "일반 연체가구 vs 30일 이상 원리금 연체가구"
    )

    st.write("")


    # ========================================================
    # 01 · VISUAL KPI CARDS
    # ========================================================

    components.html(
        """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 2px;

    background: transparent;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    color: #F8FBFF;

    overflow: hidden;
}

.grid {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 14px;
}


/* ----------------------------------------------------------
   CARD
---------------------------------------------------------- */

.card {

    position: relative;

    opacity: 0;
    transform: translateY(12px);
    animation: validateCardIn .55s cubic-bezier(.2,.8,.2,1) forwards;

    height: 175px;

    overflow: hidden;

    padding: 17px 19px;

    border-radius: 12px;

    background:

        radial-gradient(
            circle at 90% 0%,
            rgba(67,133,255,.19),
            transparent 38%
        ),

        linear-gradient(
            145deg,
            rgba(22,60,96,.98),
            rgba(13,42,72,.98)
        );

    border:
        1px solid rgba(89,174,255,.45);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 12px 28px rgba(0,0,0,.13);

    transition:
        transform .20s ease,
        box-shadow .20s ease;
}


.card:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 15px 35px rgba(67,133,255,.16);
}


.card::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;

    width: 100%;
    height: 3px;

    background:
        linear-gradient(
            90deg,
            #4385FF,
            #32C8FF,
            transparent
        );
}


.card.risk::before {

    background:
        linear-gradient(
            90deg,
            #FF704D,
            #FF9A80,
            transparent
        );
}


.label {

    font-size: 10px;

    color: #BCD0E3;

    font-weight: 750;

    letter-spacing: .45px;
}


.value {

    margin-top: 7px;

    font-size: 27px;

    line-height: 1;

    color: #FFFFFF;

    font-weight: 850;

    letter-spacing: -1px;

    text-shadow:
        0 0 18px rgba(50,200,255,.25);
}


.risk .value {

    color: #FF8A6D;

    text-shadow:
        0 0 20px rgba(255,112,77,.30);
}


.meta {

    margin-top: 5px;

    color: #819AB4;

    font-size: 8.5px;

    font-weight: 650;
}


/* ----------------------------------------------------------
   CARD 1 · PROGRESS
---------------------------------------------------------- */

.progress-bg {

    width: 100%;
    height: 8px;

    margin-top: 17px;

    overflow: hidden;

    border-radius: 10px;

    background:
        rgba(130,165,200,.17);
}


.progress-fill {

    width: 42.72%;
    height: 100%;

    border-radius: 10px;

    background:
        linear-gradient(
            90deg,
            #FF704D,
            #FF9A80
        );

    box-shadow:
        0 0 13px rgba(255,112,77,.35);

    animation:
        fill1 .8s ease;
}


@keyframes fill1 {

    from {
        width: 0;
    }

    to {
        width: 42.72%;
    }
}


/* ----------------------------------------------------------
   MINI COMPARISON
---------------------------------------------------------- */

.mini-row {

    display: grid;

    grid-template-columns:
        62px 1fr 52px;

    align-items: center;

    gap: 7px;

    margin-top: 9px;
}


.name {

    font-size: 8.5px;

    color: #A9BDD1;

    font-weight: 650;
}


.num {

    font-size: 8.5px;

    color: #DDE9F5;

    text-align: right;

    font-weight: 750;

    font-variant-numeric:
        tabular-nums;
}


.track {

    height: 7px;

    border-radius: 8px;

    overflow: hidden;

    background:
        rgba(130,165,200,.15);
}


.bar {

    height: 100%;

    border-radius: 8px;

    background:
        linear-gradient(
            90deg,
            #4385FF,
            #32C8FF
        );
}


.bar.orange {

    background:
        linear-gradient(
            90deg,
            #FF704D,
            #FF9A80
        );

    box-shadow:
        0 0 10px rgba(255,112,77,.28);
}

</style>

</head>


<body>

<div class="grid">


    <!-- CARD 1 -->

    <div class="card risk">

        <div class="label">
            30D+ SHARE · 연체가구 내 비중
        </div>

        <div class="value">
            42.72%
        </div>

        <div class="meta">
            778 / 1,821 DELINQUENT OBS.
        </div>

        <div class="progress-bg">
            <div class="progress-fill"></div>
        </div>

        <div class="meta">
            GENERAL 57.28% · 30D+ 42.72%
        </div>

    </div>


    <!-- CARD 2 -->

    <div class="card">

        <div class="label">
            ASSET GAP · 자산 중앙값
        </div>

        <div class="value">
            −81.24%
        </div>

        <div class="meta">
            GENERAL → 30D+ DELINQUENCY
        </div>


        <div class="mini-row">

            <div class="name">
                일반 연체
            </div>

            <div class="track">
                <div
                    class="bar"
                    style="width:100%;">
                </div>
            </div>

            <div class="num">
                27,018
            </div>

        </div>


        <div class="mini-row">

            <div class="name">
                30일+
            </div>

            <div class="track">
                <div
                    class="bar orange"
                    style="width:18.76%;">
                </div>
            </div>

            <div class="num">
                5,068
            </div>

        </div>

    </div>


    <!-- CARD 3 -->

    <div class="card risk">

        <div class="label">
            PERSONAL / WORKPLACE BORROWING
        </div>

        <div class="value">
            2.45×
        </div>

        <div class="meta">
            보유비율 · 30D+ / GENERAL
        </div>


        <div class="mini-row">

            <div class="name">
                일반 연체
            </div>

            <div class="track">
                <div
                    class="bar"
                    style="width:40.7%;">
                </div>
            </div>

            <div class="num">
                10.16%
            </div>

        </div>


        <div class="mini-row">

            <div class="name">
                30일+
            </div>

            <div class="track">
                <div
                    class="bar orange"
                    style="width:100%;">
                </div>
            </div>

            <div class="num">
                24.94%
            </div>

        </div>

    </div>


</div>

</body>
</html>
""",
        height=190,
        scrolling=False
    )


    st.write("")


    # ========================================================
    # 02 · PROFILE DATA
    # ========================================================

    profile_data = {

        "자산": {
            "general": 27018,
            "long": 5068,
            "change": -81.24,
            "rbc": -0.4264
        },

        "저축금액": {
            "general": 2631,
            "long": 704,
            "change": -73.24,
            "rbc": -0.3397
        },

        "유동자산": {
            "general": 3930,
            "long": 1470,
            "change": -62.60,
            "rbc": -0.2872
        },

        "부채": {
            "general": 8000,
            "long": 3920,
            "change": -51.00,
            "rbc": -0.2322
        },

        "처분가능소득": {
            "general": 4378,
            "long": 2698.5,
            "change": -38.36,
            "rbc": -0.3225
        },

        "가구원수": {
            "general": 3,
            "long": 2,
            "change": -33.33,
            "rbc": -0.2354
        },

        "소비지출": {
            "general": 2760,
            "long": 1904,
            "change": -31.01,
            "rbc": -0.3145
        }
    }


    selected_profile = st.selectbox(

        "비교 변수 선택 · INSPECT CHARACTERISTIC",

        list(profile_data.keys()),

        index=0
    )


    info = profile_data[
        selected_profile
    ]


    # ========================================================
    # 03 · FINANCIAL CAPACITY CHART
    # ========================================================

    chart_col, insight_col = st.columns(
        [1.42, .58],
        gap="large"
    )


    with chart_col:

        variables = [
            "자산",
            "저축금액",
            "유동자산",
            "부채",
            "처분가능소득",
            "가구원수",
            "소비지출"
        ]


        changes = [
            profile_data[v]["change"]
            for v in variables
        ]


        # ----------------------------------------------------
        # COLORS
        # selected = cyan
        # remaining = cobalt
        # ----------------------------------------------------

        colors = []

        line_colors = []

        line_widths = []


        for variable in variables:

            if variable == selected_profile:

                colors.append("#32C8FF")
                line_colors.append("#BFF3FF")
                line_widths.append(2)

            else:

                colors.append("#4385FF")
                line_colors.append(
                    "rgba(110,165,255,.35)"
                )
                line_widths.append(.5)


        fig_profile = go.Figure()


        fig_profile.add_trace(
            go.Bar(

                x=changes,
                y=variables,

                orientation="h",

                marker=dict(
                    color=colors,

                    line=dict(
                        color=line_colors,
                        width=line_widths
                    )
                ),

                # IMPORTANT:
                # 직접 숫자 표시

                text=[
                    f"<b>{x:.1f}%</b>"
                    for x in changes
                ],

                textposition="inside",

                insidetextanchor="start",

                textfont=dict(
                    size=15,
                    color="#FFFFFF"
                ),

                cliponaxis=False,

                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>"
                    "일반 연체 대비 30일+ 연체"
                    "<br>"
                    "<b>%{x:.2f}%</b>"
                    "<extra></extra>"
                )
            )
        )


        # ZERO LINE

        fig_profile.add_vline(

            x=0,

            line_width=2,

            line_color="rgba(220,240,255,.58)"
        )


        fig_profile.update_layout(

            height=525,

            title=dict(

                text=(
                    "<b>30일+ 연체가구의 재무여력 차이</b>"
                    "<br>"
                    "<span style='font-size:11px;'>"
                    "일반 연체가구 대비 중앙값 차이 · OBSERVED DATA"
                    "</span>"
                ),

                x=.01,

                font=dict(
                    size=18,
                    color="#FFFFFF"
                )
            ),


            paper_bgcolor=
                "rgba(0,0,0,0)",


            plot_bgcolor=
                "rgba(16,45,75,.54)",


            margin=dict(
                l=25,
                r=35,
                t=85,
                b=75
            ),


            xaxis=dict(

                title=dict(
                    text="일반 연체가구 대비 차이 (%)",

                    font=dict(
                        size=15,
                        color="#D7E6F4"
                    ),

                    standoff=18
                ),

                # +274% 제거했으므로
                # 음수 영역을 크게 사용

                range=[-100, 5],

                tickvals=[
                    -100,
                    -80,
                    -60,
                    -40,
                    -20,
                    0
                ],

                ticktext=[
                    "−100%",
                    "−80%",
                    "−60%",
                    "−40%",
                    "−20%",
                    "0%"
                ],

                gridcolor=
                    "rgba(150,190,225,.13)",

                zeroline=False,

                tickfont=dict(
                    size=13,
                    color="#C5D8E9"
                )
            ),


            yaxis=dict(

                autorange="reversed",

                title=None,

                tickfont=dict(
                    size=15,
                    color="#F1F7FD"
                ),

                ticklabelposition="outside"
            ),


            showlegend=False,


            hoverlabel=dict(

                bgcolor="#123252",

                bordercolor="#32C8FF",

                font=dict(
                    size=13,
                    color="#FFFFFF"
                )
            )
        )


        animated_bar_chart(
            fig_profile,
            key="profile_animation",
            steps=16,
            delay=0.04
        )


        st.caption(
            "CYAN · 현재 선택 변수  |  "
            "COBALT · 기타 재무특성"
        )


    # ========================================================
    # 04 · CHARACTERISTIC INSPECTOR
    # ========================================================

    with insight_col:

        st.caption(
            "CHARACTERISTIC INSPECTOR"
        )

        st.markdown(
            f"## {selected_profile}"
        )

        st.write("")


        general = info["general"]
        long_value = info["long"]
        change = info["change"]


        m1, m2 = st.columns(2)


        with m1:

            if selected_profile == "가구원수":

                st.metric(
                    "일반 연체",
                    f"{general:.0f}명"
                )

            else:

                st.metric(
                    "일반 연체",
                    f"{general:,.1f}"
                )


        with m2:

            if selected_profile == "가구원수":

                st.metric(
                    "30일+ 연체",
                    f"{long_value:.0f}명"
                )

            else:

                st.metric(
                    "30일+ 연체",
                    f"{long_value:,.1f}"
                )


        st.write("")

        st.caption(
            "OBSERVED DIFFERENCE"
        )


        st.markdown(
            f"""
<div style="
    font-size:38px;
    font-weight:850;
    color:#FF704D;
    letter-spacing:-1.5px;
    text-shadow:
        0 0 20px rgba(255,112,77,.30);
    margin-top:-5px;
    margin-bottom:8px;
">
    {change:.2f}%
</div>
""",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # VARIABLE INTERPRETATION
        # ----------------------------------------------------

        if selected_profile == "자산":

            interpretation = (
                "30일 이상 연체가구의 자산 중앙값은 "
                "일반 연체가구보다 약 81.2% 낮았습니다."
            )


        elif selected_profile == "저축금액":

            interpretation = (
                "30일 이상 연체가구의 저축금액 중앙값은 "
                "일반 연체가구보다 약 73.2% 낮았습니다."
            )


        elif selected_profile == "유동자산":

            interpretation = (
                "30일 이상 연체가구의 유동자산 중앙값은 "
                "일반 연체가구보다 약 62.6% 낮았습니다."
            )


        elif selected_profile == "부채":

            interpretation = (
                "총부채 중앙값 자체는 30일 이상 연체가구에서 "
                "약 51.0% 낮게 관측되었습니다. "
                "따라서 단순한 부채 규모만으로 "
                "취약성을 설명하기 어렵습니다."
            )


        elif selected_profile == "처분가능소득":

            interpretation = (
                "30일 이상 연체가구의 처분가능소득 중앙값은 "
                "일반 연체가구보다 약 38.4% 낮았습니다."
            )


        elif selected_profile == "소비지출":

            interpretation = (
                "30일 이상 연체가구의 소비지출 중앙값은 "
                "일반 연체가구보다 약 31.0% 낮았습니다."
            )


        else:

            interpretation = (
                "30일 이상 연체가구의 가구원수 중앙값은 "
                "일반 연체가구보다 낮게 관측되었습니다."
            )


        st.write(
            interpretation
        )


        st.caption(
            f'RANK-BISERIAL CORRELATION · '
            f'{info["rbc"]:+.4f}'
        )


        st.write("")


        st.warning(
            "관측된 집단 간 차이이며, "
            "연체의 인과요인으로 해석하지 않습니다."
        )


    # ========================================================
    # 05 · RISK DEBT SIGNAL
    # ========================================================

    st.divider()


    st.caption(
        "DEBT STRUCTURE · RISK SIGNAL"
    )


    st.markdown(
        """
### 재무여력은 낮았지만, :orange[위험부채의 구성비]는 더 높게 관측되었습니다.
"""
    )


    risk_left, risk_right = st.columns(
        [1.05, .95],
        gap="large"
    )


    # ========================================================
    # UNSERCURED RISK DEBT
    # ========================================================

    with risk_left:

        fig_risk = go.Figure()


        fig_risk.add_trace(
            go.Bar(

                x=[
                    0.19,
                    0.71
                ],

                y=[
                    "일반 연체",
                    "30일+ 연체"
                ],

                orientation="h",

                marker=dict(
                    color=[
                        "#4385FF",
                        "#FF704D"
                    ]
                ),

                text=[
                    "0.19",
                    "0.71"
                ],

                textposition="inside",

                textfont=dict(
                    size=16,
                    color="#FFFFFF"
                ),

                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>"
                    "무담보위험부채비율 %{x:.2f}"
                    "<extra></extra>"
                )
            )
        )


        fig_risk.update_layout(

            height=290,

            title=dict(

                text=(
                    "<b>무담보위험부채비율</b>"
                    "<br>"
                    "<span style='font-size:11px;'>"
                    "0.19 → 0.71 · +274.75%"
                    "</span>"
                ),

                x=.02,

                font=dict(
                    size=17,
                    color="#FFFFFF"
                )
            ),

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(16,45,75,.54)",

            margin=dict(
                l=20,
                r=30,
                t=80,
                b=40
            ),

            xaxis=dict(

                range=[0, .80],

                tickvals=[
                    0,
                    .2,
                    .4,
                    .6,
                    .8
                ],

                gridcolor=
                    "rgba(150,190,225,.12)",

                tickfont=dict(
                    size=12,
                    color="#BFD2E4"
                )
            ),

            yaxis=dict(

                autorange="reversed",

                tickfont=dict(
                    size=14,
                    color="#F1F7FD"
                )
            ),

            showlegend=False
        )


        st.plotly_chart(
        apply_motion(fig_risk),

            use_container_width=True,

            config={
                "displaylogo": False,
                "displayModeBar": False
            }
        )


    # ========================================================
    # PERSONAL / WORKPLACE BORROWING
    # ========================================================

    with risk_right:

        st.caption(
            "PERSONAL / WORKPLACE BORROWING"
        )


        st.markdown(
            """
<div style="
    font-size:46px;
    font-weight:900;
    line-height:1;
    color:#FF704D;
    letter-spacing:-2px;
    text-shadow:
        0 0 25px rgba(255,112,77,.34);
    margin:10px 0 5px 0;
">
    2.45×
</div>
""",
            unsafe_allow_html=True
        )


        st.caption(
            "30일+ 연체가구의 상대 보유비율"
        )


        st.write("")


        r1, r2 = st.columns(2)


        with r1:

            st.metric(
                "일반 연체",
                "10.16%"
            )


        with r2:

            st.metric(
                "30일+ 연체",
                "24.94%"
            )


        st.write("")


        st.markdown(
            "**+14.77%p**"
        )


        st.caption(
            "χ² = 69.60 · p < .001"
        )


        st.write(
            "30일 이상 연체가구에서 "
            "개인·직장 차입 보유비율이 "
            "일반 연체가구의 약 2.45배로 관측되었습니다."
        )


    # ========================================================
    # 06 · KEY FINDING
    # ========================================================

    st.divider()


    st.caption(
        "KEY FINDING · OBSERVED HOUSEHOLD PROFILE"
    )


    st.markdown(
        """
### 30일 이상 연체가구는 :orange[단순히 부채가 많은 집단]으로 설명되지 않았습니다.
"""
    )


    st.write(
        "실제 관측자료에서는 상대적으로 낮은 "
        "자산·유동성·저축 수준과 함께, "
        "높은 무담보 위험부채 비중 및 특정 차입구조가 "
        "동시에 관측되었습니다."
    )


    st.caption(
        "집단 간 연관성에 대한 기술적 분석이며 "
        "인과관계를 의미하지 않습니다."
    )


    # ========================================================
    # 07 · NAVIGATION
    # ========================================================

    st.write("")


    back_col, empty_col = st.columns(
        [1, 5]
    )


    with back_col:

        if st.button(
            "← EXPLAIN",
            use_container_width=True
        ):

            st.session_state.page = "EXPLAIN"

            st.rerun()  
            
# ============================================================
# 09. VALIDATE · OUT-OF-TIME VALIDATION
# ============================================================

elif st.session_state.page == "VALIDATE":

    motion_signal("TEMPORAL VALIDATION · LIVE")

    st.markdown(":blue[**05 / OUT-OF-TIME VALIDATION**]")

    st.markdown(
        "## DEV에서 선정한 XGBoost는 미래 시점에서도 유지되는가?"
    )

    st.caption(
        "2021–2023 DEVELOPMENT → 2024 INPUT → 2025 OOT VALIDATION"
    )

    st.write("")


    # ========================================================
    # 01 · PERFORMANCE SHIFT
    # ========================================================

    st.caption("01 / PERFORMANCE SHIFT")

    st.markdown(
        "### 미래 시점에서의 :orange[성능 변화]"
    )

    st.write(
        "DEV에서 선정한 XGBoost와 분류 임계값 0.7786을 "
        "그대로 고정하여 2025 OOT 성능을 평가했습니다."
    )

    st.write("")


    # --------------------------------------------------------
    # VISUAL KPI CARDS
    # --------------------------------------------------------

    components.html(
        """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 2px;

    background: transparent;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    color: #F8FBFF;

    overflow: hidden;
}


.grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 14px;
}


.card {

    position: relative;

    height: 176px;

    overflow: hidden;

    padding: 17px 19px;

    border-radius: 12px;

    background:

        radial-gradient(
            circle at 90% 0%,
            rgba(67,133,255,.20),
            transparent 40%
        ),

        linear-gradient(
            145deg,
            rgba(22,60,96,.98),
            rgba(13,42,72,.98)
        );

    border:
        1px solid rgba(89,174,255,.43);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 12px 28px rgba(0,0,0,.13);

    transition:
        transform .20s ease,
        box-shadow .20s ease;
}


.card:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 15px 35px rgba(67,133,255,.17);
}


.card::before {

    content: "";

    position: absolute;

    top: 0;
    left: 0;

    width: 100%;
    height: 3px;

    background:
        linear-gradient(
            90deg,
            #4385FF,
            #32C8FF,
            transparent
        );
}


.label {

    font-size: 10px;

    font-weight: 750;

    letter-spacing: .5px;

    color: #BBD0E4;
}


.row {

    display: grid;

    grid-template-columns:
        1fr auto 1fr;

    align-items: center;

    gap: 8px;

    margin-top: 15px;
}


.dev,
.oot {

    font-size: 24px;

    font-weight: 850;

    letter-spacing: -1px;
}


.dev {

    color: #6DA4FF;

    text-shadow:
        0 0 17px rgba(67,133,255,.27);
}


.oot {

    color: #55D6FF;

    text-shadow:
        0 0 17px rgba(50,200,255,.25);
}


.arrow {

    color: #7895B2;

    font-size: 19px;

    font-weight: 700;
}


.names {

    display: flex;

    justify-content: space-between;

    margin-top: 4px;

    color: #7F9AB4;

    font-size: 8px;

    font-weight: 700;

    letter-spacing: .4px;
}


.track {

    position: relative;

    height: 5px;

    margin-top: 13px;

    border-radius: 10px;

    background:
        rgba(125,165,205,.15);
}


.dev-dot {

    position: absolute;

    left: 84%;

    top: 50%;

    width: 10px;
    height: 10px;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    background: #4385FF;

    box-shadow:
        0 0 12px rgba(67,133,255,.50);
}


.oot-dot {

    position: absolute;

    left: 64%;

    top: 50%;

    width: 10px;
    height: 10px;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    background: #32C8FF;

    box-shadow:
        0 0 12px rgba(50,200,255,.50);
}


.delta {

    margin-top: 10px;

    color: #FF8B70;

    font-size: 10px;

    font-weight: 800;

    text-shadow:
        0 0 12px rgba(255,112,77,.22);
}


.meta {

    margin-top: 3px;

    color: #7993AD;

    font-size: 8px;

    font-weight: 650;
}


.card:nth-child(2){animation-delay:.08s}
.card:nth-child(3){animation-delay:.16s}

@keyframes validateCardIn{
    to{opacity:1;transform:translateY(0)}
}

.dev-dot{animation:devPulse 1.8s ease-in-out infinite}
.oot-dot{animation:ootPulse 1.8s .25s ease-in-out infinite}

@keyframes devPulse{
    0%,100%{box-shadow:0 0 8px rgba(67,133,255,.35)}
    50%{box-shadow:0 0 18px rgba(67,133,255,.68)}
}
@keyframes ootPulse{
    0%,100%{box-shadow:0 0 8px rgba(50,200,255,.35)}
    50%{box-shadow:0 0 18px rgba(50,200,255,.68)}
}
</style>

</head>


<body>

<div class="grid">


    <!-- PR AUC -->

    <div class="card">

        <div class="label">
            PR-AUC · PRIMARY METRIC
        </div>

        <div class="row">

            <div class="dev">
                0.2203
            </div>

            <div class="arrow">
                →
            </div>

            <div class="oot">
                0.1519
            </div>

        </div>

        <div class="names">
            <span>DEV OOF</span>
            <span>2025 OOT</span>
        </div>

        <div class="track">
            <div class="dev-dot"></div>
            <div class="oot-dot"></div>
        </div>

        <div class="delta">
            ▼ 0.0684
        </div>

    </div>


    <!-- ROC AUC -->

    <div class="card">

        <div class="label">
            ROC-AUC · DISCRIMINATION
        </div>

        <div class="row">

            <div class="dev">
                0.8034
            </div>

            <div class="arrow">
                →
            </div>

            <div class="oot">
                0.7874
            </div>

        </div>

        <div class="names">
            <span>DEV OOF</span>
            <span>2025 OOT</span>
        </div>

        <div class="track">
            <div
                class="dev-dot"
                style="left:82%;">
            </div>

            <div
                class="oot-dot"
                style="left:78%;">
            </div>
        </div>

        <div class="delta">
            ▼ 0.0160
        </div>

    </div>


    <!-- KS -->

    <div class="card">

        <div class="label">
            KS · SEPARATION POWER
        </div>

        <div class="row">

            <div class="dev">
                0.4877
            </div>

            <div class="arrow">
                →
            </div>

            <div class="oot">
                0.4680
            </div>

        </div>

        <div class="names">
            <span>DEV OOF</span>
            <span>2025 OOT</span>
        </div>

        <div class="track">

            <div
                class="dev-dot"
                style="left:63%;">
            </div>

            <div
                class="oot-dot"
                style="left:58%;">
            </div>

        </div>

        <div class="delta">
            ▼ 0.0197
        </div>

    </div>


</div>

</body>
</html>
""",
        height=192,
        scrolling=False
    )


    st.write("")


    # ========================================================
    # 02 · PERFORMANCE COMPARISON CHART
    # ========================================================

    metric_names = [
        "PR-AUC",
        "ROC-AUC",
        "KS",
        "Precision",
        "Recall",
        "F1"
    ]


    dev_values = [
        .2203,
        .8034,
        .4877,
        .2630,
        .3438,
        .2980
    ]


    oot_values = [
        .1519,
        .7874,
        .4680,
        .1847,
        .3064,
        .2304
    ]


    fig_validate = go.Figure()


    fig_validate.add_trace(
        go.Bar(

            name="DEV OOF",

            x=metric_names,
            y=dev_values,

            marker=dict(
                color="#4385FF"
            ),

            text=[
                f"{v:.4f}"
                for v in dev_values
            ],

            textposition="outside",

            textfont=dict(
                size=13,
                color="#CFE0FF"
            ),

            hovertemplate=(
                "<b>%{x}</b>"
                "<br>"
                "DEV OOF %{y:.4f}"
                "<extra></extra>"
            )
        )
    )


    fig_validate.add_trace(
        go.Bar(

            name="2025 OOT",

            x=metric_names,
            y=oot_values,

            marker=dict(
                color="#32C8FF"
            ),

            text=[
                f"{v:.4f}"
                for v in oot_values
            ],

            textposition="outside",

            textfont=dict(
                size=13,
                color="#D8F7FF"
            ),

            hovertemplate=(
                "<b>%{x}</b>"
                "<br>"
                "2025 OOT %{y:.4f}"
                "<extra></extra>"
            )
        )
    )


    fig_validate.update_layout(

        height=430,

        barmode="group",

        title=dict(

            text=(
                "<b>DEV → OOT 성능 비교</b>"
                "<br>"
                "<span style='font-size:11px;'>"
                "FINAL XGBOOST · FROZEN THRESHOLD = 0.7786"
                "</span>"
            ),

            x=.01,

            font=dict(
                size=18,
                color="#FFFFFF"
            )
        ),

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            "rgba(16,45,75,.54)",

        margin=dict(
            l=45,
            r=25,
            t=85,
            b=55
        ),

        xaxis=dict(

            tickfont=dict(
                size=14,
                color="#EDF6FF"
            )
        ),

        yaxis=dict(

            title=dict(
                text="Metric Value",

                font=dict(
                    size=14,
                    color="#D7E6F4"
                )
            ),

            range=[0, .9],

            gridcolor=
                "rgba(150,190,225,.13)",

            tickfont=dict(
                size=12,
                color="#BDD0E2"
            )
        ),

        legend=dict(

            orientation="h",

            x=.68,
            y=1.14,

            font=dict(
                size=11,
                color="#D5E4F3"
            )
        ),

        hoverlabel=dict(
            bgcolor="#123252",
            font_color="#FFFFFF"
        )
    )


    st.plotly_chart(
        apply_motion(fig_validate),

        use_container_width=True,

        config={
            "displaylogo": False,
            "displayModeBar": False
        }
    )


    st.caption(
        "COBALT · DEV OOF   |   "
        "CYAN · 2025 OOT   |   "
        "OOT는 모형 선정 및 Threshold 조정에 사용하지 않음"
    )


    # ========================================================
    # 03 · INPUT STABILITY · PSI
    # ========================================================

    st.divider()

    st.caption(
        "02 / INPUT STABILITY"
    )

    st.markdown(
        "### 성능 감소가 :blue[입력변수의 분포 변화] 때문이었는가?"
    )


    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box}
body{
    margin:0;padding:3px;background:transparent;color:#F8FBFF;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    overflow:hidden;
}
.monitor{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
}
.mcard{
    position:relative;
    height:112px;
    padding:14px 16px;
    border-radius:11px;
    overflow:hidden;
    background:
        radial-gradient(circle at 92% 0%,rgba(47,224,208,.14),transparent 42%),
        linear-gradient(145deg,rgba(20,57,92,.96),rgba(10,35,60,.98));
    border:1px solid rgba(50,200,255,.32);
    opacity:0;
    transform:translateY(12px);
    animation:enter .52s cubic-bezier(.2,.8,.2,1) forwards;
    transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;
}
.mcard:nth-child(2){animation-delay:.07s}
.mcard:nth-child(3){animation-delay:.14s}
.mcard:nth-child(4){animation-delay:.21s}
.mcard:hover{
    transform:translateY(-3px);
    border-color:rgba(47,224,208,.60);
    box-shadow:0 12px 28px rgba(47,224,208,.08);
}
.label{
    font-size:9px;font-weight:800;letter-spacing:.55px;color:#8FA9C3;
}
.value{
    margin-top:7px;font-size:29px;font-weight:900;letter-spacing:-1.2px;
    color:#EAF7FF;
}
.aqua{color:#55E5D7;text-shadow:0 0 18px rgba(47,224,208,.18)}
.orange{color:#FF8B70}
.sub{margin-top:3px;font-size:9px;font-weight:650;color:#8FA9C3}
.track{
    height:5px;margin-top:8px;border-radius:99px;background:rgba(130,170,205,.13);
    overflow:hidden;
}
.fill{
    height:100%;width:0;border-radius:99px;
    background:linear-gradient(90deg,#4385FF,#2FE0D0);
    animation:grow 1.05s .35s cubic-bezier(.2,.8,.2,1) forwards;
}
.ref{
    position:absolute;right:14px;bottom:12px;font-size:8px;color:#FF9B84;font-weight:800;
}
@keyframes enter{to{opacity:1;transform:translateY(0)}}
@keyframes grow{to{width:41.3%}}
@media(prefers-reduced-motion:reduce){
    *{animation-duration:.001ms!important;transition-duration:.001ms!important}
    .fill{width:41.3%}
}
</style>
</head>
<body>
<div class="monitor">
  <div class="mcard">
    <div class="label">VARIABLES CHECKED</div>
    <div class="value">12</div>
    <div class="sub">INPUT FEATURES</div>
  </div>
  <div class="mcard">
    <div class="label">MAX PSI</div>
    <div class="value aqua">0.0413</div>
    <div class="sub">주거비 · HIGHEST</div>
    <div class="track"><div class="fill"></div></div>
    <div class="ref">0.10 REF</div>
  </div>
  <div class="mcard">
    <div class="label">ABOVE 0.10</div>
    <div class="value aqua">0</div>
    <div class="sub">NO VARIABLE EXCEEDED</div>
  </div>
  <div class="mcard">
    <div class="label">INPUT STABILITY</div>
    <div class="value aqua">STABLE</div>
    <div class="sub">12 / 12 BELOW REFERENCE</div>
  </div>
</div>
</body>
</html>
""",
        height=126,
        scrolling=False
    )



    psi_data = {

        "주거비": .0413,
        "소비지출": .0360,
        "처분가능소득": .0244,
        "저축금액": .0080,
        "가구원수": .0077,
        "무담보위험부채비율": .0075,
        "자산": .0074,
        "유동자산": .0068,
        "개인·직장 차입": .0067,
        "부채": .0064,
        "카드대출": .0022,
        "신용대출": .0012
    }


    psi_names = list(
        psi_data.keys()
    )[::-1]


    psi_values = [
        psi_data[x]
        for x in psi_names
    ]


    fig_psi = go.Figure()


    fig_psi.add_trace(
        go.Bar(

            x=psi_values,
            y=psi_names,

            orientation="h",

            marker=dict(
                color="#2FE0D0"
            ),

            text=[
                f"{v:.4f}"
                for v in psi_values
            ],

            textposition="outside",

            textfont=dict(
                size=12,
                color="#CFFFF8"
            ),

            cliponaxis=False,

            hovertemplate=(
                "<b>%{y}</b>"
                "<br>"
                "PSI %{x:.4f}"
                "<br>"
                "0.10 미만 · Stable"
                "<extra></extra>"
            )
        )
    )


    # 0.10 reference line

    fig_psi.add_vline(

        x=.10,

        line_width=2,

        line_dash="dash",

        line_color=
            "rgba(255,112,77,.75)"
    )


    fig_psi.add_annotation(

        x=.10,
        y=11.3,

        text="<b>0.10 REFERENCE</b>",

        showarrow=False,

        xanchor="right",

        font=dict(
            size=10,
            color="#FF9B84"
        )
    )


    fig_psi.update_layout(

        height=470,

        title=dict(

            text=(
                "<b>12개 입력변수 PSI</b>"
                "<br>"
                "<span style='font-size:11px;'>"
                "ALL VARIABLES BELOW 0.10"
                "</span>"
            ),

            x=.01,

            font=dict(
                size=18,
                color="#FFFFFF"
            )
        ),

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            "rgba(16,45,75,.54)",

        margin=dict(
            l=25,
            r=70,
            t=80,
            b=55
        ),

        xaxis=dict(

            title=dict(
                text="Population Stability Index (PSI)",

                font=dict(
                    size=14,
                    color="#D7E6F4"
                )
            ),

            range=[0, .115],

            tickfont=dict(
                size=12,
                color="#BDD0E2"
            ),

            gridcolor=
                "rgba(150,190,225,.13)"
        ),

        yaxis=dict(

            tickfont=dict(
                size=13,
                color="#EDF6FF"
            )
        ),

        showlegend=False,

        hoverlabel=dict(
            bgcolor="#123252",
            bordercolor="#2FE0D0",
            font_color="#FFFFFF"
        )
    )


    animated_bar_chart(
        fig_psi,
        key="psi_animation",
        steps=16,
        delay=0.04
    )


    p1, p2 = st.columns(
        [1, 2],
        gap="large"
    )


    with p1:

        st.metric(
            "MAX PSI",
            "0.0413"
        )

        st.caption(
            "주거비 · 12개 변수 모두 < 0.10"
        )


    with p2:

        st.markdown(
            "### :blue[INPUT DISTRIBUTION · STABLE]"
        )

        st.write(
            "12개 주요 입력변수의 PSI가 모두 0.10 미만으로 나타났습니다. "
            "따라서 OOT에서의 성능 감소를 소득·자산·부채 등 "
            "주요 입력변수의 단순한 분포 변화만으로 설명하기는 어렵습니다."
        )

        st.caption(
            "PSI는 개별 변수의 주변분포 안정성을 확인하는 지표이며, "
            "개념 변화나 변수 간 결합분포 변화를 배제하지는 않습니다."
        )


    # ========================================================
    # 04 · 2024 INPUT → 2025 OOT OUTCOME
    # ========================================================

    st.divider()

    st.caption("03 / TEMPORAL TRANSITION")

    st.markdown(
        "### :blue[2024년 가구정보]는 2025년 실제 장기연체 결과로 어떻게 연결되었는가?"
    )

    st.write(
        "DEV에서 확정한 XGBoost와 임계값 0.7786을 변경하지 않고, "
        "2024년 가구정보를 입력해 2025년 실제 30일 이상 장기연체 여부를 평가했습니다."
    )

    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box}
body{
    margin:0;padding:3px;background:transparent;color:#F8FBFF;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    overflow:hidden;
}
.stage{
    position:relative;
    height:320px;
    border-radius:14px;
    overflow:hidden;
    border:1px solid rgba(67,133,255,.28);
    background:
      radial-gradient(circle at 16% 50%,rgba(67,133,255,.18),transparent 25%),
      radial-gradient(circle at 84% 50%,rgba(255,112,77,.12),transparent 25%),
      linear-gradient(135deg,rgba(11,36,62,.98),rgba(15,48,79,.96));
}
.grid{
    position:absolute;inset:0;opacity:.22;
    background-image:
      linear-gradient(rgba(120,175,230,.10) 1px,transparent 1px),
      linear-gradient(90deg,rgba(120,175,230,.10) 1px,transparent 1px);
    background-size:46px 46px;
}
.node{
    position:absolute;top:55px;width:210px;height:205px;padding:16px;
    border-radius:13px;
    background:linear-gradient(145deg,rgba(21,59,95,.96),rgba(10,34,59,.98));
    opacity:0;transform:translateY(12px);
    animation:nodeIn .55s cubic-bezier(.2,.8,.2,1) forwards;
}
.left{
    left:34px;border:1px solid rgba(67,133,255,.55);
    box-shadow:0 0 30px rgba(67,133,255,.07);
}
.right{
    right:34px;border:1px solid rgba(255,112,77,.48);
    box-shadow:0 0 30px rgba(255,112,77,.06);
    animation-delay:1.1s;
}
.kicker{font-size:9px;font-weight:800;letter-spacing:.7px;color:#8EA9C5}
.year{
    margin-top:6px;font-size:42px;line-height:1;font-weight:950;letter-spacing:-2px;
}
.left .year{color:#76A8FF}
.right .year{color:#FF8B70}
.big{margin-top:13px;font-size:25px;font-weight:900;letter-spacing:-1px}
.small{margin-top:3px;font-size:10px;color:#91ABC4;font-weight:650}
.metrics{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:10px}
.metric{
    padding:7px;border-radius:8px;background:rgba(120,170,215,.08);
    border:1px solid rgba(120,170,215,.12);
}
.mv{font-size:16px;font-weight:900;color:#F4FAFF}
.ml{font-size:7px;font-weight:800;color:#7896B4;letter-spacing:.35px}
.rail{
    position:absolute;left:270px;right:270px;top:156px;height:5px;
    border-radius:99px;background:rgba(120,170,215,.13);overflow:visible;
}
.progress{
    position:absolute;left:0;top:0;height:100%;width:0;border-radius:99px;
    background:linear-gradient(90deg,#4385FF,#32C8FF,#FF704D);
    box-shadow:0 0 16px rgba(50,200,255,.28);
    animation:travel 1.55s .48s cubic-bezier(.2,.75,.2,1) forwards;
}
.signal{
    position:absolute;left:0;top:50%;width:16px;height:16px;border-radius:50%;
    transform:translate(-50%,-50%);
    background:#EAF8FF;border:3px solid #32C8FF;
    box-shadow:0 0 22px rgba(50,200,255,.65);
    animation:signalMove 1.55s .48s cubic-bezier(.2,.75,.2,1) forwards;
}
.arrow{
    position:absolute;left:50%;top:105px;transform:translateX(-50%);
    text-align:center;opacity:0;animation:fade .4s .8s forwards;
}
.arrow .main{font-size:12px;font-weight:900;color:#C9DDF0;letter-spacing:.7px}
.arrow .sub{font-size:8px;color:#7694B1;margin-top:4px}
.result{
    position:absolute;left:50%;bottom:14px;transform:translateX(-50%) translateY(8px);
    opacity:0;white-space:nowrap;
    padding:9px 16px;border-radius:999px;
    background:rgba(255,112,77,.10);border:1px solid rgba(255,112,77,.30);
    color:#FFD1C6;font-size:10px;font-weight:800;letter-spacing:.35px;
    animation:resultIn .5s 1.85s forwards;
}
@keyframes nodeIn{to{opacity:1;transform:translateY(0)}}
@keyframes travel{to{width:100%}}
@keyframes signalMove{to{left:100%;border-color:#FF704D;box-shadow:0 0 24px rgba(255,112,77,.60)}}
@keyframes fade{to{opacity:1}}
@keyframes resultIn{to{opacity:1;transform:translateX(-50%) translateY(0)}}
@media(prefers-reduced-motion:reduce){
  *{animation-duration:.001ms!important;animation-delay:0ms!important}
  .progress{width:100%}.signal{left:100%}
}
</style>
</head>
<body>
<div class="stage">
  <div class="grid"></div>

  <div class="node left">
    <div class="kicker">MODEL INPUT · t</div>
    <div class="year">2024</div>
    <div class="big">6,607</div>
    <div class="small">금융부채 보유가구 · HOUSEHOLD INPUT</div>
    <div class="metrics">
      <div class="metric"><div class="mv">12</div><div class="ml">FEATURES</div></div>
      <div class="metric"><div class="mv">0.7786</div><div class="ml">FROZEN THRESHOLD</div></div>
    </div>
  </div>

  <div class="arrow">
    <div class="main">XGBOOST · NEXT-YEAR RISK</div>
    <div class="sub">DEV에서 확정한 모델과 임계값을 그대로 적용</div>
  </div>

  <div class="rail">
    <div class="progress"></div>
    <div class="signal"></div>
  </div>

  <div class="node right">
    <div class="kicker">OBSERVED OUTCOME · t+1</div>
    <div class="year">2025</div>
    <div class="big">173</div>
    <div class="small">ACTUAL 30D+ DELINQUENT HOUSEHOLDS · 2.62%</div>
    <div class="metrics">
      <div class="metric"><div class="mv">0.1519</div><div class="ml">PR-AUC</div></div>
      <div class="metric"><div class="mv">0.7874</div><div class="ml">ROC-AUC</div></div>
    </div>
  </div>

  <div class="result">2024 INPUT → 2025 OOT · TEMPORALLY SEPARATED VALIDATION</div>
</div>
</body>
</html>
""",
        height=335,
        scrolling=False
    )

    st.caption(
        "2024년 입력정보에서 2025년 실제 결과까지 시간적으로 분리해 평가했으며, "
        "OOT 결과는 모형 선정이나 Threshold 조정에 사용하지 않았습니다."
    )


    # ========================================================
    # 05 · OOT CONFUSION MATRIX
    # ========================================================

    st.divider()

    st.caption("04 / OOT CLASSIFICATION RESULT")
    st.markdown("### 고정 임계값 :blue[0.7786] 적용 시 실제 분류 결과")
    st.write(
        "DEV OOF에서 확정한 임계값을 OOT에서 변경하지 않고 적용해, "
        "2025년 실제 장기연체 여부와 모델의 분류 결과를 직접 비교했습니다."
    )

    tn, fp, fn, tp = 6200, 234, 120, 53
    actual_positive = tp + fn
    predicted_positive = tp + fp
    recall_oot = tp / actual_positive
    precision_oot = tp / predicted_positive
    f1_oot = 2 * precision_oot * recall_oot / (precision_oot + recall_oot)

    cm_k1, cm_k2, cm_k3, cm_k4 = st.columns(4)
    with cm_k1:
        st.metric("ACTUAL 30D+", f"{actual_positive:,}", "2025 OBSERVED")
    with cm_k2:
        st.metric("TRUE POSITIVE", f"{tp:,}", "CORRECTLY FLAGGED")
    with cm_k3:
        st.metric("RECALL", f"{recall_oot:.2%}", "53 / 173")
    with cm_k4:
        st.metric("PRECISION", f"{precision_oot:.2%}", "53 / 287")

    st.write("")

    # 의미별 색상을 사용해 TN 6,200이 나머지 셀의 시각적 대비를 압도하지 않도록 구성
    cm_z = np.array([[0, 1], [2, 3]])
    cm_counts = np.array([[tn, fp], [fn, tp]])
    cm_labels = np.array([
        [f"<b>TN</b><br>{tn:,}<br><span style='font-size:11px'>정상 → 정상</span>",
         f"<b>FP</b><br>{fp:,}<br><span style='font-size:11px'>정상 → 위험</span>"],
        [f"<b>FN</b><br>{fn:,}<br><span style='font-size:11px'>장기연체 → 정상</span>",
         f"<b>TP</b><br>{tp:,}<br><span style='font-size:11px'>장기연체 → 위험</span>"]
    ])

    fig_cm = go.Figure(
        go.Heatmap(
            z=cm_z,
            x=["정상 예측", "장기연체 위험 예측"],
            y=["실제 정상", "실제 30일+ 연체"],
            text=cm_labels,
            texttemplate="%{text}",
            textfont=dict(size=18, color="#F8FBFF"),
            customdata=cm_counts,
            colorscale=[
                [0.00, "#153A5E"], [0.32, "#153A5E"],
                [0.33, "#5A3A38"], [0.65, "#5A3A38"],
                [0.66, "#263B59"], [0.82, "#263B59"],
                [0.83, "#176C78"], [1.00, "#176C78"],
            ],
            zmin=0, zmax=3,
            showscale=False,
            xgap=5, ygap=5,
            hovertemplate=(
                "<b>%{y}</b><br>%{x}<br>가구 수 %{customdata:,}<extra></extra>"
            ),
        )
    )

    fig_cm.update_layout(
        height=410,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(16,45,75,.30)",
        margin=dict(l=35, r=25, t=25, b=55),
        font=dict(color="#D9E8F7"),
        xaxis=dict(
            title=dict(text="MODEL PREDICTION", font=dict(size=12, color="#8FA9C3")),
            side="bottom",
            tickfont=dict(size=15, color="#EDF6FF"),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(text="ACTUAL OUTCOME", font=dict(size=12, color="#8FA9C3")),
            autorange="reversed",
            tickfont=dict(size=15, color="#EDF6FF"),
            showgrid=False,
        ),
        hoverlabel=dict(bgcolor="#123252", bordercolor="#32C8FF", font_color="#FFFFFF"),
    )

    st.plotly_chart(
        apply_motion(fig_cm),
        use_container_width=True,
        config={"displaylogo": False, "displayModeBar": False},
    )

    st.markdown(
        f"""
        <div style="margin-top:4px;padding:16px 19px;border-left:3px solid #32C8FF;
                    background:rgba(50,200,255,.055);border-radius:0 8px 8px 0;">
            <span style="color:#F8FBFF;font-weight:800;">
                실제 장기연체 {actual_positive:,}가구 중
                <span style="color:#32C8FF;">{tp:,}가구를 포착</span>
            </span>
            <span style="color:#9DB4CC;">
                &nbsp;·&nbsp; Recall {recall_oot:.2%}
                &nbsp;·&nbsp; Precision {precision_oot:.2%}
                &nbsp;·&nbsp; F1 {f1_oot:.4f}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "TN 6,200 · FP 234 · FN 120 · TP 53  |  "
        "Threshold 0.7786은 DEV OOF에서 확정 후 OOT에서 고정"
    )


    # ========================================================
    # 06 · KEY FINDING
    # ========================================================

    st.divider()

    st.caption(
        "KEY FINDING · TEMPORAL GENERALIZATION"
    )


    st.markdown(
        """
### :orange[PR-AUC는 감소]했지만, ROC-AUC와 KS의 하락은 상대적으로 제한적이었습니다.
"""
    )


    st.write(
        "동시에 12개 입력변수의 PSI가 모두 0.10 미만으로 나타나, "
        "OOT 성능 감소를 주요 입력변수의 단순한 분포 변화만으로 "
        "설명하기는 어려웠습니다."
    )


    st.caption(
        "XGBoost는 클래스 불균형 보정을 적용했으므로 "
        "출력값은 보정된 실제 연체확률이 아니라 예측 위험점수로 해석합니다."
    )


    # ========================================================
    # 07 · NAVIGATION
    # ========================================================

    st.write("")


    back_col, empty_col = st.columns(
        [1, 5]
    )


    with back_col:

        if st.button(
            "← PROFILE",
            use_container_width=True
        ):

            st.session_state.page = "PROFILE"

            st.rerun()
            
# ============================================================
# 10. SCREEN · RISK SCREENING
# ============================================================

elif st.session_state.page == "SCREEN":

    motion_signal("RISK SCREENING · LIVE")

    st.markdown(":orange[**06 / RISK SCREENING**]")

    st.markdown(
        "## 위험점수 상위 가구에 실제 30일 이상 연체가구가 얼마나 집중되는가?"
    )

    st.caption(
        "2025 OOT · XGBOOST RISK SCORE · CUMULATIVE GAIN"
    )

    st.write("")


    # ========================================================
    # 01 · INTERACTIVE SCREENING LEVEL
    # ========================================================

    gain_data = {
        10: 49.13,
        20: 64.16,
        30: 72.83,
        40: 78.61,
        50: 83.82,
        60: 89.02,
        70: 91.33,
        80: 95.95,
        90: 97.69,
        100: 100.00
    }


    selected_top = st.select_slider(
        "우선 검토 범위 · SCREENING COVERAGE",
        options=list(gain_data.keys()),
        value=10,
        format_func=lambda x: f"TOP {x}%"
    )


    selected_gain = gain_data[selected_top]


    st.write("")


    # ========================================================
    # 02 · HERO KPI
    # ========================================================

    hero_left, hero_right = st.columns(
        [1.12, .88],
        gap="large"
    )


    with hero_left:

        st.caption("CUMULATIVE CAPTURE")

        animated_gain_card(
            selected_gain,
            steps=20,
            delay=0.025
        )

        st.markdown(
            f"### 상위 :orange[{selected_top}%] 위험구간의 누적 포착률"
        )

        if selected_top == 10:

            st.write(
                "전체 6,607가구 중 위험점수 상위 10%를 우선 검토하면, "
                "실제 30일 이상 원리금 연체가구 173가구 중 "
                "85가구가 이 구간에 포함됩니다."
            )

        else:

            st.write(
                f"위험점수 상위 {selected_top}% 구간까지 확대하면 "
                f"실제 30일 이상 원리금 연체가구의 "
                f"{selected_gain:.2f}%가 누적 포함됩니다."
            )


    with hero_right:

        # Only exact top-10 supporting metrics are available.
        if selected_top == 10:

            k1, k2 = st.columns(2)

            with k1:
                st.metric(
                    "SELECTED",
                    "661",
                    help="위험점수 상위 10% 가구 수"
                )

            with k2:
                st.metric(
                    "30D+ CAPTURED",
                    "85 / 173"
                )

            k3, k4 = st.columns(2)

            with k3:
                st.metric(
                    "EVENT RATE",
                    "12.86%"
                )

            with k4:
                st.metric(
                    "LIFT",
                    "4.91×"
                )

            st.caption(
                "TOP 10% 구간에서 확인된 실제 OOT 결과"
            )

        else:

            st.metric(
                "CUMULATIVE GAIN",
                f"{selected_gain:.2f}%"
            )

            st.caption(
                "해당 구간에서는 확보된 Cumulative Gain만 표시합니다. "
                "Lift 및 구간 연체율을 임의로 추정하지 않습니다."
            )


    # ========================================================
    # 03 · CUMULATIVE GAIN CHART
    # ========================================================

    st.divider()

    st.caption("01 / CUMULATIVE GAIN")

    st.markdown(
        "### 검토 범위를 넓힐수록 실제 연체가구를 얼마나 포착하는가?"
    )


    x_gain = list(gain_data.keys())
    y_gain = list(gain_data.values())


    fig_gain = go.Figure()


    # Random baseline
    fig_gain.add_trace(
        go.Scatter(
            x=[0, 100],
            y=[0, 100],

            mode="lines",

            name="Random",

            line=dict(
                color="rgba(155,180,205,.40)",
                width=2,
                dash="dash"
            ),

            hoverinfo="skip"
        )
    )


    # Model cumulative gain
    fig_gain.add_trace(
        go.Scatter(
            x=[0] + x_gain,
            y=[0] + y_gain,

            mode="lines+markers",

            name="XGBoost",

            line=dict(
                color="#4385FF",
                width=4
            ),

            marker=dict(
                size=9,
                color="#32C8FF",
                line=dict(
                    width=2,
                    color="#E7F8FF"
                )
            ),

            fill="tonexty",

            fillcolor="rgba(67,133,255,.10)",

            hovertemplate=(
                "<b>TOP %{x}%</b>"
                "<br>"
                "누적 포착률 %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )


    # Selected point
    fig_gain.add_trace(
        go.Scatter(
            x=[selected_top],
            y=[selected_gain],

            mode="markers+text",

            marker=dict(
                size=19,
                color="#FF704D",
                line=dict(
                    width=3,
                    color="#FFE0D8"
                )
            ),

            text=[
                f"<b>TOP {selected_top}% · "
                f"{selected_gain:.2f}%</b>"
            ],

            textposition="top center",
            cliponaxis=False,

            textfont=dict(
                size=14,
                color="#FFFFFF"
            ),

            showlegend=False,

            hovertemplate=(
                f"<b>SELECTED · TOP {selected_top}%</b>"
                f"<br>누적 포착률 {selected_gain:.2f}%"
                "<extra></extra>"
            )
        )
    )


    fig_gain.update_layout(
        height=480,

        title=dict(
            text=(
                "<b>2025 OOT · Cumulative Gain</b>"
                "<br>"
                "<span style='font-size:11px;'>"
                "HIGHER CURVE = STRONGER RISK CONCENTRATION"
                "</span>"
            ),
            x=.01,
            font=dict(
                size=18,
                color="#FFFFFF"
            )
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(16,45,75,.54)",

        margin=dict(
            l=65,
            r=35,
            t=90,
            b=70
        ),

        xaxis=dict(
            title=dict(
                text="우선 검토 가구 비중 (%)",
                font=dict(
                    size=15,
                    color="#D7E6F4"
                )
            ),

            range=[0, 102],

            tickvals=[
                0, 10, 20, 30, 40, 50,
                60, 70, 80, 90, 100
            ],

            ticksuffix="%",

            tickfont=dict(
                size=13,
                color="#C5D8E9"
            ),

            gridcolor="rgba(150,190,225,.12)"
        ),

        yaxis=dict(
            title=dict(
                text="실제 30일+ 연체가구 누적 포착률 (%)",
                font=dict(
                    size=15,
                    color="#D7E6F4"
                )
            ),

            range=[0, 108],

            ticksuffix="%",

            tickfont=dict(
                size=13,
                color="#C5D8E9"
            ),

            gridcolor="rgba(150,190,225,.12)"
        ),

        legend=dict(
            orientation="h",
            x=.73,
            y=1.13,
            font=dict(
                size=11,
                color="#D5E4F3"
            )
        ),

        hoverlabel=dict(
            bgcolor="#123252",
            bordercolor="#32C8FF",
            font=dict(
                size=13,
                color="#FFFFFF"
            )
        )
    )


    st.plotly_chart(
        apply_motion(fig_gain),
        use_container_width=True,
        config={
            "displaylogo": False,
            "displayModeBar": False
        }
    )


    # ========================================================
    # 04 · TOP 10 HERO SIGNAL
    # ========================================================

    st.divider()

    st.caption("02 / TOP 10% RISK CONCENTRATION")

    st.markdown(
        "### 전체를 동일하게 보는 대신 :orange[위험점수 상위 10%]를 먼저 본다면"
    )


    top_left, top_right = st.columns(
        [1, 1],
        gap="large"
    )


    with top_left:

        # visual comparison of event rates
        fig_lift = go.Figure()


        fig_lift.add_trace(
            go.Bar(
                x=[
                    "전체 OOT",
                    "위험점수 TOP 10%"
                ],

                y=[
                    2.62,
                    12.86
                ],

                marker=dict(
                    color=[
                        "#4385FF",
                        "#FF704D"
                    ]
                ),

                text=[
                    "2.62%",
                    "12.86%"
                ],

                textposition="outside",

                textfont=dict(
                    size=16,
                    color="#FFFFFF"
                ),

                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>"
                    "30일+ 실제 연체율 %{y:.2f}%"
                    "<extra></extra>"
                )
            )
        )


        fig_lift.update_layout(
            height=340,

            title=dict(
                text=(
                    "<b>30일+ 실제 연체율</b>"
                    "<br>"
                    "<span style='font-size:11px;'>"
                    "OVERALL vs TOP 10% RISK SEGMENT"
                    "</span>"
                ),

                x=.02,

                font=dict(
                    size=18,
                    color="#FFFFFF"
                )
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(16,45,75,.54)",

            margin=dict(
                l=55,
                r=30,
                t=85,
                b=55
            ),

            yaxis=dict(
                title=dict(
                    text="Actual 30D+ Rate (%)",
                    font=dict(
                        size=14,
                        color="#D7E6F4"
                    )
                ),

                range=[0, 15],

                ticksuffix="%",

                gridcolor="rgba(150,190,225,.13)",

                tickfont=dict(
                    size=12,
                    color="#BDD0E2"
                )
            ),

            xaxis=dict(
                tickfont=dict(
                    size=14,
                    color="#EDF6FF"
                )
            ),

            showlegend=False
        )


        animated_bar_chart(
            fig_lift,
            key="lift_animation",
            steps=18,
            delay=0.045
        )


    with top_right:

        st.caption("LIFT · RISK CONCENTRATION")

        st.markdown(
            """
<div style="
    font-size:66px;
    font-weight:900;
    line-height:.95;
    color:#FF704D;
    letter-spacing:-3px;
    text-shadow:
        0 0 30px rgba(255,112,77,.35);
    margin:15px 0 8px 0;
">
    4.91×
</div>
""",
            unsafe_allow_html=True
        )

        st.write(
            "전체 OOT의 30일 이상 연체율은 약 2.62%였지만, "
            "위험점수 상위 10% 구간에서는 12.86%였습니다."
        )

        st.markdown(
            "**85 / 173 actual 30D+ households captured**"
        )

        st.write(
            "즉 전체 실제 30일 이상 연체가구의 "
            "**49.13%가 상위 10% 위험구간에 포함**되었습니다."
        )


    # ========================================================
    # 05 · FINAL MESSAGE
    # ========================================================

    st.divider()

    st.caption(
        "KEY FINDING · SCREENING UTILITY"
    )

    st.markdown(
        """
### 전체 6,607가구의 :orange[10%를 우선 검토]하면, 실제 30일 이상 연체가구의 :orange[약 절반]이 해당 구간에 포함되었습니다.
"""
    )

    st.write(
        "따라서 본 모형은 모든 가구를 동일한 우선순위로 관리하기보다, "
        "상대적으로 위험도가 높은 가구를 선별하여 우선 검토하는 "
        "스크리닝 및 조기경보 보조수단으로 활용 가능성을 확인했습니다."
    )

    st.caption(
        "본 결과는 2025 OOT 표본에서의 위험집중도 평가이며, "
        "실제 금융기관의 의사결정 기준이나 자동 승인·거절 기준을 의미하지 않습니다."
    )


    # ========================================================
    # 06 · NAVIGATION
    # ========================================================

    st.write("")

    back_col, empty_col, next_col = st.columns([1, 4, 1])

    with back_col:
        if st.button("← VALIDATE", use_container_width=True):
            st.session_state.page = "VALIDATE"
            st.rerun()

    with next_col:
        if st.button("CONCLUSION →", use_container_width=True):
            st.session_state.page = "CONCLUSION"
            st.rerun()
            

# ============================================================
# 11. CONCLUSION · KEY TAKEAWAYS
# ============================================================

elif st.session_state.page == "CONCLUSION":

    motion_signal("KEY TAKEAWAYS · FINAL")
    st.markdown(":blue[**09 / CONCLUSION**]")
    st.markdown("## 이번 분석이 보여준 :orange[핵심 결론]")
    st.caption("FINDING · EVIDENCE · MODEL ROLE · LIMITATIONS & NEXT STEP")
    st.write("")

    # 핵심 결론을 먼저 제시
    st.markdown(
        """
        <div style="padding:22px 24px;border:1px solid rgba(50,200,255,.34);border-radius:13px;background:linear-gradient(135deg,rgba(67,133,255,.10),rgba(50,200,255,.045));">
          <div style="font-size:11px;font-weight:900;letter-spacing:.11em;color:#32C8FF;">FINAL TAKEAWAY</div>
          <div style="font-size:25px;line-height:1.42;font-weight:900;color:#F8FBFF;margin-top:8px;">장기연체 위험은 단순한 부채 규모보다 <span style="color:#FF8A70;">재무적 완충여력과 부채구조</span>를 함께 볼 때 더 잘 구분되었습니다.</div>
          <div style="font-size:14px;line-height:1.7;color:#BFD0E2;margin-top:10px;">가구의 현재 재무정보를 활용해 다음 해 장기연체 가능성이 높은 가구를 우선 선별하는 보조적 위험관리 도구의 가능성을 확인했습니다.</div>
        </div>
        """, unsafe_allow_html=True
    )

    st.write("")
    r1, r2, r3 = st.columns(3, gap="large")
    with r1:
        st.markdown(
            '<div style="min-height:220px;padding:21px;border:1px solid rgba(67,133,255,.30);border-radius:12px;background:rgba(16,43,73,.68);">'
            '<div style="color:#6DA4FF;font-weight:900;letter-spacing:.08em;font-size:11px;">01 · OBSERVED PROFILE</div>'
            '<h3 style="color:#F8FBFF;line-height:1.35;margin-bottom:10px;">실제 장기연체가구는<br>완충여력이 더 낮았습니다.</h3>'
            '<p style="color:#BFD0E2;line-height:1.65;font-size:13px;">일반연체가구보다 자산·유동자산·저축 수준이 낮았고, 무담보 위험부채와 개인·직장 차입 구조에서도 차이가 나타났습니다.</p>'
            '</div>', unsafe_allow_html=True)
    with r2:
        st.markdown(
            '<div style="min-height:220px;padding:21px;border:1px solid rgba(50,200,255,.30);border-radius:12px;background:rgba(16,43,73,.68);">'
            '<div style="color:#32C8FF;font-weight:900;letter-spacing:.08em;font-size:11px;">02 · MODEL EVIDENCE</div>'
            '<h3 style="color:#F8FBFF;line-height:1.35;margin-bottom:10px;">XGBoost도 여러 재무정보를<br>종합적으로 활용했습니다.</h3>'
            '<p style="color:#BFD0E2;line-height:1.65;font-size:13px;">SHAP에서 자산이 가장 높은 중요도를 보였고, 소득·유동성·소비·부채·신용대출이 함께 주요 변수로 나타났습니다.</p>'
            '</div>', unsafe_allow_html=True)
    with r3:
        st.markdown(
            '<div style="min-height:220px;padding:21px;border:1px solid rgba(255,112,77,.30);border-radius:12px;background:rgba(16,43,73,.68);">'
            '<div style="color:#FF9E87;font-weight:900;letter-spacing:.08em;font-size:11px;">03 · PRACTICAL ROLE</div>'
            '<h3 style="color:#F8FBFF;line-height:1.35;margin-bottom:10px;">확정 판정보다<br>고위험가구 우선 선별</h3>'
            '<p style="color:#BFD0E2;line-height:1.65;font-size:13px;">고정 임계값의 포착에는 한계가 있었지만, 위험점수 상위 10%에 실제 장기연체가구의 49.1%가 포함돼 우선순위화 가능성을 보였습니다.</p>'
            '</div>', unsafe_allow_html=True)

    st.divider()
    st.caption("LIMITATIONS · NEXT STEP")
    st.markdown("### 결과를 실제 활용으로 연결하기 위해 남은 과제")
    l1, l2, l3, l4 = st.columns(4)
    with l1:
        st.metric("DATA", "신용정보 제약", "세부 거래·상환이력 부재")
    with l2:
        st.metric("IMBALANCE", "약 3%", "목적별 임계값 필요")
    with l3:
        st.metric("TEMPORAL", "추가 검증", "OOT 성능 변화")
    with l4:
        st.metric("INTERPRETATION", "연관성", "인과관계 아님")

    st.markdown(
        '<div style="margin-top:10px;padding:14px 18px;border-left:3px solid #4385FF;background:rgba(67,133,255,.06);border-radius:0 9px 9px 0;color:#BFD0E2;line-height:1.65;">'
        '<b style="color:#F8FBFF;">NEXT STEP</b>&nbsp;&nbsp;보다 다양한 신용정보와 추가 시계열 데이터를 활용하고 검증방법을 보완해 모델의 안정성과 실제 활용 가능성을 확인할 필요가 있습니다.'
        '</div>', unsafe_allow_html=True
    )

    st.write("")
    back_col, empty_col = st.columns([1, 5])
    with back_col:
        if st.button("← SCREEN", use_container_width=True):
            st.session_state.page = "SCREEN"
            st.rerun()

