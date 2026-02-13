# 🎙️ TTS-Arena: Ses Modelleri Kıyaslama Arenası

<div align="center">
    
![Project Status](https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge) 
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white) 
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch&logoColor=white) 
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Transformers-yellow?style=for-the-badge) 
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

</div>

---

## 🚀 Proje Özeti

**TTS-Arena**, Türkçe dil desteğine odaklanan, açık kaynaklı Metinden Sese modellerini endüstriyel standartlarda kıyaslamak için geliştirilmiş ileri seviye bir yapay zeka arenasıdır. Proje, özellikle kurumsal terminoloji ve karmaşık dil yapıları üzerinde yüksek doğruluklu ses sentezi sağlamak amacıyla modüler bir mimari ile tasarlanmıştır.

### 🌟 Temel Özellikler

* **Modüler Model Orkestrasyonu:** Yeni modellerin sisteme zahmetsizce entegre edilmesini sağlayan `Handler` ve `Service` yapısı.
* **Gelişmiş Metin Normalizasyonu:** Türkçe fonetik kuralları, sayısal değerler ve kısaltmalar üzerinde ileri seviye ön işleme.
* **Dinamik Tensör Yönetimi:** Sinirsel ağlardaki maskeleme ve boyut hatalarını çekirdek seviyesinde çözen hata bastırma mekanizması.
* **İnteraktif Analiz Paneli:** Sadece tek bir modeli değil birden fazla modeli aynı anda test etme kabileyeti.

---

## 🛠️ Sistem Mimarisi

TTS-Arena, metin girişinden ses dalgasına kadar uçtan uca yüksek performanslı bir boru hattı sunar.

### 1. Veri ve İşlem Akışı

```mermaid
graph TD
    subgraph "Metin İşleme Katmanı"
        A[Ham Metin] -->|Normalizasyon| B(Türkçe Dil İşleme)
        B -->|Fonetik Analiz| C{IPA Mapping}
    end

    subgraph "Sinirsel Çıkarım (Inference)"
        C -->|Vektör Girişi| D[AutoTTSHandler]
        D -->|Tensor Masking| E[Neural Model Core]
        E -->|Raw Waveform| F[Vocoder / Post-Process]
    end

    subgraph "Servis Katmanı"
        F --> G[FastAPI Endpoint]
        G --> H[Streamlit UI]
    end

```

---


### 🐳 Docker ile Hızlı Kurulum

Projeyi izole ve optimize edilmiş bir konteyner ortamında başlatmak için:

```bash
docker-compose build --parallel
docker-compose up -d

```

## 🤝 İletişim

Sistem mimarisi veya model entegrasyonu ile ilgili sorularınız için GitHub Issues üzerinden iletişime geçebilirsiniz.

---

<div align="center">
<sub>Türkçe Ses Teknolojilerinin Geleceği İçin Geliştirildi. ❤️</sub>
</div>

---
