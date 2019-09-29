from tkinter import *
from tkinter.filedialog import askopenfilename
myWin = Tk()

apkPath = StringVar()

signFilePath = StringVar()
signPwd = StringVar()
signAlias = StringVar()
signAliasPwd = StringVar()

allChannel = StringVar()
outPutDir = StringVar()

# 标题
myWin.title("欢迎使用Apk签名工具")
# 窗口大小
myWin.geometry("720x720")


def selectApkPath():
    apk_path_ = askopenfilename()
    apkPath.set(apk_path_)


# 选择apk文件
Label(myWin, text="apk路径：").grid(row=0, column=0)
Entry(myWin, textvariable=apkPath).grid(row=0, column=1)
Button(myWin, text="选择", command=selectApkPath).grid(row=0, column=2)


def selectSignFilePath():
    sign_path_ = askopenfilename()
    signFilePath.set(sign_path_)


# 签名信息
Label(myWin, text="签名文件路径：").grid(row=1, column=0)
Entry(myWin, textvariable=signFilePath).grid(row=1, column=1)
Button(myWin, text="选择", command=selectSignFilePath).grid(row=1, column=2)
# 签名密码配置
Label(myWin, text="签名密码：").grid(row=2, column=0)
Entry(myWin, textvariable=signPwd).grid(row=2, column=1)

Label(myWin, text="签名别名：").grid(row=3, column=0)
Entry(myWin, textvariable=signAlias).grid(row=3, column=1)

Label(myWin, text="签名别名密码：").grid(row=4, column=0)
Entry(myWin, textvariable=signAliasPwd).grid(row=4, column=1)


def clickSubmit():
    print("apkPath:" + str(apkPath.get()))
    print("signFilePath:" + str(signFilePath.get()))
    print("signPwd:" + str(signPwd.get()))
    print("signAlias:" + str(signAlias.get()))
    print("signAliasPwd:" + str(signAliasPwd.get()))

    #打渠道包

    #签名


Button(myWin, text="确定", command=clickSubmit).grid(row=5, column=0)
myWin.mainloop()
