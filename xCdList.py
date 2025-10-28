import csv
import subprocess
import os

def createCard(name, cardType, cost, text, image,hp, shield, devCost, sync):
    code = "\\begin{tikzpicture} \n\cardbackground{" +cardType+ "} \n"
    code += "\cardimage{" + image + "} \n"
    code += "\cardtitle{" + name+ "} \n"
    code += "\cardborder{} \n"
    code += "\cardcontent{" + text + "} \n"
    code += "\cardprice{" + str(cost) + "} \n"
    if devCost != "":
        code += "\carddevcost{" + devCost + "} \n"
    if hp != "":
        code += "\cardhp{" + hp + "} \n"
    if shield != "":
        code += "\cardshield{" + shield + "} \n"
    code += "\sync{" + sync + "}\n"
    code += "\end{tikzpicture}\n\hspace{-4mm}\n"
    return code

def createStoryCard(name, text):
    code = "\\begin{tikzpicture} \n\cardbackground{""} \n"
    code += "\cardtitle{" + name+ "} \n"
    code += "\cardborder{} \n"
    code += "\cardstorycontent{" + text + "} \n"
    code += "\end{tikzpicture}\n\hspace{-4mm}\n"
    return code

def replaceText(text, charsToRemove):
    return text.replace(charsToRemove, "")

def processCards(baseFile = "ZXcList", fileName = "cdList.csv"):
    texFile = baseFile + ".tex"
    pdfFile = baseFile + ".pdf"
    numCards = 0
    f = open(texFile, "w")
    f.write(makeHeader())
    if not os.path.exists(fileName):
        return
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name Of card']
            cost = row['cost']
            cardType = row['type'].capitalize()
            image = row['Image']
            originalText = row['description']
            text1 = replaceText(originalText, "@__")
            text2 = replaceText(text1, "A@")
            text3 = text2.replace(" newline", " \\newline")
            text = text3
            try:
                hp = row['HP']
            except:
                hp = ""
            try:
                shield = row['Shield']
            except:
                shield = ""
            try:
                devCost = row['Development Cost']
            except:
                devCost = ""
            try:
                sync = row ['Sync']
            except:
                sync = ""
            try:
                number = row['Supply']
            except:
                number = 1
            if number == "":
                continue
            if cardType == "":
                continue
            if row['Card Status'] == "":
                continue
            if cardType == "Story":
                card = createStoryCard(name, text)
            else:
                card = createCard(name, cardType, cost, text,image, hp, shield, devCost, sync)
            f.write(card*int(number))
            numCards += int(number)
    if numCards % 3 == 2:
        card = createCard("Blank", "", "", "","", "", "", "", "")
        f.write(card)
    f.write("\end{center}\n\end{document}")
    f.close()
    compileFile(texFile)
    subprocess.Popen([pdfFile],shell=True)
    return

def makeHeader():
    header = "\\documentclass{article}\n\\nonstopmode\n\input{libs.tex}"
    header +="\n\input{colors.tex}\n\input{tikzcardsTwo.tex}"
    header +="\n\\begin{document}\n\\begin{center}"
    return header

def compileFile(fileName):
    proc=subprocess.Popen(['pdflatex',fileName])
    proc.communicate()

def multiProcessor():
    baseFile = "ZXcList"
    fileName = "cdList"
    numFiles = input("Number of files to run:? ")
    for i in range(int(numFiles)):
        processCards(baseFile+str(i), fileName+str(i)+".csv")
        print(fileName+str(i)+".csv")

multiProcessor()
