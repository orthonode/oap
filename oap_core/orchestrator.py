import pandas as pd
import json
from assurance import OrthonodeAssurancePlatform

def run_forensic_audit(input_csv, output_prefix="OR_AUDIT", vehicle_type="CAR"):
    print(f"[OAP] Starting forensic audit on {input_csv}")

    # Initialize OAP core
    oap = OrthonodeAssurancePlatform(vehicle_type=vehicle_type)

    df = pd.read_csv(input_csv)

    audit_logs = []

    # Precompute dt if not supplied
    if 'dt' not in df.columns:
        df['dt'] = df['timestamp'].diff().fillna(method='bfill')

    for _, row in df.iterrows():
        # Defensive dt
        dt = max(float(row['dt']), 1e-3)

        packet = {
            'speed': row['speed'],
            'accel_x': row['accel_x'],
            'lat_g': row.get('lat_g', None),
            'curvature': row.get('curvature', None),
            'hdop': row.get('hdop', 1.0),
            'dt': dt,

            # Tier-2 augmenters (optional)
            'brightness': row.get('brightness', None),
            'entropy': row.get('entropy', None),
        }

        oap.process_packet(packet)

        # Capture only meaningful violations
        if oap.integrity_risk > 0:
            audit_logs.append({
                "timestamp": row['timestamp'],
                "integrity_risk": oap.integrity_risk,
                "quality_risk": oap.quality_risk,
                "weather_mode": oap.weather_mode
            })

    # --- OUTPUTS ---

    # 1. Surgical log (engineers)
    surgical_path = f"{output_prefix}_SURGICAL_LOG.csv"
    pd.DataFrame(audit_logs).to_csv(surgical_path, index=False)

    # 2. Executive summary (non-technical)
    summary = {
        "entity": "Orthonode Infrastructure Labs",
        "vehicle_profile": vehicle_type,
        "total_samples": int(len(df)),
        "violation_events": int(len(audit_logs)),
        "audit_classification": (
            "FAIL"
            if oap.integrity_risk >= 50
            else "PASS"
        ),
        "notes": "Results derived from deterministic kinematic validation (OAP v2.5.x)."
    }

    summary_path = f"{output_prefix}_SUMMARY.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[OAP] Audit complete → {summary['audit_classification']}")
    return summary_path, surgical_path
