import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtPositioning import QGeoPositionInfoSource

API_KEY = "fa86174b884d9604d4b909820a187e30"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🌦 Thời Tiết Hiện Tại")
        self.setGeometry(450, 250, 460, 420)

        # --- UI header ---
        self.title_label = QLabel("Xem Thời Tiết", self)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #2980B9; margin-bottom: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # -------- A) Tìm theo thành phố --------
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Nhập tên thành phố (vd: Hanoi)")
        self.city_input.setFont(QFont("Arial", 12))
        self.city_input.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid gray;")

        self.btn_check = QPushButton("🔍 Xem thời tiết (theo thành phố)")
        self.btn_check.setFont(QFont("Arial", 12))
        self.btn_check.setStyleSheet("background-color: #27AE60; color: white; padding: 8px; border-radius: 8px;")
        self.btn_check.clicked.connect(self.get_weather_by_city)

        row_city = QHBoxLayout()
        row_city.addWidget(self.city_input)
        row_city.addWidget(self.btn_check)

        # -------- B) Tìm theo tọa độ --------
        lat_lbl = QLabel("Lat:")
        lon_lbl = QLabel("Lon:")
        self.lat_input = QLineEdit()
        self.lon_input = QLineEdit()
        self.lat_input.setPlaceholderText("vd: 21.0278")
        self.lon_input.setPlaceholderText("vd: 105.8342")
        for w in (self.lat_input, self.lon_input):
            w.setFont(QFont("Arial", 12))
            w.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid gray;")

        self.btn_check_coord = QPushButton("🧭 Xem thời tiết (theo tọa độ)")
        self.btn_check_coord.setFont(QFont("Arial", 12))
        self.btn_check_coord.setStyleSheet("background-color: #D35400; color: white; padding: 8px; border-radius: 8px;")
        self.btn_check_coord.clicked.connect(self.get_weather_by_coord_fields)

        row_coord_top = QHBoxLayout()
        row_coord_top.addWidget(lat_lbl)
        row_coord_top.addWidget(self.lat_input)
        row_coord_top.addWidget(lon_lbl)
        row_coord_top.addWidget(self.lon_input)

        # -------- C) GPS (thiết bị) --------
        self.btn_gps = QPushButton("📍 Dùng vị trí GPS (thiết bị)")
        self.btn_gps.setFont(QFont("Arial", 12))
        self.btn_gps.setStyleSheet("background-color: #8E44AD; color: white; padding: 8px; border-radius: 8px;")
        self.btn_gps.clicked.connect(self.start_gps)

        # -------- Status + Result --------
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #7F8C8D; margin-top: 4px;")

        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("margin-top: 10px; color: #2C3E50;")

        # Layout tổng
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(row_city)
        layout.addLayout(row_coord_top)
        layout.addWidget(self.btn_check_coord)
        layout.addWidget(self.btn_gps)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Qt Positioning setup ---
        self.geo_source = QGeoPositionInfoSource.createDefaultSource(self)
        if self.geo_source:
            self.geo_source.setUpdateInterval(2000)  # ms
            self.geo_source.positionUpdated.connect(self.on_position_updated)
            try:
                self.geo_source.errorOccurred.connect(self.on_gps_error)
            except Exception:
                pass

    # ---------------- Weather request helpers ----------------
    def fetch_weather_by_coords(self, lat: float, lon: float):
        params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "vi"}
        self._request_and_render(params, coord_hint=(lat, lon))

    def fetch_weather_by_city(self, city: str):
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"}
        self._request_and_render(params, city_hint=city)

    def _request_and_render(self, params: dict, city_hint: str = "", coord_hint=None):
        try:
            resp = requests.get(BASE_URL, params=params, timeout=10)
            data = resp.json()
            cod = data.get("cod", 0)
            try:
                cod = int(cod)
            except Exception:
                cod = 0

            if cod != 200:
                msg = data.get("message", "Không xác định")
                if city_hint:
                    QMessageBox.critical(self, "Lỗi", f"Không tìm thấy thành phố: {city_hint}\n({msg})")
                else:
                    QMessageBox.critical(self, "Lỗi", f"Không lấy được thời tiết từ toạ độ!\n({msg})")
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            name = data.get("name") or ""
            sys_info = data.get("sys", {})
            country = sys_info.get("country") or ""

            # Dòng vị trí hiển thị đẹp
            if city_hint:
                location_line = f"📍 Thành phố: {city_hint}"
                if name and name.lower() != city_hint.lower():
                    location_line += f" (gần: {name}{', ' + country if country else ''})"
            else:
                if coord_hint:
                    lat, lon = coord_hint
                    nice = f"{lat:.5f}, {lon:.5f}"
                    if name:
                        location_line = f"📍 Vị trí: {name}{', ' + country if country else ''} ({nice})"
                    else:
                        location_line = f"📍 Toạ độ: {nice}"
                else:
                    location_line = "📍 Vị trí không xác định"

            self.result_label.setText(
                f"{location_line}\n"
                f"🌡 Nhiệt độ: {temp}°C\n"
                f"🤔 Cảm giác như: {feels_like}°C\n"
                f"💧 Độ ẩm: {humidity}%\n"
                f"☁️ Trạng thái: {description.capitalize()}"
            )
        except requests.Timeout:
            QMessageBox.critical(self, "Lỗi", "Kết nối quá thời gian (timeout). Vui lòng thử lại.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lấy dữ liệu!\n{str(e)}")

    # ---------------- City flow ----------------
    def get_weather_by_city(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên thành phố!")
            return
        self.fetch_weather_by_city(city)

    # ---------------- Coordinate flow ----------------
    def get_weather_by_coord_fields(self):
        lat_txt = self.lat_input.text().strip().replace(",", ".")
        lon_txt = self.lon_input.text().strip().replace(",", ".")
        if not lat_txt or not lon_txt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ Lat và Lon!")
            return
        try:
            lat = float(lat_txt)
            lon = float(lon_txt)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Lat/Lon phải là số thập phân hợp lệ!")
            return

        if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
            QMessageBox.warning(self, "Lỗi", "Phạm vi hợp lệ: Lat ∈ [-90, 90], Lon ∈ [-180, 180].")
            return

        self.fetch_weather_by_coords(lat, lon)

    # ---------------- GPS flow ----------------
    def start_gps(self):
        if not self.geo_source:
            QMessageBox.warning(
                self, "Thiếu vị trí",
                "Thiết bị không cung cấp dịch vụ vị trí (GPS/Wi-Fi). "
                "Hãy bật Location Services trong hệ điều hành rồi thử lại."
            )
            return
        self.status_label.setText("🔄 Đang lấy vị trí... Hãy bật GPS/Location cho thiết bị.")
        self.btn_gps.setEnabled(False)
        try:
            self.geo_source.startUpdates()
        except Exception as e:
            self.btn_gps.setEnabled(True)
            self.status_label.setText("")
            QMessageBox.critical(self, "Lỗi GPS", f"Không thể bắt đầu lấy vị trí:\n{e}")

    def on_position_updated(self, info):
        coord = info.coordinate()
        lat = coord.latitude()
        lon = coord.longitude()
        try:
            self.geo_source.stopUpdates()
        except Exception:
            pass
        self.btn_gps.setEnabled(True)
        self.status_label.setText(f"✅ Đã lấy toạ độ: {lat:.5f}, {lon:.5f}")
        self.fetch_weather_by_coords(lat, lon)

    def on_gps_error(self, error):
        self.btn_gps.setEnabled(True)
        self.status_label.setText("")
        QMessageBox.critical(
            self, "Lỗi GPS",
            "Không thể truy cập vị trí.\n"
            "• Bật Location Services (GPS) trong hệ điều hành.\n"
            "• Cấp quyền vị trí cho ứng dụng (nếu hệ điều hành yêu cầu).\n"
            "• Thử lại sau vài giây."
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
