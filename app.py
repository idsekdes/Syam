import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SYAM DIGITAL - Minimalis", layout="wide")

# --- 2. CSS MINIMALIS (Latar Putih, Teks Kontras) ---
st.markdown("""
    <style>
    /* Background Utama Putih */
    .stApp { background-color: #ffffff; }
    
    /* Container Kartu Identitas */
    .id-card-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Foto Profile Box */
    .photo-box {
        border: 1px solid #e0e0e0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        background-color: #fcfcfc;
    }

    /* Tabel Identitas Minimalis */
    .info-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .info-row { border-bottom: 1px solid #f0f0f0; }
    .label-cell { 
        color: #666666; 
        font-size: 0.85rem; 
        padding: 8px 5px; 
        width: 35%;
        font-weight: 500;
    }
    .value-cell { 
        color: #222222; 
        font-size: 0.9rem; 
        padding: 8px 5px; 
        font-weight: 600;
    }
    
    /* Header Admin Minimalis */
    .admin-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #333333;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI DIALOG (MODAL) MINIMALIS ---
@st.dialog("Identitas", width="large")
def rincian_penduduk(data):
    with st.container():
        col_left, col_right = st.columns([1, 2.5], gap="large")
        
        # --- BAGIAN KIRI: FOTO & NAMA UTAMA ---
        with col_left:
            st.markdown('<div class="photo-box">', unsafe_allow_html=True)
            foto_url = data.get('FOTO')
            if pd.notna(foto_url) and str(foto_url).startswith('http'):
                st.image(foto_url, use_container_width=True)
            else:
                st.image("https://cdn-icons-png.flaticon.com", use_container_width=True)
            
            st.markdown(f"### {data.get('NAMA', '-')}")
            st.markdown(f"<p style='color:#666;'>Nama: {data.get('NAMA', '-')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#666;'>NIK: {data.get('NIK', '-')}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- BAGIAN KANAN: TABEL DETAIL ---
        with col_right:
            st.markdown('<div class="admin-header">Identitas 📝</div>', unsafe_allow_html=True)
            
            # Membagi data menjadi 2 kolom tabel agar mirip gambar
            sub_col1, sub_col2 = st.columns(2)
            
            def render_row(label, value):
                return f"""
                <div class="info-row">
                    <table style="width:100%">
                        <tr>
                            <td class="label-cell">● {label}</td>
                            <td class="value-cell">{value}</td>
                        </tr>
                    </table>
                </div>
                """

            with sub_col1:
                st.markdown(render_row("Nama Lengkap", data.get("NAMA", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Tempat Lahir", data.get("TEMPATLAHIR", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Tanggal Lahir", data.get("TANGGALLAHIR", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Pendidikan", data.get("PENDIDIKAN_KK_ID", "-")), unsafe_allow_html=True)
                st.markdown(render_row("SHDK", data.get("SHDK", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Usia", f"{data.get('UMUR', '-')} TAHUN")), unsafe_allow_html=True)

            with sub_col2:
                st.markdown(render_row("Nomor KK", data.get("NO_KK", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Jenis Kelamin", data.get("JENIS_KELAMIN", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Agama", data.get("AGAMA", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Pekerjaan", data.get("PEKERJAAN_ID", "-")), unsafe_allow_html=True)
                st.markdown(render_row("Desa", data.get("DESA", "Wani Lumbumpetigo")), unsafe_allow_html=True)
                st.markdown(render_row("Kecamatan", data.get("KECAMATAN", "Tanantovea")), unsafe_allow_html=True)

    if st.button("Tutup", use_container_width=True):
        st.rerun()

# --- 4. HALAMAN UTAMA (MENU NAVIGASI) ---
# Tambahkan logika navigasi sidebar dan pencarian seperti sebelumnya di sini...
