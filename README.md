# YOLOv8 ve PyQt5 İle Nesne Tespiti Masaüstü Uygulaması

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple?style=for-the-badge&logo=yolo)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?style=for-the-badge&logo=qt)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv)

## 📖 Proje Hakkında
Bu proje, **YOLOv8 (You Only Look Once)** derin öğrenme modelini kullanıcı dostu bir arayüzle buluşturan gelişmiş bir masaüstü uygulamasıdır.

Kullanıcılar, Python ve PyQt5 ile geliştirilen bu arayüz üzerinden hem **fotoğraf** hem de **video** dosyaları üzerinde yüksek doğrulukla nesne tespiti yapabilirler. Proje, karmaşık kod yapılarıyla uğraşmadan, eğitilmiş bir yapay zeka modelini günlük hayatta kullanılabilir hale getirmeyi amaçlar.

---

## 📱 Uygulama Özellikleri

Uygulama, kullanıcılara esnek test imkanları sunmaktadır:

### 📸 1. Resim ile Tespit
* **Galeriden Seçim:** Bilgisayarınızdaki klasörlerden `.jpg`, `.png`, `.jpeg` formatındaki görselleri kolayca yükleyebilirsiniz.
* **Anlık Analiz:** Seçilen fotoğraf saniyeler içinde analiz edilir ve tespit edilen nesneler kutucuklar (Bounding Box) ile işaretlenir.

### 🎥 2. Video ile Tespit (Yeni!)
* **Video Desteği:** Galerinizdeki `.mp4`, `.avi` formatındaki video dosyalarını yükleyerek hareketli görüntüler üzerinde test yapabilirsiniz.
* **Kare Kare Analiz:** Uygulama, videoyu kare kare (frame by frame) işleyerek nesneleri takip eder ve sonuçları gerçek zamanlı olarak ekrana yansıtır.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Gereksinimleri Yükleyin
Terminal veya Komut İstemi'ni (CMD) açarak gerekli kütüphaneleri yükleyin:
```bash
pip install ultralytics PyQt5 opencv-python
(Mac kullanıcıları için pip3 kullanılabilir.)
### 2. Projeyi İndirin
Repoyu klonlayın veya zip olarak indirip klasöre çıkartın. Önemli: Klasör yapısının şu şekilde olduğundan emin olun:

gui_app.py (Ana uygulama kodu)

best.pt (Eğitilmiş YOLO modeli - Bu dosya kod ile aynı dizinde olmalıdır)

3. Uygulamayı Başlatın
Terminali açın, proje klasörünün içine girin ve uygulamayı çalıştırın:

Bash

cd proje_klasorunuz
python gui_app.py
Mac Kullanıcıları İçin Not: Eğer python komutu hata verirse lütfen şu şekilde deneyin:

Bash

python3 gui_app.py
