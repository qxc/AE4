import csv
import subprocess

def createBoss(name, unleash, setup, rules, hp, difficulty, image, diffR):
    code = "\\begin{tikzpicture} \n\draw[black] \shapeCard; \\newline"
    code += "\\newcommand{\Or}{\\textbf{OR}};"
    code += "\n\draw[ultra thick] (\cardwidth/2, \cardheight*.56) rectangle (0, \cardheight); \n"
    code += "\\name{" + name + " \image{" + image + "} \hp{" + hp + "}};\n"
    code += "\setup{" + setup + "}\n"
    code += "\\unleash{" + unleash + "}\n"
    code += "\\difficulty{" + difficulty + "}\n"
    code += "\\rules{" + rules + "};"
    code += "\\diffR{" + diffR + "};"
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
                difficulty = row['Difficulty']
            except:
                difficulty = ""
            try:
                diffR = row['Difficulty Rating']
            except:
                diffR = ""
            if row['Card Status'] == "":
                continue
            char = createBoss(name, unleash, setup, rules, hp, difficulty, image, diffR)
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
    header +="\n\pgfmathsetmacro{\cardwidth}{17.5}\n\pgfmathsetmacro{\cardheight}{26}\n\pgfmathsetmacro{\offset}{.5}"
    header +="\n\pgfmathsetmacro{\\tw}{8cm}\n\pgfmathsetmacro{\squarewidth}{2.5}\n\pgfmathsetmacro{\squareheight}{2.25}"
    header +="\n\def\shapeCard{(0,0) rectangle (\cardwidth,\cardheight)}\n\\newcommand{\Money}{\includegraphics[height = .4cm]{money} }\n\\newcommand{\cardborder}{"
    header +="\draw[black] \shapeCard;\n\draw[ultra thick] (\cardwidth/2, \cardheight/2) rectangle (0, \cardheight);}"
    header += "\n\\newcommand{\\name}[1]{\\node[text width = \\tw] at (\cardwidth/4, \cardheight-\offset*2) {\LARGE{#1}};}"
    header += "\n\\newcommand{\setup}[1]{\\node[text width = \\tw] at (\cardwidth/4, \cardheight*.87) {\large \\textbf{Setup:} #1};}"
    header += "\n\\newcommand{\\unleash}[1]{\\node[text width = \\tw] at (\cardwidth/4, \cardheight*.67) {\large \\textbf{Unleash:} #1};}"
    header += "\n\\newcommand{\\difficulty}[1]{\\node[text width = \\tw] at (\cardwidth/4, \cardheight*.20) {\\textbf{Additional Difficulty Rules:} #1};}"
    header += "\n\\newcommand{\\rules}[1]{\\node at (\cardwidth*.7, \cardheight/2+10) ; \\node[text width = 7 cm] at (\cardwidth*3/4, \cardheight/2+2) {\large \\textbf{Rules:} #1};}"
    header += "\n\\newcommand{\image}[1]{\includegraphics[height = .8cm]{#1}}"
    header += "\n\\newcommand{\hp}[1]{\\textbf{#1} \image{heart}}"
    header += "\n\\newcommand{\\diffR}[1]{\\node[text width = \\tw] at (\cardwidth*.9, \cardheight*.95) {\\textbf{Difficulty Rating:} #1};}"
    header += "\n\\begin{document}\n\\begin{center}\n\pagestyle{empty}"
    return header



processBoss()
