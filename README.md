# ⚗️ FCOT ChemSafe — Chemical Compatibility Checker

> Sistem pengecekan kompatibilitas penyimpanan bahan kimia berbasis **teori FCOT**  
> *(Flammable · Corrosive · Oxidizing · Toxic)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📌 Tentang Aplikasi

**FCOT ChemSafe** membantu petugas laboratorium, teknisi K3, dan peneliti dalam menentukan apakah dua bahan kimia **aman disimpan berdekatan** berdasarkan kategori bahayanya.

### Aturan Kompatibilitas FCOT

| Pasangan | Status | Alasan |
|----------|--------|--------|
| 🔥 Flammable + 🧪 Corrosive | ✅ **BOLEH** | Korosif inert terhadap organik flammable |
| 💥 Oxidizing + ☠️ Toxic | ✅ **BOLEH** | Oksidator stabil dengan racun non-organik |
| 🔥 Flammable + 💥 Oxidizing | ❌ **LARANG** | Risiko ignisi spontan & ledakan |
| 🧪 Corrosive + 💥 Oxidizing | ❌ **LARANG** | Reaksi eksotermik berbahaya |
| 🔥 Flammable + ☠️ Toxic | ⚠️ **PISAH** | Evaluasi kasus per kasus |
| 🧪 Corrosive + ☠️ Toxic | ⚠️ **PISAH** | Evaluasi kasus per kasus |

---

## 🖥️ Fitur

| Fitur | Deskripsi |
|-------|-----------|
| 🏠 **Dashboard** | Statistik database, legenda FCOT, pencarian bahan kimia |
| 🔬 **Cek Kompatibilitas** | Input 2 bahan → hasil analisis lengkap + rekomendasi |
| 📚 **Panduan FCOT** | Kategori, matriks kompatibilitas, APD & respons darurat |
| ⭐ **Favorit** | Simpan pasangan yang sering dicek, export CSV |

---

## 🚀 Cara Deploy ke Streamlit Cloud

### 1. Fork / Upload ke GitHub

```bash
# Clone repo ini
git clone https://github.com/username/fcot-chemsafe.git
cd fcot-chemsafe

# Pastikan struktur file:
# ├── app.py
# ├── requirements.txt
# └── README.md
```

### 2. Deploy di Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub Anda
3. Klik **"New app"**
4. Pilih repository ini → branch `main` → file `app.py`
5. Klik **"Deploy!"**

### 3. Jalankan Lokal (Opsional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

## 📁 Struktur File

```
fcot-chemsafe/
├── app.py              # Aplikasi utama Streamlit
├── requirements.txt    # Dependensi Python
└── README.md           # Dokumentasi ini
```

---

## 🧪 Database Bahan Kimia

Aplikasi mencakup **32 bahan kimia umum** dari 4 kategori:

- **🔥 Flammable (8):** Etanol, Aseton, Bensin, Metanol, Toluena, IPA, Dietil eter, Heksana
- **🧪 Corrosive (8):** H₂SO₄, HCl, NaOH, HNO₃, NH₃, Asam Asetat, KOH, H₃PO₄
- **💥 Oxidizing (7):** H₂O₂, KMnO₄, NaOCl, K₂Cr₂O₇, HClO₄, NO₂, O₃
- **☠️ Toxic (9):** KCN, Hg, CHCl₃, HCHO, Benzena, Pb(NO₃)₂, As₂O₃, CCl₄

---

## ⚠️ Disclaimer

> Aplikasi ini hanya sebagai **alat bantu referensi cepat**.  
> Selalu konsultasikan **Safety Data Sheet (SDS/MSDS)** resmi dan regulasi setempat sebelum menyimpan bahan kimia berbahaya.  
> Pengguna bertanggung jawab penuh atas keputusan penyimpanan yang diambil.

---

## 📄 Lisensi

MIT License — bebas digunakan untuk keperluan edukasi dan laboratorium.
