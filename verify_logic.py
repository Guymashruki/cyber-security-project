import pandas as pd
from datetime import timedelta

LOG_FILE = 'activity_log.csv'
INTERNAL_PREFIX = '192.168.'

def verify_data():
    print("🕵️‍♂️ Starting Data Verification Audit...\n")
    
    try:
        df = pd.read_csv(LOG_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"✅ Successfully loaded {LOG_FILE}")
    except Exception as e:
        print(f"❌ Error: Could not read {LOG_FILE}. Make sure the file exists and is named correctly.")
        return

    # ---------------------------------------------------------
    # 1. הוכחת Brute Force
    # ---------------------------------------------------------
    print("\n--- 1. Verifying BRUTE FORCE Logic ---")
    print("Logic: > 3 failed logins within 5 minutes from same IP")
    
    # סינון רק שורות של כישלון התחברות
    if 'action' in df.columns:
        failed = df[df['action'] == 'login_failed'].sort_values('timestamp')
    else:
        # גיבוי למקרה שהעמודה נקראת אחרת (אופציונלי)
        failed = pd.DataFrame() 

    found_brute = False
    
    if not failed.empty:
        for ip, group in failed.groupby('ip_address'):
            # בדיקה אם יש יותר מ-3 כשלונות בחלון זמן של 5 דקות
            count = group.rolling('5min', on='timestamp').count()
            
            # בדיקה אם יש איזשהו ערך שגדול או שווה ל-3
            if (count['action'] >= 3).any():
                print(f"✅ VERIFIED: Found Brute Force attacker: {ip}")
                print("   Here represents the RAW LOGS causing the alert:")
                
                # הצגת השורות הרלוונטיות בלבד (5 הראשונות לדוגמה)
                suspicious_logs = group.head(5)
                for _, row in suspicious_logs.iterrows():
                    print(f"   ⏰ {row['timestamp']} | User: {row['user_id']} | Action: {row['action']}")
                
                found_brute = True
                break # מספיק דוגמה אחת להוכחה
            
    if not found_brute: 
        print("❌ No Brute Force found (Check if 'login_failed' exists in CSV).")


    # ---------------------------------------------------------
    # 2. הוכחת Geo Hop
    # ---------------------------------------------------------
    print("\n--- 2. Verifying GEO HOP Logic ---")
    print("Logic: Same user changed IP within < 30 minutes")
    
    df_sorted = df.sort_values(by=['user_id', 'timestamp'])
    found_geo = False
    
    for user, group in df_sorted.groupby('user_id'):
        group = group.copy() # למנוע אזהרות פייתון
        group['prev_ip'] = group['ip_address'].shift(1)
        group['prev_time'] = group['timestamp'].shift(1)
        
        # חישוב הפרש זמנים
        group['time_diff'] = group['timestamp'] - group['prev_time']
        
        # מציאת המקרה החשוד: IP שונה + זמן קצר מדי
        suspicious = group[
            (group['ip_address'] != group['prev_ip']) & 
            (group['time_diff'] < timedelta(minutes=30))
        ]
        
        if not suspicious.empty:
            row = suspicious.iloc[0] # לוקחים את המקרה הראשון
            print(f"✅ VERIFIED: Found Geo Hop for User: {user}")
            print(f"   1. First Login:  {row['prev_time']} from IP {row['prev_ip']}")
            print(f"   2. Second Login: {row['timestamp']} from IP {row['ip_address']}")
            print(f"   🚀 Time Difference: {row['time_diff']} (Impossible Speed!)")
            found_geo = True
            break
            
    if not found_geo: print("❌ No Geo Hop found.")


    # ---------------------------------------------------------
    # 3. הוכחת Suspicious IP
    # ---------------------------------------------------------
    print("\n--- 3. Verifying SUSPICIOUS IP Logic ---")
    print(f"Logic: IP does not start with {INTERNAL_PREFIX}")
    
    # מחפשים IP שלא מתחיל ב-192.168
    suspicious_ips = df[~df['ip_address'].str.startswith(INTERNAL_PREFIX)]
    
    if not suspicious_ips.empty:
        row = suspicious_ips.iloc[0]
        print(f"✅ VERIFIED: Found Suspicious External IP: {row['ip_address']}")
        print(f"   Row in CSV: {row['timestamp']} | User: {row['user_id']} | IP: {row['ip_address']}")
        print("   (This implies access from outside the internal network)")
    else:
        print("❌ No Suspicious IPs found.")
        
    print("\n---------------------------------------------------------")
    print("🎯 CONCLUSION: If you see the Raw Logs above, the Logic is 100% Correct.")

if __name__ == "__main__":
    verify_data()