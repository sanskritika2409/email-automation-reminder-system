import pandas as pd
from datetime import datetime
import os

from src.utils import load_contacts, load_reminders, load_template
from src.mailer import send_email

# ==============================
# ✅ FIXED ABSOLUTE PATH (IMPORTANT)
# ==============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "email.log")

# ==============================
# 🧾 FORCE LOG WRITER
# ==============================
def write_log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")
        f.flush()   # 🔥 IMPORTANT REAL-TIME WRITE

# ==============================
# 🚀 MAIN FUNCTION
# ==============================

print("🚀 RUN_SYSTEM CALLED")
write_log("🚀 RUN_SYSTEM CALLED")
def run_system(dry_run=True):

    write_log("===== RUN STARTED =====")

    contacts = load_contacts()
    reminders = load_reminders()
    template = load_template()

    report = []

    for _, c in contacts.iterrows():
        for _, r in reminders.iterrows():

            write_log(f"Processing: {c['email']} | {r['subject']}")

            body = template.format(
                name=c["name"],
                message=r["message"]
            )

            status = send_email(
                c["email"],
                r["subject"],
                body,
                dry_run
            )

            write_log(f"STATUS: {status}")

            report.append({
                "name": c["name"],
                "email": c["email"],
                "subject": r["subject"],
                "status": status,
                "time": datetime.now()
            })

    df = pd.DataFrame(report)

    df.to_csv(os.path.join(OUTPUT_DIR, "report.csv"), index=False)

    write_log("===== RUN COMPLETED =====")

    return df