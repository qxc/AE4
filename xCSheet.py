import csv
import subprocess
# Loading the pyPdf Library
from PyPDF2 import PdfFileWriter, PdfFileReader


def createChar(name, hand, deck, breaches, startCard, abilityName, abilityDescription, abilityCost, notes, image):
    code = "\\begin{tikzpicture} \n\cardborder \n\\basicinfo \n"
    code += "\\name{" + name + "}{" + image + "}\n"
    code += "\\ability{" + abilityName+ ": "
    code += abilityDescription + "}{"
    code += abilityCost + "}\n"
    code += "\startingDeck{" + deck[0] + "}{" + deck[1] + "}{" + deck[2] + "}{" + deck[3] + "}{" + deck[4] + "}\n"
    code += "\startingHand{" + hand[0] + "}{" + hand[1] + "}{" + hand[2] + "}{" + hand[3] + "}{" + hand[4] + "}\n"
    code += "\\notes{" + notes + "}\n"
    #print(breaches)
    #1 = D, L = 4, R = 2, U = 3, X = 0, O = 5
    #6 = SD, 7 = SL, 8 = SR, 9 = SU, 10 = SO
    code += "\startingPrep"
    for i in range (0,4):
        if breaches[i] == 0:
            code+= "{}{1}"
        elif breaches[i] == 5:
            code+= "{own" + str(i) + ".png}{1}"
        elif breaches[i] == 6:
            code+= "{specialbreachO.png}{1}"
        elif breaches[i] == 9:
            code+= "{specialbreach0.png}{" + str(breaches[i]%4) + "}"
        elif breaches[i] == 10:
            code+= "{specialbreach0.png}{" + str(breaches[i]%4) + "}"
        elif breaches[i] == 11:
            code+= "{specialbreach0.png}{" + str(breaches[i]%4) + "}"
        elif breaches[i] == 12:
            code+= "{specialbreach0.png}{" + str(breaches[i]%4) + "}"
        else:
            code+= "{rent" + str(i) + ".png}{" + str(breaches[i]) + "}"
            
    #print(code)
    code += "\n\end{tikzpicture}\n"
    return code

def processCards(fileName = "cSheet.csv"):
    #f = open("cSheet.txt", "w")
    pdfFiles = []
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            startCard = row['Starter Name']
            startCard2 = row['Starter Name2']
            hand = []
            hand.append(row['H1'])
            hand.append(row['H2'])
            hand.append(row['H3'])
            hand.append(row['H4'])
            hand.append(row['H5'])
            hand = processStart(hand,startCard, startCard2)
            deck = []
            deck.append(row['D1'])
            deck.append(row['D2'])
            deck.append(row['D3'])
            deck.append(row['D4'])
            deck.append(row['D5'])
            deck = processStart(deck,startCard, startCard2)
            breaches = []
            breaches.append(row['B1'])
            breaches.append(row['B2'])
            breaches.append(row['B3'])
            breaches.append(row['B4'])
            breaches = processBreaches(breaches)
            abilityName = row['Ability Name']
            abilityDescription = row['Ability Description']
            abilityCost = row['Ability Cost']
            notes = row['Notes']
            image = row['Image']
            if row['Card Status'] == "":
                continue
            char = createChar(name, hand, deck, breaches, startCard, abilityName, abilityDescription, abilityCost, notes, image)
            makePDF(name,char)
            pdfName = "charSheet" + name + ".pdf"
            pdfFiles.append(pdfName)
            #f.write(char)
    # Creating an object where pdf pages are appended to
    output = PdfFileWriter()
    for pdfName in pdfFiles:
        # Appending two pdf-pages from two different files
        append_pdf(PdfFileReader(open(pdfName,"rb")),output)
    # Writing all the collected pages to a file
    finalFileName="ZxcharSheetsAll.pdf"
    output.write(open(finalFileName,"wb"))
    subprocess.Popen([finalFileName],shell=True)
    return

def processStart(hand,startCard, startCard2):
    for i in range(0,5): 
        if hand[i] == 'C':
            hand[i] = 'Crystal'
        if hand[i] == 'S':
            hand[i] = 'Spark'
        if hand[i] == 'U':
            hand[i] = startCard
        if hand[i] == 'U2':
            hand[i] = startCard2
            

    return hand

def processBreaches(breaches):
    for i in range (0,4):
        if breaches[i] == 'D':
            breaches[i] = 1
        if breaches[i] == 'L':
            breaches[i] = 4
        if breaches[i] == 'R':
            breaches[i] = 2
        if breaches[i] == 'U':
            breaches[i] = 3
        if breaches[i] == 'X':
            breaches[i] = 0
        if breaches[i] == 'O':
            breaches[i] = 5
        if breaches[i] == 'SD':
            breaches[i] = 9
        if breaches[i] == 'SR':
            breaches[i] = 10
        if breaches[i] == 'SU':
            breaches[i] = 11
        if breaches[i] == 'SL':
            breaches[i] = 12
        if breaches[i] == 'SO':
            breaches[i] = 6
#1 = D, L = 4, R = 2, U = 3, X = 0, O = 5
    return breaches

def makePDF(name, char):
    fileName = "charSheet" + name + ".tex"
    f = open(fileName, "w")
    f.write("\\nonstopmode\n\input{charBoard.tex}\n\\begin{document}\n")
    f.write(char)
    f.write("\n \end{document}")
    f.close()
    compileFile(fileName)
    

def compileFile(fileName):
    proc=subprocess.Popen(['pdflatex',fileName])
    proc.communicate()



# Creating a routine that appends files to the output file
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


processCards()
