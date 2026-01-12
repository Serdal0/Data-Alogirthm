def gini_hesapla(grup):
    if len(grup) == 0:
        return 0
    
    toplam_eleman = sum(grup)
    p_kareler_toplami = 0

    for sinif_sayisi in grup:
        oran = sinif_sayisi / toplam_eleman
        p_kareler_toplami += oran **2
    gini = 1- p_kareler_toplami
    return gini

# Weighted Gini
def bolunme_kalitesi(sol, sag):
    toplam_sol = sum(sol)
    toplam_sag = sum(sag)
    toplam_hepsi = toplam_sag + toplam_sol

    gini_sol = gini_hesapla(sol)
    gini_sag = gini_hesapla(sag)

    agirlikli_gini = (toplam_sol / toplam_hepsi) * gini_sol + (toplam_sag / toplam_hepsi) * gini_sag

    return agirlikli_gini

sol_grup = [10,0] # Tam saf
sag_grup = [5,5] # Tam karışık

print(f"sol gini: {gini_hesapla(sol_grup):.4f}")
print(f"sağ grup: {gini_hesapla(sag_grup):.4f}")
print(f"Toplam bölünme kalitesi: {bolunme_kalitesi(sol_grup, sag_grup):.4f}")



