# -----------------------------------------------------------------------------
# Orthonode Assurance Platform (OAP) | Service Daemon v2.5.0
# Execution Layer: oap_daemon.py
#
# Copyright (c) 2026 Orthonode Infrastructure Labs Private Limited.
# All Rights Reserved.
#
# PROPRIETARY & CONFIDENTIAL: This file is part of the OAP production stack.
# Unauthorized execution, reverse engineering, or redistribution of this
# service daemon is strictly prohibited.
#
# Operational Jurisdiction: Balaghat / Bhopal, MP, India.
# -----------------------------------------------------------------------------

# FILE: oap_daemon.py
import sys
import io
import time
import random

# Force UTF-8 for Windows PowerShell
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from oap_core.assurance import OrthonodeAssurancePlatform
except ImportError:
    print("❌ Error: Could not find oap_core/assurance.py")
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
    print("🚀 OAP v2.5.0 | ORTHONODE INFRASTRUCTURE | SERVICE STARTED")
    print("-------------------------------------------------------")
    
    oap = OrthonodeAssurancePlatform(vehicle_type='CAR')
    tick = 0
    
    try:
        while True:
            packet = generate_mock_data(tick)
            verdict = oap.process_packet(packet)
            
            ts = time.strftime("%H:%M:%S")
            
            # FIXED: Changed 'nap' to 'oap'
            risk_str = f"{oap.integrity_risk:.1f}"
            
            print(f"[{ts}] TICK: {tick:03} | RISK: {risk_str.rjust(5)} | {verdict}")
            
            tick += 1
            time.sleep(0.2) # Faster replay for benchmark
            
    except KeyboardInterrupt:
        print("\n🛑 SERVICE STOPPED.")

if __name__ == "__main__":
    run_service()
