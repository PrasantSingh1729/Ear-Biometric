import os
import random
# for i in range(100):
#     print(str(random.randint(0,2960)))
# # 2960
# exit()
folder = "img/common"
nameset = set()
newname = 0
for count, filename in enumerate(os.listdir(folder)):
    while newname in nameset:
        newname = random.randint(0,2960)
    dst = f"{str(newname)}.jpg"
    src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
    dst =f"{folder}/{dst}"
    os.rename(src, dst)
    nameset.add(newname)
