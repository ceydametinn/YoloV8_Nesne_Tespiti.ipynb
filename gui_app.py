import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO

class NesneTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 Proje - Resim, Video ve Kamera")
        self.setGeometry(100, 100, 1200, 800)
        
        # --- MODELİ YÜKLE ---
        try:
            # best.pt dosyası bu kodla aynı klasörde olmalı
            self.model = YOLO("best.pt")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Model yüklenirken hata oluştu:\n{e}\n\nLütfen 'best.pt' dosyasının bu kodla yan yana olduğundan emin olun.")

        # Değişkenler
        self.cap = None  # Video/Kamera yakalayıcı
        self.timer = QTimer() # Zamanlayıcı (Kareleri yenilemek için)
        self.timer.timeout.connect(self.goruntuyu_guncelle)
        self.secilen_resim_yolu = None
        
        self.initUI()

    def initUI(self):
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        ana_layout = QVBoxLayout()

        # Başlık
        baslik = QLabel("Düğme ve İplik Tespiti")
        baslik.setFont(QFont("Arial", 18, QFont.Bold))
        baslik.setAlignment(Qt.AlignCenter)
        ana_layout.addWidget(baslik)

        # Görüntü Panelleri (Yan Yana)
        resim_layout = QHBoxLayout()
        
        # Sol Panel (Orijinal / Kaynak)
        self.label_orijinal = QLabel("Kaynak Görüntü")
        self.label_orijinal.setFixedSize(550, 450)
        self.label_orijinal.setStyleSheet("border: 2px solid black; background-color: #ddd;")
        self.label_orijinal.setAlignment(Qt.AlignCenter)
        
        # Sağ Panel (Tespit Sonucu)
        self.label_sonuc = QLabel("Tespit Sonucu")
        self.label_sonuc.setFixedSize(550, 450)
        self.label_sonuc.setStyleSheet("border: 2px solid green; background-color: #ddd;")
        self.label_sonuc.setAlignment(Qt.AlignCenter)

        resim_layout.addWidget(self.label_orijinal)
        resim_layout.addWidget(self.label_sonuc)
        ana_layout.addLayout(resim_layout)

        # Bilgi Ekranı
        self.bilgi_kutusu = QLabel("Hazır...")
        self.bilgi_kutusu.setFont(QFont("Arial", 11))
        self.bilgi_kutusu.setStyleSheet("color: blue;")
        self.bilgi_kutusu.setAlignment(Qt.AlignCenter)
        ana_layout.addWidget(self.bilgi_kutusu)

        # --- BUTONLAR ---
        # 1. Satır: Resim İşlemleri
        btn_layout1 = QHBoxLayout()
        self.btn_resim_sec = QPushButton("1. Resim Seç")
        self.btn_resim_sec.clicked.connect(self.resim_sec)
        
        self.btn_resim_test = QPushButton("2. Resmi Test Et")
        self.btn_resim_test.clicked.connect(self.resim_test_et)
        self.btn_resim_test.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;") # Yeşil

        btn_layout1.addWidget(self.btn_resim_sec)
        btn_layout1.addWidget(self.btn_resim_test)

        # 2. Satır: Video ve Kamera İşlemleri (EKSTRA PUAN KISMI)
        btn_layout2 = QHBoxLayout()
        self.btn_video_sec = QPushButton("Video Seç ve Oynat")
        self.btn_video_sec.clicked.connect(self.video_sec_ve_baslat)
        
        self.btn_kamera = QPushButton("Canlı Kamera Aç")
        self.btn_kamera.clicked.connect(self.kamera_ac)
        self.btn_kamera.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;") # Mavi

        self.btn_durdur = QPushButton("DURDUR")
        self.btn_durdur.clicked.connect(self.durdur)
        self.btn_durdur.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;") # Kırmızı

        btn_layout2.addWidget(self.btn_video_sec)
        btn_layout2.addWidget(self.btn_kamera)
        btn_layout2.addWidget(self.btn_durdur)

        ana_layout.addLayout(btn_layout1)
        ana_layout.addLayout(btn_layout2)
        ana_widget.setLayout(ana_layout)

    # --- RESİM FONKSİYONLARI ---
    def resim_sec(self):
        self.durdur() # Varsa videoyu durdur
        dosya, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resimler (*.jpg *.jpeg *.png)")
        if dosya:
            self.secilen_resim_yolu = dosya
            pixmap = QPixmap(dosya).scaled(550, 450, Qt.KeepAspectRatio)
            self.label_orijinal.setPixmap(pixmap)
            self.label_sonuc.clear()
            self.label_sonuc.setText("Test Et butonuna basınız...")
            self.bilgi_kutusu.setText(f"Seçilen Resim: {dosya}")

    def resim_test_et(self):
        if not self.secilen_resim_yolu:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        self.bilgi_kutusu.setText("İşleniyor...")
        # Model tahmini
        results = self.model(self.secilen_resim_yolu)
        
        # Sonuç görselini al
        annotated_frame = results[0].plot() 
        
        # Görüntüyü PyQt formatına çevir ve göster
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        img = self.convert_cv_qt(annotated_frame)
        self.label_sonuc.setPixmap(img)
        
        # Sayım yap ve yazdır
        self.sayim_yap(results[0])

    # --- VİDEO ve KAMERA FONKSİYONLARI ---
    def video_sec_ve_baslat(self):
        self.durdur()
        dosya, _ = QFileDialog.getOpenFileName(self, "Video Seç", "", "Videolar (*.mp4 *.avi *.mov)")
        if dosya:
            self.cap = cv2.VideoCapture(dosya)
            self.timer.start(30) # Her 30 milisaniyede bir kareyi güncelle
            self.bilgi_kutusu.setText("Video oynatılıyor...")

    def kamera_ac(self):
        self.durdur()
        self.cap = cv2.VideoCapture(0) # 0 = Bilgisayarın Webcam'i
        if not self.cap.isOpened():
             QMessageBox.warning(self, "Hata", "Kamera açılamadı! Başka bir program kullanıyor olabilir.")
             return
        self.timer.start(30)
        self.bilgi_kutusu.setText("Canlı kamera başlatıldı...")

    def goruntuyu_guncelle(self):
        # Bu fonksiyon video/kamera açıkken sürekli çalışır
        ret, frame = self.cap.read()
        if ret:
            # 1. Orijinal kareyi sol panele bas
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.label_orijinal.setPixmap(self.convert_cv_qt(frame_rgb))
            
            # 2. Model ile tahmin yap
            results = self.model(frame, verbose=False) # verbose=False logları temiz tutar
            annotated_frame = results[0].plot()
            
            # 3. Sonucu sağ panele bas
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            self.label_sonuc.setPixmap(self.convert_cv_qt(annotated_frame))
            
            # (İsteğe bağlı) Canlı sayım yapmak için aşağıdaki satırı açabilirsin ama videoyu yavaşlatabilir.
            # self.sayim_yap(results[0]) 
        else:
            self.durdur()

    def durdur(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.label_orijinal.setText("Durduruldu")
        self.bilgi_kutusu.setText("İşlem durduruldu.")

    def convert_cv_qt(self, cv_img):
        # OpenCV görüntüsünü PyQt görüntüsüne çevirir
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        to_qt = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(to_qt).scaled(550, 450, Qt.KeepAspectRatio)

    def sayim_yap(self, result):
        names = result.names
        classes = result.boxes.cls.cpu().numpy()
        counts = {}
        for cls in classes:
            name = names[int(cls)]
            counts[name] = counts.get(name, 0) + 1
        
        if not counts:
            text = "Herhangi bir nesne tespit edilemedi."
        else:
            text = " | ".join([f"{k}: {v} adet" for k, v in counts.items()])
        
        self.bilgi_kutusu.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = NesneTespitUygulamasi()
    pencere.show()
    sys.exit(app.exec_())