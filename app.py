import streamlit as st
import joblib
import numpy as np
import pandas as pd

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Sistem Rekomendasi Tanaman untuk Petani",
    page_icon="🌱",
    layout="centered"
)

# =====================================
# LOAD ARTEFAK
# =====================================
@st.cache_resource
def load_artefak():
    model = joblib.load("crop_recommendation_model.pkl")
    scaler = joblib.load("scaler.pkl")
    fitur = joblib.load("fitur.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    return model, scaler, fitur, label_encoder

try:
    model, scaler, fitur, label_encoder = load_artefak()
except Exception as e:
    st.error(f"Gagal memuat artefak model: {e}")
    st.info("Pastikan Anda sudah menjalankan ulang train_model.py agar fitur.pkl ikut terbuat.")
    st.stop()

# =====================================
# HEADER
# =====================================
st.title("🌱 Sistem Rekomendasi Tanaman")

st.markdown("""
Aplikasi ini menggunakan algoritma **Random Forest Classifier**
untuk memberikan rekomendasi tanaman berdasarkan kondisi tanah
dan lingkungan.
""")

st.divider()

# =====================================
# SIDEBAR INPUT
# =====================================
st.sidebar.header("Input Kondisi Lahan")

input_user = {}

# Looping untuk membuat input berdasarkan fitur.pkl
for f in fitur:
    input_user[f] = st.sidebar.number_input(
        label=str(f),
        value=0.0,
        step=0.1,
        format="%.2f"
    )

# =====================================
# PREDIKSI
# =====================================
if st.sidebar.button("🌱 Rekomendasikan Tanaman", type="primary", use_container_width=True):
    try:
        # Ubah dictionary input_user menjadi DataFrame (menghindari error urutan kolom)
        data_baru = pd.DataFrame([input_user])

        # Scaling data
        data_scaled = scaler.transform(data_baru)

        # Melakukan prediksi
        prediksi = model.predict(data_scaled)
        nama_tanaman = label_encoder.inverse_transform(prediksi)[0]

        # Menampilkan hasil utama
        st.success(f"### 🌾 Tanaman yang Direkomendasikan: **{nama_tanaman.upper()}**")

        st.subheader("Data Input")
        st.dataframe(data_baru, use_container_width=True, hide_index=True)

        # Menampilkan probabilitas (Top 5)
        if hasattr(model, "predict_proba"):
            probabilitas = model.predict_proba(data_scaled)[0]

            hasil_prob = pd.DataFrame({
                "Tanaman": label_encoder.classes_,
                "Probabilitas (%)": np.round(probabilitas * 100, 2)
            }).sort_values("Probabilitas (%)", ascending=False)

            st.subheader("Top 5 Rekomendasi Tanaman")
            st.dataframe(hasil_prob.head(5), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Terjadi error saat prediksi: {e}")

else:
    st.info("Masukkan kondisi lahan pada sidebar lalu klik tombol **Rekomendasikan Tanaman**.")

# =====================================
# FOOTER
# =====================================
st.divider()

st.caption("© 2026 Sistem Rekomendasi Tanaman Menggunakan Random Forest")