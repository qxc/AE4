import csv
import subprocess

def createBoss(name, setup, rules, hp, image, expDifficulty, nightDifficulty, exhaustEffect):
    code = "\\begin{tikzpicture} \n\draw[black] \shapeCard; \\newline"
    code += "\\newcommand{\Or}{\\textbf{OR}};"
    code += "\n\draw[ultra thick] (\cardwidth/2, \cardheight*.45) rectangle (0, \cardheight); \n"
    code += "\\name{" + name + " \image{" + image + "} \hp{" + hp + "}};\n"
    code += "\setup{" + setup + "}\n"
    code += "\\rules{" + rules + "};"
    code += "\\expDifficulty{" + expDifficulty + "};"
    code += "\\nightDifficulty{" + nightDifficulty + "};"
    code += "\\exhaustEffect{" + exhaustEffect + "};"
    code += "\n\end{tikzpicture}\n\n"
    return code

def processBoss(fileName = "bSheet.csv"):
    baseFile = "ZXbSheet"
    texFile = baseFile+".tex"
    pdfFile = baseFile + ".pdf"
    f = open(texFile, "w")
    f.write(makeHeader())
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            try:
                unleash = row['Unleash']
            except:
                unleash = ""
            setup = row['Setup']
            rules = row['Rules']
            hp = row['Health']
            image = row['Image']
            try:
                expDifficulty = row['Expert Difficulty']
            except:
                expDifficulty = ""
            try:
                nightDifficulty = row['Nightmare Difficulty']
            except:
                nightDifficulty = ""
            if row['Card Status'] == "":
                continue
            try:
                exhaustEffect = row['Exhaust Effect']
            except:
                exhaustEffect = ""
            char = createBoss(name, setup, rules, hp, image, expDifficulty, nightDifficulty, exhaustEffect)
            f.write(char)
    f.write("\n \end{center} \n \end{document}")
    f.close()
    print(makeHeader())
    compileFile(texFile)
    subprocess.Popen([pdfFile],shell=True)
    return

def makePDF(name, char):
    fileName = "bossSheet" + name + ".tex"
    f = open(fileName, "w")
    f.write(makeHeader())
    f.write(char)
    f.write("\n \end{center} \n \end{document}")
    f.close()
    compileFile(fileName)
    
def compileFile(fileName):
    proc=subprocess.Popen(['pdflatex',fileName])
    proc.communicate()

def makeHeader():
    header ="\\nonstopmode\n\\documentclass{article}\n\input{libs.tex}\n\input{colors.tex}\n\\usepackage[none]{hyphenat}"
    header += "\n\input{tikzcardsTwo.tex}"
    header += "\n\input{tikzBoss.tex}"
    header += "\n\\begin{document}\n\\begin{center}\n\pagestyle{empty}"
    return header



processBoss()
