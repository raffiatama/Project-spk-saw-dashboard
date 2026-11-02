
import streamlit as st
import pandas as pd
import numpy as np
import os

# ==========================================
# KONFIGURASI
# ==========================================

st.set_page_config(
    page_title="SPK Seleksi Karyawan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PENGATURAN FILE DATA
# ==========================================

os.makedirs("data", exist_ok=True)

FILE_DATA = "data/karyawan.csv"
FILE_PENILAIAN = "data/penilaian_jurnal.csv"

KOLOM = ["ID", "Nama Kandidat"]

if not os.path.exists(FILE_DATA):
    pd.DataFrame(columns=KOLOM).to_csv(
        FILE_DATA,
        index=False,
        encoding="utf-8-sig"
    )


def load_data():
    df = pd.read_csv(FILE_DATA, dtype=str).fillna("")

    for kolom in KOLOM:
        if kolom not in df.columns:
            df[kolom] = ""

    return df[KOLOM]


def save_data(df):
    df.to_csv(
        FILE_DATA,
        index=False,
        encoding="utf-8-sig"
    )


def generate_id(df):
    nomor = 1

    if not df.empty:
        angka = []

        for item in df["ID"]:
            try:
                angka.append(int(item.replace("K", "")))
            except ValueError:
                pass

        if angka:
            nomor = max(angka) + 1

    return f"K{nomor:03d}"


df = load_data()

# ==========================================
# DATA KRITERIA JURNAL
# ==========================================

data_kriteria = pd.DataFrame({
    "Kode": ["K1", "K2", "K3", "K4", "K5"],
    "Nama Kriteria": [
        "Wawancara",
        "Uji Kompetensi",
        "Nilai Akademik",
        "Pengalaman Bekerja",
        "Kepribadian"
    ],
    "Bobot": [15, 30, 15, 10, 30],
    "Jenis": [
        "Benefit",
        "Benefit",
        "Benefit",
        "Benefit",
        "Benefit"
    ]
})

# Bobot dalam bentuk desimal
bobot = np.array([0.15, 0.30, 0.15, 0.10, 0.30])

# ==========================================
# SKALA PENILAIAN
# ==========================================

data_skala = pd.DataFrame({
    "Keterangan": [
        "Baik Sekali",
        "Baik",
        "Cukup",
        "Kurang",
        "Kurang Sekali"
    ],
    "Nilai": [5, 4, 3, 2, 1]
})

# ==========================================
# DATA ALTERNATIF JURNAL
# ==========================================

data_penilaian = pd.DataFrame({
    "Nomor Peserta": [
        "0001",
        "0002",
        "0003",
        "0004",
        "0005"
    ],
    "Nama Kandidat": [
        "KANDIDAT 1",
        "KANDIDAT 2",
        "KANDIDAT 3",
        "KANDIDAT 4",
        "KANDIDAT 5"
    ],
    "K1 - Wawancara": [5, 4, 3, 3, 4],
    "K2 - Uji Kompetensi": [4, 5, 5, 5, 4],
    "K3 - Nilai Akademik": [3, 3, 3, 3, 3],
    "K4 - Pengalaman Bekerja": [3, 2, 4, 4, 3],
    "K5 - Kepribadian": [4, 3, 3, 5, 3]
})

# ==========================================
# PROSES PERHITUNGAN SAW
# ==========================================

kolom_nilai = [
    "K1 - Wawancara",
    "K2 - Uji Kompetensi",
    "K3 - Nilai Akademik",
    "K4 - Pengalaman Bekerja",
    "K5 - Kepribadian"
]

# Matriks keputusan
matriks_x = data_penilaian[kolom_nilai].astype(float)

# Nilai maksimum setiap kriteria
nilai_maksimum = matriks_x.max()

# Normalisasi karena seluruh kriteria benefit
matriks_r = matriks_x.div(nilai_maksimum, axis=1)

# Perhitungan nilai preferensi
nilai_preferensi = matriks_r.dot(bobot)

# Data hasil perhitungan
hasil_saw = pd.DataFrame({
    "Nomor Peserta": data_penilaian["Nomor Peserta"],
    "Nama Kandidat": data_penilaian["Nama Kandidat"],
    "Nilai Preferensi": nilai_preferensi
})

# ==========================================
# CSS DASHBOARD
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #EDF3F6;
    color: #202A35;
}

[data-testid="stSidebar"] {
    background-color: #202A35;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    color: #20B8C5;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #B8C7D1;
}

