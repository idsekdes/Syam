import streamlit as st
import pandas as pd
import re

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Pencarian Data Desa", layout="wide")
st.title('🏘️ Dashboard Data Desa')

# 2. Membuat Koneksi ke Neon (PENTING: Variabel 'conn' dibuat di sini)
try:
    conn = st.connection("postgresql", type="sql")
except Exception as e:
    st.error(f"Gagal koneksi ke database. Cek file secrets.toml Anda. Error: {e}")
    st.stop()

# 3. Fungsi Pembersih Nama Kolom (Senjata Pamungkas)
def clean_column_name(name):
    name = str(name).upper()
    # Hapus semua karakter aneh (Tab, Newline, dll) ganti dengan spasi
    name = re.sub(r'[^A-Z0-9]', ' ', name)
    # Buang spasi ganda dan spasi di awal/akhir
    return " ".join(name.split())

# 4. Ambil Data dari Neon
try:
    df_neon = conn.query("SELECT * FROM data_desa;", ttl="1m")
    # Bersihkan semua nama kolom dari database
    df_neon.columns = [clean_column_name(c) for c in df_neon.columns]
except Exception as e:
    st.error(f"Gagal mengambil data dari tabel 'data_desa'. Pastikan tabel sudah ada di Neon. Error: {e}")
    st.stop()

st.divider()
st.subheader("🔍 Pencarian Data Desa")

# 5. Input Filter
col1, col2 = st.columns(2)

with col1:
    if 'NAMA KEC' in df_neon.columns:
        list_kec = sorted(df_neon['NAMA KEC'].unique().tolist())
        pilih_kec = st.selectbox("Pilih Kecamatan", ["Semua"] + list_kec)
    else:
        st.warning(f"Kolom 'NAMA KEC' tidak ditemukan. Kolom yang ada: {df_neon.columns.tolist()}")
        pilih_kec = "Semua"

with col2:
    cari_desa = st.text_input("Ketik Nama Desa")

# 6. Proses Filter Data
filtered_df = df_neon.copy()

if pilih_kec != "Semua":
    filtered_df = filtered_df[filtered_df['NAMA KEC'] == pilih_kec]

if cari_desa and 'NAMA DESA' in filtered_df.columns:
    # Filter nama desa (tidak peka huruf besar/kecil)
    filtered_df = filtered_df[filtered_df['NAMA DESA'].str.contains(cari_desa, case=False, na=False)]

# 7. Tampilkan Tabel Hasil
st.write(f"Menemukan **{len(filtered_df)}** data.")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# 8. Hitung Total Pagu (Opsional)
if 'PAGU' in filtered_df.columns and not filtered_df.empty:
    # Pastikan data pagu berupa angka
    total_pagu = pd.to_numeric(filtered_df['PAGU'], errors='coerce').sum()
    st.success(f"💰 Total Pagu: **Rp {total_pagu:,.0f}**")
@st.cache_data
def load_csv_data():
    # Link sakti untuk download CSV langsung tanpa nyasar ke HTML
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ4zaZ2dGcSyoZl6ccR-G77IuJw7P5eJwuF41H3JzlhQacxTSSQFv0slnkckAymsIkI6CFnpOQsbJM8/pub?gid=361483384&single=true&output=csv"
    return pd.read_csv(url)

import io

# --- FITUR DOWNLOAD EXCEL ---
st.divider()
st.subheader("📥 Download Laporan")

