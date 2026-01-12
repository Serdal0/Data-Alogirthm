import math
import random
def oklid_uzakligi(p1, p2):
    """İki nokta arasındaki Öklid uzaklığını hesaplar."""
    toplam = 0
    for i in range(len(p1)):
        toplam += (p1[i] - p2[i]) ** 2
    return math.sqrt(toplam)


def k_means(veriler, k=2, iterasyon=10):
    """
    K-Means kümeleme algoritması.
    
    Parametreler:
    - veriler: Kümelenecek veri noktaları
    - k: Küme sayısı
    - iterasyon: Maksimum iterasyon sayısı
    
    Dönüş:
    - kumeler: Her kümedeki noktalar
    - merkezler: Her kümenin merkezi
    """
    # Rastgele başlangıç merkezleri seç
    merkezler = random.sample(veriler, k)
    
    for tur in range(iterasyon):
        # Her küme için boş liste oluştur
        kumeler = [[] for _ in range(k)]
        
        # Her noktayı en yakın merkeze ata
        for nokta in veriler:
            mesafeler = [oklid_uzakligi(nokta, merkez) for merkez in merkezler]
            en_yakin_index = mesafeler.index(min(mesafeler))
            kumeler[en_yakin_index].append(nokta)
        
        # Yeni merkezleri hesapla
        yeni_merkezler = []
        for i in range(k):
            if not kumeler[i]:  # Eğer küme boşsa
                yeni_merkezler.append(merkezler[i])
                continue
            
            # Her boyut için ortalama al
            boyut_sayisi = len(veriler[0])
            yeni_merkez = []
            for j in range(boyut_sayisi):
                boyut_toplami = sum(nokta[j] for nokta in kumeler[i])
                yeni_merkez.append(round(boyut_toplami / len(kumeler[i]), 2))
            yeni_merkezler.append(yeni_merkez)
        
        merkezler = yeni_merkezler
        print(f"Tur {tur+1}: Merkezler güncellendi - {merkezler}")
    
    return kumeler, merkezler


# K-MEANS ÖRNEK KULLANIM
print("\n" + "=" * 60)
print("K-MEANS ALGORİTMASI")
print("=" * 60)

veriler = [
    [190, 95], [195, 100], [185, 90],  # Basketbolcu grubu
    [160, 50], [165, 55], [158, 48],   # Jokey grubu
    [170, 70], [172, 72]               # Futbolcu grubu
]

k_kume = 3
iterasyon_sayisi = 10

print(f"\nVeri Sayısı: {len(veriler)}")
print(f"Küme Sayısı (K): {k_kume}")
print(f"İterasyon Sayısı: {iterasyon_sayisi}\n")

son_kumeler, son_merkezler = k_means(veriler, k=k_kume, iterasyon=iterasyon_sayisi)

print("\n--- K-Means Sonuçları ---")
for i, (kume, merkez) in enumerate(zip(son_kumeler, son_merkezler), 1):
    print(f"\nKüme {i}:")
    print(f"  Merkez: {merkez}")
    print(f"  Eleman Sayısı: {len(kume)}")
    print(f"  Elemanlar: {kume}")