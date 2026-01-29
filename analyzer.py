import pandas as pd
import json
from datetime import timedelta

# --- הגדרות ---
LOG_FILE = 'activity_log.csv'
OUTPUT_FILE = 'security_report.json'
INTERNAL_IP_PREFIX = '192.168.'
BRUTE_FORCE_WINDOW = timedelta(minutes=5)
BRUTE_FORCE_THRESHOLD = 3
GEO_HOP_WINDOW = timedelta(minutes=30)  # אם החלפת IP תוך פחות מ-30 דקות - זה חשוד

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def detect_brute_force(df):
    """1. זיהוי רצף כשלונות התחברות (Brute Force)"""
    anomalies = []
    failed_logins = df[df['action'] == 'login_failed'].copy()
    
    if failed_logins.empty:
        return anomalies

    for ip, group in failed_logins.groupby('ip_address'):
        group = group.sort_values('timestamp').set_index('timestamp')
        count = group.rolling(window='5min').count()['action']
        suspicious = count[count >= BRUTE_FORCE_THRESHOLD]
        
        for ts, val in suspicious.items():
            user_id = group.loc[ts, 'user_id']
            if isinstance(user_id, pd.Series): user_id = user_id.iloc[0]
            
            anomalies.append({
                "timestamp": str(ts),
                "user_id": user_id,
                "ip_address": ip,
                "reason": f"Brute Force: {int(val)} failed logins in 5 min"
            })
    return anomalies

def detect_suspicious_ips(df):
    """2. זיהוי כתובות IP חיצוניות (לא מהמשרד)"""
    anomalies = []
    suspicious_df = df[~df['ip_address'].str.startswith(INTERNAL_IP_PREFIX)]
    
    for _, row in suspicious_df.iterrows():
        anomalies.append({
            "timestamp": str(row['timestamp']),
            "user_id": row['user_id'],
            "ip_address": row['ip_address'],
            "reason": "Suspicious IP: External access detected"
        })
    return anomalies

def detect_geo_hops(df):
    """3. זיהוי מעבר מהיר וחשוד בין כתובות IP (Geo-hopping / Impossible Travel)"""
    anomalies = []
    
    # מיון לפי משתמש וזמן (כדי לראות את רצף הפעולות של כל אדם)
    df_sorted = df.sort_values(by=['user_id', 'timestamp'])
    
    for user, group in df_sorted.groupby('user_id'):
        # יצירת עמודות עזר: מה היה ה-IP הקודם ומתי זה קרה
        group['prev_ip'] = group['ip_address'].shift(1)
        group['prev_time'] = group['timestamp'].shift(1)
        
        # סינון: רק מקרים שבהם ה-IP השתנה
        ip_changes = group[group['ip_address'] != group['prev_ip']]
        
        for _, row in ip_changes.iterrows():
            # אם יש נתונים קודמים (לא השורה הראשונה)
            if pd.notna(row['prev_time']):
                time_diff = row['timestamp'] - row['prev_time']
                
                # אם השינוי קרה מהר מדי (פחות מ-30 דקות)
                if time_diff < GEO_HOP_WINDOW:
                    anomalies.append({
                        "timestamp": str(row['timestamp']),
                        "user_id": user,
                        "ip_address": row['ip_address'],
                        "reason": f"Geo Hop Alert: Jumped from {row['prev_ip']} within {time_diff}"
                    })
                    
    return anomalies

def main():
    print("--- RSecurity Analyzer Started ---")
    df = load_data(LOG_FILE)
    if df is None: return

    anomalies = []
    
    # הרצת כל 3 הבדיקות
    print("Running Brute Force detection...")
    anomalies.extend(detect_brute_force(df))
    
    print("Running Suspicious IP detection...")
    anomalies.extend(detect_suspicious_ips(df))
    
    print("Running Geo-Hop detection...")
    anomalies.extend(detect_geo_hops(df))
    
    # הסרת כפילויות חכמה (לפי מפתח ייחודי)
    unique_anomalies = {f"{a['timestamp']}_{a['user_id']}_{a['reason']}": a for a in anomalies}.values()
    
    report = {
        "summary": {
            "total_logs": len(df),
            "anomalies_found": len(unique_anomalies)
        },
        "anomalies": list(unique_anomalies)
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Done! Found {len(unique_anomalies)} anomalies.")
    print(f"Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()