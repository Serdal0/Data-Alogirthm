# Veri Algoritmaları (Data Algorithms)

Bu repository, veri madenciliği ve makine öğrenmesi kapsamında kullanılan temel **sınıflandırma** ve **kümeleme** algoritmalarının Python ile sıfırdan geliştirilmiş implementasyonlarını içermektedir.

Amaç; hazır kütüphaneleri soyut şekilde kullanmak yerine, algoritmaların **çalışma mantığını**, **karar süreçlerini** ve **hesaplama adımlarını** doğrudan kod üzerinden öğrenmektir.

## İçerik

- **KNN (K-Nearest Neighbors)**  
  Mesafeye dayalı bir sınıflandırma algoritması.

- **K-Means**  
  Denetimsiz öğrenme kapsamında kullanılan kümeleme algoritması.

- **Gini Index**  
  Karar ağaçlarında kullanılan saflık (impurity) ölçütü.

- **Twoing Algorithm**  
  Karar ağaçlarında bölme (split) kriteri olarak kullanılan yöntem.

## Dosya Yapısı

```text
.
├── app.py        # Algoritmaların test / çalıştırma dosyası
├── knn.py        # KNN algoritması implementasyonu
├── kmeans.py    # K-Means algoritması implementasyonu
├── gini.py      # Gini Index hesaplamaları
├── twoing.py    # Twoing algoritması
