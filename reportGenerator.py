import json
from openai import OpenAI
from blocks.excelManager import ExcelManager
from blocks.analyzeTable import tableAnalysis
from blocks.reportTable import tableReporting
from blocks.reportSections import summary, methodology, References, introduction
from docx import Document



docFile = "report\\Report_cleanery.docx"

document = Document()

jsonPath = "settings_cleanery_2.json"
with open(jsonPath) as f:
    settings = json.load(f)









clientOpenAI = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=settings['openAI']['apikey']
)

excelMan = ExcelManager()

generationBlocks = []
generationBlockTypes = []
for blk in settings["report_generation_order"]:
    blockType = settings[blk]['blockType']
    print(f"Working on: {blk}    - CHAT-GPT API")

    if blockType == 'tableAnalysis':
        tableAnalysisBlock = tableAnalysis(settings[blk], settings)
        tableAnalysisBlock.generateTablePrompts(excelMan)
        tableAnalysisBlock.analyzeGPT(clientOpenAI)
        generationBlocks.append(tableAnalysisBlock)
        generationBlockTypes.append('tableAnalysis')

    if blockType == "tableReporting":
        tableReportingBlock = tableReporting(settings[blk], settings)
        tableReportingBlock.generateTablePrompts(excelMan)
        tableReportingBlock.analyzeGPT(clientOpenAI)
        generationBlocks.append(tableReportingBlock)
        generationBlockTypes.append('tableReporting')

    if blockType == "summary":
        summaryBlock = summary(settings[blk], settings)
        summaryBlock.generateSummaryPrompts(generationBlocks)
        summaryBlock.summarizeGPT(clientOpenAI)
        generationBlocks.append(summaryBlock)
        generationBlockTypes.append('summary')

    if blockType == "introduction":
        introductionBlock = introduction(settings[blk], settings)
        introductionBlock.generateIntroPrompts(generationBlocks)
        introductionBlock.introGPT(clientOpenAI)
        generationBlocks.append(introductionBlock)
        generationBlockTypes.append('introduction')

    if blockType == "references":
        referencesBlock = References(settings[blk], settings)
        generationBlocks.append(referencesBlock)
        generationBlockTypes.append('references')

print(f"Generating the Document Now!")
# Generating The Report HERE!!!
for i in range(len(generationBlockTypes)):
    if generationBlockTypes[i] == 'summary':
        generationBlocks[i].generateReport(document)

for i in range(len(generationBlockTypes)):
    if generationBlockTypes[i] == 'introduction':
        generationBlocks[i].generateReport(document)


# Generating The Methodology!!!
methBlock = methodology(settings)
methBlock.generateReport(document)


# Generating Table Reporting!
for i in range(len(generationBlockTypes)):
    if generationBlockTypes[i] == 'tableReporting':
        generationBlocks[i].generateReport(document)


# Generating Table Analysis!
document.add_heading("Results")
for i in range(len(generationBlockTypes)):
    if generationBlockTypes[i] == 'tableAnalysis':
        generationBlocks[i].generateReport(document,excelManager=excelMan)


# Adding The References
document.add_heading("References")
for i in range(len(generationBlockTypes)):
    if generationBlockTypes[i] == 'references':
        generationBlocks[i].generateReport(document,excelManager=excelMan)


document.save(docFile)
print("Report Has Been Generated!!!")






