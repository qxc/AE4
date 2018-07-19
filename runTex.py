import subprocess

def test(fileName):

    proc=subprocess.Popen(['pdflatex',fileName])

    proc.communicate()