if not filtered_df.empty:
    # Buat buffer memori untuk file Excel
    buffer = io.BytesIO()
    
    # Gunakan ExcelWriter dari pandas
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='Data_Desa')
        
        # Atur format (opsional: agar kolom rapi)
        workbook = writer.book
        worksheet = writer.sheets['Data_Desa']
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        
        for col_num, value in enumerate(filtered_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

    # Tombol Download Streamlit
    st.download_button(
        label="📄 Simpan ke Excel (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"Laporan_Desa_{pilih_kec}_{cari_desa}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.warning("Tidak ada data untuk didownload.")
# Tambahkan link penduduk di bagian atas
URL_PENDUDUK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRd3_sz649R1j66EVGQIzrBZa-fQJTR0IvBXiFXlI7nlFmQgbG__qVa9EUM5JUkalFQUXaT3oPLlv2Y/pub?gid=0&single=true&output=csv"

if st.button("👥 Sinkronkan Data Penduduk"):
    df_penduduk = pd.read_csv(URL_PENDUDUK)
    # Bersihkan nama kolom agar standar SQL
    df_penduduk.columns = [str(c).strip().upper().replace(' ', '_') for c in df_penduduk.columns]
    
    # Simpan ke tabel berbeda di Neon
    df_penduduk.to_sql('data_penduduk', conn.engine, if_exists='replace', index=False)
    st.success("Data Penduduk berhasil masuk ke Neon!")

# Buat Menu di Samping
menu = st.sidebar.selectbox("Pilih Menu", ["💰 Anggaran Desa", "👨‍👩‍👧‍👦 Data Penduduk"])

if menu == "💰 Anggaran Desa":
    st.header("Monitoring Anggaran Desa")
    # ... (Masukkan kode pencarian anggaran yang sudah jadi tadi disini) ...
    df_neon = conn.query("SELECT * FROM data_desa;")
    st.dataframe(df_neon)

elif menu == "👨‍👩‍👧‍👦 Data Penduduk":
    st.header("📂 Database Penduduk Desa")
    
    # 1. Ambil data dari tabel penduduk di Neon
    try:
        df_orang = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
        
        # --- PEMBERSIH KOLOM (Agar Pencarian Lancar) ---
        df_orang.columns = [str(c).strip().upper() for c in df_orang.columns]
        
        # 2. Fitur Pencarian
        col1, col2 = st.columns([2, 1])
        with col1:
            cari_nama = st.text_input("🔍 Cari Nama Penduduk (Ketik Nama)")
        with col2:
            # Misal ada kolom JENIS KELAMIN atau DESA di data pendudukmu
            if 'DESA' in df_orang.columns:
                list_desa = sorted(df_orang['DESA'].unique())
                pilih_desa = st.selectbox("Filter Desa", ["Semua"] + list_desa)
            else:
                pilih_desa = "Semua"

        # 3. Logika Filter
        filtered_orang = df_orang.copy()
        
        if cari_nama:
            # Mencari nama yang mengandung kata kunci (tidak peka huruf besar/kecil)
            filtered_orang = filtered_orang[filtered_orang['NAMA'].str.contains(cari_nama, case=False, na=False)]
        
        if pilih_desa != "Semua":
            filtered_orang = filtered_orang[filtered_orang['DESA'] == pilih_desa]

        # 4. Tampilkan Hasil
        st.write(f"Ditemukan **{len(filtered_orang)}** jiwa.")
        st.dataframe(filtered_orang, use_container_width=True, hide_index=True)
        
        # 5. Statistik Singkat (Contoh: Total Laki-laki / Perempuan)
        if 'JENIS KELAMIN' in filtered_orang.columns:
            st.divider()
            st.subheader("📊 Statistik Penduduk")
            st.bar_chart(filtered_orang['JENIS KELAMIN'].value_counts())

    except Exception as e:
        st.error(f"Gagal memuat data. Pastikan sudah klik 'Sinkronkan Data Penduduk'.")
        st.info("Tips: Cek apakah tabel 'data_penduduk' sudah ada di SQL Editor Neon.")
# --- Tambahkan Statistik Penduduk ---
if not filtered_orang.empty:
    st.divider()
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Total Jiwa", len(filtered_orang))
        
    # Jika ada kolom 'JENIS KELAMIN'
    if 'JENIS KELAMIN' in filtered_orang.columns:
        with c2:
            laki = len(filtered_orang[filtered_orang['JENIS KELAMIN'] == 'LAKI-LAKI'])
            st.metric("Laki-laki", laki)
        with c3:
            perempuan = len(filtered_orang[filtered_orang['JENIS KELAMIN'] == 'PEREMPUAN'])
            st.metric("Perempuan", perempuan)

    # Tambahkan Grafik Kelompok Umur jika ada kolom 'UMUR'
    if 'UMUR' in filtered_orang.columns:
        st.subheader("📊 Komposisi Umur")
        st.bar_chart(filtered_orang['UMUR'].value_counts().sort_index())
# 1. Buat Fungsi Modal (Dialog)
@st.dialog("📄 Rincian Data Penduduk")
def rincian_penduduk(data):
    st.write(f"### {data['NAMA']}")
    st.divider()
    
    # Menampilkan data dalam 2 kolom agar rapi
    c1, c2 = st.columns(2)
    for i, (col, val) in enumerate(data.items()):
        if i % 2 == 0:
            c1.markdown(f"**{col}:** {val}")
        else:
            c2.markdown(f"**{col}:** {val}")
    
    st.divider()
    if st.button("Tutup"):
        st.rerun()

# 2. Update Tampilan Hasil Pencarian (Setelah filter_orang jadi)
if not filtered_orang.empty:
    st.write(f"Ditemukan **{len(filtered_orang)}** jiwa.")
    
    # Tampilkan tabel ringkas (hanya kolom penting)
    kolom_tampil = ['NAMA', 'JENIS KELAMIN', 'DESA'] # Sesuaikan kolom yang ada
    # Pastikan kolom ini ada di data anda
    kolom_fix = [c for c in kolom_tampil if c in filtered_orang.columns]
    
    # Looping untuk membuat tombol detail tiap orang
    for index, row in filtered_orang.iterrows():
        with st.container(border=True):
            col_nama, col_tombol = st.columns([3, 1])
            col_nama.write(f"**{row['NAMA']}** ({row.get('DESA', 'N/A')})")
            
            # Jika tombol diklik, panggil fungsi Modal
            if col_tombol.button("👁️ Detail", key=f"btn_{index}"):
                rincian_penduduk(row)

else:
    st.info("Ketik nama untuk mencari...")
import streamlit as st
import pandas as pd

# 1. FUNGSI MODAL DENGAN FOTO
@st.dialog("📄 PROFIL DIGITAL PENDUDUK", width="large")
def rincian_penduduk(data):
    # 1. CSS Custom untuk mempercantik tampilan (Optional)
    st.markdown("""
        <style>
        [data-testid="stExpander"] { border: none; box-shadow: none; }
        .main-profile { background-color: #f0f2f6; padding: 20px; border-radius: 15px; }
        </style>
    """, unsafe_allow_html=True)

    # 2. Header Utama (Foto & Info Penting)
    with st.container():
        col_foto, col_utama = st.columns([1, 2])
        
        with col_foto:
            # Menggunakan kolom 'FOTO' sesuai data Anda
            url_foto = data.get('FOTO')
            if pd.notna(url_foto) and str(url_foto).startswith('http'):
                st.image(url_foto, use_container_width=True, caption=f"ID: {data.get('NIK')}")
            else:
                st.image("https://cdn-icons-png.flaticon.com", 
                         use_container_width=True, caption="Foto Tidak Tersedia")

        with col_utama:
            st.title(f" {data.get('NAMA', 'TANPA NAMA')}")
            st.subheader(f"🏷️ {data.get('SHDK', 'ANGGOTA KELUARGA')}")
            
            # Kartu Info Cepat
            c1, c2 = st.columns(2)
            c1.metric("Umur", f"{data.get('UMUR', '-')} Thn")
            c2.metric("Status", f"{data.get('STATUS', 'Hidup')}")
            
            st.markdown(f"📍 **Alamat:** {data.get('ALAMAT', '-')}")
            st.markdown(f"💳 **No. KK:** `{data.get('NO_KK', '-')}`")

    st.divider()

    # 3. Data Detail Terstruktur dalam Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Data Pribadi", "👪 Keluarga", "🏫 Lainnya"])

    with tab1:
        st.write("### Informasi Personal")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**NIK:** `{data.get('NIK', '-')}`")
            st.markdown(f"**Jenis Kelamin:** {data.get('JENIS_KELAMIN', '-')}")
            st.markdown(f"**Tempat Lahir:** {data.get('TEMPATLAHIR', '-')}")
        with col_b:
            st.markdown(f"**Tanggal Lahir:** {data.get('TANGGALLAHIR', '-')}")
            st.markdown(f"**Agama:** {data.get('AGAMA', '-')}")
            st.markdown(f"**Pendidikan:** {data.get('PENDIDIKAN_KK_ID', '-')}")

    with tab2:
        st.write("### Hubungan Keluarga")
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown(f"👨 **Nama Ayah:** {data.get('NAMA_AYAH', '-')}")
            st.markdown(f"🆔 **NIK Ayah:** {data.get('NIK_AYAH', '-')}")
        with col_d:
            st.markdown(f"👩 **Nama Ibu:** {data.get('NAMA_IBU', '-')}")
            st.markdown(f"🆔 **NIK Ibu:** {data.get('NIK_IBU', '-')}")
        st.info(f"💍 **Status Perkawinan:** {data.get('STATUS_KAWIN', '-')}")

    with tab3:
        st.write("### Data Tambahan")
        col_e, col_f = st.columns(2)
        with col_e:
            st.markdown(f"💼 **Pekerjaan:** {data.get('PEKERJAAN_ID', '-')}")
            st.markdown(f"🏘️ **Dusun:** {data.get('DUSUN', '-')}")
        with col_f:
            st.markdown(f"🇮🇩 **Kewarganegaraan:** {data.get('WARGANEGARA_ID', '-')}")

    st.divider()
    
    # Tombol Aksi
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("❌ Tutup"):
            st.rerun()
    with col_btn2:
        st.caption("Data ini bersumber dari Sistem Informasi Desa Digital.")
