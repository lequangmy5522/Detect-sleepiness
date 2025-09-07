import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont


API_KEY = "fa86174b884d9604d4b909820a187e30"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🌦 Thời Tiết Hiện Tại")
        self.setGeometry(450, 250, 400, 300)

        # Nhãn tiêu đề
        self.title_label = QLabel("Xem Thời Tiết", self)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #2980B9; margin-bottom: 15px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Ô nhập thành phố
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Nhập tên thành phố (vd: Hanoi)")
        self.city_input.setFont(QFont("Arial", 12))
        self.city_input.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid gray;")

        # Nút xem thời tiết
        self.btn_check = QPushButton("🔍 Xem thời tiết")
        self.btn_check.setFont(QFont("Arial", 12))
        self.btn_check.setStyleSheet("background-color: #27AE60; color: white; padding: 8px; border-radius: 8px;")
        self.btn_check.clicked.connect(self.get_weather)

        # Nhãn hiển thị kết quả
        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("margin-top: 10px; color: #2C3E50;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên thành phố!")
            return

        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"}
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if data["cod"] != 200:
                QMessageBox.critical(self, "Lỗi", f"Không tìm thấy thành phố: {city}")
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            self.result_label.setText(
                f"📍 Thành phố: {city}\n"
                f"🌡 Nhiệt độ: {temp}°C\n"
                f"🤔 Cảm giác như: {feels_like}°C\n"
                f"💧 Độ ẩm: {humidity}%\n"
                f"☁️ Trạng thái: {description.capitalize()}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lấy dữ liệu!\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
