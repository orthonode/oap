# FILE: nap_daemon.py
import sys
import io
import time
import random

# Force UTF-8 for Windows PowerShell
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from nap_core.assurance import NexusAssurancePlatform
except ImportError:
    print("❌ Error: Could not find nap_core/assurance.py")
    sys.exit(1)

def generate_mock_data(tick):
    # --- SCENARIO 1: HONEST DRIVING (Ticks 0-20) ---
    # Speed: 12.5 m/s (~45 km/h)
    # Lat G: 0.16 G (Consistent with physics)
    data = {
        'speed': 12.5,  
        'lat_g': 0.16,  
        'curvature': 0.01,
        'hdop': 1.0, 
        'accel_x': 0.5, 
        'dt': 1.0,
        'brightness': 150, 
        'entropy': 0.8
    }
    
    # --- SCENARIO 2: SPLINE SPOOF ATTACK (Ticks 20-40) ---
    # Attacker increases speed and turns, but forgets to fake G-force
    if 20 <= tick <= 40:
        data['speed'] = 20.0     # 72 km/h
        data['curvature'] = 0.05 # Sharp turn
        data['lat_g'] = 0.01     # 0G (Device is flat on desk)
    
    # --- SCENARIO 3: RECOVERY (Ticks 41+) ---
    # Attacker stops. Back to honest driving.
    if tick > 40:
        data['speed'] = 12.5
        data['lat_g'] = 0.16
        data['curvature'] = 0.01

    return data

def run_service():
    print("🚀 NAP v1.0 | HIVEMAPPER INFRASTRUCTURE | SERVICE STARTED")
    print("-------------------------------------------------------")
    
    nap = NexusAssurancePlatform(vehicle_type='CAR')
    tick = 0
    
    try:
        while True:
            packet = generate_mock_data(tick)
            verdict = nap.process_packet(packet)
            
            ts = time.strftime("%H:%M:%S")
            # Format output for readability
            risk_str = f"{nap.integrity_risk:.1f}"
            print(f"[{ts}] TICK: {tick:03} | RISK: {risk_str.rjust(5)} | {verdict}")
            
            tick += 1
            time.sleep(0.2) # Faster replay for benchmark
            
    except KeyboardInterrupt:
        print("\n🛑 SERVICE STOPPED.")

if __name__ == "__main__":
    run_service()