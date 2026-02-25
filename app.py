import streamlit as st
import pandas as pd
import re
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Informasi Desa Digital", layout="wide", page_icon="🏘️")

# Custom CSS untuk tampilan lebih modern
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 2. KONEKSI DATABASE ---
try:
    conn = st.connection("postgresql", type="sql")
except Exception as e:
    st.error("Gagal koneksi ke database. Cek secrets.toml.")
    st.stop()

# --- 3. FUNGSI PEMBERSIH & HELPER ---
def clean_col(name):
    return " ".join(str(name).upper().split()).strip()

@st.dialog("📄 PROFIL DIGITAL PENDUDUK", width="large")
def rincian_penduduk(data):
    col_foto, col_utama = st.columns([1, 2])
    with col_foto:
        url_foto = data.get('FOTO')
        if pd.notna(url_foto) and str(url_foto).startswith('http'):
            st.image(url_foto, use_container_width=True, caption=f"NIK: {data.get('NIK')}")
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)

    with col_utama:
        st.title(data.get('NAMA', 'TANPA NAMA'))
        st.subheader(f"🆔 {data.get('SHDK', 'ANGGOTA KELUARGA')}")
        c1, c2 = st.columns(2)
        c1.metric("Umur", f"{data.get('UMUR', '-')} Thn")
        c2.metric("Status", f"{data.get('STATUS', 'Hidup')}")
        st.markdown(f"📍 **Alamat:** {data.get('ALAMAT', '-')}")

    st.divider()
    t1, t2, t3 = st.tabs(["📋 Data Pribadi", "👪 Keluarga", "🏫 Pekerjaan & Lainnya"])
    with t1:
        st.write("### Informasi Personal")
        ca, cb = st.columns(2)
        ca.markdown(f"**NIK:** `{data.get('NIK', '-')}`\n\n**Jenis Kelamin:** {data.get('JENIS_KELAMIN', '-')}\n\n**Agama:** {data.get('AGAMA', '-')}")
        cb.markdown(f"**Tgl Lahir:** {data.get('TANGGALLAHIR', '-')}\n\n**Tempat Lahir:** {data.get('TEMPATLAHIR', '-')}\n\n**Pendidikan:** {data.get('PENDIDIKAN_KK_ID', '-')}")
    with t2:
        st.write("### Hubungan Keluarga")
        cc, cd = st.columns(2)
        cc.markdown(f"👨 **Ayah:** {data.get('NAMA_AYAH', '-')}\n\n🆔 **NIK Ayah:** {data.get('NIK_AYAH', '-')}")
        cd.markdown(f"👩 **Ibu:** {data.get('NAMA_IBU', '-')}\n\n🆔 **NIK Ibu:** {data.get('NIK_IBU', '-')}")
        st.info(f"💍 **Status Perkawinan:** {data.get('STATUS_KAWIN', '-')}")
    with t3:
        st.write("### Detail Administrasi")
        ce, cf = st.columns(2)
        ce.markdown(f"💼 **Pekerjaan:** {data.get('PEKERJAAN_ID', '-')}\n\n🏘️ **Dusun:** {data.get('DUSUN', '-')}")
        cf.markdown(f"🇮🇩 **Warganegara:** {data.get('WARGANEGARA_ID', '-')}\n\n💳 **No. KK:** `{data.get('NO_KK', '-')}`")

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("📌 MENU DESA")
menu = st.sidebar.radio("Pindah Halaman:", ["💰 Anggaran Desa", "👨‍👩‍👧‍👦 Data Penduduk", "⚙️ Pengaturan Data"])

# --- 5. HALAMAN: ANGGARAN DESA ---
if menu == "💰 Anggaran Desa":
    st.header("📊 Monitoring Anggaran Desa")
    df_anggaran = conn.query("SELECT * FROM data_desa;", ttl="1m")
    df_anggaran.columns = [clean_col(c) for c in df_anggaran.columns]

    col1, col2 = st.columns(2)
    with col1:
        pilih_kec = st.selectbox("Filter Kecamatan", ["Semua"] + sorted(df_anggaran['NAMA KEC'].unique().tolist()))
    with col2:
        cari_desa = st.text_input("Cari Nama Desa")

    filtered = df_anggaran.copy()
    if pilih_kec != "Semua": filtered = filtered[filtered['NAMA KEC'] == pilih_kec]
    if cari_desa: filtered = filtered[filtered['NAMA DESA'].str.contains(cari_desa, case=False, na=False)]

    st.dataframe(filtered, use_container_width=True, hide_index=True)
    
    if not filtered.empty:
        st.divider()
        m1, m2, m3 = st.columns(3)
        pagu = pd.to_numeric(filtered['PAGU'], errors='coerce').sum()
        m1.metric("Total Pagu", f"Rp {pagu:,.0f}")
        m2.metric("Total Tahap 1", f"Rp {pd.to_numeric(filtered['TAHAP 1'], errors='coerce').sum():,.0f}")
        m3.metric("Total Tahap 2", f"Rp {pd.to_numeric(filtered['TAHAP 2'], errors='coerce').sum():,.0f}")

# --- 6. HALAMAN: DATA PENDUDUK ---
elif menu == "👨‍👩‍👧‍👦 Data Penduduk":
    st.header("📂 Database Kependudukan")
    df_penduduk = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
    df_penduduk.columns = [clean_col(c) for c in df_penduduk.columns]

    cari_nama = st.text_input("🔍 Masukkan Nama Penduduk (Contoh: SYAMSUDDIN)")
    
    if cari_nama:
        res = df_penduduk[df_penduduk['NAMA'].str.contains(cari_nama, case=False, na=False)]
        st.write(f"Ditemukan **{len(res)}** Jiwa")
        
        for idx, row in res.iterrows():
            with st.container(border=True):
                c_nama, c_btn = st.columns([3, 1])
                c_nama.write(f"### {row['NAMA']}\nNIK: `{row['NIK']}` | Dusun: {row.get('DUSUN','-')}")
                if c_btn.button("👁️ Lihat Detail", key=f"p_{idx}"):
                    rincian_penduduk(row)
    else:
        st.info("Silakan ketik nama penduduk untuk menampilkan rincian.")

# --- 7. HALAMAN: PENGATURAN ---
elif menu == "⚙️ Pengaturan Data":
    st.header("⚙️ Sinkronisasi Data")
    st.warning("Gunakan tombol ini hanya jika ada perubahan di Google Sheets.")
    
    url_ang = st.text_input("Link CSV Anggaran", "https://docs.google.com")
    url_pen = st.text_input("Link CSV Penduduk", "PASTE_LINK_CSV_PENDUDUK_ANDA")

    if st.button("🔄 Perbarui Semua Data (Overide Neon)"):
        with st.spinner("Sedang menyinkronkan..."):
            # Update Anggaran
            df1 = pd.read_csv(url_ang)
            df1.to_sql('data_desa', conn.engine, if_exists='replace', index=False)
            # Update Penduduk
            df2 = pd.read_csv(url_pen)
            df2.to_sql('data_penduduk', conn.engine, if_exists='replace', index=False)
            st.success("Semua data berhasil diperbarui!")
            st.rerun()
