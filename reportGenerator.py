import json
from openai import OpenAI
from blocks.excelManager import ExcelManager
from blocks.analyzeTable import tableAnalysis
from blocks.reportTable import tableReporting
from blocks.reportSections import summary, methodology, References, introduction, conclusion
from docx import Document
import os

docFile = "report\\Report_cleanery.docx"

document = Document()
headings=[]
#jsonPath = "settings_cleanery_2.json"
jsonPath = "settings_cleanery_2.json"
#optionsjson = 'options.json'
portfolios= []
choice = ''  # 0 for simple, 1 for simple_1, 2 for simple_2


def main():
    # ask for the order of presentation

    with open(jsonPath) as f:
        settings = json.load(f)
    """
    with open(optionsjson) as f:
        options = json.load(f)
    report_headings = options[choice]["report_style"]
    """

    clientOpenAI = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=settings['openAI']['apikey']
    )

    excelMan = ExcelManager()

    generationBlocks = []
    generationBlockTypes = []
    for blk in settings["report_generation_order"]:
        print(blk)
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

        if blockType == "conclusion":
            conclusionBlock = conclusion(settings[blk], settings)
            conclusionBlock.generateConclusionPrompts(generationBlocks)
            conclusionBlock.ConcludeGPT(clientOpenAI)
            generationBlocks.append(conclusionBlock)
            generationBlockTypes.append('conclusion')

        if blockType == "references":
            referencesBlock = References(settings[blk], settings)
            generationBlocks.append(referencesBlock)
            generationBlockTypes.append('references')

    print(f"Generating the Document Now!")

    lwr_headings= [heading.lower() for heading in headings]

    print(lwr_headings)
    for heading in lwr_headings:
        print(heading)
        if heading == 'summary':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'summary':
                    generationBlocks[i].generateReport(document)
                    #lwr_headings.remove('summary')
        if heading == 'introduction':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'introduction':
                    generationBlocks[i].generateReport(document)
                    #lwr_headings.remove('introduction')
        if heading == 'methodology':
            methBlock = methodology(settings)
            methBlock.generateReport(document)
            #lwr_headings.remove('methodology')
        if heading == 'results':

            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'tableReporting':
                    generationBlocks[i].generateReport(document)
                    #lwr_headings.remove('results')
        if heading == 'conclusion':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'conclusion':
                    generationBlocks[i].generateReport(document)
                    #lwr_headings.remove('conclusion')


    """
    for headings in lwr_headings:
        print(headings)
        if headings == 'summary':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'summary':
                    generationBlocks[i].generateReport(document)
                    lwr_headings.remove('summary')
        if headings == 'introduction':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'introduction':
                    generationBlocks[i].generateReport(document)
                    lwr_headings.remove('introduction')
        if headings == 'methodology':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'methodology':
                    generationBlocks[i].generateReport(document)
                    lwr_headings.remove('methodology')
        if headings == 'results':
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'tableReporting':
                    generationBlocks[i].generateReport(document)
                    lwr_headings.remove('results')

    
    for i in range(len(generationBlockTypes)):
        print(f'Heading:{i}', generationBlockTypes[i])
        if generationBlockTypes[i] in lwr_headings and generationBlockTypes[i] != 'results':
            print('Putting into word under heading:', generationBlockTypes[i])
            generationBlocks[i].generateReport(document)
            generationBlockTypes.remove(generationBlockTypes[i])
   
    
    
    for heading in report_headings:
        if heading not in ['Introduction', 'Summary', 'Methodology', 'Results', 'Conclusion', 'References']:
            print(f"Invalid Heading: {heading}")
            print("Program Terminating")
            exit()

        for i in range(len(generationBlockTypes)):
            print(f'Heading:{i}', generationBlockTypes[i])
            if generationBlockTypes[i] == heading.lower() and heading  'Results':
                print('Putting into word under heading:', heading)
                generationBlocks[i].generateReport(document)
                report_headings.remove(heading)
            if heading == 'Results':
                if generationBlockTypes[i] == 'tableReporting':
                    generationBlocks[i].generateReport(document)
               
                if generationBlockTypes[i] == 'tableAnalysis':
                    generationBlocks[i].generateReport(document, excelManager=excelMan)
               

        if heading == 'Introduction' and intro == False:
            intro = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'introduction':
                    generationBlocks[i].generateReport(document)
        if heading == 'Summary' and summ == False:
            summ = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'summary':
                    generationBlocks[i].generateReport(document)
        if heading == 'Methodology' and meth == False:
            meth = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'methodology':
                    generationBlocks[i].generateReport(document)
        if heading == 'Results' and res_1 == False or res_2 == False:
            res_1 = True
            res_2 = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'tableReporting':
                    generationBlocks[i].generateReport(document)
               
                if generationBlockTypes[i] == 'tableAnalysis':
                    generationBlocks[i].generateReport(document, excelManager=excelMan)
                
        if heading == 'Conclusion' and conc == False:
            conc = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'conclusion':
                    generationBlocks[i].generateReport(document)
        if heading == 'References' and ref == False:
            ref = True
            for i in range(len(generationBlockTypes)):
                if generationBlockTypes[i] == 'references':
                    generationBlocks[i].generateReport(document, excelManager=excelMan)
        """

    document.save(docFile)
    print("Report Has Been Generated!!!")
    os.remove(jsonPath)

# main()
