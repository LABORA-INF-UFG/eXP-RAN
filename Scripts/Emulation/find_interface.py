import re
import os
import sys

filename = sys.argv[1]
ctn_number = sys.argv[2]

file = open(filename, "r")
lineList = file.readlines()
file.close()

lastline = lineList[-1]
result = re.search('> (.*)_l', lastline)
result = result.group(1) + "_l"

os.system("echo {} > /home/expran/expran_temp/ctn{}_interface.txt".format(result, ctn_number))