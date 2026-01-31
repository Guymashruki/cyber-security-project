import requests
import json
import os
from datetime import datetime

# הגדרות חיבור לשרת
SERVER_URL = "http://127.0.0.1:8080/report"
REPORT_FILE = "security_report.json"

def send_data():
    print("🚀 Starting upload process...")
    
    # 1. בדיקה שהדוח קיים
    if not os.path.exists(REPORT_FILE):
        print(f"❌ Error: {REPORT_FILE} not found!")
        print("   -> Please run 'python analyzer.py' first to generate the report.")
        return

    # 2. קריאת הדוח והכנת החבילה לשליחה
    try:
        with open(REPORT_FILE, 'r') as f:
            report_data = json.load(f)
            
            # אנחנו עוטפים את הנתונים במבנה שהשרת החדש מצפה לו
            payload = {
                "title": "Security Audit Log",
                "content": json.dumps(report_data), # הופכים את ה-JSON לטקסט (String)
                "tags": ["security", "audit", "v1"],
                "date": str(datetime.now())
            }
            
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return

    # 3. שליחה לשרת (POST request)
    try:
        print(f"📡 Sending data to {SERVER_URL}...")
        response = requests.post(SERVER_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ SUCCESS! Data uploaded successfully.")
            print(f"   Server replied: {response.json()}")
        else:
            print(f"❌ Failed to upload. Status Code: {response.status_code}")
            print(f"   Response text: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: Is the server running? ({e})")
        print("   -> Make sure to run: python -m uvicorn server:app --reload --port 8080")

if __name__ == "__main__":
    send_data()