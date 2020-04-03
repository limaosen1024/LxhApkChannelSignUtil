import os
path = "/Users/lixiaohui/Desktop/360/"
files = os.listdir(path)
for file in files:
    if file.startswith("beilehu"):
        splitStr = file.split("_")
        print(splitStr)
        newName = splitStr[0]+"_"+splitStr[6]+".apk"
        print(newName)
        os.rename(path+file,path+newName)