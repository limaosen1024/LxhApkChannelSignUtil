import os
import sys
import shutil
from xml.etree import ElementTree as ET

cmd_res = 0
apk_tool_path = os.path.abspath("./script/apktool_2.4.0.jar");
zip_align_tool_path = os.path.abspath("./script/buidl-tools-29.0.1/zipalign")
apksigner_align_tool_path = os.path.abspath("./script/buidl-tools-29.0.1/apksigner")


def renameFile(file_path, channel):
    file_name_list = os.path.splitext(os.path.basename(file_path))
    new_file_name = (file_name_list[0].split("_"))[0] + "_" + channel + file_name_list[1]
    file_dir = os.path.dirname(file_path)
    new_file_path = file_dir + "/" + new_file_name
    os.rename(file_path, new_file_path)


def signApk(temp_unsign_apk_dir, unsign_apk_file_name, out_sign_file_dir, keystore_path, keystore_pwd,
            keystore_alias_name, channel):
    unsign_file_name_list = os.path.splitext(unsign_apk_file_name)
    v1_sign_apk_path = temp_unsign_apk_dir + "/" + unsign_file_name_list[0] + "_v1sign" + unsign_file_name_list[1]
    unsign_apk_path = temp_unsign_apk_dir + "/" + unsign_apk_file_name
    # V1签名
    sign_v1_cmd = r'jarsigner -verbose -keystore %s -storepass %s -signedjar %s %s %s' % (
        keystore_path, keystore_pwd, v1_sign_apk_path, unsign_apk_path, keystore_alias_name)
    cmd_res = os.system(sign_v1_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    check_v1_sign_cmd = r'jarsigner -verify -verbose %s' % (v1_sign_apk_path)
    cmd_res = os.system(check_v1_sign_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    print("V1签名成功：" + v1_sign_apk_path)
    # zipalign
    if not os.path.exists(out_sign_file_dir):
        os.makedirs(out_sign_file_dir)

    v1_sign_zip_apk_path = out_sign_file_dir + "/" + unsign_file_name_list[0] + "_sign_zip" + unsign_file_name_list[1]
    zip_align_cmd = r'%s -v 4 %s %s' % (zip_align_tool_path, v1_sign_apk_path, v1_sign_zip_apk_path)
    cmd_res = os.system(zip_align_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    print("zipalign成功：" + v1_sign_zip_apk_path)
    # v2签名
    sign_v2_cmd = '%s sign --ks %s --ks-pass pass:%s --ks-key-alias %s %s' % (apksigner_align_tool_path,
                                                                              keystore_path, keystore_pwd,
                                                                              keystore_alias_name, v1_sign_zip_apk_path)
    cmd_res = os.system(sign_v2_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    check_v2_sign_cmd = r'./script/buidl-tools-29.0.1/apksigner verify -v --print-certs %s' % (v1_sign_zip_apk_path)
    cmd_res = os.system(check_v2_sign_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    print("v2签名成功：" + v1_sign_zip_apk_path)
    renameFile(v1_sign_zip_apk_path, channel)


# 备份manifest文件
def backUpManifest(back_manifest_dir, temp_manifest_path):
    back_up_manifest_file_path = back_manifest_dir + "/AndroidManifest.xml"
    # 如果存在删除以前的文件
    if os.path.exists(back_manifest_dir):
        print("删除备份manifest：" + back_manifest_dir)
        shutil.rmtree(back_manifest_dir)
    os.makedirs(back_manifest_dir)
    print("备份manifest:" + back_up_manifest_file_path)
    # 复制temp到back的路径
    shutil.copy(temp_manifest_path, back_up_manifest_file_path)
    print("备份manifest成功:" + back_up_manifest_file_path)
    return back_up_manifest_file_path


def modifyChannel(channel, back_up_manifest_file_path, temp_manifest_path, unzip_temp_dir, temp_dir, apk_file,
                  out_sign_file_dir, keystore_path, keystore_pwd, keystore_alias_name):
    android_ns = 'http://schemas.android.com/apk/res/android'
    print("修改的渠道为：" + channel)
    # 替换channel value
    ET.register_namespace('android', android_ns)
    tree = ET.parse(back_up_manifest_file_path)
    root = tree.getroot()
    key = '{' + android_ns + '}name'
    val = '{' + android_ns + '}value'
    app_node = root.find('application')
    if app_node is None:
        return
    meta_data_list = app_node.findall('meta-data')
    if meta_data_list is not None:
        for metaDataNode in meta_data_list:
            key_name = metaDataNode.attrib[key]
            # if keyName == 'UMENG_CHANNEL' or keyName == 'DC_CHANNEL' or keyName == 'channel_value':
            if key_name == 'UMENG_CHANNEL':
                metaDataNode.set(val, channel)
    tree.write(temp_manifest_path, 'UTF-8')
    print("修改manifest文件成功:" + temp_manifest_path)
    file_name_list = os.path.splitext(os.path.basename(apk_file))
    # temp/test_legu_lxh/
    temp_unsign_apk_dir = temp_dir + "/" + file_name_list[0]
    unsign_apk_file_name = file_name_list[0] + "_" + channel + "_unsigned" + file_name_list[1]
    # 生成未签名的apk
    unsign_apk_file_path = temp_unsign_apk_dir + "/" + unsign_apk_file_name
    apk_tool_unsign_apk_cmd = r'java -jar %s -p %s b %s -o %s' % (apk_tool_path,
                                                                  "./framework", unzip_temp_dir, unsign_apk_file_path)
    cmd_res = os.system(apk_tool_unsign_apk_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    print("生成未签名apk:" + unsign_apk_file_path)
    # 签名
    signApk(temp_unsign_apk_dir, unsign_apk_file_name, out_sign_file_dir, keystore_path, keystore_pwd,
            keystore_alias_name, channel)


def channelApk(apk_file, channel_list, temp_dir, out_sign_file_dir, keystore_path, keystore_pwd, keystore_alias_name):
    # 解压的文件路径
    unzip_temp_dir = temp_dir + "/channelTemp"
    # 判断是否有文件，否则删除
    if os.path.exists(unzip_temp_dir):
        print("删除老的解压目录：" + unzip_temp_dir)
        shutil.rmtree(unzip_temp_dir)
    # 创建临时目录
    os.makedirs(unzip_temp_dir)
    print("apk解压目录为：" + unzip_temp_dir)
    # apktool解压apk
    apk_tool_unzip_cmd = r'java -jar %s -p %s d -f -s %s  -o %s' % (apk_tool_path,
                                                                    "./framework", apk_file, unzip_temp_dir)
    cmd_res = os.system(apk_tool_unzip_cmd)
    if (cmd_res != 0):
        sys.exit(0)
    print("apk解压成功：" + unzip_temp_dir)
    # 得到解压的manifest文件路径
    temp_manifest_path = unzip_temp_dir + "/AndroidManifest.xml"
    print("解压的Manifest文件地址：" + temp_manifest_path)
    # 备份一份到
    back_manifest_dir = temp_dir + "/manifestBackUp"
    back_up_manifest_file_path = backUpManifest(back_manifest_dir, temp_manifest_path)
    print("开始修改渠道:" + "\n".join(channel_list))
    # 去执行每一个
    for channel in channel_list:
        modifyChannel(channel, back_up_manifest_file_path, temp_manifest_path, unzip_temp_dir, temp_dir, apk_file,
                      out_sign_file_dir, keystore_path, keystore_pwd, keystore_alias_name)


keystore_config_file_path = "./keystore_config.txt"


def saveKeyStore(keystore_path, keystore_pass, keystore_alias):
    oldPath, oldPass, oldAlias = readKeyStore()
    newCon = keystore_path + "\n" + keystore_pass + "\n" + keystore_alias
    oldCon = oldPath + "\n" + oldPass + "\n" + oldAlias
    if oldCon == newCon:
        return
    if os.path.exists(keystore_config_file_path):
        os.remove(keystore_config_file_path)
    print("保存签名配置成功")
    fi = open(keystore_config_file_path, "w", encoding="utf-8")
    fi.write(newCon)


def readKeyStore():
    if (os.path.exists(keystore_config_file_path)):
        fi = open(keystore_config_file_path, "r", encoding="utf-8")
        cont = fi.read()
        cont_list = cont.split("\n")
        print("读取签名配置成功")
        return cont_list[0], cont_list[1], cont_list[2]
    else:
        return "", "", ""


def start(apk_file, channel_list, out_sign_file_dir, keystore_path, keystore_pwd, keystore_alias_name):
    print("开始多渠道打包，原Apk路径为：" + apk_file)
    temp_dir = "./temp"
    if os.path.exists(temp_dir):
        print("删除老的临时文件目录：" + temp_dir)
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    print("临时文件目录为：" + temp_dir)
    run_res = 1
    try:
        channelApk(apk_file, channel_list, temp_dir, out_sign_file_dir, keystore_path, keystore_pwd,
                   keystore_alias_name)
    except:
        print("except")
        run_res = 0
    finally:
        print("删除临时文件：" + temp_dir)
        shutil.rmtree(temp_dir)

    if run_res == 1:
        print("成功")


print(os.path.abspath("./script/apktool_2.4.0.jar"))
