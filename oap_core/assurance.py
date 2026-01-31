@'
# FILE: oap_core/assurance.py
import math
from collections import deque

# --- CONFIGURATION: VEHICLE PROFILES ---
VEHICLE_PROFILES = {
    'CAR':   {'max_roll': 5.0,  'lat_g_scale': 1.0, 'vib_floor': 0.02},
    'BIKE':  {'max_roll': 45.0, 'lat_g_scale': 0.4, 'vib_floor': 0.10}, 
    'TRUCK': {'max_roll': 3.0,  'lat_g_scale': 0.8, 'vib_floor': 0.05}
}

class OrthonodeAssurancePlatform:
    def __init__(self, vehicle_type='CAR'):
        self.profile = VEHICLE_PROFILES.get(vehicle_type, VEHICLE_PROFILES['CAR'])
        self.integrity_risk = 0.0  # Fraud (Blocking)
        self.quality_risk = 0.0    # Environment (Throttling)
        self.accel_buffer = deque(maxlen=50) 
        self.weather_mode = "CLEAR" 

    def _get_geometry_confidence(self, hdop, speed):
        if hdop > 2.5: return "LOW"  
        if speed < 15: return "LOW"  
        return "HIGH"

    def _detect_weather(self, frame_brightness, frame_entropy):
        if frame_brightness < 30: return "DARK"
        if frame_brightness > 100 and frame_entropy < 0.2: return "RAIN_FOG"
        return "CLEAR"

    def verify_kinematics(self, speed, lat_g, curvature, hdop):
        if self._get_geometry_confidence(hdop, speed) == "LOW": return 0.0 

        expected_lat_g = (speed ** 2) * curvature / 9.81
        scaled_expected_g = expected_lat_g * self.profile['lat_g_scale']
        error = abs(scaled_expected_g - abs(lat_g))

        if error > 0.4: return 20.0 
        return 0.0

    def verify_temporal_continuity(self, current_accel, dt):
        if len(self.accel_buffer) < 2: return 0.0
        prev_accel = self.accel_buffer[-1]
        jerk = abs(current_accel - prev_accel) / dt
        if jerk > 50.0: return 10.0 
        return 0.0

    def process_packet(self, data):
        self.weather_mode = self._detect_weather(data['brightness'], data['entropy'])

        k_penalty = self.verify_kinematics(data['speed'], data['lat_g'], data['curvature'], data['hdop'])
        self.integrity_risk += k_penalty

        self.accel_buffer.append(data['accel_x'])
        j_penalty = self.verify_temporal_continuity(data['accel_x'], data['dt'])
        self.quality_risk += j_penalty 

        if self.weather_mode == "CLEAR":
            if data['entropy'] < 0.1 and data['speed'] > 30:
                self.integrity_risk += 5.0 

        self.integrity_risk = max(0, self.integrity_risk - 0.5)
        self.quality_risk   = max(0, self.quality_risk - 1.0)

        if self.integrity_risk > 50: return "⛔ BLOCK (RC_FAIL_Integrity)"
        elif self.quality_risk > 50: return "⚠️ THROTTLE (RC_WARN_Quality)"
        else: return "✅ MINT (RC_PASS)"
'@ | Out-File -Encoding UTF8 oap_core\assurance.py