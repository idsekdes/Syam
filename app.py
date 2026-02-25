import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - Minimalis", layout="wide")

# --- 2. CSS FIX (Memaksa Teks Terlihat Tajam) ---
st.markdown("""
    <style>
    /* Paksa Background Utama Putih Bersih */
    .stApp { background-color: #ffffff !important; }
    
    /* Paksa SEMUA teks di area utama menjadi Hitam Pekat */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp div {
        color: #1e293b !important;
    }

    /* Khusus untuk teks Nama di daftar (sebelum klik rincian) */
    .stMarkdown p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* Sidebar tetap biarkan gelap agar kontras */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* Card Identitas Minimalis (Latar Putih, Border Abu-abu) */
    .info-row { border-bottom: 1px solid #e2e8f0; margin-bottom: 2px; }
    .label-cell { color: #64748b !important; font-size: 0.85rem; padding: 5px; width: 45%; }
    .value-cell { color: #0f172a !important; font-size: 0.9rem; padding: 5px; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)


# --- 3. FUNGSI RENDER BARIS TABEL ---
def render_row(label, value):
    val = str(value) if pd.notna(value) else "-"
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

# --- 4. FUNGSI DIALOG (MODAL) MINIMALIS ---
@st.dialog("Identitas", width="large")
def rincian_penduduk(data):
    col_left, col_right = st.columns([1, 2.5], gap="large")
    
    with col_left:
        st.markdown('<div class="photo-box">', unsafe_allow_html=True)
        foto_url = data.get('FOTO')
        if pd.notna(foto_url) and str(foto_url).startswith('http'):
            st.image(foto_url, use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)
        
        st.markdown(f"### {data.get('NAMA', '-')}")
        st.markdown(f"<p style='color:#666; margin-bottom:2px;'>Nama: {data.get('NAMA', '-')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#666;'>NIK: {data.get('NIK', '-')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="admin-header">Identitas 📄</div>', unsafe_allow_html=True)
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            st.markdown(render_row("Nama Lengkap", data.get("NAMA", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Tempat Lahir", data.get("TEMPATLAHIR", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Tanggal Lahir", data.get("TANGGALLAHIR", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Pendidikan", data.get("PENDIDIKAN_KK_ID", "-")), unsafe_allow_html=True)
            st.markdown(render_row("SHDK", data.get("SHDK", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Usia", f"{data.get('UMUR', '-')} TAHUN"), unsafe_allow_html=True)

        with sub_col2:
            st.markdown(render_row("Nomor KK", data.get("NO_KK", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Jenis Kelamin", data.get("JENIS_KELAMIN", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Agama", data.get("AGAMA", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Pekerjaan", data.get("PEKERJAAN_ID", "-")), unsafe_allow_html=True)
            st.markdown(render_row("Desa", data.get("DESA", "Wani Lumbumpetigo")), unsafe_allow_html=True)
            st.markdown(render_row("Kecamatan", data.get("KECAMATAN", "Tanantovea")), unsafe_allow_html=True)

    if st.button("Tutup", use_container_width=True):
        st.rerun()

# --- 5. HALAMAN UTAMA ---
try:
    conn = st.connection("postgresql", type="sql")
    st.sidebar.title("SYAM DIGITAL")
    menu = st.sidebar.radio("PILIH MENU", ["Data Penduduk", "Data Anggaran"])

    if menu == "Data Penduduk":
        st.title("📂 Database Kependudukan")
        # Sesuaikan Query dengan tabel Anda
        df_p = conn.query("SELECT * FROM data_penduduk LIMIT 20;", ttl="1m")
        
        # Bersihkan nama kolom jadi huruf besar
        df_p.columns = [str(c).upper().strip() for c in df_p.columns]

        for i, row in df_p.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{row.get('NAMA', 'TANPA NAMA')}**")
                if c2.button("👁️ Rincian", key=f"det_{i}"):
                    rincian_penduduk(row)
except Exception as e:
    st.error(f"Koneksi Database Gagal: {e}")
