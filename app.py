import streamlit as st
import pandas as pd
import re
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SID Digital", layout="wide", page_icon="🏘️")

# CSS SAKTI: Memperbaiki warna teks metrik & ukuran font
st.markdown("""
    <style>
    /* Paksa teks metrik dan label menjadi Hitam Pekat */
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; font-size: 1.8rem !important; }
    [data-testid="stMetricLabel"] { color: #1e293b !important; font-weight: bold !important; font-size: 1rem !important; }
    
    /* Berikan background putih pada area informasi agar kontras di Dark Mode */
    [data-testid="column"] { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
    
    /* Tulisan Alamat dan Judul */
    .big-font { font-size: 115% !important; color: #000000 !important; font-weight: bold; }
    .stMarkdown p { color: #000000 !important; }
    
    /* Box NIK & KK agar lebih Gelap teksnya */
    code { font-size: 110% !important; color: #ffffff !important; background-color: #1e293b !important; padding: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. KONEKSI DATABASE ---
conn = st.connection("postgresql", type="sql")

# --- 3. FUNGSI HELPER ---
def clean_col(name):
    return " ".join(str(name).upper().split()).strip()

# --- 2. PERBAIKAN FUNGSI MODAL (Ganti Baris 26-68) ---
@st.dialog("📄 PROFIL DIGITAL PENDUDUK", width="large")
def rincian_penduduk(data):
    col_foto, col_utama = st.columns([1, 2]) # Perbandingan lebar 1:2
    
    with col_foto:
        url_foto = data.get('FOTO')
        if pd.notna(url_foto) and str(url_foto).startswith('http'):
            st.image(url_foto, use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)

    with col_utama:
        st.markdown(f"<h1 style='color:black; margin-bottom:0;'>👤 {data.get('NAMA', 'TANPA NAMA')}</h1>", unsafe_allow_html=True)
        st.success(f"📋 **STATUS:** {data.get('SHDK', 'ANGGOTA KELUARGA')}")
        
        # Kartu Metrik dengan Background Putih (Sudah diatur di CSS atas)
        m1, m2, m3 = st.columns(3)
        m1.metric("Umur", f"{data.get('UMUR', '-')} Thn")
        m2.metric("Status", f"{data.get('STATUS', 'Hidup')}")
        m3.metric("Dusun", f"{data.get('DUSUN', '-')}")
        
        # Teks Alamat Hitam Tebal
        st.markdown(f'<p class="big-font">📍 <b>Alamat:</b> {data.get("ALAMAT", "-")}</p>', unsafe_allow_html=True)
        
        # NIK & KK GABUNG (Background Gelap, Teks Putih Terang agar Jelas)
        st.write("💳 **Identitas (Klik ikon kanan untuk salin):**")
        identitas = f"NIK: {data.get('NIK', '-')} | No. KK: {data.get('NO_KK', '-')}"
        st.code(identitas, language="text")

    st.divider()
    t1, t2, t3 = st.tabs(["📋 Data Pribadi", "👪 Keluarga", "💼 Administrasi"])
    
    with t1:
        st.write("### Informasi Personal")
        ca, cb = st.columns(2)
        ca.markdown(f"**Jenis Kelamin:** {data.get('JENIS_KELAMIN', '-')}\n\n**Agama:** {data.get('AGAMA', '-')}\n\n**Tempat Lahir:** {data.get('TEMPATLAHIR', '-')}")
        cb.markdown(f"**Tgl Lahir:** {data.get('TANGGALLAHIR', '-')}\n\n**Pendidikan:** {data.get('PENDIDIKAN_KK_ID', '-')}\n\n**Gol. Darah:** {data.get('GOLONGAN_DARAH', '-')}")
            
    with t2:
        st.write("### Hubungan Keluarga")
        cc, cd = st.columns(2)
        cc.markdown(f"👨 **Ayah:** {data.get('NAMA_AYAH', '-')}\n\n🆔 **NIK Ayah:** {data.get('NIK_AYAH', '-')}")
        cd.markdown(f"👩 **Ibu:** {data.get('NAMA_IBU', '-')}\n\n🆔 **NIK Ibu:** {data.get('NIK_IBU', '-')}")
        st.warning(f"💍 **Status Perkawinan:** {data.get('STATUS_KAWIN', '-')}")
            
    with t3:
        st.write("### Detail Pekerjaan")
        ce, cf = st.columns(2)
        ce.markdown(f"💼 **Pekerjaan:** {data.get('PEKERJAAN_ID', '-')}\n\n🇮🇩 **Warganegara:** {data.get('WARGANEGARA_ID', '-')}")
        cf.markdown(f"🏘️ **Dusun:** {data.get('DUSUN', '-')}\n\n🏷️ **Status:** {data.get('STATUS', '-')}")

# --- 4. NAVIGASI SIDEBAR ---
menu = st.sidebar.radio("PILIH HALAMAN:", ["💰 Anggaran Desa", "👨‍👩‍👧‍👦 Data Penduduk", "⚙️ Sinkronisasi Data"])

# --- 5. HALAMAN ANGGARAN ---
if menu == "💰 Anggaran Desa":
    st.header("📊 Monitoring Anggaran Desa")
    df_ang = conn.query("SELECT * FROM data_desa;", ttl="1m")
    df_ang.columns = [clean_col(c) for c in df_ang.columns]
    
    k1, k2 = st.columns(2)
    pilih_kec = k1.selectbox("Kecamatan", ["Semua"] + sorted(df_ang['NAMA KEC'].unique().tolist()))
    cari_desa = k2.text_input("Cari Desa")
    
    filt = df_ang.copy()
    if pilih_kec != "Semua": filt = filt[filt['NAMA KEC'] == pilih_kec]
    if cari_desa: filt = filt[filt['NAMA DESA'].str.contains(cari_desa, case=False, na=False)]
    
    st.dataframe(filt, use_container_width=True, hide_index=True)
    if not filt.empty:
        total = pd.to_numeric(filt['PAGU'], errors='coerce').sum()
        st.success(f"💰 **Total Pagu Terfilter: Rp {total:,.0f}**")

# --- 6. HALAMAN PENDUDUK ---
elif menu == "👨‍👩‍👧‍👦 Data Penduduk":
    st.header("📂 Database Kependudukan")
    df_pen = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
    df_pen.columns = [clean_col(c) for c in df_pen.columns]
    
    cari_nama = st.text_input("🔍 Cari Nama Warga (Contoh: SYAMSUDDIN)")
    
    if cari_nama:
        res = df_pen[df_pen['NAMA'].str.contains(cari_nama, case=False, na=False)]
        st.write(f"Ditemukan **{len(res)}** Jiwa")
        for idx, row in res.iterrows():
            with st.container(border=True):
                c_n, c_b = st.columns([3, 1])
                c_n.write(f"### {row['NAMA']}\nNIK: `{row['NIK']}`")
                if c_b.button("👁️ Rincian", key=f"p_{idx}"):
                    rincian_penduduk(row)

# --- 7. HALAMAN SINKRON ---
elif menu == "⚙️ Sinkronisasi Data":
    st.header("⚙️ Update Database dari Google Sheets")
    u_ang = st.text_input("Link CSV Anggaran", "https://docs.google.com")
    u_pen = st.text_input("Link CSV Penduduk", "PASTE_LINK_CSV_PENDUDUK_DI_SINI")
    
    if st.button("🔄 Jalankan Sinkronisasi"):
        with st.spinner("Sedang memproses..."):
            pd.read_csv(u_ang).to_sql('data_desa', conn.engine, if_exists='replace', index=False)
            pd.read_csv(u_pen).to_sql('data_penduduk', conn.engine, if_exists='replace', index=False)
            st.success("Berhasil! Database Neon telah diperbarui.")
            st.rerun()
