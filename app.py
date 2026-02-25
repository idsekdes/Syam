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

