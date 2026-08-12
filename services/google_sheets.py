import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

def get_sheet():
    spreadsheet_id = os.environ["SPREADSHEET_ID"]

    worksheet_name = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%B")

    credentials_json = os.getenv("GOOGLE_CREDENTIALS")

    if credentials_json:
        credentials = Credentials.from_service_account_info(
            json.loads(credentials_json),
            scopes=SCOPES,
        )
    else:
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        credentials_file = os.path.join(
            project_root,
            "credentials",
            "google-service-account.json",
        )

        credentials = Credentials.from_service_account_file(
            credentials_file,
            scopes=SCOPES,
        )

    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)

    return spreadsheet.worksheet(worksheet_name)

def append_transaction(
    date: str,
    item: str,
    amount: str,
    transaction_type: str,
    description: str,
):
    sheet = get_sheet()

    # Determine the row that will be appended
    next_row = len(sheet.get_all_values()) + 1

    # Put the amount in the correct column
    expense = amount if transaction_type == "expense" else ""
    income = amount if transaction_type == "income" else ""

    # Running balance formula
    remaining_formula = (
        f'=IF(OR(C{next_row}<>"",D{next_row}<>""),'
        f'SUM($D$2:INDEX(D:D,ROW()))-'
        f'SUM($C$2:INDEX(C:C,ROW())),"")'
    )

    # Column order:
    # Date | Item | Expenses | Income | Remaining | Description | Category
    row = [
        date,
        item,
        expense,
        income,
        remaining_formula,
        description,
        "",
    ]

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED",
    )