import streamlit as st
import pandas as pd
import re
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - ULTRA DARK", layout="wide", page_icon="🏘️")

# --- 2. CSS CUSTOM (BLACK & BLUE THEME) ---
st.markdown("""
    <style>
    /* Global Styles - Paksa Background Hitam */
    .stApp { background-color: #000000 !important; color: #3b82f6 !important; }
    [data-testid="stHeader"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e3a8a; }
    
    /* Modal / Dialog Box */
    div[role="dialog"] { background-color: #000000 !important; border: 2px solid #1e40af !important; }

    /* Card Box - Background Hitam, Border Biru */
    .info-box { 
        background-color: #0a0a0a; 
        border: 1px solid #1e40af; 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 12px; 
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
    }
    
    /* Teks Label & Value - Warna Biru Elektrik */
    .label-txt { color: #60a5fa !important; font-size: 0.85rem; margin-bottom: 2px; font-weight: bold; text-transform: uppercase; }
    .value-txt { color: #3b82f6 !important; font-size: 1.1rem; font-weight: 800; border-bottom: 1px solid #1e3a8a; padding-bottom: 5px; }
    
    /* Section Header */
    .section-header { 
        color: #60a5fa; 
        font-weight: 800; 
        font-size: 1.2rem; 
        margin-top: 15px;
        margin-bottom: 15px;
        text-shadow: 0 0 5px #1e40af;
    }

    /* Admin Card Header */
    .admin-card { 
        background: #0f172a; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #3b82f6; 
        margin-bottom: 25px; 
        text-align: center;
    }

    /* Override Streamlit UI Colors */
    h1, h2, h3, p, span, div { color: #3b82f6 !important; }
    .stButton>button { background-color: #1e40af !important; color: white !important; border-radius: 8px; border: none; }
    .stTextInput>div>div>input { background-color: #0f172a !important; color: #3b82f6 !important; border: 1px solid #1e40af !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. KONEKSI DATABASE ---
conn = st.connection("postgresql", type="sql")

# --- 4. FUNGSI HELPER ---
def clean_col(name):
    return " ".join(str(name).upper().split()).strip()

@st.dialog("👁️ DETAIL DATA PENDUDUK - SYAM DIGITAL", width="large")
def rincian_penduduk(data):
    # HEADER ADMIN
    st.markdown(f"""
        <div class="admin-card">
            <h1 style='margin:0; color:#3b82f6 !important; font-size:2rem;'>SYAM DIGITAL</h1>
            <p style='margin:5px; color:#60a5fa !important;'>👑 <b>ADMINISTRATOR SISTEM</b></p>
            <div style='display:flex; justify-content:center; gap:10px; margin-top:10px;'>
                <span style='color:#10b981 !important; font-weight:bold;'>● ONLINE</span>
                <span style='color:#3b82f6 !important; font-weight:bold;'>✓ TERVERIFIKASI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_foto, c_intro = st.columns([1, 2])
    with c_foto:
        url = data.get('FOTO')
        if pd.notna(url) and str(url).startswith('http'):
            st.image(url, use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)
    
    with c_intro:
        st.markdown(f"<p class='label-txt'>Mode Tampilan</p><p class='value-text' style='font-size:1.5rem; font-weight:bold;'>DETAIL LENGKAP DATA PENDUDUK</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#3b82f6 !important; text-transform:uppercase;'>{data.get('NAMA', 'TANPA NAMA')}</h1>", unsafe_allow_html=True)
        st.write("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("<div class='section-header'>👤 INFORMASI PERSONAL</div>", unsafe_allow_html=True)
        items_p = [
            ("NIK", data.get('NIK','-')),
            ("NAMA LENGKAP", data.get('NAMA','-')),
            ("NO. KK", data.get('NO_KK','-')),
            ("JENIS KELAMIN", data.get('JENIS_KELAMIN','-')),
            ("TEMPAT, TGL LAHIR", f"{data.get('TEMPATLAHIR','-')}, {data.get('TANGGALLAHIR','-')}")
        ]
        for label, val in items_p:
            st.markdown(f"<div class='info-box'><p class='label-txt'>{label}</p><p class='value-txt'>{val}</p></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🎓 PENDIDIKAN & AGAMA</div>", unsafe_allow_html=True)
        items_edu = [
            ("AGAMA", data.get('AGAMA','-')),
            ("PENDIDIKAN", data.get('PENDIDIKAN_KK_ID','-')),
            ("STATUS PERKAWINAN", data.get('STATUS_KAWIN','-')),
            ("PEKERJAAN", data.get('PEKERJAAN_ID','-'))
        ]
        for label, val in items_edu:
            st.markdown(f"<div class='info-box'><p class='label-txt'>{label}</p><p class='value-txt'>{val}</p></div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='section-header'>👨‍👩‍👧‍👦 INFORMASI KELUARGA</div>", unsafe_allow_html=True)
        items_fam = [
            ("SHDK", data.get('SHDK','-')),
            ("KEWARGANEGARAAN", data.get('WARGANEGARA_ID','-')),
            ("NAMA AYAH", data.get('NAMA_AYAH','-')),
            ("NAMA IBU", data.get('NAMA_IBU','-'))
        ]
        for label, val in items_fam:
            st.markdown(f"<div class='info-box'><p class='label-txt'>{label}</p><p class='value-txt'>{val}</p></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🏠 ALAMAT LENGKAP</div>", unsafe_allow_html=True)
        items_loc = [
            ("ALAMAT", data.get('ALAMAT','-')),
            ("DESA", data.get('DESA','WANI LUMBUMPETIGO')),
            ("KECAMATAN", data.get('KECAMATAN','TANANTOVEA')),
            ("KABUPATEN", "DONGGALA"),
            ("PROVINSI", "SULAWESI TENGAH")
        ]
        for label, val in items_loc:
            st.markdown(f"<div class='info-box'><p class='label-txt'>{label}</p><p class='value-txt'>{val}</p></div>", unsafe_allow_html=True)

    if st.button("🚪 TUTUP DETAIL", use_container_width=True):
        st.rerun()

# --- 5. SIDEBAR ---
st.sidebar.markdown("<h1 style='text-align:center;'>SYAM DIGITAL</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("NAVIGASI", ["💰 ANGGARAN DESA", "👨‍👩‍👧‍👦 DATA PENDUDUK", "⚙️ SINKRONISASI"])

# --- 6. HALAMAN ANGGARAN ---
if menu == "💰 ANGGARAN DESA":
    st.title("📊 MONITORING ANGGARAN")
    df = conn.query("SELECT * FROM data_desa;", ttl="1m")
    df.columns = [clean_col(c) for c in df.columns]
    
    filt_kec = st.selectbox("KECAMATAN", ["SEMUA"] + sorted(df['NAMA KEC'].unique().tolist()))
    filt_desa = st.text_input("CARI DESA")
    
    res = df.copy()
    if filt_kec != "SEMUA": res = res[res['NAMA KEC'] == filt_kec]
    if filt_desa: res = res[res['NAMA DESA'].str.contains(filt_desa, case=False)]
    
    st.dataframe(res, use_container_width=True)

# --- 7. HALAMAN PENDUDUK ---
elif menu == "👨‍👩‍👧‍👦 DATA PENDUDUK":
    st.title("📂 DATABASE KEPENDUDUKAN")
    df_p = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
    df_p.columns = [clean_col(c) for c in df_p.columns]
    
    nama_input = st.text_input("🔍 CARI NAMA PENDUDUK (HURUF BESAR)")
    
    if nama_input:
        match = df_p[df_p['NAMA'].str.contains(nama_input, case=False, na=False)]
        for i, r in match.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.write(f"### {r['NAMA']}")
                c1.write(f"NIK: {r['NIK']}")
                if c2.button("👁️ DETAIL", key=f"d_{i}"):
                    rincian_penduduk(r)

# --- 8. HALAMAN SINKRON ---
elif menu == "⚙️ SINKRONISASI":
    st.title("⚙️ PENGATURAN DATABASE")
    link_p = st.text_input("LINK CSV PENDUDUK")
    if st.button("🔄 UPDATE DATABASE"):
        with st.spinner("Memproses..."):
            pd.read_csv(link_p).to_sql('data_penduduk', conn.engine, if_exists='replace', index=False)
            st.success("DATABASE UPDATED!")
