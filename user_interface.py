import json

import reportGenerator
import json
from openai import OpenAI
from blocks.excelManager import ExcelManager
from blocks.analyzeTable import tableAnalysis
from blocks.reportTable import tableReporting
from blocks.reportSections import summary, methodology, References, introduction
from docx import Document
import sys
import pandas as pd
import os

# clean the cache in the code

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

title_img = Image.open('title_bg2.png')
fnt = ImageFont.truetype("arial.ttf", 50, encoding="unic")
fnt_date = ImageFont.truetype("arial.ttf", 30, encoding="unic")
d = ImageDraw.Draw(title_img)
from reportGenerator import appendix_data

report_name = input("What is the name of the report? ")
reportGenerator.docFile = f"report\\{report_name}.docx"
product_name = input("What is the name of the product? ")
# jsonPath = f"settings_{report_name}.json"
company_name = input("What is the name of the company? ")
report_purpose = input("What is the purpose of the report? ")

# report_purpose = input("What is the purpose of the report? ")
d.multiline_text((10, 600), f"Chemical\n Analysis\n {report_name}", font=fnt, fill=(255, 255, 255))
d.multiline_text((10, 800), today, font=fnt_date, fill=(255, 255, 255))
title_img.save(f'title_bg2_{report_name}.png')
reportGenerator.title_img = f'title_bg2_{report_name}.png'
back_bone_json = 'settings.json'
new_json = f"settings_{report_name}.json"

# ask for the kind of reports
with open('options.json') as f:
    options = json.load(f)
structures = []

print("the report can have the following styles")
print("0: ‘Summary’, ‘Introduction’, ‘Methodology’, ‘Results’, ‘Conclusion’")
print("1: ‘Summary’, ‘Results’, ‘Conclusion’ ")
print("2: ‘Introduction’, ‘Methodology’, ‘Results’, ‘Conclusion’, ‘Summary’")

report_structure = input("What is the report structure you want? ")
back_bone_json = 'settings_cleanery_2.json'

print('The backbone json file is: ', back_bone_json)
with open(back_bone_json) as f:
    settings = json.load(f)

if report_structure == '0':
    report_generation_order_backbone = options['simple']['report_generation_order_backbone']
    print('The backbone report generation order is: ', report_generation_order_backbone)
    reportGenerator.headings = ['summary', 'introduction', 'methodology', 'results', 'conclusion']
    reportGenerator.choice = 'simple'
elif report_structure == '1':
    report_generation_order_backbone = options['simple_1']['report_generation_order_backbone']
    print('The backbone report generation order is: ', report_generation_order_backbone)
    reportGenerator.choice = 'simple_1'
    reportGenerator.headings = ['summary', 'results', 'conclusion']
elif report_structure == '2':
    report_generation_order_backbone = options['simple_2']['report_generation_order_backbone']
    print('The backbone report generation order is: ', report_generation_order_backbone)
    reportGenerator.choice = 'simple_2'
    reportGenerator.headings = ['introduction', 'methodology', 'results', 'conclusion', 'summary']
else:
    print("Invalid input. Please try again")
    sys.exit()