.main-title {
    font-size: 30px;
    font-weight: 700;
    color: #202A35;
}

.main-subtitle {
    color: #667784;
    font-size: 14px;
}

.stat-card {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 12px;
    border-left: 5px solid #20B8C5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.stat-label {
    font-size: 13px;
    color: #667784;
}

.stat-value {
    font-size: 27px;
    font-weight: bold;
    color: #202A35;
}

.panel {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.stButton > button {
    background-color: #20B8C5;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1596A1;
    color: #FFFFFF;
}

[data-testid="stAppDeployButton"] {
    background-color: #20B8C5 !important;
    color: #FFFFFF !important;
    border-radius: 8px;
}

[data-testid="stMainMenu"] button {
    color: #20B8C5 !important;
}

[data-testid="stAppDeployButton"]:hover,
[data-testid="stMainMenu"] button:hover {
    background-color: #1596A1 !important;
    color: #FFFFFF !important;
}

hr {
    border-color: #DCE5EA;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">SPK SAW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Sistem Seleksi Penerimaan Karyawan'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    menu = st.radio(
        "MENU UTAMA",
        [
            "Dashboard",
            "Data Karyawan",
            "Kriteria & Bobot",
            "Penilaian",
            "Perhitungan SAW",
            "Hasil Perangkingan"
        ]
    )

    st.markdown("---")
    st.caption("Metode: Simple Additive Weighting")
    st.caption("Versi 1.0")

# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.markdown(
        '<div class="main-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Sistem Pendukung Keputusan Seleksi Penerimaan Karyawan'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    statistik = [
        (col1, "Total Kandidat", str(len(data_penilaian)), "👥"),
        (col2, "Total Kriteria", "5", "📋"),
        (col3, "Metode", "SAW", "⚙️"),
        (col4, "Status Sistem", "Aktif", "🟢")
    ]

    for col, label, value, icon in statistik:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{icon} {label}</div>
                <div class="stat-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Tentang Sistem")

        st.write("""
        Aplikasi Sistem Pendukung Keputusan ini dirancang
        untuk membantu proses seleksi penerimaan karyawan
        menggunakan metode Simple Additive Weighting (SAW).

        Sistem melakukan penilaian berdasarkan beberapa
        kriteria, kemudian menghasilkan nilai preferensi
        dan perangkingan kandidat.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Informasi Metode")

        st.write("**Metode:** Simple Additive Weighting")
        st.write("**Jenis Sistem:** Sistem Pendukung Keputusan")
        st.write("**Objek:** Seleksi Penerimaan Karyawan")
        st.write("**Output:** Nilai Preferensi dan Ranking")

        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.info(
        "Gunakan menu navigasi di sebelah kiri "
        "untuk mengakses fitur sistem."
    )

# ==========================================
# DATA KARYAWAN
# ==========================================

elif menu == "Data Karyawan":

    st.markdown(
        '<div class="main-title">Data Karyawan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Kelola data kandidat penerimaan karyawan'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Kandidat Terdaftar</div>
            <div class="stat-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Status Pengelolaan Data</div>
            <div class="stat-value">Aktif</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("Daftar Kandidat")

    if df.empty:
        st.info(
            "Belum ada data kandidat. "
            "Silakan tambahkan kandidat baru."
        )
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("ID Kandidat"),
                "Nama Kandidat": st.column_config.TextColumn(
                    "Nama Kandidat"
                )
            }
        )

    st.markdown("---")

    # TAMBAH KANDIDAT

    with st.expander("➕ Tambah Kandidat Baru", expanded=True):

        with st.form("form_tambah"):

            nama = st.text_input(
                "Nama Kandidat",
                placeholder="Masukkan nama kandidat"
            )

            tambah = st.form_submit_button(
                "Simpan Kandidat",
                use_container_width=True
            )

            if tambah:

                if not nama.strip():
                    st.error("Nama kandidat harus diisi.")

                elif nama.strip().lower() in [
                    n.lower() for n in df["Nama Kandidat"]
                ]:
                    st.warning("Nama kandidat sudah terdaftar.")

                else:
                    id_baru = generate_id(df)

                    data_baru = pd.DataFrame([{
                        "ID": id_baru,
                        "Nama Kandidat": nama.strip()
                    }])

                    df = pd.concat(
                        [df, data_baru],
                        ignore_index=True
                    )

                    save_data(df)

                    st.success(
                        f"Kandidat {nama.strip()} berhasil ditambahkan."
                    )

                    st.rerun()

    # EDIT KANDIDAT

    with st.expander("✏️ Edit Data Kandidat"):

        if df.empty:
            st.warning("Belum ada kandidat yang dapat diedit.")

        else:

            pilihan_edit = st.selectbox(
                "Pilih Kandidat",
                df["ID"].tolist(),
                format_func=lambda x: (
                    f"{x} - "
                    f"{df.loc[df['ID'] == x, 'Nama Kandidat'].iloc[0]}"
                ),
                key="pilihan_edit"
            )

            nama_lama = df.loc[
                df["ID"] == pilihan_edit,
                "Nama Kandidat"
            ].iloc[0]

            with st.form("form_edit"):

                nama_baru = st.text_input(
                    "Nama Kandidat",
                    value=nama_lama
                )

                simpan_edit = st.form_submit_button(
                    "Simpan Perubahan",
                    use_container_width=True
                )

                if simpan_edit:

                    if not nama_baru.strip():
                        st.error("Nama kandidat tidak boleh kosong.")

                    elif nama_baru.strip().lower() in [
                        n.lower()
                        for n in df.loc[
                            df["ID"] != pilihan_edit,
                            "Nama Kandidat"
                        ]
                    ]:
                        st.warning("Nama kandidat sudah digunakan.")

                    else:
                        df.loc[
                            df["ID"] == pilihan_edit,
                            "Nama Kandidat"
                        ] = nama_baru.strip()

                        save_data(df)

                        st.success("Data kandidat berhasil diperbarui.")
                        st.rerun()

    # HAPUS KANDIDAT

    with st.expander("🗑️ Hapus Data Kandidat"):

        if df.empty:
            st.warning("Belum ada kandidat yang dapat dihapus.")

        else:

            pilihan_hapus = st.selectbox(
                "Pilih kandidat yang akan dihapus",
                df["ID"].tolist(),
                format_func=lambda x: (
                    f"{x} - "
                    f"{df.loc[df['ID'] == x, 'Nama Kandidat'].iloc[0]}"
                ),
                key="pilihan_hapus"
            )

            nama_hapus = df.loc[
                df["ID"] == pilihan_hapus,
                "Nama Kandidat"
            ].iloc[0]

            st.warning(f"Kandidat yang dipilih: {nama_hapus}")

            konfirmasi = st.checkbox(
                "Saya yakin ingin menghapus kandidat ini."
            )

            if st.button(
                "Hapus Kandidat",
                use_container_width=True,
                disabled=not konfirmasi
            ):

                df = df[df["ID"] != pilihan_hapus]
                save_data(df)

                st.success("Data kandidat berhasil dihapus.")
                st.rerun()

# ==========================================
# KRITERIA & BOBOT
# ==========================================

elif menu == "Kriteria & Bobot":

    st.markdown(
        '<div class="main-title">Kriteria & Bobot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Kriteria penilaian berdasarkan jurnal tahun 2025'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total Kriteria</div>
            <div class="stat-value">5</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total Bobot</div>
            <div class="stat-value">100%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Jenis Kriteria</div>
            <div class="stat-value">Benefit</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("Tabel Kriteria dan Bobot")

    st.dataframe(
        data_kriteria,
        use_container_width=True,
        hide_index=True
    )

    st.success("Total bobot kriteria adalah 100%.")

    st.divider()

    st.subheader("Grafik Bobot Kriteria")

    grafik_bobot = data_kriteria.set_index("Kode")[["Bobot"]]

    st.bar_chart(
        grafik_bobot,
        horizontal=True,
        color="#20B8C5"
    )

    st.divider()

    st.subheader("Keterangan Kriteria")

    for _, row in data_kriteria.iterrows():
        with st.expander(
            f"{row['Kode']} - {row['Nama Kriteria']}"
        ):
            st.write(f"**Bobot:** {row['Bobot']}%")
            st.write(f"**Jenis:** {row['Jenis']}")

    st.caption(
        "Sumber: Tantowi dan Inalawie (2025), Tabel 1, halaman 86."
    )

# ==========================================
# PENILAIAN KANDIDAT
# ==========================================

elif menu == "Penilaian":

    st.markdown(
        '<div class="main-title">Penilaian Kandidat</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Data penilaian lima kandidat berdasarkan jurnal tahun 2025'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("Skala Penilaian")

    st.dataframe(
        data_skala,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Sumber: Tantowi dan Inalawie (2025), Tabel 2, halaman 86."
    )

    st.divider()

    st.subheader("Matriks Penilaian Kandidat")

    st.dataframe(
        data_penilaian,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Sumber: Tantowi dan Inalawie (2025), Tabel 3, halaman 87."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Jumlah Kandidat</div>
            <div class="stat-value">5</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Jumlah Kriteria</div>
            <div class="stat-value">5</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    if st.button(
        "Simpan Data Penilaian",
        use_container_width=True
    ):

        data_penilaian.to_csv(
            FILE_PENILAIAN,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("Data penilaian jurnal berhasil disimpan.")

# ==========================================
# PERHITUNGAN SAW
# ==========================================

elif menu == "Perhitungan SAW":

    st.markdown(
        '<div class="main-title">Perhitungan SAW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Proses normalisasi dan perhitungan nilai preferensi'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # RUMUS SAW

    st.subheader("Tahapan Perhitungan")

    st.info(
        "Karena seluruh kriteria merupakan benefit, "
        "normalisasi dilakukan dengan membagi nilai setiap "
        "alternatif dengan nilai maksimum pada kriterianya."
    )

    st.latex(r"R_{ij} = \frac{X_{ij}}{\max(X_{ij})}")

    st.write(
        "Nilai preferensi dihitung dengan menjumlahkan "
        "hasil perkalian nilai normalisasi dan bobot kriteria."
    )

    st.latex(r"V_i = \sum_{j=1}^{n} W_j R_{ij}")

    st.divider()

    # LANGKAH 1

    st.subheader("1. Matriks Keputusan (X)")

    st.write(
        "Matriks keputusan diperoleh dari data penilaian "
        "lima kandidat terhadap lima kriteria."
    )

    matriks_tampil = matriks_x.copy()

    matriks_tampil.index = data_penilaian["Nama Kandidat"]

    matriks_tampil.columns = [
        "K1",
        "K2",
        "K3",
        "K4",
        "K5"
    ]

    st.dataframe(
        matriks_tampil,
        use_container_width=True
    )

    st.caption(
        "Sumber data: Tantowi dan Inalawie (2025), Tabel 3, halaman 87."
    )

    st.divider()

    # LANGKAH 2

    st.subheader("2. Nilai Maksimum Setiap Kriteria")

    data_maksimum = pd.DataFrame({
        "Kode Kriteria": ["K1", "K2", "K3", "K4", "K5"],
        "Nama Kriteria": [
            "Wawancara",
            "Uji Kompetensi",
            "Nilai Akademik",
            "Pengalaman Bekerja",
            "Kepribadian"
        ],
        "Nilai Maksimum": nilai_maksimum.values
    })

    st.dataframe(
        data_maksimum,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # LANGKAH 3

    st.subheader("3. Normalisasi Matriks (R)")

    st.write(
        "Setiap nilai pada matriks keputusan dibagi dengan "
        "nilai maksimum dari kriteria yang sama."
    )

    matriks_normalisasi = matriks_r.copy()

    matriks_normalisasi.index = data_penilaian["Nama Kandidat"]

    matriks_normalisasi.columns = [
        "K1",
        "K2",
        "K3",
        "K4",
        "K5"
    ]

    st.dataframe(
        matriks_normalisasi.style.format("{:.2f}"),
        use_container_width=True
    )

    st.caption(
        "Hasil normalisasi mengikuti Tabel 4 jurnal, halaman 88."
    )

    st.divider()

    # LANGKAH 4

    st.subheader("4. Perhitungan Nilai Preferensi (V)")

    st.write("Bobot yang digunakan dalam perhitungan:")

    data_bobot = pd.DataFrame({
        "Kriteria": ["K1", "K2", "K3", "K4", "K5"],
        "Bobot": [15, 30, 15, 10, 30],
        "Bobot Desimal": bobot
    })

    st.dataframe(
        data_bobot,
        use_container_width=True,
        hide_index=True
    )

    st.write("Hasil perkalian normalisasi dengan bobot:")

    matriks_terbobot = matriks_r.mul(bobot, axis=1)

    matriks_terbobot.index = data_penilaian["Nama Kandidat"]

    matriks_terbobot.columns = [
        "K1",
        "K2",
        "K3",
        "K4",
        "K5"
    ]

    st.dataframe(
        matriks_terbobot.style.format("{:.4f}"),
        use_container_width=True
    )

    st.divider()

    st.subheader("5. Hasil Nilai Preferensi")

    hasil_tampil = hasil_saw.copy()

    hasil_tampil["Nilai Preferensi"] = (
        hasil_tampil["Nilai Preferensi"].round(3)
    )

    st.dataframe(
        hasil_tampil,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "Perhitungan SAW berhasil dilakukan berdasarkan "
        "data alternatif dan bobot pada jurnal."
    )

    st.caption(
        "Sumber: Tantowi dan Inalawie (2025), "
        "perhitungan manual halaman 87–89."
    )


# ==========================================
# HASIL PERANGKINGAN
# ==========================================

elif menu == "Hasil Perangkingan":

    st.markdown(
        '<div class="main-title">Hasil Perangkingan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Hasil akhir seleksi penerimaan karyawan menggunakan metode SAW'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # ======================================
    # URUTKAN HASIL NILAI PREFERENSI
    # ======================================

    hasil_ranking = hasil_saw.copy()

    hasil_ranking = hasil_ranking.sort_values(
        by="Nilai Preferensi",
        ascending=False
    ).reset_index(drop=True)

    hasil_ranking.insert(
        0,
        "Peringkat",
        range(1, len(hasil_ranking) + 1)
    )

    hasil_ranking["Nilai Preferensi"] = (
        hasil_ranking["Nilai Preferensi"].round(3)
    )

    # ======================================
    # KANDIDAT TERBAIK
    # ======================================

    kandidat_terbaik = hasil_ranking.iloc[0]

    st.subheader("Kandidat dengan Nilai Tertinggi")

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Peringkat 1 - Kandidat Terbaik</div>
        <div class="stat-value">
            {kandidat_terbaik['Nama Kandidat']}
        </div>
        <div class="stat-label">
            Nilai Preferensi:
            <b>{kandidat_terbaik['Nilai Preferensi']:.3f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ======================================
    # STATISTIK PERANGKINGAN
    # ======================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Jumlah Kandidat</div>
            <div class="stat-value">{len(hasil_ranking)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Nilai Tertinggi</div>
            <div class="stat-value">
                {hasil_ranking['Nilai Preferensi'].max():.3f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Nilai Terendah</div>
            <div class="stat-value">
                {hasil_ranking['Nilai Preferensi'].min():.3f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ======================================
    # TABEL HASIL PERANGKINGAN
    # ======================================

    st.subheader("Tabel Hasil Perangkingan")

    st.dataframe(
        hasil_ranking,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Peringkat": st.column_config.NumberColumn(
                "Peringkat",
                format="%d"
            ),
            "Nomor Peserta": st.column_config.TextColumn(
                "Nomor Peserta"
            ),
            "Nama Kandidat": st.column_config.TextColumn(
                "Nama Kandidat"
            ),
            "Nilai Preferensi": st.column_config.NumberColumn(
                "Nilai Preferensi",
                format="%.3f"
            )
        }
    )

    st.divider()

    # ======================================
    # GRAFIK PERBANDINGAN
    # ======================================

    st.subheader("Grafik Perbandingan Nilai SAW")

    grafik_ranking = hasil_ranking.set_index(
        "Nama Kandidat"
    )[["Nilai Preferensi"]]

    st.bar_chart(
        grafik_ranking,
        horizontal=True,
        color="#20B8C5"
    )

    st.divider()

    # ======================================
    # KESIMPULAN
    # ======================================

    st.subheader("Kesimpulan Hasil")

    st.write(
        f"Berdasarkan hasil perhitungan metode "
        f"Simple Additive Weighting (SAW), "
        f"{kandidat_terbaik['Nama Kandidat']} memperoleh "
        f"nilai preferensi tertinggi sebesar "
        f"{kandidat_terbaik['Nilai Preferensi']:.3f} "
        f"dan menempati peringkat pertama."
    )

    st.info(
        "Semakin tinggi nilai preferensi, semakin tinggi "
        "peringkat kandidat dalam hasil perhitungan SAW."
    )

    st.caption(
        "Hasil perangkingan dihitung otomatis berdasarkan "
        "nilai preferensi dari halaman Perhitungan SAW."
    )

    st.divider()

    # ======================================
    # UNDUH HASIL
    # ======================================

    st.subheader("Unduh Hasil Perangkingan")

    csv_ranking = hasil_ranking.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Hasil Perangkingan (CSV)",
        data=csv_ranking,
        file_name="hasil_perangkingan_saw.csv",
        mime="text/csv",
        use_container_width=True
    )

