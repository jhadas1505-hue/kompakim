import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FCOT ChemSafe",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --card:      #1a2236;
    --border:    #2a3650;
    --accent-f:  #ff6b35;
    --accent-c:  #4ecdc4;
    --accent-o:  #ffe66d;
    --accent-t:  #a29bfe;
    --text:      #e2e8f0;
    --muted:     #8892a4;
    --green:     #00d084;
    --red:       #ff4757;
    --radius:    14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; }

/* HERO BANNER */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(78,205,196,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,107,53,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    background: linear-gradient(90deg, #4ecdc4, #a29bfe, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--muted);
    font-size: 1.05rem;
    margin: 0;
    font-family: 'DM Sans', sans-serif;
}

/* STAT CARDS */
.stat-grid { display:flex; gap:16px; margin-bottom:28px; flex-wrap:wrap; }
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    flex: 1;
    min-width: 140px;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content:'';
    position:absolute;
    top:0; left:0;
    width:4px; height:100%;
    border-radius: 4px 0 0 4px;
}
.stat-card.f::before { background:var(--accent-f); }
.stat-card.c::before { background:var(--accent-c); }
.stat-card.o::before { background:var(--accent-o); }
.stat-card.t::before { background:var(--accent-t); }
.stat-num {
    font-family:'Syne',sans-serif;
    font-size:2rem;
    font-weight:800;
    margin:0;
}
.stat-label { color:var(--muted); font-size:0.82rem; margin:4px 0 0; }

/* COMPATIBILITY RESULT */
.result-box {
    border-radius: var(--radius);
    padding: 28px 32px;
    margin: 20px 0;
    border: 2px solid;
    text-align: center;
}
.result-box.compatible {
    background: rgba(0,208,132,0.07);
    border-color: var(--green);
}
.result-box.incompatible {
    background: rgba(255,71,87,0.07);
    border-color: var(--red);
}
.result-icon { font-size: 3.5rem; margin-bottom: 12px; }
.result-title {
    font-family:'Syne',sans-serif;
    font-size:1.8rem;
    font-weight:800;
    margin:0 0 8px;
}
.result-desc { color:var(--muted); font-size:0.97rem; line-height:1.6; }

/* FCOT BADGE */
.fcot-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    font-family:'Space Mono',monospace;
    letter-spacing:1px;
    margin: 2px 4px;
}
.badge-F { background:rgba(255,107,53,0.15); color:var(--accent-f); border:1px solid rgba(255,107,53,0.3); }
.badge-C { background:rgba(78,205,196,0.15); color:var(--accent-c); border:1px solid rgba(78,205,196,0.3); }
.badge-O { background:rgba(255,230,109,0.15); color:var(--accent-o); border:1px solid rgba(255,230,109,0.3); }
.badge-T { background:rgba(162,155,254,0.15); color:var(--accent-t); border:1px solid rgba(162,155,254,0.3); }

/* CHEM CARD */
.chem-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin: 8px 0;
    transition: border-color 0.2s;
}
.chem-card:hover { border-color: #4ecdc4; }
.chem-name { font-family:'Syne',sans-serif; font-weight:700; font-size:1.05rem; }

/* GUIDE TABLE */
.guide-matrix {
    background: var(--card);
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
}
.guide-matrix table { width:100%; border-collapse:collapse; }
.guide-matrix th {
    background: var(--surface);
    padding: 12px 16px;
    font-family:'Syne',sans-serif;
    font-weight:700;
    font-size:0.88rem;
    letter-spacing:0.5px;
    border-bottom: 1px solid var(--border);
    color: var(--muted);
    text-transform:uppercase;
}
.guide-matrix td {
    padding: 10px 16px;
    border-bottom: 1px solid rgba(42,54,80,0.5);
    font-size:0.9rem;
}
.guide-matrix tr:last-child td { border-bottom:none; }

/* FAV CARD */
.fav-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 20px;
    margin: 8px 0;
    display:flex;
    align-items:center;
    gap:12px;
}
.fav-dot {
    width:10px; height:10px;
    border-radius:50%;
    flex-shrink:0;
}
.fav-dot.ok  { background:var(--green); }
.fav-dot.no  { background:var(--red); }

