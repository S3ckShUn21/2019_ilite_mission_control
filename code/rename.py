#
#   PDFs take too long to load on the RPi. Instead I am using an image viewer
#   on a folder of images for each slide; this loads WAY quicker.
#   Powerpoint needs to be exported to a folder of PNGs which is done easy
#   enough however, the files need to be renamed from "Slide1' "Slide2" to
#   "01" "02"... "11"... so linux shows pictures in order in the slide show.
#   This script renames the folder of PNGs given the folder name
#

import os
import re
import sys

if len(sys.argv) < 2:
    print("Please enter a folder name")
    print("You only have to enter the folder's name")
    print("No need to think about relative path to the file")
    sys.exit(-1)

path = "/home/ilite/Mission_Control_2019_files/media"
path = path + sys.argv[1]
files = sorted(os.listdir(path))

for file in files:
    file_num = re.search("\d\d?", file)
    num_format = "{:0>2d}".format(int(file_num.group()))
    new_filename = num_format + ".PNG"
    os.rename(os.path.join(path, file), os.path.join(path, new_filename))
    # print(os.path.join(path,new_filename))
