import sys
import subprocess
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiện Ích Ô Tô")
        self.setGeometry(400, 200, 500, 300)

        self.title_label = QLabel("Tùy Chọn Tiện Ích", self)
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.btn_drowsiness = QPushButton("🚗 Phát hiện buồn ngủ")
        self.btn_weather = QPushButton("🌦 Xem thời tiết")

        for b, color in [(self.btn_drowsiness, "#27AE60"), (self.btn_weather, "#2980B9")]:
            b.setFont(QFont("Arial", 12))
            b.setStyleSheet(f"background-color:{color}; color:white; padding:10px; border-radius:8px;")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.btn_drowsiness)
        layout.addWidget(self.btn_weather)

        container = QWidget(); container.setLayout(layout)
        self.setCentralWidget(container)

        # Gốc dự án: .../DETECT-SLEEPINESS  (vì file này nằm trong .../gui)
        self.project_root = Path(__file__).resolve().parents[1]

        self.btn_drowsiness.clicked.connect(self.open_drowsiness)
        self.btn_weather.clicked.connect(self.open_weather)

    def _run(self, args):
        try:
            subprocess.Popen(
                [sys.executable, *args],
                cwd=str(self.project_root),                  # chạy từ gốc dự án
                # creationflags=subprocess.CREATE_NEW_CONSOLE # (tuỳ chọn) mở console riêng trên Windows
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi chạy tiện ích", str(e))

    def open_drowsiness(self):
        # chạy module: sibling folder 'driving_sleep'
        self._run(["-m", "driving_sleep.core.drowsiness_yawn", "--webcam", "0"])

    def open_weather(self):
        # chạy module: sibling folder 'weathers'
        self._run(["-m", "weathers.weather_gui"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
