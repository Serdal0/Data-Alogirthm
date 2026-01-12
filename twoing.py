def twoing_deger_hesapla(sol_toplam, sag_toplam):
    """
    Twoing kriteri ile bölünme kalitesini hesaplar.
    İkili bölünmeler için optimize edilmiş bir ölçüttür.
    
    Formül: (P_L * P_R / 4) * [Σ|L_i/L - R_i/R|]^2
    
    Parametreler:
    - sol_toplam: Sol grubun sınıf dağılımı
    - sag_toplam: Sağ grubun sınıf dağılımı
    
    Dönüş:
    - twoing_deger: Twoing skoru (yüksek = iyi bölünme)
    """
    so = sum(sol_toplam)  # Sol toplam
    sa = sum(sag_toplam)  # Sağ toplam
    
    if so == 0 or sa == 0:
        return 0
    
    total = so + sa
    p_so = so / total  # Sol grubun oranı
    p_sa = sa / total  # Sağ grubun oranı
    
    # Sınıf dağılımları arasındaki farkı hesapla
    top_dif = 0
    for i in range(len(sol_toplam)):
        sol_oran = sol_toplam[i] / so
        sag_oran = sag_toplam[i] / sa
        top_dif += abs(sol_oran - sag_oran)
    
    # Twoing formülü
    twoing_deger = (p_so * p_sa / 4) * (top_dif ** 2)
    
    return twoing_deger


# TWOING ÖRNEK KULLANIM
print("\n" + "=" * 60)
print("TWOING KRİTERİ ALGORİTMASI")
print("=" * 60)

# Örnek bölünmeler
print("\n--- Örnek 1: İyi Bölünme ---")
sol1 = [8, 2]  # Sol grup: Çoğunlukla sınıf 1
sag1 = [2, 8]  # Sağ grup: Çoğunlukla sınıf 2
skor1 = twoing_deger_hesapla(sol1, sag1)
print(f"Sol: {sol1}, Sağ: {sag1}")
print(f"Twoing Skoru: {skor1:.4f}")
print("Yorum: Yüksek skor - İyi ayırt edici bölünme")

print("\n--- Örnek 2: Mükemmel Bölünme ---")
sol2 = [10, 0]  # Sol grup: Sadece sınıf 1
sag2 = [0, 10]  # Sağ grup: Sadece sınıf 2
skor2 = twoing_deger_hesapla(sol2, sag2)
print(f"Sol: {sol2}, Sağ: {sag2}")
print(f"Twoing Skoru: {skor2:.4f}")
print("Yorum: Maksimum skor - Mükemmel bölünme")

print("\n--- Örnek 3: Zayıf Bölünme ---")
sol3 = [5, 5]  # Sol grup: Dengeli
sag3 = [5, 5]  # Sağ grup: Dengeli
skor3 = twoing_deger_hesapla(sol3, sag3)
print(f"Sol: {sol3}, Sağ: {sag3}")
print(f"Twoing Skoru: {skor3:.4f}")
print("Yorum: Düşük skor - Zayıf ayırt edicilik")

print("\n--- Örnek 4: Orta Bölünme ---")
sol4 = [7, 3]  # Sol grup: Çoğunlukla sınıf 1
sag4 = [3, 7]  # Sağ grup: Çoğunlukla sınıf 2
skor4 = twoing_deger_hesapla(sol4, sag4)
print(f"Sol: {sol4}, Sağ: {sag4}")
print(f"Twoing Skoru: {skor4:.4f}")
print("Yorum: Orta skor - Kabul edilebilir bölünme")

print("\n" + "=" * 60)
print("TÜM ALGORİTMALAR BAŞARIYLA ÇALIŞTIRILDI!")
print("=" * 60)