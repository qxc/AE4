import csv
import subprocess
import os

def createCard(name, cardType, cost, text, image,hp, shield, sync, afterburn, supplyDeck, levelNum, minionBonus, playerCount):
    code = "\\begin{tikzpicture} \n\cardbackground{" +cardType+ "} \n"
    code += "\cardimage{" + image + "} \n"
    code += "\cardtitle{" + name+ "} \n"
    code += "\cardborder{} \n"
    code += "\cardcontent{" + text + "} \n"
    code += "\cardprice{" + str(cost) + "} \n"
    if levelNum != "":
        code += "\levelNum{" + str(levelNum) + "} \n"
    if minionBonus != "":
        code += "\minionBonus{" + str(minionBonus) + "} \n"
    if hp != "":
        code += "\cardhp{" + hp + "} \n"
    if shield != "":
        code += "\cardshield{" + shield + "} \n"
    code += "\sync{" + sync + "}\n"
    if afterburn != "":
        code += "\myburn{" + afterburn + "} \n"
    if supplyDeck != "":
        code += "\supplyDeck{" + supplyDeck + "} \n"
    if playerCount != "":
        code += "\playerCount{" + playerCount + "} \n"
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
    f = open(texFile, "w")
    f.write(makeHeader())
    if not os.path.exists(fileName):
        return
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Card Status'] == "":
                continue
            name = row['Name Of Card']
            try:
                cost = row['Cost']
            except:
                cost = ""
            try:
                cardType = row['Type'].capitalize()
            except:
                cardType = ""
            image = row['Image']
            originalText = row['Description']
            text1 = originalText.replace("@__", "\\newline ")
            text2 = replaceText(text1, "A@")
            text3 = text2.replace("@6", "\Money ")
            text4 = text3.replace(" newline", " \\newline")
            text = text4
            try:
                supplyDeck = row['Supply Deck']
            except: supplyDeck = ""
            try:
                afterburn = row['Afterburn Text']
            except: afterburn = ""
            try:
                hp = row['HP']
            except:
                hp = ""
            try:
                shield = row['Shield']
            except:
                shield = ""
            try:
                sync = row ['Sync']
            except:
                sync = ""
            try:
                number = row['Supply']
            except:
                number = 1
            try:
                levelNum = row['LevelNum']
            except:
                levelNum = ""
            try:
                minionBonus = row['Minion Bonus']
            except:
                minionBonus = ""
            try:
                playerCount = row['Player Count']
            except:
                playerCount = ""
            if number == "":
                continue
            card = createCard(name, cardType, cost, text, image, hp, shield, sync, afterburn, supplyDeck, levelNum, minionBonus, playerCount)
            f.write(card*int(number))
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
