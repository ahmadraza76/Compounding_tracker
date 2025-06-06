# app/utils/export_utils.py
from openpyxl import Workbook
from io import BytesIO
from app.utils.data_utils import get_user_data
from app.utils.calculation_utils import calculate_compounding

def generate_excel_report(user_id: str) -> BytesIO:
    """Generate Excel report for user progress."""
    user_data = get_user_data(user_id)
    if not user_data.get("history"):
        return None

    language = user_data.get("language", "en")
    currency = user_data.get("currency", "₹")
    target = user_data.get("target", {})
    start_date = user_data.get("start_date")
    history = user_data.get("history", [])
    stoploss = user_data.get("stoploss")

    wb = Workbook()
    ws = wb.active
    ws.title = "Progress Report"

    # Headers
    headers = [
        "Date" if language == "en" else "तारीख",
        "Balance" if language == "en" else "बैलेंस",
        "Expected Balance" if language == "en" else "अपेक्षित बैलेंस",
        "Stop-Loss Status" if language == "en" else "स्टॉप-लॉस स्थिति"
    ]
    ws.append(headers)

    # Data
    for entry in history:
        date = entry["date"]
        balance = entry["balance"]
        days_passed = (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        expected_balance = calculate_compounding(
            float(target.get("start_amount", 0)),
            float(target.get("rate", 0)),
            target.get("mode", "daily"),
            days_passed
        ) if target else 0.0
        stoploss_status = ""
        if stoploss and target:
            stoploss_level = float(target["start_amount"]) * (1 - stoploss / 100)
            stoploss_status = ("Triggered" if language == "en" else "ट्रिगर हुआ") if balance < stoploss_level else ("Safe" if language == "en" else "सुरक्षित")
        ws.append([date, f"{currency}{balance:,.2f}", f"{currency}{expected_balance:,.2f}", stoploss_status])

    # Save to BytesIO
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
