import csv
import subprocess

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
    
def processCards(fileName = "cdList3.csv"):
    baseFile = "ZXcList3"
    texFile = baseFile + ".tex"
    pdfFile = baseFile + ".pdf"
    f = open(texFile, "w")
    f.write(makeHeader())
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name of card']
            cost = row['cost']
            cardType = row['type'].capitalize()
            image = row['Image']
            text = row['description']
            hp = row['HP']
            shield = row['Shield']
            devCost = row['Development Cost']
            sync = row ['Sync']

            if cardType == "":
                continue
            if row['Card Status'] == "":
                continue
            if cardType == "Story":
                card = createStoryCard(name, text)
            else:
                card = createCard(name, cardType, cost, text,image, hp, shield, devCost, sync)
            number = row['supply'] #this line and the next are the ones i changed
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

processCards()
