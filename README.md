# Orthonode Assurance Platform (OAP) v2.5.0
**Status:** PRODUCTION-READY | **Classification:** PROPRIETARY / RESTRICTED

## 🛡️ Executive Summary
OAP is the flagship deterministic hardware attestation engine developed by **Orthonode Infrastructure Labs**. It serves as a specialized "Filter Cascade" for DePIN and automated logistics, designed to distinguish between simulated telemetry and physical reality at the kinematic level. 

Initially optimized for Hivemapper evaluation, OAP v2.5.0 is now the primary production auditing layer for the Orthonode ecosystem.

## 🏛️ Architecture
The system utilizes a 4-Layer "Filter Cascade":
1.  **Layer 1 (The Edge):** Deterministic physics validation (Speed ↔ LatG ↔ Curvature).
2.  **Layer 2 (The Cloud):** Context-aware gating (Environment, Thermal, Cultural Entropy).
3.  **Layer 3 (The Auditor):** Narrative consistency checks (Session continuity).
4.  **Layer 4 (The Economy):** Risk-based reward throttling and Sybil resistance.

## 📊 Benchmark Results (v2.5.0 Stability)
* **Attack Vector:** Spline Spoof (Simulated 72km/h turn with 0.0G lateral force).
* **Detection Time:** < 2.0 seconds (Real-time edge processing).
* **Result:** Immediate BLOCK (Integrity Risk > 50).
* **Recovery:** "Leaky Bucket" forgiveness algorithm confirmed in `TEST_02_Soak_Stability_Proof.log`.

## 📂 Repository Structure
* `/oap_core`: The core logic library (Assurance Engine).
* `/oap_daemon.py`: The executable service runner.
* `TEST_*.log`: Validation benchmarks and stress tests.

---
**Copyright © 2026 Orthonode Infrastructure Labs Private Limited.**
*Confidentiality Notice: This repository contains proprietary trade secrets. Unauthorized access or distribution is strictly prohibited.*
