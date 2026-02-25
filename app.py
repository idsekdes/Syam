import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - Dashboard", layout="wide")

# --- 2. CSS UNTUK KETERBACAAN MAKSIMAL (Sangat Tajam) ---
st.markdown("""
    <style>
    /* Latar Belakang Utama (Abu-abu sangat muda agar tidak silau) */
    .stApp { background-color: #f1f5f9; }
    
    /* Paksa semua teks utama menjadi Hitam Pekat */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {
        color: #0f172a !important; 
        font-family: 'Inter', sans-serif;
    }

    /* Styling Kartu di Halaman Utama */
    .warga-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* MODAL: Paksa Putih Bersih & Teks Hitam */
    div[role="dialog"] { background-color: #ffffff !important; border-radius: 20px !important; }
    
    /* Baris Tabel Identitas (Kontras Tinggi) */
    .info-row { border-bottom: 1px solid #f1f5f9; background-color: #ffffff; }
    .label-cell { 
        color: #64748b !important; /* Abu-abu tua untuk label */
        font-size: 0.9rem; 
        padding: 10px; 
        width: 40%; 
        font-weight: 500; 
    }
    .value-cell { 
        color: #0f172a !important; /* Hitam pekat untuk nilai */
        font-size: 1rem; 
        padding: 10px; 
        font-weight: 700; 
    }

    /* Tombol Biru Profesional */
    .stButton>button {
        background-color: #1e40af !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI RENDER BARIS TABEL (Sangat Bersih) ---
def render_row(label, value):
    val = str(value).strip() if value and str(value).lower() != 'nan' else "-"
    return f"""
    <div class="info-row">
        <table style="width:100%; border-spacing:0;">
            <tr>
                <td class="label-cell">● {label}</td>
                <td class="value-cell">{val}</td>
            </tr>
        </table>
    </div>
    """

# --- 4. FUNGSI DIALOG (MODAL) IDENTITAS ---
@st.dialog("Rincian Identitas", width="large")
def rincian_penduduk(data):
    # Header Modal
    st.markdown(f"<h2 style='color:#1e3a8a; border-bottom:3px solid #1e3a8a; padding-bottom:10px;'>📄 {data.get('NAMA', '-')}</h2>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 2], gap="large")
    
    with col_left:
        # Frame Foto
        st.markdown('<div style="border:3px solid #f1f5f9; border-radius:15px; padding:10px; background:white;">', unsafe_allow_html=True)
        foto_url = data.get('FOTO')
        if pd.notna(foto_url) and str(foto_url).startswith('http'):
            st.image(foto_url, use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("---")
        st.markdown(f"**NIK:** `{data.get('NIK', '-')}`")
        st.markdown(f"**Status:** :green[{data.get('STATUS', 'Hidup')}]")

    with col_right:
        sub1, sub2 = st.columns(2)
        with sub1:
            st.markdown(render_row("Nama Lengkap", data.get("NAMA")), unsafe_allow_html=True)
            st.markdown(render_row("Tempat Lahir", data.get("TEMPATLAHIR")), unsafe_allow_html=True)
            st.markdown(render_row("Tanggal Lahir", data.get("TANGGALLAHIR")), unsafe_allow_html=True)
            st.markdown(render_row("Pendidikan", data.get("PENDIDIKAN_KK_ID")), unsafe_allow_html=True)
        with sub2:
            st.markdown(render_row("Nomor KK", data.get("NO_KK")), unsafe_allow_html=True)
            st.markdown(render_row("Jenis Kelamin", data.get("JENIS_KELAMIN")), unsafe_allow_html=True)
            st.markdown(render_row("Agama", data.get("AGAMA")), unsafe_allow_html=True)
            st.markdown(render_row("Pekerjaan", data.get("PEKERJAAN_ID")), unsafe_allow_html=True)
        
        st.markdown(render_row("Alamat Lengkap", data.get("ALAMAT")), unsafe_allow_html=True)
        st.markdown(render_row("Desa/Kecamatan", f"{data.get('DESA')} / {data.get('KECAMATAN')}") , unsafe_allow_html=True)

    if st.button("Tutup Halaman", use_container_width=True):
        st.rerun()

# --- 5. HALAMAN UTAMA ---
try:
    conn = st.connection("postgresql", type="sql")
    
    st.sidebar.markdown("<h2 style='color:white; background:#1e3a8a; padding:10px; border-radius:10px; text-align:center;'>SYAM DIGITAL</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio("NAVIGASI MENU", ["📊 Data Penduduk", "💰 Anggaran Desa"])

    if menu == "📊 Data Penduduk":
        st.title("📂 Database Kependudukan")
        st.markdown("Cari data penduduk dengan mengetik nama di bawah ini:")
        
        cari_nama = st.text_input("🔍 Masukkan Nama Warga", placeholder="Contoh: SYAMSUDDIN")
        
        # Ambil Data
        df = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
        df.columns = [str(c).upper().strip() for c in df.columns]

        # Logika Pencarian
        if cari_nama:
            df_res = df[df['NAMA'].str.contains(cari_nama, case=False, na=False)]
        else:
            df_res = df.head(10)

        st.write(f"Menampilkan **{len(df_res)}** hasil pencarian.")

        # List Kartu Warga
        for i, row in df_res.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="warga-card">
                    <table style="width:100%;">
                        <tr>
                            <td style="width:70%;">
                                <b style="font-size:1.1rem; color:#1e3a8a;">{row['NAMA']}</b><br>
                                <span style="color:#64748b; font-size:0.9rem;">NIK: {row['NIK']} | Dusun: {row.get('DUSUN', '-')}</span>
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                # Tombol Rincian
                if st.button(f"👁️ Lihat Rincian {row['NAMA']}", key=f"btn_{i}", use_container_width=True):
                    rincian_penduduk(row)

except Exception as e:
    st.error(f"Koneksi Gagal: {e}")
