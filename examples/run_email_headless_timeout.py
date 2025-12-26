import sys
import os
import json
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.test_email import SAMPLE_DATA
from backend.services.email_service import email_service


def send_report(recipient, out):
    try:
        res = email_service.send_analysis_report(
            recipient_email=recipient,
            risk_level=SAMPLE_DATA["risk_level"],
            summary=SAMPLE_DATA["summary"],
            total_flagged_amount=SAMPLE_DATA["total_flagged_amount"],
            flags=SAMPLE_DATA["flags"],
            recommendations=SAMPLE_DATA["recommendations"],
            visualizations=None,
            document_name=SAMPLE_DATA.get("document_name")
        )
        out.append(res)
    except Exception as e:
        out.append({"success": False, "message": f"Exception: {e}"})


def main(timeout_seconds=30):
    recipient = getattr(email_service, 'gmail_user', None)
    if len(sys.argv) >= 2:
        recipient = sys.argv[1]

    if not recipient:
        print("No recipient configured or provided. Provide recipient as arg or set GMAIL_USER in .env")
        sys.exit(1)

    print(f"Sending test email to: {recipient} (timeout {timeout_seconds}s)")

    out = []
    t = threading.Thread(target=send_report, args=(recipient, out), daemon=True)
    t.start()
    t.join(timeout_seconds)

    if t.is_alive():
        print(json.dumps({"success": False, "message": "Timed out while sending email"}, indent=2))
        return

    if out:
        print(json.dumps(out[0], indent=2))
    else:
        print(json.dumps({"success": False, "message": "No result returned"}, indent=2))


if __name__ == '__main__':
    main()
