import streamlit as st
import pandas as pd
import time

# ---------- 1. KONFIGURASI HALAMAN ----------
st.set_page_config(
    page_title='AgroSmart | Rekomendasi Tanaman Presisi',
    page_icon='🌱',
    layout='centered',
)

# ---------- 2. SUNTIKAN UI DESIGN CUSTOM CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important;
    }
    
    [data-testid="stHeader"], #MainMenu, footer { display: none !important; }
    
    .hero-box {
        background: #FFFFFF;
        padding: 25px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .main-title { font-size: 24px !important; font-weight: 800; color: #0284C7; }
    .subtitle { font-size: 13px !important; color: #64748B; margin-top: 8px; }
    
    /* Input Fields White Style */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
    }
    
    .section-title {
        font-size: 14px; font-weight: 700; color: #1E293B;
        margin-top: 20px; margin-bottom: 10px;
        border-left: 3px solid #0284C7; padding-left: 10px;
    }
    
    .result-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 25px; border-radius: 12px; text-align: center;
        color: white; margin: 20px 0;
    }
    .result-value { font-size: 32px; font-weight: 800; color: #34D399; }
    </style>
""", unsafe_allow_html=True)

# ---------- 3. HEADER ----------
st.markdown("""
    <div class="hero-box">
        <div class="main-title">🌾 Sistem Rekomendasi Tanaman Presisi</div>
        <div class="subtitle">Optimalisasi Produktivitas Lahan Berbasis Atribut Tanah dan Cuaca</div>
    </div>
""", unsafe_allow_html=True)

# ---------- 4. FORM INPUT ----------
st.markdown('<div class="section-title">🧪 Atribut Unsur Hara Tanah</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
n_input = col1.number_input('Nitrogen (N)', 0, 150, 40)
p_input = col2.number_input('Fosfor (P)', 0, 150, 42)
k_input = col3.number_input('Kalium (K)', 0, 210, 43)

st.markdown('<div class="section-title">🌤️ Parameter Cuaca & Lingkungan</div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)
temp_input = col4.number_input('Temperatur (°C)', 0.0, 50.0, 23.6)
hum_input = col5.number_input('Kelembapan (%)', 10.0, 100.0, 60.3)
ph_input = st.number_input('pH Tanah', 3.0, 10.0, 6.2)
rain_input = st.number_input('Curah Hujan (mm)', 0.0, 3000.0, 140.9)

hitung = st.button('Rekomendasikan Tanaman Terbaik 🌾', type='primary', use_container_width=True)

# ---------- 5. LOGIKA & OUTPUT ----------
if hitung:
    with st.spinner('Menganalisis...'):
        time.sleep(0.5)
        # Logika Simulasi
        if rain_input > 200: tanaman, prob = "Padi (Rice)", [("Padi", 92.4), ("Jagung", 4.1)]
        elif n_input > 80: tanaman, prob = "Jagung (Maize)", [("Jagung", 89.1), ("Kapas", 6.2)]
        else: tanaman, prob = "Kopi (Coffee)", [("Kopi", 74.2), ("Jute", 13.5)]

        st.markdown(f'<div class="result-card"><div style="font-size:12px">HASIL ANALISIS</div><div class="result-value">{tanaman}</div></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Top Kemungkinan**")
            with st.container(border=True): # Bingkai putih untuk tabel
                st.dataframe(pd.DataFrame(prob, columns=["Tanaman", "%"]), use_container_width=True, hide_index=True)
        with col_b:
            st.write("**Ringkasan Data**")
            with st.container(border=True): # Bingkai putih untuk tabel
                data = {"Param": ["N-P-K", "pH", "Hujan"], "Nilai": [f"{n_input}-{p_input}-{k_input}", ph_input, rain_input]}
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ---------- 6. FOOTER ----------
st.markdown("<hr><center style='color:#94A3B8; font-size:12px'>© 2026 AgroSmart | Suci Kurniati Putri</center>", unsafe_allow_html=True)