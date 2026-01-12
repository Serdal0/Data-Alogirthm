import streamlit as st
import math
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# =========================================================
# ALGORİTMALAR
# =========================================================

def oklid(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def knn_tahmin(egitim, etiketler, yeni, k):
    mesafeler = sorted(
        [(oklid(egitim[i], yeni), etiketler[i]) for i in range(len(egitim))],
        key=lambda x: x[0]
    )
    en_yakinlar = [m[1] for m in mesafeler[:k]]
    return max(set(en_yakinlar), key=en_yakinlar.count), mesafeler[:k]

def gini_hesapla(grup):
    toplam = sum(grup)
    if toplam == 0:
        return 0
    return 1 - sum((x / toplam) ** 2 for x in grup)

def twoing_hesapla(sol, sag):
    so, sa = sum(sol), sum(sag)
    if so == 0 or sa == 0:
        return 0
    p_so, p_sa = so / (so + sa), sa / (so + sa)
    diff = sum(abs((sol[i] / so) - (sag[i] / sa)) for i in range(len(sol)))
    return (p_so * p_sa / 4) * (diff ** 2)

def kmeans_merkez_bul(noktalar):
    if not noktalar:
        return [0, 0]
    return [
        round(sum(n[0] for n in noktalar) / len(noktalar), 2),
        round(sum(n[1] for n in noktalar) / len(noktalar), 2),
    ]

# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="Veri Madenciliği Laboratuvarı",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ULTRA MODERN CSS
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(14, 165, 233, 0.1) 0px, transparent 50%);
    }
    
    .main-header {
        position: relative;
        padding: 4rem 2rem;
        text-align: center;
        overflow: hidden;
        margin-bottom: 3rem;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border-radius: 24px;
        z-index: -1;
    }
    
    .main-header h1 {
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -2px;
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5)); }
        50% { filter: drop-shadow(0 0 40px rgba(168, 85, 247, 0.7)); }
    }
    
    .main-header p {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-top: 1rem;
        font-weight: 300;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.2);
    }
    
    .neon-border {
        border: 2px solid transparent;
        background: linear-gradient(rgba(30, 41, 59, 0.8), rgba(30, 41, 59, 0.8)) padding-box,
                    linear-gradient(135deg, #6366f1, #a855f7) border-box;
        border-radius: 16px;
        padding: 2rem;
    }
    
    .algo-tab {
        display: inline-block;
        padding: 1rem 2rem;
        margin: 0.5rem;
        background: rgba(30, 41, 59, 0.6);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        color: #e2e8f0;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .algo-tab:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: #6366f1;
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
    }
    
    .algo-tab.active {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-color: #a855f7;
        box-shadow: 0 0 40px rgba(168, 85, 247, 0.6);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 16px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(168, 85, 247, 0.5);
        background: linear-gradient(135deg, #7c3aed 0%, #c026d3 100%);
    }
    
    .metric-display {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-display::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .metric-display h2 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-display p {
        color: #94a3b8;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .result-badge {
        display: inline-block;
        padding: 1.5rem 3rem;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 20px;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
        margin: 2rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
    }
    
    .stat-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stat-box h3 {
        color: #6366f1;
        font-size: 1.2rem;
        margin: 0 0 1rem 0;
        font-weight: 600;
    }
    
    .stat-box p {
        color: #94a3b8;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    
    label {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    .stDataFrame {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        overflow: hidden;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    p {
        color: #94a3b8;
    }
    
    .stMarkdown {
        color: #94a3b8;
    }
    
    div[data-testid="stMetricValue"] {
        color: #6366f1 !important;
        font-size: 2rem !important;
    }
    
    .element-container {
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>⚡ VERİ MADENCİLİĞİ LABORATUVARI</h1>
    <p>Yeni Nesil Veri Madenciliği Algoritmaları Görselleştirme Platformu</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ALGORITHM SELECTOR
# =========================================================

st.markdown("<div style='text-align: center; margin-bottom: 3rem;'>", unsafe_allow_html=True)
cols = st.columns(4)

algo_options = [
    ("🎯 KNN", "knn"),
    ("🌐 K-Means", "kmeans"),
    ("📊 Gini", "gini"),
    ("⚖️ Twoing", "twoing")
]

if 'selected_algo' not in st.session_state:
    st.session_state.selected_algo = "knn"

for idx, (col, (label, value)) in enumerate(zip(cols, algo_options)):
    with col:
        if st.button(label, key=f"btn_{value}", use_container_width=True):
            st.session_state.selected_algo = value

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# KNN ALGORITHM
# =========================================================

if st.session_state.selected_algo == "knn":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 K-En Yakın Komşu Algoritması")
        st.markdown("*Gelişmiş Sınıflandırma Algoritması*")
        st.markdown("")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            boy = st.number_input("📏 Boy (cm)", 140, 220, 170, step=1)
        with c2:
            kilo = st.number_input("⚖️ Kilo (kg)", 40, 130, 70, step=1)
        with c3:
            k = st.slider("K Değeri", 1, 7, 3)
        
        st.markdown("")
        if st.button("🚀 SINIFLANDIR", key="knn_classify"):
            veriler = [
                [195, 95], [160, 52], [172, 72], [190, 92],
                [165, 55], [170, 71], [185, 88], [162, 53]
            ]
            etiketler = [
                "Basketbolcu", "Jokey", "Futbolcu", "Basketbolcu",
                "Jokey", "Futbolcu", "Basketbolcu", "Jokey"
            ]
            
            sonuc, yakinlar = knn_tahmin(veriler, etiketler, [boy, kilo], k)
            
            st.markdown(f'<div class="result-badge">🎯 {sonuc}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.markdown("### 📊 En Yakın Komşular")
            for i, (dist, label) in enumerate(yakinlar, 1):
                st.markdown(f"**{i}.** {label} — Mesafe: `{dist:.2f}`")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # 3D Visualization
        veriler = [
            [195, 95], [160, 52], [172, 72], [190, 92],
            [165, 55], [170, 71], [185, 88], [162, 53]
        ]
        etiketler = [
            "Basketball", "Jockey", "Football", "Basketball",
            "Jockey", "Football", "Basketball", "Jockey"
        ]
        
        color_map = {"Basketball": "#6366f1", "Jockey": "#a855f7", "Football": "#06b6d4"}
        
        fig = go.Figure()
        
        for label in set(etiketler):
            indices = [i for i, l in enumerate(etiketler) if l == label]
            fig.add_trace(go.Scatter(
                x=[veriler[i][0] for i in indices],
                y=[veriler[i][1] for i in indices],
                mode='markers',
                name=label,
                marker=dict(
                    size=20,
                    color=color_map[label],
                    line=dict(color='white', width=2),
                    symbol='circle'
                ),
                hovertemplate=f'<b>{label}</b><br>Height: %{{x}}<br>Weight: %{{y}}<extra></extra>'
            ))
        
        fig.add_trace(go.Scatter(
            x=[boy],
            y=[kilo],
            mode='markers',
            name='Target Point',
            marker=dict(
                size=30,
                color='#10b981',
                symbol='star',
                line=dict(color='white', width=3)
            ),
            hovertemplate='<b>Target</b><br>Height: %{x}<br>Weight: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Classification Space</b>",
            title_font=dict(size=20, color='#e2e8f0'),
            xaxis_title="Height (cm)",
            yaxis_title="Weight (kg)",
            plot_bgcolor='rgba(15, 23, 42, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                gridcolor='rgba(99, 102, 241, 0.1)',
                zerolinecolor='rgba(99, 102, 241, 0.2)'
            ),
            yaxis=dict(
                gridcolor='rgba(99, 102, 241, 0.1)',
                zerolinecolor='rgba(99, 102, 241, 0.2)'
            ),
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# K-MEANS ALGORITHM
# =========================================================

elif st.session_state.selected_algo == "kmeans":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🌐 K-Means Clustering")
        st.markdown("*Centroid-based Clustering Algorithm*")
        st.markdown("")
        
        giris = st.text_area(
            "📍 Data Points (Height, Weight)",
            "180, 80\n185, 85\n190, 90\n175, 75\n178, 78\n192, 92\n188, 88",
            height=200
        )
        
        if st.button("🎯 CALCULATE CENTROID", key="kmeans_calc"):
            noktalar = [
                [float(x.strip()) for x in satir.split(",")]
                for satir in giris.split("\n")
                if "," in satir
            ]
            merkez = kmeans_merkez_bul(noktalar)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown('<div class="metric-display">', unsafe_allow_html=True)
                st.markdown(f"<h2>{merkez[0]}</h2>", unsafe_allow_html=True)
                st.markdown("<p>Height</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="metric-display">', unsafe_allow_html=True)
                st.markdown(f"<h2>{merkez[1]}</h2>", unsafe_allow_html=True)
                st.markdown("<p>Weight</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.session_state.kmeans_data = (noktalar, merkez)
    
    with col2:
        if 'kmeans_data' in st.session_state:
            noktalar, merkez = st.session_state.kmeans_data
            
            fig = go.Figure()
            
            # Data points
            fig.add_trace(go.Scatter(
                x=[n[0] for n in noktalar],
                y=[n[1] for n in noktalar],
                mode='markers',
                name='Data Points',
                marker=dict(
                    size=18,
                    color='#6366f1',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>Point</b><br>Height: %{x}<br>Weight: %{y}<extra></extra>'
            ))
            
            # Centroid
            fig.add_trace(go.Scatter(
                x=[merkez[0]],
                y=[merkez[1]],
                mode='markers',
                name='Centroid',
                marker=dict(
                    size=35,
                    color='#10b981',
                    symbol='star',
                    line=dict(color='white', width=3)
                ),
                hovertemplate='<b>Centroid</b><br>Height: %{x}<br>Weight: %{y}<extra></extra>'
            ))
            
            # Connections
            for nokta in noktalar:
                fig.add_trace(go.Scatter(
                    x=[nokta[0], merkez[0]],
                    y=[nokta[1], merkez[1]],
                    mode='lines',
                    line=dict(color='rgba(99, 102, 241, 0.2)', width=1, dash='dot'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            fig.update_layout(
                title="<b>Cluster Visualization</b>",
                title_font=dict(size=20, color='#e2e8f0'),
                xaxis_title="Height (cm)",
                yaxis_title="Weight (kg)",
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                yaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                height=500,
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 4rem; color: #64748b;'>
                <h3>📊 Visualization Area</h3>
                <p>Enter data points and click calculate to see the cluster</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# GINI ALGORITHM
# =========================================================

elif st.session_state.selected_algo == "gini":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Gini Impurity Index")
        st.markdown("*Decision Tree Splitting Criterion*")
        st.markdown("")
        
        st.markdown('<div class="neon-border">', unsafe_allow_html=True)
        st.markdown("#### Formula")
        st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        girdi = st.text_input("🔢 Class Distribution", "5,5")
        
        if st.button("📊 CALCULATE GINI", key="gini_calc"):
            degerler = [int(x.strip()) for x in girdi.split(",")]
            gini_skor = gini_hesapla(degerler)
            
            st.markdown('<div class="metric-display">', unsafe_allow_html=True)
            st.markdown(f"<h2>{gini_skor:.4f}</h2>", unsafe_allow_html=True)
            st.markdown("<p>Gini Impurity</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.markdown("### 📈 Analysis")
            if gini_skor < 0.3:
                st.markdown("🟢 **LOW IMPURITY** — Homogeneous distribution")
            elif gini_skor < 0.5:
                st.markdown("🟡 **MEDIUM IMPURITY** — Acceptable distribution")
            else:
                st.markdown("🔴 **HIGH IMPURITY** — Heterogeneous distribution")
            
            st.markdown(f"""
            - **Total Elements:** {sum(degerler)}
            - **Number of Classes:** {len(degerler)}
            - **Gini Score:** {gini_skor:.4f}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.session_state.gini_data = (degerler, gini_skor)
    
    with col2:
        if 'gini_data' in st.session_state:
            degerler, gini_skor = st.session_state.gini_data
            
            # 3D Donut Chart
            colors = ['#6366f1', '#a855f7', '#06b6d4', '#10b981', '#f59e0b']
            
            fig = go.Figure(data=[go.Pie(
                labels=[f"Class {i+1}" for i in range(len(degerler))],
                values=degerler,
                hole=.5,
                marker=dict(
                    colors=colors[:len(degerler)],
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
                ),
                textfont=dict(size=16, color='white'),
                hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title="<b>Class Distribution</b>",
                title_font=dict(size=20, color='#e2e8f0'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='#94a3b8'),
                height=500,
                showlegend=True,
                legend=dict(
                    font=dict(color='#e2e8f0'),
                    bgcolor='rgba(30, 41, 59, 0.6)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 4rem; color: #64748b;'>
                <h3>📊 Visualization Area</h3>
                <p>Enter class distribution to see the chart</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TWOING ALGORITHM
# =========================================================

elif st.session_state.selected_algo == "twoing":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚖️ Twoing Splitting Criterion")
        st.markdown("*Binary Split Quality Measure*")
        st.markdown("")
        
        st.markdown('<div class="neon-border">', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🔵 Left Group")
            sol = st.text_input("Distribution", "10,2", key="sol_input")
        with col_b:
            st.markdown("#### 🔴 Right Group")
            sag = st.text_input("Distribution", "2,10", key="sag_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("⚖️ CALCULATE TWOING", key="twoing_calc"):
            sol_liste = [int(x.strip()) for x in sol.split(",")]
            sag_liste = [int(x.strip()) for x in sag.split(",")]
            twoing_skor = twoing_hesapla(sol_liste, sag_liste)
            
            st.markdown('<div class="metric-display">', unsafe_allow_html=True)
            st.markdown(f"<h2>{twoing_skor:.4f}</h2>", unsafe_allow_html=True)
            st.markdown("<p>Twoing Score</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.markdown("### 📊 Split Quality")
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                st.metric("Left Total", sum(sol_liste))
            with col_y:
                st.metric("Right Total", sum(sag_liste))
            with col_z:
                st.metric("Score", f"{twoing_skor:.4f}")
            
            if twoing_skor > 0.1:
                st.markdown("🟢 **HIGH QUALITY** — Excellent split")
            elif twoing_skor > 0.05:
                st.markdown("🟡 **MEDIUM QUALITY** — Acceptable split")
            else:
                st.markdown("🔴 **LOW QUALITY** — Poor split")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.session_state.twoing_data = (sol_liste, sag_liste, twoing_skor)
    
    with col2:
        if 'twoing_data' in st.session_state:
            sol_liste, sag_liste, twoing_skor = st.session_state.twoing_data
            
            fig = go.Figure()
            
            # Left group
            fig.add_trace(go.Bar(
                x=[f"Class {i+1}" for i in range(len(sol_liste))],
                y=sol_liste,
                name='Left Group',
                marker=dict(
                    color='#6366f1',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>Left Group</b><br>Class: %{x}<br>Count: %{y}<extra></extra>'
            ))
            
            # Right group
            fig.add_trace(go.Bar(
                x=[f"Class {i+1}" for i in range(len(sag_liste))],
                y=sag_liste,
                name='Right Group',
                marker=dict(
                    color='#a855f7',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>Right Group</b><br>Class: %{x}<br>Count: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title="<b>Group Comparison</b>",
                title_font=dict(size=20, color='#e2e8f0'),
                xaxis_title="Classes",
                yaxis_title="Count",
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='#94a3b8'),
                xaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                yaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                height=500,
                barmode='group',
                hovermode='x unified',
                legend=dict(
                    font=dict(color='#e2e8f0'),
                    bgcolor='rgba(30, 41, 59, 0.6)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 4rem; color: #64748b;'>
                <h3>📊 Visualization Area</h3>
                <p>Enter group distributions to see the comparison</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style='text-align: center; padding: 3rem; margin-top: 3rem; border-top: 1px solid rgba(99, 102, 241, 0.2);'>
    <p style='color: #64748b; font-size: 0.9rem;'>⚡ AI MINING LAB — Advanced Data Mining Platform</p>
    <p style='color: #475569; font-size: 0.85rem; margin-top: 0.5rem;'>Computer Engineering • 2024</p>
</div>
""", unsafe_allow_html=True)