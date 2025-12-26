import sys
import os
import json

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.test_email import SAMPLE_DATA
from backend.services.email_service import email_service


def main():
    # If recipient not provided, use configured Gmail user if available
    if len(sys.argv) < 2:
        recipient = getattr(email_service, 'gmail_user', None)
        if not recipient:
            print("Usage: python examples/run_email_headless.py recipient@example.com")
            sys.exit(1)
        print(f"No recipient argument provided — defaulting to configured Gmail user: {recipient}")
    else:
        recipient = sys.argv[1]
    print(f"Sending test email to: {recipient}")

    result = email_service.send_analysis_report(
        recipient_email=recipient,
        risk_level=SAMPLE_DATA["risk_level"],
        summary=SAMPLE_DATA["summary"],
        total_flagged_amount=SAMPLE_DATA["total_flagged_amount"],
        flags=SAMPLE_DATA["flags"],
        recommendations=SAMPLE_DATA["recommendations"],
        visualizations=None,
        document_name=SAMPLE_DATA.get("document_name")
    )

    # Print result as JSON (don't include secrets)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