/* SIDEBAR NAV */
.nav-label {
    font-family:'Syne',sans-serif;
    font-size:0.72rem;
    font-weight:700;
    letter-spacing:2px;
    text-transform:uppercase;
    color:var(--muted);
    margin: 20px 0 8px;
    padding-left:4px;
}

/* INFO BOX */
.info-strip {
    background: rgba(78,205,196,0.08);
    border-left: 3px solid var(--accent-c);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 12px 0;
    font-size:0.9rem;
    color: var(--text);
}

/* selectbox / input overrides */
div[data-baseweb="select"] > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
CHEMICALS = {
    # Flammable
    "Etanol (C₂H₅OH)":           {"fcot": ["F"], "cas": "64-17-5",  "desc": "Pelarut organik umum, mudah terbakar"},
    "Aseton (C₃H₆O)":            {"fcot": ["F"], "cas": "67-64-1",  "desc": "Pelarut ketone, titik nyala -20°C"},
    "Bensin (Gasoline)":          {"fcot": ["F"], "cas": "8006-61-9","desc": "Campuran hidrokarbon, sangat mudah terbakar"},
    "Metanol (CH₃OH)":            {"fcot": ["F"], "cas": "67-56-1",  "desc": "Alkohol sederhana, beracun dan mudah terbakar"},
    "Toluena (C₇H₈)":            {"fcot": ["F"], "cas": "108-88-3", "desc": "Pelarut aromatik, uap mudah terbakar"},
    "Isopropanol (IPA)":          {"fcot": ["F"], "cas": "67-63-0",  "desc": "Alkohol isopropil, desinfektan umum"},
    "Dietil eter (C₄H₁₀O)":      {"fcot": ["F"], "cas": "60-29-7",  "desc": "Pelarut anestesi, sangat volatil & mudah terbakar"},
    "Heksana (C₆H₁₄)":           {"fcot": ["F"], "cas": "110-54-3", "desc": "Pelarut nonpolar, titik nyala -22°C"},
    # Corrosive
    "Asam Sulfat (H₂SO₄)":       {"fcot": ["C"], "cas": "7664-93-9","desc": "Asam kuat, korosif terhadap logam & jaringan"},
    "Asam Klorida (HCl)":         {"fcot": ["C"], "cas": "7647-01-0","desc": "Asam kuat berupa larutan, uap iritatif"},
    "Natrium Hidroksida (NaOH)":  {"fcot": ["C"], "cas": "1310-73-2","desc": "Basa kuat, saponifikasi lemak jaringan"},
    "Asam Nitrat (HNO₃)":         {"fcot": ["C", "O"], "cas": "7697-37-2","desc": "Asam oksidator kuat, korosif"},
    "Amonia (NH₃)":               {"fcot": ["C"], "cas": "7664-41-7","desc": "Gas basa, korosif pada kelembaban tinggi"},
    "Asam Asetat Glasial":        {"fcot": ["C", "F"], "cas": "64-19-7","desc": "Asam organik pekat, korosif & mudah terbakar"},
    "Kalium Hidroksida (KOH)":    {"fcot": ["C"], "cas": "1310-58-3","desc": "Basa kuat, larut exotermik"},
    "Asam Fosfat (H₃PO₄)":       {"fcot": ["C"], "cas": "7664-38-2","desc": "Asam moderat, korosif pada konsentrasi tinggi"},
    # Oxidizing
    "Hidrogen Peroksida (H₂O₂)":  {"fcot": ["O"], "cas": "7722-84-1","desc": "Oksidator kuat, melepas O₂ saat terurai"},
    "Kalium Permanganat (KMnO₄)": {"fcot": ["O"], "cas": "7722-64-7","desc": "Oksidator kuat, digunakan dalam analisis"},
    "Natrium Hipoklorit (NaOCl)": {"fcot": ["O"], "cas": "7681-52-9","desc": "Pemutih klorin, oksidator ringan"},
    "Kalium Dikromat (K₂Cr₂O₇)":  {"fcot": ["O", "T"], "cas": "7778-50-9","desc": "Oksidator kuat & karsinogenik"},
    "Asam Perklorat (HClO₄)":     {"fcot": ["O", "C"], "cas": "7601-90-3","desc": "Oksidator sangat kuat, mudah meledak pekat"},
    "Nitrogen Oksida (NO₂)":      {"fcot": ["O", "T"], "cas": "10102-44-0","desc": "Gas oksidator, beracun & iritan paru"},
    "Ozon (O₃)":                  {"fcot": ["O"], "cas": "10028-15-6","desc": "Oksidator kuat, iritan saluran napas"},
    # Toxic
    "Sianida (KCN)":              {"fcot": ["T"], "cas": "151-50-8", "desc": "Sangat beracun, inhibitor enzim sitokrom c"},
    "Merkuri (Hg)":               {"fcot": ["T"], "cas": "7439-97-6","desc": "Logam berat neurotoksik, uap berbahaya"},
    "Kloroform (CHCl₃)":          {"fcot": ["T"], "cas": "67-66-3",  "desc": "Hepatotoksik, kemungkinan karsinogen"},
    "Formaldehida (HCHO)":        {"fcot": ["T"], "cas": "50-00-0",  "desc": "Karsinogen, iritan kuat, fiksatif jaringan"},
    "Benzena (C₆H₆)":             {"fcot": ["T", "F"], "cas": "71-43-2","desc": "Karsinogen, menyebabkan leukemia"},
    "Timbal Nitrat Pb(NO₃)₂":     {"fcot": ["T"], "cas": "10099-74-8","desc": "Garam timbal, toksik pada darah & saraf"},
    "Arsenik Trioksida (As₂O₃)":  {"fcot": ["T"], "cas": "1327-53-3","desc": "Karsinogen klas 1, sangat toksik"},
    "Karbontetraklorida (CCl₄)":   {"fcot": ["T"], "cas": "56-23-5",  "desc": "Hepatotoksik & nefrotoksik, deplesi ozon"},
}

