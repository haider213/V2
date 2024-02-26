# This Class Manages Excel Files and Sheets and Handles Excel Requests!
import sys
import pandas as pd 

# This class is responsible for Updating and Managing Excel Sheets!
class ExcelManager:
    def __init__(self):
        self.sheets = list()

    def requestSheet(self, excelFile, sheetName):
        # If The Sheet was read Previously! Find it and return the dataframe
        for item in self.sheets:
            if item['fileName'] == excelFile and item['sheetName'] == sheetName:
                #print("Just Returning The Previous")
                return item['table']
        
        # Otherwise Read The File
        try: 
            #print("Reading AGAIN")
            df = pd.read_excel(io=excelFile, sheet_name=sheetName)
            self.sheets.append({
                'fileName': excelFile, 
                'sheetName':sheetName,
                'table': df
            })
        except Exception as error:
            print(error)
            print("Program Failed to Read The Excel Sheet, and Received the above ERROR!")
            print("Recheck if the excel File is present and the name in system.json is correct")
            print("Recehck if the sheet name is correct")            
            print("Program is Terminating")
            sys.exit()
        # Returning The Table which was just Read by the Program!
        return df
