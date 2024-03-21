import json

import reportGenerator
import json
from openai import OpenAI
from blocks.excelManager import ExcelManager
from blocks.analyzeTable import tableAnalysis
from blocks.reportTable import tableReporting
from blocks.reportSections import summary, methodology, References, introduction
from docx import Document
#clean the cache in the code



report_name = input("What is the name of the report? ")
reportGenerator.docFile = f"report\\{report_name}.docx"
product_name = input("What is the name of the product? ")
# jsonPath = f"settings_{report_name}.json"
company_name = input("What is the name of the company? ")
report_purpose = input("What is the purpose of the report? ")

back_bone_json = 'settings.json'
new_json = f"settings_{report_name}.json"

if 'risk assesment' or 'analyze' in report_purpose:
    report_purpose = "The target company has requested a risk assessment of the ingredients in their product. "
    back_bone_json = 'settings_cleanery_2.json'
elif 'most' or 'least' or 'best' or 'worst' in report_purpose:
    report_purpose = "The target company has requested a comparison of the ingredients in their product. "
    back_bone_json = 'settings.json'
    #report_generation_order = ['tableAnalysis', 'tableReporting', 'summary', 'methodology', 'References']

# Create a Python dictionary with your data
data = {
    "target": {
        "title": "Target product and company for this report:",
        "product": product_name,
        "company": company_name,
        "purpose": report_purpose
    }

}
print('The backbone json file is: ', back_bone_json)
with open(back_bone_json) as f:
    settings = json.load(f)

settings['target']['title'] = data['target']['title']
settings['target']['product'] = data['target']['product']
settings['target']['company'] = data['target']['company']
settings['target']['purpose'] = data['target']['purpose']

with open(new_json, 'w') as f:
    print('Creating the new settings file')
    json.dump(settings, f, indent=4)

reportGenerator.jsonPath = new_json
reportGenerator.main()

# print(data)
