import csv
import subprocess
import os

def createCard(name, powerCost, text, image, hp, shield, sync):
    code = "\\begin{tikzpicture} \n"
    code += "\cardimage{" + image + "} \n"
    code += "\cardtitle{" + name+ "} \n"
    code += "\cardborder{} \n"
    code += "\cardcontent{" + text + "} \n"
    code += "\cardprice{" + str(powerCost) + "} \n"
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

def processCards(baseFile = "ZXhwList", fileName = "hwList.csv"):
    texFile = baseFile + ".tex"
    pdfFile = baseFile + ".pdf"
    f = open(texFile, "w")
    f.write(makeHeader())
    if not os.path.exists(fileName):
        return
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            try:
                powerCost = row['Power Cost']
            except:
                powerCost = ""
            image = row['Image']
            originalText = row['Power Ability']
            text1 = originalText.replace("@__", "\\newline ")
            text2 = replaceText(text1, "A@")
            text3 = text2.replace("@6", "\Money ")
            text = text3
            try:
                hp = row['Health']
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
            if number == "":
                continue
            if row['Card Status'] == "":
                continue
            card = createCard(name, powerCost, text, image, hp, shield, sync)
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
    baseFile = "ZXhwList"
    fileName = "hwList"
    processCards(baseFile, fileName+".csv")
    print(fileName+".csv")

multiProcessor()
