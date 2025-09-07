import sys
import subprocess 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tiện Ích Ô Tô")
        self.setGeometry(400, 200, 500, 300)  # (x, y, width, height)

        # Tiêu đề
        self.title_label = QLabel("Tùy Chọn Tiện Ích", self)
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setStyleSheet("color: #2E86C1; margin-bottom: 20px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Nút phát hiện buồn ngủ
        self.btn_drowsiness = QPushButton("🚗 Phát hiện buồn ngủ")
        self.btn_drowsiness.setFont(QFont("Arial", 12))
        self.btn_drowsiness.setStyleSheet("background-color: #27AE60; color: white; padding: 10px; border-radius: 8px;")

        # Nút xem thời tiết
        self.btn_weather = QPushButton("🌦 Xem thời tiết")
        self.btn_weather.setFont(QFont("Arial", 12))
        self.btn_weather.setStyleSheet("background-color: #2980B9; color: white; padding: 10px; border-radius: 8px;")

        # Layout dọc
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.btn_drowsiness)
        layout.addWidget(self.btn_weather)

        # Widget chính
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Gắn sự kiện
        self.btn_drowsiness.clicked.connect(self.open_drowsiness)
        self.btn_weather.clicked.connect(self.open_weather)

    def open_drowsiness(self):
        print("👉 Mở chức năng phát hiện buồn ngủ.")
        subprocess.Popen(["python", "driving_sleep/core/drowsiness_yawn.py", "--webcam", "0"])

    def open_weather(self):
        print("👉 Mở chức năng xem thời tiết.")
        subprocess.Popen(["python", "weathers/weather_gui.py"])

  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
