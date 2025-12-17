def hitung_skor_kesejahteraan(P, M, U, Y, S):
    """
    Menghitung skor kesejahteraan berdasarkan rumus manual.
    
    Args:
        P: Jumlah Penduduk
        M: Penduduk Miskin
        U: Pengangguran
        Y: PDRB Total ADHK
        S: Skor Tingkat Pendidikan (1-4)
    """
    # Menghindari pembagian dengan nol
    if P == 0:
        return 0
        
    pdrb_score = (Y / 1e10) * 4
    edu_score = S * 10
    poverty_impact = (M / P) * 50
    unemployment_impact = (U / P) * 50
    
    skor = pdrb_score + edu_score - poverty_impact - unemployment_impact
    return skor, pdrb_score, edu_score, poverty_impact, unemployment_impact

def tentukan_kategori(skor):
    """Menentukan kategori teks berdasarkan skor."""
    if skor < 20:
        return "Sangat Tidak Sejahtera"
    elif skor < 40:
        return "Tidak Sejahtera"
    elif skor < 60:
        return "Cukup"
    elif skor < 120:
        return "Sejahtera"
    else:
        return "Sangat Sejahtera"

def get_css_class(kategori):
    """Mengembalikan class CSS berdasarkan kategori."""
    if kategori in ["Sejahtera", "Sangat Sejahtera"]:
        return "success"
    elif kategori == "Cukup":
        return "warning"
    else:
        return "danger"
