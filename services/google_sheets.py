import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_sheet():
    # Google Spreadsheet ID from environment variables
    spreadsheet_id = os.environ["SPREADSHEET_ID"]

    # Automatically select the current month using India time.
    # Example:
    # August  -> "August"
    # September -> "September"
    # October -> "October"
    worksheet_name = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%B")

    # Find the project root directory
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # Google service account JSON file
    credentials_file = os.path.join(
        project_root,
        "credentials",
        "google-service-account.json",
    )

    # Authenticate with Google
    credentials = Credentials.from_service_account_file(
        credentials_file,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    # Open the spreadsheet
    spreadsheet = client.open_by_key(spreadsheet_id)

    # Open the current month's worksheet
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