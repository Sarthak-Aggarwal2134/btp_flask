import random
import sys
from random import randint
from numpy import cumsum
import wave
import contextlib

# Reading audio file
audioFile = sys.argv[1]
with contextlib.closing(wave.open(audioFile, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    dur = frames / float(rate)

# Preparing the data
N = randint(3, 7)
bar_score_len = randint(7, 12)
word_score = 5 * random.random()
syl_scores = [100 * random.random() for i in range(N)]
syls = ['syl#' + str(i) for i in range(N)]
x = [random.random() for j in range(N)]
x = [0] + x
x = cumsum(x)
x = [dur * i / x[-1] for i in x]
y = [random.random() for j in range(N + 1)]

bar_scores = [random.random() for i in range(bar_score_len)]
text = ['' for i in range(bar_score_len)]
for i in range(bar_score_len):
    temp = randint(1, 3)
    text[i] = ['test ' + str(i + j) for j in range(temp)]
modText = ['' for i in range(len(text))]
for i in range(len(text)):
    if len(text[i]) == 1:
        modText[i] = text[i][0]
    if len(text[i]) != 1:
        modText[i] = " <br> ".join(text[i])

# Writing the data into the file
outFileName = audioFile[:-4] + '_diagnosis.json'
with open(outFileName, "w") as outFile:
    outFile.write("{\n")
    outFile.write("\"word\":\"%3.2f\",\n" % word_score)
    outFile.write("\"phoneme\":[")
    outFile.write(",".join("\"%3.2f\"" % i for i in syl_scores))
    outFile.write("],\n")
    outFile.write("\"lables\":[")
    outFile.write(",".join("\"%s\"" % i for i in syls))
    outFile.write("],\n")
    outFile.write("\"values\":[")
    outFile.write(",".join("{\"x\":\"%3.2f\",\"y\":\"%3.2f\"}" % (i, j) for i, j in zip(x, y)))
    outFile.write("],\n")
    outFile.write("\"colors\":[")
    outFile.write(",".join("\"%3.2f\"" % i for i in bar_scores))
    outFile.write("],\n")
    outFile.write("\"details\":[")
    outFile.write(",".join("{\"text\":\"%s\"}" % i for i in modText))
    outFile.write("\n]\n}")

print(outFileName)
