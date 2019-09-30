from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from Util import *

myWin = Tk()

old_apk_path_var = StringVar()

keystore_file_path_var = StringVar()
keystore_pwd_var = StringVar()
keystore_alias_var = StringVar()

channel_list_var = StringVar()
out_put_dir_var = StringVar()
save_keystore = IntVar()
save_keystore.set(1)

keystore_file_path, keystore_pwd, keystore_alias = readKeyStore()

if (len(keystore_file_path) != 0):
    keystore_file_path_var.set(keystore_file_path)
    keystore_pwd_var.set(keystore_pwd)
    keystore_alias_var.set(keystore_alias)

# 标题
myWin.title("欢迎使用Apk签名工具")
# 窗口大小
myWin.geometry("720x720")


def selectApkPath():
    apk_path_ = askopenfilename()
    old_apk_path_var.set(apk_path_)


# 选择apk文件
Label(myWin, text="apk路径：").grid(row=0, column=0)
Entry(myWin, textvariable=old_apk_path_var).grid(row=0, column=1)
Button(myWin, text="选择", command=selectApkPath).grid(row=0, column=2)


def selectSignFilePath():
    sign_path_ = askopenfilename()
    keystore_file_path_var.set(sign_path_)


# 签名信息
Label(myWin, text="签名文件路径：").grid(row=1, column=0)
Entry(myWin, textvariable=keystore_file_path_var).grid(row=1, column=1)
Button(myWin, text="选择", command=selectSignFilePath).grid(row=1, column=2)
# 签名密码配置
Label(myWin, text="签名密码：").grid(row=2, column=0)
Entry(myWin, textvariable=keystore_pwd_var, show='*').grid(row=2, column=1)

Label(myWin, text="签名别名：").grid(row=3, column=0)
Entry(myWin, textvariable=keystore_alias_var).grid(row=3, column=1)

Label(myWin, text="本地保存签名：").grid(row=4, column=0)
Checkbutton(myWin, variable=save_keystore).grid(row=4, column=1)

Label(myWin, text="渠道列表：").grid(row=5, column=0)
Entry(myWin, textvariable=channel_list_var).grid(row=5, column=1)


def selectOutPath():
    apk_path_ = askdirectory()
    out_put_dir_var.set(apk_path_)


# 选择apk文件
Label(myWin, text="输出路径：").grid(row=6, column=0)
Entry(myWin, textvariable=out_put_dir_var).grid(row=6, column=1)
Button(myWin, text="选择", command=selectOutPath).grid(row=6, column=2)


def clickSubmit():
    old_apk_path = str(old_apk_path_var.get())
    keystore_file_path = str(keystore_file_path_var.get())
    keystore_pwd = str(keystore_pwd_var.get())
    keystore_alias = str(keystore_alias_var.get())
    out_put_dir = str(out_put_dir_var.get())
    channel_list = str(channel_list_var.get()).split(";")
    print("开始执行....")
    print("old_apk_path:" + old_apk_path)
    print("keystore_file_path:" + keystore_file_path)
    print("keystore_pwd:" + keystore_pwd)
    print("keystore_alias:" + keystore_alias)
    print("out_put_dir" + out_put_dir)
    print("channel_list：" + "".join(channel_list))
    if (save_keystore.get() == 1):
        saveKeyStore(keystore_file_path, keystore_pwd, keystore_alias)

    start(old_apk_path, channel_list, out_put_dir, keystore_file_path, keystore_pwd, keystore_alias)


Button(myWin, text="确定", command=clickSubmit).grid(row=7, column=0)
myWin.mainloop()
