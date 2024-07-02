import os,time
from ftplib import FTP
import ftplib
import threading
import tkinter
import zeep
from datetime import datetime
import traceback
import zipfile

#循环扫描文件
def monitoringFile(path_to_watch,StageType):
    while 1:
        after_files = getFiles(path_to_watch)
        if len(after_files)!= 0:
            return after_files
        else:
            time.sleep (60)

#判断文件类型是否需要上传
def judgingFileType(fileName):
    SuffixNameIndex = find_last(fileName,".")
    SuffixName = fileName[SuffixNameIndex:]
    allowSuffixNames = [".3dx",".3DX"]
    if SuffixName in allowSuffixNames:
        return True
    else:
        return False

#扫描目录下所有文件
def getFiles(path_to_watch):
    results = []
    folders = [path_to_watch]
    for folder in folders :
        # 把目录下所有文件夹存入待遍历的folders
        folders += [os.path.join(folder, x) for x in os.listdir(folder)\
                    if os.path.isdir(os.path.join(folder, x)) and not x.startswith('Uploaded_')]  

        # 把所有满足条件的文件的相对地址存入结果results
        results += [os.path.relpath(os.path.join(folder, x), start = path_to_watch)\
                for x in os.listdir(folder)\
                if os.path.isfile(os.path.join(folder, x))\
                    and not x.startswith('Uploaded_')\
                    and judgingFileType(x)]
    return results

AOI3DXSETTING = {}

#读取配置文件并检查
def readAOIConfig():
    try:
        fp = open("./AOl3DXSetting.Config","rb")
        lines = fp.readlines()
        result,AOISetting = getSetting(lines)
    except Exception as e:
        return False,traceback.format_exc()
    finally:
        if 'fp' in dir():
            fp.close()
    return result,AOISetting

#解析配置文件
def getSetting(lines):
    AOISetting = {}
    for line in lines:
        line = line.decode('utf-8')
        if line != "\r\n":
            line = line.split("=")
            key = line[0].strip()
            value = line[1].split("#")[0].strip(' ').strip('"')
        if value == "" and (key == "StageName" or key == "LineName" or key == "LocalRootDirAbsPath" \
                            or key == "AOI3DXStorageServer"):
            return False,"Setting file error:\n    "+key + " Can't be empty!"
        AOISetting[key] = value
        AOI3DXSETTING[key] = value
    return True,AOISetting

#连接登陆ftp并转入对应文件夹
def connect_ftp(host, user, passwd, absoluteDirPath, port = 21,timeout='1'):
    ftp = FTP()
    try:
        ftp.connect(host=host, port=port)
    except Exception as e:
        string = "ftp访问失败,请检查服务器IP以及网络,error:" + str(e)
        generateErrorLogs('Failed to access FTP:\n'+traceback.format_exc())
        promptBox(string)
        return None
    try:
        ftp.login(user=user, passwd=passwd)
    except Exception as e:
        string = "ftp登录失败,请检查用户名和密码,error:" + str(e)
        ftp.quit()
        generateErrorLogs('Failed to log in to FTP:\n'+traceback.format_exc())
        promptBox(string)
        return None
    try:
        url = absoluteDirPath
        ftp.cwd(url)
    except ftplib.error_perm as e:
        generateErrorLogs('Failed to open FTP directory:\n'+traceback.format_exc())
        promptBox('在ftp服务器上无法打开目录：'+url+
                      ',请检查权限和目录路径,error:'+str(e))
        ftp.quit()
        return None
    return ftp

#提示框
def promptBox(string):
    window = tkinter.Tk()            #主窗口
    window.title('AOI 3DX Exception!!!')   #窗口标题
    window.geometry('400x200')  #窗口尺寸
    var = tkinter.StringVar()    # 文字变量储存器
    var.set(string)
    l = tkinter.Label(window,
        textvariable=var,font=('Arial', 12),
                    width=75, height=9,wraplength = 320,
                    justify = 'left')
    l.pack()
    var2 = tkinter.StringVar()
    var2.set("After solving the problem, please start the program.")
    l2 = tkinter.Label(window,
        textvariable=var2,font=('Arial', 12),
                    width=75, height=3,wraplength = 360,
                    justify = 'left')
    l2.pack()
    window.mainloop()

