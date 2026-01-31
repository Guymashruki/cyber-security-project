from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# --- 1. אישור כניסה ל-React (CORS) ---
# זה קריטי! בלי זה האתר לא יוכל לקבל נתונים
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # מאפשר לכולם לגשת (לצורך הפיתוח)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- מודל הנתונים ---
class Report(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    date: str = str(datetime.now())

# זיכרון זמני (כאן נשמרים הנתונים)
reports_db = []

# --- 2. קבלת נתונים מה-Client ---
@app.post("/report")
def add_report(report: Report):
    reports_db.append(report)
    print(f"📥 Received report: {report.title}")
    return {"message": "Report added successfully", "id": len(reports_db) - 1}

# --- 3. שליחת נתונים לאתר (React) ---
@app.get("/reports")
def get_reports(tag: Optional[str] = Query(None)):
    if tag:
        return [r for r in reports_db if tag in r.tags]
    return reports_db

# הוספתי גם את זה למקרה שהאתר יבקש דוח בודד
@app.get("/report/{report_id}")
def get_report(report_id: int):
    if report_id < 0 or report_id >= len(reports_db):
        raise HTTPException(status_code=404, message="Report not found")
    return reports_db[report_id]

# להרצה:
# python -m uvicorn server:app --reload --port 8080