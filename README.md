# 🛡️ AI-Powered Financial Fraud Detection System

An AI-driven web application designed to protect modern digital banking systems from malicious activities through real-time predictive analytics and detection. Built with Python, Streamlit, and Machine Learning algorithms.

---

## 🔗 Live Application Link
🚀 **Try the Live App Here:** [ai-powered-financial-fraud-detection-system.streamlit.app](https://jviyqtghtaheemd3zn.streamlit.app/)

---

## 🎯 Objective
The goal of this project is to automate the identification of fraudulent banking transactions, reducing financial risk and providing real-time intelligence to management teams.

---

## ⚡ Key Features
* **Real-Time Risk Scoring:** Automatically evaluates threat metrics for all incoming transactions.
* **Anomalous Pattern Flagging:** Instantly detects spikes in transaction velocity, failed logins, or unfamiliar geolocations.
* **Interactive Admin Dashboard:** A clean visual panel showing volatile account flags, fraud graphs, and status metrics.

---

## ⚙️ Workflow / System Architecture
The detection engine operates seamlessly across 5 core modular stages to deliver low-latency feedback:
1. **Transaction Input:** Captures transaction details dynamically.
2. **Feature Extraction:** Evaluates inputs against real-time flags.
3. **Decision Tree Scoring:** Processes features through our ML algorithm.
4. **Risk Classification:** Evaluates total weightage points against thresholds.
5. **Alert & Dashboard Trigger:** Instantly displays "Legitimate" (Green) or "Critical Alert" (Red) banners.

---

## 📊 Model Evaluation & Metrics
To achieve high precision and audit compliance, multiple machine learning classifiers were benchmarked:

| Model Framework | Target Accuracy | Status |
| :--- | :--- | :--- |
| Logistic Regression | 82% | Benchmarked |
| **Decision Tree (Our Framework)** | **94%** | **Selected / Integrated** |
| Random Forest | 96% | Benchmarked |

### 🧠 Accuracy Formula Used:
$$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$

---

## 🛠️ Technology Stack
* **Language:** Python
* **Libraries:** Scikit-Learn, XGBoost, Pandas, NumPy, Imbalanced-Learn (SMOTE)
* **Frontend Framework:** Streamlit UI

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/swati6578/AI-Powered-Financial-Fraud-Detection-System.git](https://github.com/swati6578/AI-Powered-Financial-Fraud-Detection-System.git)
   cd AI-Powered-Financial-Fraud-Detection-System
2. **Install the required packages:**
    pip install -r requirements.txt
3. **Launch the Streamlit app:**
    streamlit run app.py