number_of_portfolio_analysis = int(input("How manu chemical portfolios do you want to analyze?"))
actual_report_generation_order = []
for i in range(number_of_portfolio_analysis):
    portfolio_name = input("What is the name of the portfolio? ")
    reportGenerator.portfolios.append(portfolio_name)
    portfolio_description = input("What is the description of the portfolio? ")
    portfolio_excel = input(f"Path to the excel for {portfolio_name}? ")
    weightages = pd.read_excel('excels\\'+portfolio_excel, sheet_name='Graph&Weightings', skiprows=range(1, 55))
    reportGenerator.appendix_data = pd.concat([reportGenerator.appendix_data, weightages], axis=0)
    for elements in report_generation_order_backbone:
        if elements == 'reportTable':
            name_of_block = 'reportTable' + portfolio_name

            actual_report_generation_order.append(name_of_block)
            data = {
                name_of_block: {
                    "blockType": "tableReporting",
                    "excel": "excels\\" + portfolio_excel,
                    "title": portfolio_name.title() + " used in Analysis:",
                    "userPrompts": [
                        "The provided table includes only " + portfolio_name,
                        "Dont include headings, or bullets, just give two paragraph response"
                    ]
                }

            }
            settings[name_of_block] = data[name_of_block]

        if elements == 'analyzeTable':
            name_of_block = 'analyzeTable' + portfolio_name
            actual_report_generation_order.append(name_of_block)

            data = {
                name_of_block: {
                    "blockType": "tableReporting",
                    "excel": "excels\\" + portfolio_excel,
                    "title": portfolio_name.title() + " used in Analysis",
                    "bubbleChart": {
                        "generate": True,
                        "type": "rankBubbles"
                    },
                    "userPrompts": [
                        "The provided table includes only " + portfolio_name,
                        "Dont include headings, or bullets, just give two paragraph response"
                    ]
                }

            }
            settings[name_of_block] = data[name_of_block]

if report_structure == '0' or '2':
    actual_report_generation_order.append("finalSummary")
    data = {
        "finalSummary": {
            "blockType": "summary",
            "userPrompts": [
                "Generate two paragraphs summary for this analysis report, the paragram should have more than 12 lines",
                "Start your response with something specific to the target company and product. ideas: {report generator company} did a complete analysis report for the target Product of target company based on these measures etc"
            ]
        }
    }

    settings['finalSummary'] = data['finalSummary']
    actual_report_generation_order.append("finalIntroduction")
    data = {
        "finalIntroduction": {
            "blockType": "introduction",
            "userPrompts": [
                "Generate two paragraphs introduction for this analysis report, the paragram should have more than 12 lines",
                "Start your response with something specific to the target company and product. ideas: {report generator company} did a complete analysis report for the target Product of target company based on these measures etc"
            ]
        }
    }

    settings['finalIntroduction'] = data['finalIntroduction']
    actual_report_generation_order.append("finalConclusion")
    data = {
        "finalConclusion": {
            "blockType": "conclusion",
            "userPrompts": [
                "Generate two paragraphs conclusion for this analysis report, the paragram should have more than 12 lines",
                "Start your response with something specific to the target company and product. ideas: {report generator company} did a complete analysis report for the target Product of target company based on these measures etc"
            ]
        }
    }

    settings['finalConclusion'] = data['finalConclusion']

    # actual_report_generation_order.append('methodology')

elif report_structure == '1':
    actual_report_generation_order.append("finalSummary")
    data = {
        "finalSummary": {
            "blockType": "summary",
            "userPrompts": [
                "Generate two paragraphs summary for this analysis report, the paragram should have more than 12 lines",
                "Start your response with something specific to the target company and product. ideas: {report generator company} did a complete analysis report for the target Product of target company based on these measures etc"
            ]
        }
    }
    settings['finalSummary'] = data['finalSummary']
    # actual_report_generation_order.append("finalConclusion")
    data = {
        "finalConclusion": {
            "blockType": "conclusion",
            "userPrompts": [
                "Generate two paragraphs introduction for this analysis report, the paragram should have more than 12 lines",
                "Start your response with something specific to the target company and product. ideas: {report generator company} did a complete analysis report for the target Product of target company based on these measures etc"
            ]
        }
    }
    actual_report_generation_order.append("finalConclusion")

print('The actual report generation order is: ', actual_report_generation_order)

# Create a Python dictionary with your data
data = {
    "target": {
        "title": "Target product and company for this report:",
        "product": product_name,
        "company": company_name,
        "purpose": report_purpose
    }

}

settings['target']['title'] = data['target']['title']
settings['target']['product'] = data['target']['product']
settings['target']['company'] = data['target']['company']
settings['target']['purpose'] = data['target']['purpose']
settings['report_generation_order'] = actual_report_generation_order

with open(new_json, 'w') as f:
    print('Creating the new settings file')
    json.dump(settings, f, indent=5)

reportGenerator.jsonPath = new_json
reportGenerator.main()
# os.remove(new_json)

# print(data)
