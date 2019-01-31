import pylab
import subprocess
import os
import re
from subprocess import call
from subprocess import check_output
import json
import numpy as np


from_memory = 0
problem = 1
# full = "_full"
full = ""
full = "_overlap"
size_of_fos = 20

if problem == 13 or problem == 14:
    dim = 905
else:
    dim = 1000
scale = dim

dglt = 8
if not from_memory:
    if full == "":
        dglt = 10
    elif full == "_overlap":
        dglt = 12

gomea_command = f"./RV-GOMEA-FOS -f -{dglt}  -s -r -b {21+problem} {dim} -100 100 0 0.35 50 25 0.9 1 3000000.0 0.1 100 0.0 1"


filename = f"{os.getcwd()}/FOS/src/FOS_f{problem}{full}.txt"
# FOS = dict()

print(gomea_command)

if not from_memory:
    path_command = "export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH"
    gomea_result = subprocess.Popen(path_command + " ; " + gomea_command, cwd=os.getcwd(), shell=True,
                                    stdout=subprocess.PIPE)
    out, err = gomea_result.communicate()
    correct = json.dumps(out.decode('utf8'))
    # print(correct)
    corr_list = correct.split("]]")[-2].split("[[")[1]
    print(corr_list)

    file = open(filename, "w")
    corr_list = "[["+corr_list+"]]"
    file.write(corr_list)
    # json.dumps(corr_list, file)
    file.close()


file = open(filename)
FOS = json.load(file)

print(len(FOS))
matrix = np.zeros((size_of_fos*len(FOS),dim))
matrix.fill(np.nan)
# matrix = np.zeros((dim,2000))
count = 0
FOS.sort(key=lambda x: len(x), reverse=True)

for element in FOS:
    # if len(element) < 3:
    #     continue
    count += 1
    for xi in element:
        for i in range(size_of_fos):
            matrix[i+((count-1)*size_of_fos)][xi] = len(FOS) - count

print(count)
current_cmap = pylab.matplotlib.cm.get_cmap()
current_cmap.set_bad(color='white')

pylab.imshow(matrix[:size_of_fos*count])
pylab.box(False)
pylab.xlim(xmin=0, xmax=1000)
pylab.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
# pylab.axes().xaxis.set_visible(True)
if full == "":
    pylab.title(f"Sparse FOS of CEC 2013 f{problem}\n ")
elif full == "_overlap":
    pylab.title(f"Manual FOS of CEC 2013 f{problem}\n ")
else:
    pylab.title(f"FOS of CEC 2013 f{problem}\n ")
pylab.savefig(f"FOS/f{problem}_FOS{full}.png")
pylab.show()


