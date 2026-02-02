import pandas as pd
import numpy as np

def validate_oap_ingest(file_path):
    print("\n--- ORTHONODE OAP VALIDATOR [v2.5.x] ---")

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f"[ERROR] Failed to load file: {e}"

    # -----------------------------
    # TIER 1 — CORE KINEMATIC DATA
    # -----------------------------
    tier1_req = ['timestamp', 'lat', 'lon', 'accel_x']
    speed_cols = ['speed', 'speed_kmh', 'speed_mps']

    missing_t1 = [c for c in tier1_req if c not in df.columns]
    speed_col = next((c for c in speed_cols if c in df.columns), None)

    if missing_t1 or not speed_col:
        print(f"[FAIL] Missing Tier-1 fields:")
        if missing_t1:
            print(f"       Core: {missing_t1}")
        if not speed_col:
            print(f"       Speed: none of {speed_cols}")
        return

    print("[PASS] Tier-1 Kinematic Core present.")
    print(f"[INFO] Speed column detected: {speed_col}")

    # -----------------------------
    # TIER 2 — OPTIONAL AUGMENTERS
    # -----------------------------
    tier2_opt = ['brightness', 'entropy', 'hdop', 'curvature']
    found_t2 = [c for c in tier2_opt if c in df.columns]

    print(f"[INFO] Tier-2 Augmenters: {found_t2 if found_t2 else 'None'}")

    # -----------------------------
    # FREQUENCY & JITTER ANALYSIS
    # -----------------------------
    if len(df) < 2:
        print("[FAIL] Insufficient samples for frequency analysis.")
        return

    time_diffs = np.diff(df['timestamp'].values)

    if np.any(time_diffs <= 0):
        print("[WARN] Non-monotonic or duplicate timestamps detected.")

    mean_dt = np.mean(time_diffs)

    if mean_dt <= 0:
        print("[FAIL] Invalid timestamp deltas. Cannot compute frequency.")
        return

    avg_hz = 1 / mean_dt
    print(f"[*] Average Sampling Frequency: {avg_hz:.2f} Hz")

    if avg_hz < 10:
        print("[WARN] <10 Hz detected. OAP-K confidence reduced.")
    elif avg_hz >= 50:
        print("[PASS] High-fidelity signal suitable for forensic audit.")

    # -----------------------------
    # DATA GAP CHECK
    # -----------------------------
    gap_threshold = mean_dt * 5
    gaps = np.sum(time_diffs > gap_threshold)

    if gaps > 0:
        print(f"[WARN] {gaps} significant data gaps detected.")
    else:
        print("[PASS] Continuous stream confirmed.")

    print("--- VALIDATION COMPLETE ---\n")
