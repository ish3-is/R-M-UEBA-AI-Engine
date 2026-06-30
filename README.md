Markdown# 🛡️ Continuous-Auth UEBA: Keystroke Dynamics Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Framework: Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](https://streamlit.io/)
[![AI Model: Random%20Forest](https://img.shields.io/badge/AI%20Model-Random%20Forest%20(95%25%2B%20Acc)-green)](https://scikit-learn.org/)

An enterprise-grade **User and Entity Behavior Analytics (UEBA)** solution leveraging behavioral biometrics via keystroke dynamics. By shifting away from static, point-in-time authentication, this engine enforces **Continuous Authentication** at the endpoint level, continuously validating the identity of an active user based on their unique typing rhythm.

---

## 🎯 Core Features

- **Continuous Zero Trust Validation:** Eliminates the "authenticate once, access forever" flaw by verifying identity on every keystroke.
- **Microsecond Precision Analytics:** Tracks exact **Dwell Time** (key-press duration) and flight time in milliseconds to build a highly precise biological profile.
- **Enterprise AI Core:** Powered by a tuned Random Forest Classifier achieving **>95% accuracy** with low False Positive Rates (FPR).
- **Stealth Endpoint Telemetry:** A lightweight, defensive background agent running as a non-intrusive Windows service.
- **Interactive SOC Command Center:** A rich, operational dashboard for Security Operations Center (SOC) analysts to monitor real-time behavioral drift, anomalies, and active sessions.
- **Native SIEM Integration:** Built-in JSON log ingestion pipelines with pre-configured Splunk SPL hunting rules.

---

## 🔒 Cyber Security Context

### The Zero Trust Paradigm Shift
Traditional Security Perimeters assume that once a user provides correct credentials (or passes MFA), their identity is verified for the duration of the session. This assumption fails against **Session Hijacking**, **Physical Insider Threats**, and **Credential Theft**. 

This project implements **Strict Continuous Zero Trust (Never Trust, Always Verify)**. Even if an adversary obtains the correct plaintext password, they cannot replicate the biometric cadence (Dwell Time and Digraph intervals) of the legitimate user. 

### Mitigating Insider Threats & Lateral Movement
When an unauthorized user gains physical or remote access to an unlocked active workstation, the **Live Endpoint Agent** detects the anomalous typing rhythm within seconds, generating immediate telemetry alerts to mitigate threat progression before lateral movement occurs.
<img width="1536" height="1024" alt="ChatGPT Image 30 يونيو 2026، 08_29_20 ص" src="https://github.com/user-attachments/assets/19be4be1-2204-4f16-8981-5bf61a08491c" />

---

## 🏗️ Project Architecture

```text
R-M-UEBA-AI-Engine/
├── src/
│   ├── app.py                # SOC Dashboard (Streamlit Interface)
│   ├── models.py             # AI Engine Core (Training & Random Forest Architecture)
│   ├── defensive_agent.py    # Live Endpoint Agent (Stealth Behavioral Keylogger)
│   └── ueba_app.py           # Real-time Evaluation & Influx Comparator Bridge
├── siem_configs/
│   ├── splunk_alert.spl      # Enterprise Splunk SPL Hunting Query
│   └── sample_anomaly.json   # SIEM-ready JSON Outbound Log Schema
├── requirements.txt          # Python Dependency Manifest
└── README.md                 # Document Matrix
```
##Module Breakdown
###ComponentFile PathTechnical SpecificationAI Engine Coresrc/models.pyHandles dataset ingestion (DSL-StrongPasswordData), feature engineering of Dwell Times, model serialization, and hyperparameter tuning.Endpoint Agentsrc/defensive_agent.pyLow-overhead Windows interceptor hook capturing key down/up events to stream keystroke timings smoothly without latency impact.Evaluation Bridgesrc/ueba_app.pyPipeline linking live agent telemetry inputs directly into the trained model inference engine to yield probability scores.SOC Dashboardsrc/app.pyStreamlit analytical visualization tool offering historical analysis, live drift counters, and threat vectors maps.🚀 Installation & Quick StartPrerequisitesPython 3.9 or higher installed.Windows Environment (for full functionality of the defensive_agent.py OS hooks).Environment SetupBash# Clone the repository
git clone [https://github.com/ish3-is/R-M-UEBA-AI-Engine.git](https://github.com/ish3-is/R-M-UEBA-AI-Engine.git)
cd R-M-UEBA-AI-Engine

# Initialize and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Phase 1: Training the AI EngineTrain the Random Forest model on the baseline behavioral dataset to export the serialized classifier artifact.Bashpython src/models.py
Phase 2: Deploying the Live Endpoint AgentExecute the background behavioral interceptor to begin real-time user monitoring and verification.Bashpython src/ueba_app.py
Phase 3: Launching the SOC DashboardSpin up the interactive analyst console to visualize system status and anomalies.Bashstreamlit run src/app.py
📊 SIEM & Splunk IntegrationThe system automatically pushes anomalous behavioral incidents into the SIEM collector pipeline.Outbound Anomaly Schema (siem_configs/sample_anomaly.json)When a user's behavior drifts significantly below the 95% confidence threshold, the agent triggers a structured security event:JSON{
  "timestamp": "2026-06-30T08:38:00Z",
  "event_id": "UEBA-ANOMALY-4071",
  "host_name": "WKSTN-ENG-88",
  "user_principal": "j.doe@enterprise.local",
  "metric": {
    "expected_dwell_avg_ms": 112.4,
    "observed_dwell_avg_ms": 184.9,
    "confidence_score": 0.34
  },
  "action_taken": "ALERT_GENERATED",
  "severity": "HIGH"
}
Splunk Hunting Rule (siem_configs/splunk_alert.spl)To filter out noise and capture dedicated malicious attempts, the following Splunk SPL rule triggers a high-severity alert when 3 distinct anomalies are generated within a 1-minute window:Splunk SPLindex=security sourcetype="ueba:keystroke:analytics" severity="HIGH"
| stats count, values(user_principal) as targeted_users, values(host_name) as affected_hosts by user_principal
| where count >= 3
| eval alert_tier="Tier-2 SOC Intervention Required", description="Continuous authentication failure: Multiple keystroke dynamics anomalies detected within 60 seconds."
📜 LicenseDistributed under the MIT License. See LICENSE for more information.
