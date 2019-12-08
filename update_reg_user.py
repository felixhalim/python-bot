import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-token.json', scope)
client = gspread.authorize(creds)

registered_user = client.open('Project_Goodall').worksheet("Registered_User")

Dictionary={}

# Function to sync with data on spreadsheet
def getLatestData():
    tele_id_list = registered_user.col_values(1)
    matric_list = registered_user.col_values(2)
    name_list = registered_user.col_values(3)
    counter_help_list = registered_user.col_values(4)
    bool_donate_list = registered_user.col_values(5)
    index_list = registered_user.col_values(6)
    value_list = list(map(list, zip(matric_list,name_list,counter_help_list,bool_donate_list,index_list)))
    Dictionary.update(dict(zip(tele_id_list, value_list)))

    return Dictionary

# Function to alter data on spreadsheet
def setData(telegram_id,index_dict,value):
    if(index_dict=="bool_donate"):
        index_dict=3
    elif(index_dict=="counter_help"):
        index_dict=2
    row_dict = Dictionary[telegram_id][4] # 4 is the index in terms of row
    registered_user.update_cell(int(row_dict)+2, int(index_dict)+2, value) # +2 offset based on spreadsheet

