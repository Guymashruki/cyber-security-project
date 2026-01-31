# 🛡️ RSecurity - Cyber Intelligence Dashboard

**A Full-Stack Cybersecurity Anomaly Detection System.** This system analyzes network activity logs, detects complex security threats using statistical logic, and visualizes the intelligence data in a real-time React dashboard.

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20|%20React%20|%20FastAPI-blue)

## ⚡ Key Features

### 🔍 Threat Detection Logic (The Brain)
The system parses raw logs (`activity_log.csv`) and identifies the following anomalies:
1.  **🚫 Brute Force Attacks:** Detects multiple failed login attempts (>5) from a single user within a short window.
2.  **🌍 Geo-Anomalies:** Flags "Impossible Travel" scenarios (e.g., login from USA and China within 1 hour).
3.  **💀 Suspicious IPs:** Cross-references connection attempts against a blacklist of known malicious subnets.
4.  **🕒 After-Hours Activity:** Flags sensitive admin operations performed outside standard business hours.

### 💻 System Architecture
* **Backend:** A REST API built with **Python (FastAPI)** that serves as the intelligence hub.
* **Frontend:** A modern SPA built with **React + Vite** and styled with **Tailwind CSS**.
* **Visualization:** Interactive charts using **Chart.js** to display attack distribution.

---

## 🛠️ Tech Stack & Requirements

### Prerequisites
Before running the project, ensure you have the following installed:
* **Python 3.8+**
* **Node.js & npm** (for the frontend)

### Technologies Used
* **Backend:** Python, FastAPI, Uvicorn, Pandas, Requests.
* **Frontend:** React, Tailwind CSS, Chart.js, Vite.
* **Tools:** Git, VS Code.

---

## 🚀 Installation & Running Guide

Follow these steps to get the system running locally.
**You will need 3 separate terminal windows.**

### Step 1: Backend Server Setup (Terminal 1) 🧠
This starts the REST API server that listens for data and serves the frontend.

1.  Open a terminal in the **root folder**.
2.  Install python dependencies:
    ```bash
    pip install fastapi uvicorn pandas requests
    ```
3.  Start the server:
    ```bash
    python -m uvicorn server:app --reload --port 8080
    ```
    > ✅ **Success:** You should see: *Application startup complete*.

### Step 2: Data Generation & Upload (Terminal 2) 📊
This step simulates the "Agent" – it analyzes the logs and sends the report to the server.

1.  Open a new terminal in the **root folder**.
2.  Run the analyzer to create the report:
    ```bash
    python analyzer.py
    ```
3.  Upload the data to the server:
    ```bash
    python client.py
    ```
    > ✅ **Success:** You should see: *SUCCESS! Data uploaded to server*.

### Step 3: Frontend Dashboard (Terminal 3) 🎨
This launches the React website.

1.  Open a new terminal.
2.  Navigate to the frontend folder:
    ```bash
    cd frontend
    ```
3.  Install dependencies (First time only):
    ```bash
    npm install
    ```
4.  Start the development server:
    ```bash
    npm run dev
    ```

### 🏁 Final Step
Open your browser and navigate to the link shown in the terminal:
👉 **http://localhost:5173**

---

## 📂 Project Structure

```text
rsecurity-dashboard/
├── activity_log.csv        # Raw log data
├── analyzer.py             # Logic for detecting anomalies
├── client.py               # Script to upload data to server
├── server.py               # FastAPI Backend Server
├── security_report.json    # Generated intelligence report
├── frontend/               # React Application
│   ├── src/
│   │   ├── App.jsx         # Main Component
│   │   ├── Dashboard.jsx   # Visualization Logic
│   │   └── main.jsx        # Entry point
│   ├── index.html          # HTML entry
│   └── package.json        # Frontend dependencies
└── README.md               # Documentation