import shutil, pathlib
from datetime import datetime
from pathlib import Path
from shutil import copytree, ignore_patterns
from googleapiclient.discovery import build # pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.oauth2 import service_account


serviceAccountFile = '../creds.json' # generated from Google Cloud Platform
destination = 'C:/Users/k2wang/Desktop/py/myScripts/scaScansStats/destination/for_matt/' # or whatever the destination path is

# communicates with Google API to interact with spreadsheet
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(serviceAccountFile, scopes = scope)
sheetId = '1Rk5pAlcaNv-Zc2Ca4xtd-uRrGmucWrG2pxLgQG8-j8s' # Stats spreadsheet ID
service = build('sheets', 'v4', credentials = creds)
sheet = service.spreadsheets()

# copy folder and tiff files to destination and ignore cr2 files
for folder in Path().iterdir():
    if folder.is_dir():
        dest = destination + str(folder)
        shutil.copytree(folder, dest, ignore = ignore_patterns('*.cr2')) # ignores raws
        
        # count how many tiff files are in each folder
        numFiles = 0
        for path in pathlib.Path(dest).iterdir():
            if path.is_file():
                numFiles += 1
        
        # add up the total file sizes in gb
        size = sum(f.stat().st_size for f in folder.glob('**/*.tif') if f.is_file())
        folderSize = round((size / 1024 / 1024 / 1024), 3) # rounds to 3 decimals
        
        # get creation date of original folder
        unixTime = folder.stat()[-1]
        
        date = str(datetime.fromtimestamp(unixTime).strftime('%Y%m%d'))
        bibCallBarcode = str(folder)
        numOfMaster = str(numFiles)
        masterFileSize = str(folderSize)

        stat = [[date,'',bibCallBarcode,'Still_Image','','TIFF',numOfMaster,masterFileSize,'','','','','DLDP','One-off','','']]

        # update Stats sheet with info
        request = sheet.values().append(spreadsheetId = sheetId, 
                                                range = 'Log!A1:P1', 
                                     valueInputOption = 'USER_ENTERED', 
                                     insertDataOption = 'INSERT_ROWS', 
                                                 body = {'values':stat}
                                                    )
        response = request.execute()
        print(response)



