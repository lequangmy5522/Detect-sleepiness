import folium
import geocoder
from geopy.geocoders import Nominatim
from datetime import datetime

class LocationTracker:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="drowsiness_detector")
        self.incidents = []
        
    def track_incident(self):
        g = geocoder.ip('me')
        if g.latlng:
            location = self.geolocator.reverse(f"{g.latlng[0]}, {g.latlng[1]}")
            incident = {
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'location': g.latlng,
                'address': location.address
            }
            self.incidents.append(incident)
            return incident
        return None

    def generate_map(self, filename='incident_map.html'):
        if not self.incidents:
            return
        
        m = folium.Map(location=self.incidents[0]['location'], zoom_start=13)
        for incident in self.incidents:
            folium.Marker(
                incident['location'],
                popup=f"Drowsiness detected at {incident['time']}\n{incident['address']}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        m.save(filename)