# Compatibility rules (FCOT theory)
# F↔C = OK, O↔T = OK, everything else = NOT OK
COMPATIBLE_PAIRS = {("F","C"), ("C","F"), ("O","T"), ("T","O")}

def get_compatibility(chem1, chem2):
    """Return (compatible: bool, reason: str)"""
    if chem1 == chem2:
        return None, "Bahan yang sama dipilih."
    types1 = set(CHEMICALS[chem1]["fcot"])
    types2 = set(CHEMICALS[chem2]["fcot"])
    # check if any pair is compatible
    for t1 in types1:
        for t2 in types2:
            if (t1, t2) in COMPATIBLE_PAIRS:
                return True, f"Bahan ini dapat disimpan berdekatan (pasangan {t1}↔{t2} diizinkan oleh teori FCOT)."
    # special: if both sets overlap (same category)
    overlap = types1 & types2
    if overlap:
        return False, f"Kedua bahan memiliki kategori yang sama ({', '.join(overlap)}). Simpan terpisah."
    return False, "Tidak ada pasangan kategori yang kompatibel menurut teori FCOT."

def badge_html(letter):
    labels = {"F":"FLAMMABLE","C":"CORROSIVE","O":"OXIDIZING","T":"TOXIC"}
    return f'<span class="fcot-badge badge-{letter}">{labels.get(letter,letter)}</span>'