#连接webservice
def getClient():
    wsdl = 'http://10.41.95.81/webservice/?wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client

#相同子字符串 最末下标
def find_last(str1,str2):
    last_index = -1
    while True:
        index = str1.find(str2,last_index+1)
        if index == -1:
            return last_index
        last_index = index

#将文件上传至ftp
def fileUpload(ftp,sFileUrl,FileUrl,rootDirAbsPath,StageType):
    try:
        fp=open(rootDirAbsPath+"\\"+FileUrl,"rb")
        index = find_last(FileUrl,"\\")
        FileName = FileUrl[index+1:]
        if index != -1:
            PathName = FileUrl[0:index]
        else:
            PathName = ""
        print(FileName)
        result = False
        try:
            ftp.cwd(sFileUrl+"\\"+PathName)
        except ftplib.error_perm as e:
            FCMD_result = ftpCreateMultilevelDirectories(ftp,sFileUrl+"\\"+PathName)
            if FCMD_result is False:
                return False
        except Exception as e:
            generateErrorLogs('Failed to open FTP directory when uploading:\n'+traceback.format_exc())
            promptBox("AOI Error:"+str(e))
            ftp.quit()
            return False
        try:
            ftp.storbinary(("STOR "+ FileName).encode("utf-8").decode("ISO-8859-1"), fp, 1024)
            result = True
        except ftplib.error_perm as e:
            generateErrorLogs('FTP exception causes file upload failure:\n'+traceback.format_exc())
            promptBox("文件上传失败,error:"+str(e))
            ftp.quit()
            result = False
        except Exception as e:
            generateErrorLogs('Other exceptions cause FTP upload files to fail:\n'+traceback.format_exc())
            promptBox("文件上传失败,error:"+str(e))
            ftp.quit()
            result = False
    finally:
        if 'fp' in dir():
            fp.close()
    if result:
        generateUploadLogs(rootDirAbsPath+"\\"+FileUrl)
        os.remove(rootDirAbsPath+"\\"+FileUrl)
    return result

#ftp创建多级目录
def ftpCreateMultilevelDirectories(ftp,PathName):
    directoryNames = PathName.split("\\")
    for directoryName in directoryNames:
        try:
            ftp.mkd(directoryName)
        except ftplib.error_perm as e:
            pass
        try:
            ftp.cwd(directoryName)
        except ftplib.error_perm as e:
            generateErrorLogs('Failed to create FTP folder:\n'+traceback.format_exc())
            promptBox('在ftp服务器上无法更改目录,请检查网络、权限和目录路径,error:'+str(e))
            ftp.quit()
            return False
    return True

#生成上传日志
def generateUploadLogs(fileUrl):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_Ymd = time.split(" ")[0]
    time_HMS = time.split(" ")[1]
    url = "../uploadLog/3DX " + AOI3DXSETTING['LineName'] + " " + AOI3DXSETTING['StageName'] + " " + time_Ymd +".txt"
    with open(url,'a+',encoding="utf-8") as t:
        t.writelines(time_HMS+":Upload "+fileUrl+"\r\n")

#生成错误日志
def generateErrorLogs(errorString):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_Ymd = time.split(" ")[0]
    time_HMS = time.split(" ")[1]
    url = "../errorLog/3DX" + AOI3DXSETTING['LineName'] + " " + AOI3DXSETTING['StageName'] + " " + time_Ymd +".txt"
    with open(url,'a+') as t:
        t.write(time_HMS+" "+errorString+"\n")

#时间字符串转时间
def timeStringConversionTime(timeString):
    return time.strptime(timeString,"%Y%m%d%H%M%S")

#时间戳转换为时间字符串
def timeStampConversionTimeString(ltime):
    return time.strftime("%Y%m%d%H%M%S",time.localtime(int(ltime)))
