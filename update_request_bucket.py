import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-token.json', scope)
client = gspread.authorize(creds)

req_bucket = client.open('Project_Goodall').worksheet("Request_Bucket")

matric_list = []
tele_id_list = []

# Function to sync with matric on spreadsheet
def getLatestMatric():
    print("Getting the latest matric from sheet...")

    matric_list = list(req_bucket.col_values(2))
    return matric_list

# Function to sync with tele_id on spreadsheet
def getLatestUsername():
    print("Getting the latest tele_id from sheet...")

    tele_id_list = list(req_bucket.col_values(1))
    
    return tele_id_list

# Function to insert data to spreadsheet
def addMatric(telegram_id,matric):
    print("Add Spreadsheet")
    new_data = [telegram_id,matric]
    lastRow = req_bucket.col_values(1)
    req_bucket.insert_row(new_data, len(lastRow)+1)

# Function to delete last data from spreadsheet
def popMatric():
    print("Pop Spreadsheet")
    lastRow = req_bucket.col_values(1)
    req_bucket.update_cell(len(lastRow), 1, "") # 1 is the tele_id
    req_bucket.update_cell(len(lastRow), 2, "") # 2 is the matric