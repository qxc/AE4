import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def SetupCreds(docid):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(docid)
    #print(spreadsheet.worksheets())
    return spreadsheet

def GetSpecificSheet(spreadsheet, name):
    return spreadsheet.worksheet(name)

def MakeSheetsAr(spreadsheet, toGet):
    ar = []
    for i in toGet:
        ar.append(GetSpecificSheet(spreadsheet,i))
    return ar

def WriteSheets(sheets, names):
    i = 0
    for w in sheets:
        filename = names[i] + '.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(w.get_all_values())
        i = i+1

def SetNames():
    nm1 = "cdList"
    nm2 = "cdList2"
    nm3 = "cdList3"
    nm4 = "bSheet"
    nm5 = "cSheet"
    return [nm1,nm2,nm3,nm4,nm5]

def SheetsToGet():
    sht1 = "Player Cards"
    sht2 = "Nemesis Cards"
    sht3 = "Starter Cards"
    sht4 = "Nemesis"
    sht5 = "Mages"
    return [sht1,sht2,sht3,sht4,sht5]

def Main():
    sheet = SetupCreds("1MiEktIMmlscJO66mtLwFz2gXhQgJ-I2yMyi7Fi_EcfA")    
    toGet = SheetsToGet()
    shtsAr = MakeSheetsAr(sheet,toGet)
    WriteSheets(shtsAr,SetNames())

#GetSheets(sheet)
#print(GetSpecificSheet(sheet, "Player Cards"))

Main()
