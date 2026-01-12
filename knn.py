import math
import random

# =========================================================
# 1. KNN (K-EN YAKIN KOMŞU) ALGORİTMASI
# =========================================================

def oklid_mesafesi(nokta1, nokta2):
    """
    İki nokta arasındaki Öklid mesafesini hesaplar.
    Formül: sqrt((x2-x1)^2 + (y2-y1)^2 + ... + (yn-yn)^2)
    """
    toplam = 0
    for i in range(len(nokta1)):
        toplam += (nokta1[i] - nokta2[i]) ** 2
    return math.sqrt(toplam)


def knn_tahmin(egitim_verisi, egitim_etiketleri, yeni_nokta, k=3):
    """
    KNN algoritması ile sınıflandırma yapar.
    
    Parametreler:
    - egitim_verisi: Eğitim veri noktaları listesi
    - egitim_etiketleri: Her veri noktasının sınıf etiketi
    - yeni_nokta: Sınıflandırılacak yeni nokta
    - k: Kaç komşuya bakılacağı
    
    Dönüş:
    - tahmin: Tahmin edilen sınıf
    - en_yakinlar: En yakın k komşu ve mesafeleri
    """
    mesafeler = []
    
    # Her eğitim noktası için mesafe hesapla
    for i in range(len(egitim_verisi)):
        mesafe = oklid_mesafesi(egitim_verisi[i], yeni_nokta)
        mesafeler.append((mesafe, egitim_etiketleri[i]))
    
    # Mesafelere göre sırala (küçükten büyüğe)
    mesafeler.sort()
    
    # En yakın k komşuyu al
    en_yakinlar = mesafeler[:k]
    
    # Oyları topla
    oylar = []
    for mesafe, etiket in en_yakinlar:
        oylar.append(etiket)
    
    # En çok oy alan sınıfı bul
    tahmin = max(set(oylar), key=oylar.count)
    
    return tahmin, en_yakinlar


# KNN ÖRNEK KULLANIM
print("=" * 60)
print("KNN ALGORİTMASI")
print("=" * 60)

# Eğitim verisi: [Boy, Kilo]
ozellikler = [
    [195, 95], [200, 105], [190, 90], [205, 110],  # Basketbolcu
    [160, 50], [162, 52], [158, 48], [165, 54],    # Jokey
    [172, 72], [170, 70], [175, 75], [168, 68]     # Futbolcu
]

etiketler = [
    "Basketbolcu", "Basketbolcu", "Basketbolcu", "Basketbolcu",
    "Jokey", "Jokey", "Jokey", "Jokey",
    "Futbolcu", "Futbolcu", "Futbolcu", "Futbolcu"
]

# Test noktası
yeni_kisi = [170, 65]
k_degeri = 3

# Tahmin yap
sonuc, yakinlar = knn_tahmin(ozellikler, etiketler, yeni_kisi, k=k_degeri)

print(f"\nYeni Kişi: Boy={yeni_kisi[0]} cm, Kilo={yeni_kisi[1]} kg")
print(f"K Değeri: {k_degeri}")
print(f"\nTahmin Edilen Sınıf: {sonuc}")
print(f"\nEn Yakın {k_degeri} Komşu:")
for i, (mesafe, etiket) in enumerate(yakinlar, 1):
    print(f"  {i}. {etiket} - Mesafe: {mesafe:.2f}")
