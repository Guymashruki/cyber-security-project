# 🛡️ RSecurity - Cyber Intelligence Dashboard

**A Full-Stack Cybersecurity Anomaly Detection System.**
This project analyzes network activity logs, detects complex security threats using deterministic logic, and visualizes the intelligence data in a real-time React dashboard.

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20|%20React%20|%20FastAPI-blue)

##  Key Features & Detection Logic

###  How It Works (The Brain)
The system parses raw logs (`activity_log.csv`) and identifies anomalies based on the following security policies:

1.  ** Brute Force Attacks:**
    * **Logic:** Detects **3 or more** failed login attempts (`login_failed`) from a single IP within a **5-minute** rolling window.
    * *Why?* Identifies aggressive password guessing attempts.

2.  ** Geo-Anomalies (Impossible Travel):**
    * **Logic:** Flags users who change IP addresses (jump locations) within less than **30 minutes**.
    * *Why?* It is physically impossible to travel between different network locations in such a short time.

3.  ** Suspicious IPs (Access Control):**
    * **Logic:** Flags any access attempt from an IP address that **does not start with** `192.168.` (Internal Office Range).
    * *Why?* Enforces a strict "Internal Use Only" policy. Any external access is treated as a potential breach.

---

##  Tech Stack & Requirements

### Prerequisites
* **Python 3.8+**
* **Node.js & npm** (for the frontend)

### Technologies
* **Backend:** Python, FastAPI, Uvicorn, Pandas (Data Analysis).
* **Frontend:** React, Vite, Tailwind CSS, Chart.js (Visualization).
* **Communication:** REST API, JSON.

---

##  Installation & Running Guide

Follow these steps to get the system running locally.
**You will need 3 separate terminal windows.**

### Step 1: Start the Backend Server (Terminal 1) 
This starts the REST API server that acts as the bridge between the data and the dashboard.

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

### Step 2: Generate & Upload Data (Terminal 2) 
This step simulates the "Security Agent" – it analyzes the logs and sends the report to the server.

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

### Step 3: Start the Frontend Dashboard (Terminal 3) 
This launches the React user interface.

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
 **http://localhost:5173**

---

##  Project Structure

```text
rsecurity-dashboard/
├── activity_log.csv        # Raw log data input
├── analyzer.py             # Detection Logic (Brute Force, Geo, IP)
├── client.py               # Script to upload data to server
├── server.py               # FastAPI Backend Server
├── security_report.json    # Generated intelligence report
├── frontend/               # React Application
│   ├── src/
│   │   ├── App.jsx         # Main Component
│   │   ├── Dashboard.jsx   # Visualization & Charts
│   └── package.json
└── README.md               # Documentation