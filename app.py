import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - DARK MODE", layout="wide")

# --- 2. CSS CUSTOM (Halaman Utama GELAP, Teks PUTIH) ---
st.markdown("""
    <style>
    /* Paksa Halaman Utama jadi GELAP */
    .stApp {
        background-color: #0f172a !important;
    }

    /* Paksa Semua Teks di Halaman Utama jadi PUTIH BERSIH */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label, .stApp div {
        color: #ffffff !important;
    }

    /* Kotak Input (Pencarian) agar tetap terbaca */
    .stTextInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
    }

    /* Container Nama Penduduk (Card) */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
        padding: 10px;
    }

    /* MODAL TETAP PUTIH BERSIH (Agar Identitas Jelas) */
    div[role="dialog"] {
        background-color: #ffffff !important;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, 
    div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] td {
        color: #1a202c !important; /* Teks Hitam di dalam Modal */
    }

    /* Tabel Identitas di dalam Modal */
    .info-row { border-bottom: 1px solid #edf2f7; margin-bottom: 2px; background-color: #ffffff; }
    .label-cell { color: #4a5568 !important; font-size: 0.85rem; padding: 8px; width: 45%; font-weight: 500; }
    .value-cell { color: #1a202c !important; font-size: 0.95rem; padding: 8px; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI RENDER BARIS TABEL (Untuk Modal) ---
def render_row(label, value):
    val = str(value).strip() if value and str(value).lower() != 'nan' else "-"
    return f"""
    <div class="info-row">
        <table style="width:100%; border-spacing:0; background-color:white;">
            <tr>
                <td class="label-cell">● {label}</td>
                <td class="value-cell">{val}</td>
            </tr>
        </table>
    </div>
    """

# --- 4. FUNGSI DIALOG (MODAL) IDENTITAS ---
@st.dialog("Identitas", width="large")
def rincian_penduduk(data):
    col_left, col_right = st.columns([1, 2.5], gap="large")
    
    with col_left:
        st.markdown('<div style="border:2px solid #e2e8f0; border-radius:12px; padding:10px; background:white; text-align:center;">', unsafe_allow_html=True)
        foto_url = data.get('FOTO')
        if pd.notna(foto_url) and str(foto_url).startswith('http'):
            st.image(foto_url, use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)
        
        st.markdown(f"<h3>{data.get('NAMA', '-')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>NIK: {data.get('NIK', '-')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<h2 style="border-bottom:3px solid #1a202c; padding-bottom:5px;">Identitas 📄</h2>', unsafe_allow_html=True)
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            st.markdown(render_row("Nama Lengkap", data.get("NAMA")), unsafe_allow_html=True)
            st.markdown(render_row("Tempat Lahir", data.get("TEMPATLAHIR")), unsafe_allow_html=True)
            st.markdown(render_row("Tanggal Lahir", data.get("TANGGALLAHIR")), unsafe_allow_html=True)
            st.markdown(render_row("Pendidikan", data.get("PENDIDIKAN_KK_ID")), unsafe_allow_html=True)
            st.markdown(render_row("SHDK", data.get("SHDK")), unsafe_allow_html=True)
            st.markdown(render_row("Usia", f"{data.get('UMUR', '-')} TAHUN"), unsafe_allow_html=True)

        with sub_col2:
            st.markdown(render_row("Nomor KK", data.get("NO_KK")), unsafe_allow_html=True)
            st.markdown(render_row("Jenis Kelamin", data.get("JENIS_KELAMIN")), unsafe_allow_html=True)
            st.markdown(render_row("Agama", data.get("AGAMA")), unsafe_allow_html=True)
            st.markdown(render_row("Pekerjaan", data.get("PEKERJAAN_ID")), unsafe_allow_html=True)
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
        
        cari_nama = st.text_input("🔍 Cari Nama Warga")
        
        df_p = conn.query("SELECT * FROM data_penduduk;", ttl="1m")
        df_p.columns = [str(c).upper().strip() for c in df_p.columns]

        df_res = df_p[df_p['NAMA'].str.contains(cari_nama, case=False, na=False)] if cari_nama else df_p.head(10)

        for i, row in df_res.iterrows():
            with st.container():
                c1, c2 = st.columns([3, 1])
                c1.write(f"### {row.get('NAMA', 'TANPA NAMA')}")
                if c2.button("👁️ Rincian", key=f"det_{i}"):
                    rincian_penduduk(row)

except Exception as e:
    st.error(f"Kesalahan: {e}")
