# 🛠️ Süreç Madenciliği Projesi

Bu proje, bir `.CSV` dosyasından süreç verilerini okuyarak temel süreç madenciliği analizlerini gerçekleştiren ve analiz sonuçlarını hem **konsol üzerinden** hem de **web tabanlı arayüzle (Streamlit)** kullanıcıya sunan bir uygulamadır.

---

## 🚀 Özellikler

* 📈 Aktivite frekanslarını analiz eder.
* 🔄 Süreç akış diyagramı oluşturur.
* ⏱ Ortalama işlem sürelerini ve geçişleri hesaplar.
* 🌐 Hem terminal hem de web arayüzü ile çalışır.

---

## 🧰 Kullanım Şekilleri

### 1⃣ Konsol Tabanlı Analiz Aracı

#### 🔧 Kurulum

```bash
pip install pandas matplotlib graphviz
```

📌 *Not: `graphviz` kütüphanesi için sisteminize Graphviz yazılımını da yüklemeniz gerekebilir.*
👉 Kurulum için: [Graphviz Download](https://graphviz.org/download/)

#### ▶️ Çalıştırma

```bash
python process_miner.py
```

Ardından .CSV dosya yolunu girmeniz istenecek. Analiz sonrası:

* `activity_frequencies.png` — Aktivite frekanslarını gösterir.
* `process_flow.png` — Süreç akışını görselleştirir.

---

### 2⃣ Web Tabanlı Arayüz (Streamlit ile)

#### 🔧 Kurulum

```bash
pip install pandas matplotlib graphviz streamlit
```

#### ▶️ Çalıştırma

```bash
streamlit run app.py
```

Tarayıcınızda açılan arayüz üzerinden .CSV dosyasını yükleyerek aşağıdaki analizleri görebilirsiniz:

* Aktivite frekans grafiği
* Süreç akış diyagramı
* Ortalama tamamlanma süresi
* En sık geçiş yapan adımlar

📁 Tüm grafikler `streamlit_outputs` klasörünüze de kaydedilecektir.

---

## 📄 Gerekli .CSV Formatı

Aşağıdaki başlıklara sahip olmalıdır:

| Sütun Adı       | Açıklama                                           |
| --------------- | -------------------------------------------------- |
| `Case ID`       | Sürece ait vaka/örnek numarası                     |
| `Activity Name` | Gerçekleşen adım/aktivite ismi                     |
| `Start Time`    | Aktivitenin başlama zamanı (`YYYY-MM-DD HH:MM:SS`) |
| `End Time`      | Aktivitenin bitiş zamanı                           |

---

## 🖼️ Uygulama Görselleri

### Streamlit Ana Sayfa

<img src="https://github.com/user-attachments/assets/ecc2e967-3eb3-4cc5-8f67-d36185dcc23e" width="600" alt="Streamlit Arayüzü - Giriş" />

### Aktivite Frekans Grafiği

<img src="https://github.com/user-attachments/assets/ddec0746-4678-4df5-98f3-716dab78269f" width="600" alt="Aktivite Frekansları" />

### Süreç Akış Diyagramı

<img src="https://github.com/user-attachments/assets/e723f035-bd41-4f3e-a9f0-7d3182fef9e6" width="600" alt="Süreç Akışı" />

---