def chem_badges(name):
    return "".join(badge_html(l) for l in CHEMICALS[name]["fcot"])

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "favorites" not in st.session_state:
    st.session_state.favorites = []   # list of dicts

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:24px 0 8px;'>
      <span style='font-size:2.8rem;'>⚗️</span><br>
      <span style='font-family:Syne,sans-serif;font-weight:800;font-size:1.3rem;
                   background:linear-gradient(90deg,#4ecdc4,#a29bfe);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        FCOT ChemSafe
      </span><br>
      <span style='color:#8892a4;font-size:0.78rem;'>Chemical Storage Safety</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Menu Utama</div>', unsafe_allow_html=True)
    page = st.radio(
        "Pilih Halaman",
        ["🏠 Dashboard", "🔬 Cek Kompatibilitas", "📚 Panduan FCOT", "⭐ Favorit"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="nav-label">Legenda Kategori</div>', unsafe_allow_html=True)
    for letter, color, label, icon in [
        ("F","#ff6b35","Flammable","🔥"),
        ("C","#4ecdc4","Corrosive","🧪"),
        ("O","#ffe66d","Oxidizing","💥"),
        ("T","#a29bfe","Toxic","☠️"),
    ]:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin:6px 0;
                    background:#1a2236;border-radius:8px;padding:8px 12px;'>
          <span style='font-size:1.1rem;'>{icon}</span>
          <div>
            <div style='font-family:Space Mono,monospace;font-size:0.78rem;
                        font-weight:700;color:{color};'>{label}</div>
            <div style='color:#8892a4;font-size:0.72rem;'>Kategori {letter}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='color:#8892a4;font-size:0.75rem;text-align:center;line-height:1.6;'>
      Berdasarkan teori FCOT<br>
      <em>Flammable · Corrosive · Oxidizing · Toxic</em>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">⚗️ FCOT ChemSafe</div>
      <p class="hero-sub">
        Sistem pengecekan kompatibilitas penyimpanan bahan kimia berbasis teori FCOT —
        pastikan bahan kimia Anda disimpan aman dan sesuai regulasi.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Stat cards
    f_count = sum(1 for d in CHEMICALS.values() if "F" in d["fcot"])
    c_count = sum(1 for d in CHEMICALS.values() if "C" in d["fcot"])
    o_count = sum(1 for d in CHEMICALS.values() if "O" in d["fcot"])
    t_count = sum(1 for d in CHEMICALS.values() if "T" in d["fcot"])

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card f">
        <p class="stat-num" style="color:var(--accent-f)">🔥 {f_count}</p>
        <p class="stat-label">Flammable</p>
      </div>
      <div class="stat-card c">
        <p class="stat-num" style="color:var(--accent-c)">🧪 {c_count}</p>
        <p class="stat-label">Corrosive</p>
      </div>
      <div class="stat-card o">
        <p class="stat-num" style="color:var(--accent-o)">💥 {o_count}</p>
        <p class="stat-label">Oxidizing</p>
      </div>
      <div class="stat-card t">
        <p class="stat-num" style="color:var(--accent-t)">☠️ {t_count}</p>
        <p class="stat-label">Toxic</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Two columns
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 🔑 Aturan Emas FCOT")
        st.markdown("""
        <div class="info-strip">
          Teori FCOT membagi bahan kimia ke dalam 4 kategori berdasarkan bahaya utamanya.
          Hanya pasangan kategori tertentu yang <strong>aman disimpan berdekatan</strong>.
        </div>
        """, unsafe_allow_html=True)

        rules = [
            ("🔥 Flammable", "🧪 Corrosive", "✅ BOLEH", "#00d084"),
            ("🧪 Corrosive", "🔥 Flammable", "✅ BOLEH", "#00d084"),
            ("💥 Oxidizing", "☠️ Toxic",     "✅ BOLEH", "#00d084"),
            ("☠️ Toxic",     "💥 Oxidizing", "✅ BOLEH", "#00d084"),
            ("🔥 Flammable", "💥 Oxidizing", "❌ LARANG", "#ff4757"),
            ("🔥 Flammable", "☠️ Toxic",     "⚠️ PISAH",  "#ffa502"),
            ("🧪 Corrosive", "💥 Oxidizing", "❌ LARANG", "#ff4757"),
            ("🧪 Corrosive", "☠️ Toxic",     "⚠️ PISAH",  "#ffa502"),
        ]
        for r in rules:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;background:#1a2236;
                        border-radius:8px;padding:10px 14px;margin:5px 0;
                        border:1px solid #2a3650;'>
              <span style='flex:1;font-size:0.88rem;'>{r[0]}</span>
              <span style='color:#8892a4;font-size:0.75rem;'>+</span>
              <span style='flex:1;font-size:0.88rem;'>{r[1]}</span>
              <span style='font-family:Space Mono,monospace;font-size:0.78rem;
                           font-weight:700;color:{r[3]};white-space:nowrap;'>{r[2]}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📋 Database Bahan Kimia")
        search = st.text_input("🔍 Cari bahan kimia...", placeholder="Ketik nama bahan...")
        filtered = {k: v for k, v in CHEMICALS.items()
                    if search.lower() in k.lower()} if search else CHEMICALS

        for name, data in list(filtered.items())[:10]:
            st.markdown(f"""
            <div class="chem-card">
              <div class="chem-name">{name}</div>
              <div style='margin:4px 0 6px;font-size:0.8rem;color:#8892a4;'>{data['desc']}</div>
              {chem_badges(name)}
              <span style='font-family:Space Mono,monospace;font-size:0.72rem;
                           color:#8892a4;margin-left:6px;'>CAS: {data['cas']}</span>
            </div>
            """, unsafe_allow_html=True)

        if len(filtered) > 10:
            st.markdown(f"<div style='color:#8892a4;font-size:0.82rem;text-align:center;'>… dan {len(filtered)-10} bahan lainnya</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: CEK KOMPATIBILITAS
# ─────────────────────────────────────────────
elif page == "🔬 Cek Kompatibilitas":
    st.markdown("## 🔬 Cek Kompatibilitas Penyimpanan")
    st.markdown("""
    <div class="info-strip">
      Pilih <strong>dua bahan kimia</strong> yang ingin Anda simpan berdekatan.
      Sistem akan memeriksa apakah kombinasi tersebut aman berdasarkan teori FCOT.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧫 Bahan Kimia 1")
        chem1 = st.selectbox("Pilih bahan pertama", list(CHEMICALS.keys()), key="c1")
        d1 = CHEMICALS[chem1]
        st.markdown(f"""
        <div class="chem-card">
          <div class="chem-name">{chem1}</div>
          <div style='color:#8892a4;font-size:0.85rem;margin:4px 0 8px;'>{d1['desc']}</div>
          {chem_badges(chem1)}
          <div style='margin-top:6px;font-size:0.78rem;color:#8892a4;'>CAS: {d1['cas']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🧫 Bahan Kimia 2")
        chem2 = st.selectbox("Pilih bahan kedua", list(CHEMICALS.keys()), key="c2", index=8)
        d2 = CHEMICALS[chem2]
        st.markdown(f"""
        <div class="chem-card">
          <div class="chem-name">{chem2}</div>
          <div style='color:#8892a4;font-size:0.85rem;margin:4px 0 8px;'>{d2['desc']}</div>
          {chem_badges(chem2)}
          <div style='margin-top:6px;font-size:0.78rem;color:#8892a4;'>CAS: {d2['cas']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, _ = st.columns([1.2, 1, 2])
    with col_btn1:
        check = st.button("⚡ Cek Kompatibilitas", type="primary", use_container_width=True)
    with col_btn2:
        save_fav = st.button("⭐ Simpan ke Favorit", use_container_width=True)

    if chem1 == chem2:
        st.warning("⚠️ Pilih dua bahan yang berbeda untuk pengecekan.")
    else:
        compatible, reason = get_compatibility(chem1, chem2)

        if check or save_fav:
            if compatible:
                st.markdown(f"""
                <div class="result-box compatible">
                  <div class="result-icon">✅</div>
                  <div class="result-title" style="color:#00d084;">KOMPATIBEL</div>
                  <p class="result-desc">{reason}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box incompatible">
                  <div class="result-icon">🚫</div>
                  <div class="result-title" style="color:#ff4757;">TIDAK KOMPATIBEL</div>
                  <p class="result-desc">{reason}</p>
                </div>
                """, unsafe_allow_html=True)

            # Detail analysis
            st.markdown("#### 📊 Analisis Detail")
            a1, a2, a3 = st.columns(3)
            with a1:
                st.markdown(f"""
                <div class="chem-card" style="text-align:center;">
                  <div style='font-size:0.75rem;color:#8892a4;margin-bottom:4px;'>BAHAN 1</div>
                  <div class="chem-name" style='font-size:0.9rem;'>{chem1}</div>
                  <div style='margin-top:8px;'>{chem_badges(chem1)}</div>
                </div>
                """, unsafe_allow_html=True)
            with a2:
                icon = "✅" if compatible else "❌"
                clr  = "#00d084" if compatible else "#ff4757"
                txt  = "AMAN" if compatible else "BAHAYA"
                st.markdown(f"""
                <div class="chem-card" style="text-align:center;border-color:{clr};">
                  <div style='font-size:2.5rem;'>{icon}</div>
                  <div style='font-family:Syne,sans-serif;font-weight:800;
                              font-size:1rem;color:{clr};'>{txt}</div>
                </div>
                """, unsafe_allow_html=True)
            with a3:
                st.markdown(f"""
                <div class="chem-card" style="text-align:center;">
                  <div style='font-size:0.75rem;color:#8892a4;margin-bottom:4px;'>BAHAN 2</div>
                  <div class="chem-name" style='font-size:0.9rem;'>{chem2}</div>
                  <div style='margin-top:8px;'>{chem_badges(chem2)}</div>
                </div>
                """, unsafe_allow_html=True)

            # Recommendation
            if compatible:
                st.success("💡 **Rekomendasi:** Bahan ini dapat ditempatkan di lemari/rak yang sama. Tetap pastikan ventilasi cukup dan wadah tertutup rapat.")
            else:
                st.error("⛔ **Rekomendasi:** Simpan bahan ini di lokasi terpisah dengan jarak minimal 3 meter atau di lemari berbeda. Pasang label bahaya yang jelas.")

            if save_fav:
                entry = {
                    "chem1": chem1, "chem2": chem2,
                    "compatible": compatible,
                    "timestamp": datetime.now().strftime("%d %b %Y, %H:%M")
                }
                # avoid duplicate
                exists = any(f["chem1"]==chem1 and f["chem2"]==chem2 for f in st.session_state.favorites)
                if not exists:
                    st.session_state.favorites.append(entry)
                    st.toast("⭐ Pasangan disimpan ke Favorit!", icon="✅")
                else:
                    st.toast("Pasangan ini sudah ada di Favorit.", icon="ℹ️")

# ─────────────────────────────────────────────
#  PAGE: PANDUAN FCOT
# ─────────────────────────────────────────────
elif page == "📚 Panduan FCOT":
    st.markdown("## 📚 Panduan Teori FCOT")

    tab1, tab2, tab3 = st.tabs(["🧱 Kategori FCOT", "📊 Matriks Kompatibilitas", "⚠️ Bahaya & Pencegahan"])

    with tab1:
        cats = [
            ("F","🔥","Flammable","#ff6b35",
             "Bahan yang mudah terbakar pada suhu dan tekanan normal.",
             ["Titik nyala rendah (flashpoint < 60°C)", "Uap mudah tersulut api",
              "Perlu disimpan jauh dari sumber panas & api terbuka",
              "Gunakan lemari tahan api (flammable cabinet)"],
             ["Etanol, Aseton, Bensin, Metanol, Toluena, Dietil eter"]),
            ("C","🧪","Corrosive","#4ecdc4",
             "Bahan yang dapat merusak jaringan biologis atau material melalui reaksi kimia.",
             ["pH sangat rendah (<2) atau sangat tinggi (>12)", "Merusak kulit, mata, saluran napas",
              "Dapat mengkorosi logam & beton", "Simpan di wadah non-reaktif (PE, PTFE)"],
             ["H₂SO₄, HCl, NaOH, NH₃, HNO₃, KOH"]),
            ("O","💥","Oxidizing","#ffe66d",
             "Bahan yang melepaskan oksigen dan mendukung pembakaran bahan lain.",
             ["Meningkatkan kecepatan kebakaran secara drastis", "Bereaksi hebat dengan bahan organik",
              "Simpan jauh dari bahan mudah terbakar", "Hindari kontaminasi bahan organik sekecil apapun"],
             ["H₂O₂, KMnO₄, HClO₄, NaOCl, K₂Cr₂O₇, O₃"]),
            ("T","☠️","Toxic","#a29bfe",
             "Bahan yang berbahaya bagi kesehatan melalui inhalasi, kontak, atau ingesti.",
             ["Dosis lethal (LD50) sangat rendah", "Dapat bersifat karsinogenik, mutagenik, teratogenik",
              "Wajib APD lengkap saat penanganan", "Simpan di lemari terkunci berventilasi"],
             ["KCN, Hg, CHCl₃, Formaldehida, Benzena, Arsenik"]),
        ]
        for letter, icon, name, color, desc, props, ex in cats:
            with st.expander(f"{icon}  {name} (Kategori {letter})", expanded=(letter=="F")):
                st.markdown(f"""
                <div style='border-left:3px solid {color};padding-left:16px;margin-bottom:12px;'>
                  <p style='color:#e2e8f0;font-size:0.95rem;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Karakteristik:**")
                    for p in props:
                        st.markdown(f"• {p}")
                with c2:
                    st.markdown("**Contoh Bahan:**")
                    st.markdown(f"<div style='color:#8892a4;font-size:0.88rem;'>{ex[0]}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### Matriks Kompatibilitas FCOT")
        st.markdown("""
        <div class="info-strip">
          ✅ = Dapat disimpan berdekatan &nbsp;|&nbsp;
          ❌ = Harus terpisah &nbsp;|&nbsp;
          ⚠️ = Perlu penilaian risiko tambahan
        </div>
        """, unsafe_allow_html=True)

        matrix_data = {
            "":            ["🔥 F", "🧪 C", "💥 O", "☠️ T"],
            "🔥 Flammable":  ["—",   "✅",   "❌",   "⚠️"],
            "🧪 Corrosive":  ["✅",  "—",    "❌",   "⚠️"],
            "💥 Oxidizing":  ["❌",  "❌",   "—",    "✅"],
            "☠️ Toxic":      ["⚠️",  "⚠️",   "✅",   "—"],
        }
        df = pd.DataFrame(matrix_data).set_index("")
        st.dataframe(df, use_container_width=True)

        st.markdown("""
        <div style='background:#1a2236;border-radius:12px;padding:20px 24px;margin-top:16px;'>
          <p style='font-family:Syne,sans-serif;font-weight:700;margin:0 0 12px;'>📌 Catatan Penting:</p>
          <ul style='color:#8892a4;font-size:0.9rem;line-height:1.8;margin:0;padding-left:20px;'>
            <li><strong style='color:#e2e8f0;'>F + C (✅)</strong> — Asam korosif memiliki sifat inert terhadap bahan flammable organik pada kondisi normal.</li>
            <li><strong style='color:#e2e8f0;'>O + T (✅)</strong> — Oksidator anorganik umumnya stabil bila dicampur penyimpanan dengan racun non-organik.</li>
            <li><strong style='color:#e2e8f0;'>F + O (❌)</strong> — SANGAT BERBAHAYA. Oksidator dapat memicu ignisi bahan flammable secara spontan.</li>
            <li><strong style='color:#e2e8f0;'>C + O (❌)</strong> — Asam korosif + oksidator → reaksi eksotermik, potensi ledakan.</li>
            <li><strong style='color:#e2e8f0;'>F + T (⚠️)</strong> — Bergantung pada spesifik bahan; banyak bahan toxic juga flammable.</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### ⚠️ Panduan Pencegahan & APD")
        hazards = [
            ("🔥","Flammable","#ff6b35",
             "Kebakaran, ledakan uap, flash fire",
             "Jas lab katun, sarung tangan nitril, kacamata splash-proof, sepatu safety. Hindari pakaian sintetis.",
             "APAR CO₂ atau dry powder. JANGAN gunakan air pada cairan flammable. Evakuasi area radius 15m."),
            ("🧪","Corrosive","#4ecdc4",
             "Luka bakar kimia, iritasi saluran napas, korosi peralatan",
             "Jas lab tahan kimia, sarung tangan karet tebal, face shield, sepatu boots. Apron PE untuk konsentrasi tinggi.",
             "Siram dengan air mengalir ≥20 menit. Lepas pakaian terkontaminasi. Segera ke Unit Medis."),
            ("💥","Oxidizing","#ffe66d",
             "Mendukung kebakaran, reaksi eksotermik, ledakan kontak organik",
             "Jas lab katun (hindari sintetis), sarung tangan nitril, kacamata safety. Hindari kontak kulit langsung.",
             "Air dalam jumlah besar untuk pengencer. Jauhkan dari bahan organik. Hubungi Damkar jika berskala besar."),
            ("☠️","Toxic","#a29bfe",
             "Keracunan akut/kronis, kanker, gangguan sistem saraf",
             "Respirator yang sesuai (minimal P100), sarung tangan ganda, jas Tyvek, kacamata tertutup penuh.",
             "Panggil bantuan medis SEGERA. Bawa ke udara segar. Berikan antidot spesifik jika tersedia."),
        ]
        for icon, cat, color, hazard, ppe, response in hazards:
            st.markdown(f"""
            <div style='background:#1a2236;border:1px solid #2a3650;border-radius:12px;
                        padding:20px 24px;margin:10px 0;border-left:4px solid {color};'>
              <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.05rem;
                          color:{color};margin-bottom:12px;'>{icon} {cat}</div>
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;'>
                <div>
                  <div style='font-size:0.72rem;color:#8892a4;text-transform:uppercase;
                              letter-spacing:1px;margin-bottom:6px;'>⚡ Risiko Utama</div>
                  <div style='font-size:0.88rem;color:#e2e8f0;'>{hazard}</div>
                </div>
                <div>
                  <div style='font-size:0.72rem;color:#8892a4;text-transform:uppercase;
                              letter-spacing:1px;margin-bottom:6px;'>🦺 APD Wajib</div>
                  <div style='font-size:0.88rem;color:#e2e8f0;'>{ppe}</div>
                </div>
                <div>
                  <div style='font-size:0.72rem;color:#8892a4;text-transform:uppercase;
                              letter-spacing:1px;margin-bottom:6px;'>🚨 Respons Darurat</div>
                  <div style='font-size:0.88rem;color:#e2e8f0;'>{response}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: FAVORIT
# ─────────────────────────────────────────────
elif page == "⭐ Favorit":
    st.markdown("## ⭐ Pasangan Favorit")
    st.markdown("""
    <div class="info-strip">
      Simpan kombinasi yang sering Anda cek. Tambahkan dari halaman <strong>Cek Kompatibilitas</strong>.
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.favorites:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;color:#8892a4;'>
          <div style='font-size:3rem;margin-bottom:12px;'>📋</div>
          <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;
                      color:#e2e8f0;margin-bottom:8px;'>Belum ada favorit</div>
          <p>Cek kompatibilitas dua bahan dan klik tombol <strong>⭐ Simpan ke Favorit</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown(f"**{len(st.session_state.favorites)} pasangan tersimpan**")
        with col_h2:
            if st.button("🗑️ Hapus Semua", use_container_width=True):
                st.session_state.favorites = []
                st.rerun()

        for i, fav in enumerate(st.session_state.favorites):
            compat = fav["compatible"]
            dot_class = "ok" if compat else "no"
            status_txt = "✅ Kompatibel" if compat else "❌ Tidak Kompatibel"
            status_clr = "#00d084" if compat else "#ff4757"

            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"""
                <div class="fav-card">
                  <div class="fav-dot {dot_class}"></div>
                  <div style='flex:1;'>
                    <div style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;'>
                      {fav['chem1']}
                      <span style='color:#8892a4;font-weight:400;'> + </span>
                      {fav['chem2']}
                    </div>
                    <div style='margin-top:4px;'>
                      {chem_badges(fav['chem1'])} {chem_badges(fav['chem2'])}
                    </div>
                  </div>
                  <div style='text-align:right;'>
                    <div style='font-family:Space Mono,monospace;font-size:0.78rem;
                                font-weight:700;color:{status_clr};'>{status_txt}</div>
                    <div style='font-size:0.72rem;color:#8892a4;margin-top:2px;'>{fav['timestamp']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"del_{i}", help="Hapus dari favorit"):
                    st.session_state.favorites.pop(i)
                    st.rerun()

        # Summary stats
        n_ok  = sum(1 for f in st.session_state.favorites if f["compatible"])
        n_no  = len(st.session_state.favorites) - n_ok
        st.markdown("<br>", unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"""
            <div class="stat-card c" style='text-align:center;'>
              <p class="stat-num" style='color:var(--green);'>✅ {n_ok}</p>
              <p class="stat-label">Pasangan Kompatibel</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="stat-card f" style='text-align:center;'>
              <p class="stat-num" style='color:var(--red);'>❌ {n_no}</p>
              <p class="stat-label">Pasangan Tidak Kompatibel</p>
            </div>
            """, unsafe_allow_html=True)

        # Export CSV
        if st.button("📥 Download Favorit sebagai CSV"):
            rows = []
            for fav in st.session_state.favorites:
                rows.append({
                    "Bahan 1": fav["chem1"],
                    "Bahan 2": fav["chem2"],
                    "Status": "Kompatibel" if fav["compatible"] else "Tidak Kompatibel",
                    "Waktu": fav["timestamp"],
                })
            df_fav = pd.DataFrame(rows)
            csv = df_fav.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh CSV", csv, "fcot_favorites.csv", "text/csv")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#8892a4;font-size:0.78rem;padding:12px 0;'>
  ⚗️ <strong style='color:#e2e8f0;'>FCOT ChemSafe</strong> &nbsp;·&nbsp;
  Dibuat berdasarkan teori FCOT untuk keselamatan laboratorium &nbsp;·&nbsp;
  <em>Selalu konsultasikan SDS (Safety Data Sheet) bahan kimia Anda</em>
</div>
""", unsafe_allow_html=True)
