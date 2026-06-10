import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# 1. Load Data
print("Memuat data jenis_tanaman.csv...")
df = pd.read_csv("jenis_tanaman.csv")

# 2. Pisahkan Fitur (X) dan Target (y)
# NAMA KOLOM DISESUAIKAN DENGAN GAMBAR
X = df[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']]
y = df['Crop']

# 3. Label Encoding untuk Target (Mengubah teks tanaman menjadi angka)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 5. Standarisasi Data (Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Latih Model Random Forest
print("Melatih model Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Cek Akurasi
akurasi = model.score(X_test_scaled, y_test)
print(f"Model selesai dilatih dengan akurasi: {akurasi * 100:.2f}%")

# 7. Simpan Model dan Preprocessing Tools ke format .pkl
joblib.dump(model, "crop_recommendation_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

# BARIS INI DITAMBAHKAN AGAR FITUR.PKL TERBUAT
joblib.dump(X.columns.tolist(), "fitur.pkl")

print("Berhasil! Keempat file .pkl telah dibuat dan siap digunakan oleh Streamlit.")