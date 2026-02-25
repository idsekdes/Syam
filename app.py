import streamlit as st
import pandas as pd
import re
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - SID", layout="wide", page_icon="🏘️")

# --- 2. CSS CUSTOM (PREMIUM DESIGN) ---
st.markdown("""
    <style>
    /* Global Styles */
    .main { background-color: #f1f5f9; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: white; }
    
    /* Header Admin Style */
    .admin-card { background: white; padding: 15px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .status-online { color: #10b981; font-weight: bold; font-size: 0.8rem; }
    .badge-verify { background-color: #3b82f6; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; }
    
    /* Modal Detail Style */
    .info-box { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .label-txt { color: #64748b; font-size: 0.8rem; margin-bottom: 0px; font-weight: 500; }
    .value-txt { color: #1e293b; font-size: 1rem; font-weight: 700; margin-top: -5px; }
    .section-header { color: #1e3a8a; font-weight: 800; font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; margin-bottom: 10px; padding-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. KONEKSI DATABASE ---
conn = st.connection("postgresql", type="sql")

# --- 4. FUNGSI HELPER ---
def clean_col(name):
    return " ".join(str(name).upper().split()).strip()

@st.dialog("👁️ Detail Lengkap Data Penduduk", width="large")
def rincian_penduduk(data):
    # HEADER MODAL: SYAM DIGITAL ADMIN
    st.markdown(f"""
        <div class="admin-card">
            <h3 style='margin:0; color:#1e293b;'>SYAM DIGITAL</h3>
            <p style='margin:0; color:#64748b;'>👑 <b>ADMIN</b> | Administrator Sistem Data Penduduk</p>
            <span class="status-online">● Online</span> <span class="badge-verify">✓ Terverifikasi</span>
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
        st.write("Mode Tampilan: **Detail Lengkap**")
        st.title(data.get('NAMA', 'TANPA NAMA'))
        st.info("💡 Informasi lengkap dan terverifikasi data penduduk")

    st.divider()

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("<div class='section-header'>👤 Informasi Personal</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='info-box'><p class='label-txt'>NIK:</p><p class='value-txt'>{data.get('NIK','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Nama Lengkap:</p><p class='value-txt'>{data.get('NAMA','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>No. KK:</p><p class='value-txt'>{data.get('NO_KK','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Jenis Kelamin:</p><p class='value-txt'>{data.get('JENIS_KELAMIN','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Tempat, Tanggal Lahir:</p><p class='value-txt'>{data.get('TEMPATLAHIR','-')}, {data.get('TANGGALLAHIR','-')}</p></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🎓 Pendidikan & Agama</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='info-box'><p class='label-txt'>Agama:</p><p class='value-txt'>{data.get('AGAMA','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Pendidikan:</p><p class='value-txt'>{data.get('PENDIDIKAN_KK_ID','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Status Perkawinan:</p><p class='value-txt'>{data.get('STATUS_KAWIN','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Pekerjaan:</p><p class='value-txt'>{data.get('PEKERJAAN_ID','-')}</p></div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='section-header'>👨‍👩‍👧‍👦 Informasi Keluarga</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='info-box'><p class='label-txt'>SHDK:</p><p class='value-txt'>{data.get('SHDK','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>WNI:</p><p class='value-txt'>{data.get('WARGANEGARA_ID','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Nama Ayah:</p><p class='value-txt'>{data.get('NAMA_AYAH','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Nama Ibu:</p><p class='value-txt'>{data.get('NAMA_IBU','-')}</p></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🏠 Alamat Lengkap</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='info-box'><p class='label-txt'>Alamat:</p><p class='value-txt'>{data.get('ALAMAT','-')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Desa:</p><p class='value-txt'>{data.get('DESA','Wani Lumbumpetigo')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Kecamatan:</p><p class='value-txt'>{data.get('KECAMATAN','Tanantovea')}</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><p class='label-txt'>Kabupaten:</p><p class='value-txt'>Donggala</p></div>", unsafe_allow_html=True)

    if st.button("❌ Tutup", use_container_width=True):
        st.rerun()

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 style='color:white;'>SYAM DIGITAL</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("PILIH MENU", ["💰 Anggaran Desa", "👨‍👩‍👧‍👦 Data Penduduk", "⚙️ Sinkronisasi"])

# --- 6. HALAMAN: ANGGARAN DESA ---
if menu == "💰 Anggaran Desa":
    st.title("📊 Monitoring Anggaran Desa")
    df_ang = conn.query("SELECT * FROM data_desa;", ttl="1m")
    df_ang.columns = [clean_col(c) for c in df_ang.columns]
    
    c1, c2 = st.columns(2)
    with c1: kec = st.selectbox("Kecamatan", ["Semua"] + sorted(df_ang['NAMA KEC'].unique().tolist()))
    with c2: desa = st.text_input("Cari Nama Desa")
    
    filt = df_ang.copy()
    if kec != "Semua": filt = filt[filt['NAMA KEC'] == kec]
    if desa: filt = filt[filt['NAMA DESA'].str.contains(desa, case=False)]
    
    st.dataframe(filt, use_container_width=True, hide_index=True)
    if not filt.empty:
        total = pd.to_numeric(filt['PAGU'], errors='coerce').sum()
        st.metric("Total Pagu Terfilter", f"Rp {total:,.0f}")

# --- 7. HALAMAN: DATA PENDUDUK ---
elif menu == "👨‍👩‍👧‍👦 Data Penduduk":
    st.title("📂 Database Kependudukan")
    df_pen = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
    df_pen.columns = [clean_col(c) for c in df_pen.columns]
    
    cari = st.text_input("🔍 Cari Nama Penduduk (Contoh: FITRIA)")
    
    if cari:
        res = df_pen[df_pen['NAMA'].str.contains(cari, case=False, na=False)]
        st.write(f"Menampilkan **{len(res)}** hasil")
        for idx, row in res.iterrows():
            with st.container(border=True):
                ca, cb = st.columns([3, 1])
                ca.write(f"### {row['NAMA']}\nNIK: `{row['NIK']}` | SHDK: {row.get('SHDK','-')}")
                if cb.button("👁️ Detail", key=f"det_{idx}"):
                    rincian_penduduk(row)
    else:
        st.info("Masukkan nama penduduk untuk melihat detail.")

# --- 8. HALAMAN: SINKRONISASI ---
elif menu == "⚙️ Sinkronisasi":
    st.title("⚙️ Pengaturan Database")
    u_ang = st.text_input("Link CSV Anggaran", "https://docs.google.com")
    u_pen = st.text_input("Link CSV Penduduk", "PASTE_LINK_CSV_PENDUDUK_BARU_ANDA")
    
    if st.button("🔄 Jalankan Sinkronisasi"):
        with st.spinner("Mengupdate data..."):
            pd.read_csv(u_ang).to_sql('data_desa', conn.engine, if_exists='replace', index=False)
            pd.read_csv(u_pen).to_sql('data_penduduk', conn.engine, if_exists='replace', index=False)
            st.success("Sinkronisasi Berhasil!")
            st.rerun()
