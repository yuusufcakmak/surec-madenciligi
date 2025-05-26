# Süreç Madenciliği Projesi

Bu proje, bir .CSV dosyasından süreç verilerini okuyarak temel analizleri yapabilen ve kullanıcıya sunabilen basitleştirilmiş bir süreç madenciliği uygulamasıdır.

Uygulamanın iki farklı kullanım şekli vardır:
1.  Konsol Tabanlı Analiz Aracı
2.  Web Tabanlı Kullanıcı Arayüzü (Streamlit ile)

## 1. Konsol Tabanlı Analiz Aracı

### Kurulum ve Çalıştırma
1.  Projeyi klonlayın veya indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install pandas matplotlib graphviz
    ```
    *Not: `graphviz` Python kütüphanesinin çalışabilmesi için sisteminizde Graphviz yazılımının da kurulu olması ve PATH ortam değişkenine eklenmiş olması gerekebilir. Kurulum detayları için: https://graphviz.org/download/*
3.  `process_miner.py` betiğini çalıştırın:
    ```bash
    python process_miner.py
    ```
4.  Program sizden bir .CSV dosyasının yolunu girmenizi isteyecektir.
5.  Analiz sonuçları konsolda gösterilecek ve aşağıdaki grafik dosyaları projenizin ana dizinine kaydedilecektir:
    *   `activity_frequencies.png` (Adım frekansları bar grafiği)
    *   `process_flow.png` (Basit süreç akış diyagramı)

## 2. Web Tabanlı Kullanıcı Arayüzü (Streamlit)

### Kurulum ve Çalıştırma
1.  Projeyi klonlayın veya indirin.
2.  Gerekli tüm kütüphaneleri yükleyin (konsol aracı için gerekenlere ek olarak `streamlit`):
    ```bash
    pip install pandas matplotlib graphviz streamlit
    ```
    *Graphviz kurulum notu yukarıdaki bölümle aynıdır.*
3.  Streamlit uygulamasını çalıştırın:
    ```bash
    streamlit run app.py
    ```
4.  Web tarayıcınızda açılan arayüz üzerinden bir .CSV dosyası yükleyin.
5.  Analiz sonuçları ve görseller web sayfasında görüntülenecektir. Grafikler ayrıca `streamlit_outputs` adlı bir klasöre kaydedilecektir.

## .CSV Dosya Formatı

Kullanılacak .CSV dosyası minimum aşağıdaki sütunları içermelidir:
*   `Case ID`
*   `Activity Name`
*   `Start Time`
*   `End Time`

Tarih/saat sütunları (`Start Time`, `End Time`) pandas tarafından okunabilir formatta olmalıdır (örn: `YYYY-MM-DD HH:MM:SS`). 