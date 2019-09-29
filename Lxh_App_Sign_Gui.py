from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from Util import *

myWin = Tk()

apkPath = StringVar()

signFilePath = StringVar()
signPwd = StringVar()
signAlias = StringVar()

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

Label(myWin, text="渠道列表：").grid(row=4, column=0)
Entry(myWin, textvariable=allChannel).grid(row=4, column=1)


def selectOutPath():
    apk_path_ = askdirectory()
    outPutDir.set(apk_path_)


# 选择apk文件
Label(myWin, text="输出路径：").grid(row=5, column=0)
Entry(myWin, textvariable=outPutDir).grid(row=5, column=1)
Button(myWin, text="选择", command=selectOutPath).grid(row=5, column=2)


def clickSubmit():
    oldApkPath = str(apkPath.get())
    signFilePathR = str(signFilePath.get())
    signPwdR = str(signPwd.get())
    signAliasName = str(signAlias.get())
    outPutDirR = str(outPutDir.get())
    channel_list = str(allChannel.get()).split(";")

    print("apkPath:" + oldApkPath)
    print("signFilePath:" + signFilePathR)
    print("signPwd:" + signPwdR)
    print("signAlias:" + signAliasName)
    print("outPutDirR" + outPutDirR)
    print("channel_list：" + "".join(channel_list))
    # channelApk(oldApkPath, channel_list, outPutDir, signFilePath, signPwdR, signAliasName)
    saveKeyStore(signFilePathR,signPwdR,signAliasName)


Button(myWin, text="确定", command=clickSubmit).grid(row=6, column=0)
myWin.mainloop()
