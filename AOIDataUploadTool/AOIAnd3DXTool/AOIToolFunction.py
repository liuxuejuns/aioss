import os,time,re
from ftplib import FTP
import ftplib
import threading
import tkinter
import zeep
from datetime import datetime
import traceback
import zipfile
import sys

#连接webservice
#172.30.97.62:正式服务器厂线端口IP 10.41.16.94:正式服务器OA端口IP 10.41.95.82:开发服务器IP
def getClient():
    wsdl = 'http://172.30.97.62/webservice/?wsdl'
    transport=zeep.Transport(cache=None)
    client = zeep.Client(wsdl=wsdl, transport=transport)
    client.service._binding_options['address']='http://172.30.97.62/webservice/'
    return client

#扫描根目录
def monitoringFile(path_to_watch,StageType,MachineType):
    print("扫描")
    lenPTW = len(path_to_watch.split("\\")) # 根目录路径长度
    if StageType == "AXI":
        after_files = getAXIFiles(path_to_watch,MachineType,lenPTW)
    elif StageType == "SMT_SPI":
        after_files = getSMT_SPIFiles(path_to_watch,lenPTW)
    elif StageType == "SMT_AOI":
        after_files = getSMT_AOIFiles(path_to_watch,lenPTW)
    elif StageType == "DIP_AOI":
        after_files = getDIP_AOIFiles(path_to_watch,lenPTW)
    elif StageType == "Final_AOI":
        after_files = getFinal_AOIFiles(path_to_watch,lenPTW)
    if len(after_files)!= 0:
        return after_files
    else:
        time.sleep(60*60)
        return []

def getSMT_SPIFiles(path_to_watch,lenPTW):
    results = []
    now = datetime.now().strftime("%Y%m%d")
    for root,dirs,files in os.walk(path_to_watch):
        rs = root.split("\\")
        len_result1 = (len(rs) == lenPTW + 1) #存放csv文件的文件夹路径的长度为根目录长度加1
        len_result2 = (len(rs) == lenPTW + 5) #存放图片文件的文件夹路径的长度为根目录长度加5
        # if条件 路径长度 第一层文件夹名格式
        if (len_result1 or len_result2) and re.fullmatch(r"\d{8}",rs[lenPTW]):
            uploaded_fns = readAOIDataUploadIdentification(root)
            for file in files:
                fn,ft = os.path.splitext(file) #fn：文件名 ft：文件类型
                #if条件 路径长度 文件类型 csv文件名格式 文件是否被上传 文件创建时间为今天以前
                if ((len_result1 and ft in [".csv",".CSV"] and re.fullmatch(r"[^_]+_[^_]+_\d{14}.+",fn)) or
                        (len_result2 and ft in [".png",".PNG",".JPG",".jpg",".jpeg",".JPEG"])) and not file in uploaded_fns \
                        and time.strftime("%Y%m%d",time.localtime(int(os.path.getctime(os.path.join(root, file))))) < now \
                            and not fn.startswith('Uploaded_'):
                    results.append(os.path.relpath(os.path.join(root, file), start = path_to_watch))
                    if len(results) >= 12000:
                        return results
    return results

def getSMT_AOIFiles(path_to_watch,lenPTW):
    results = []
    for root,dirs,files in os.walk(path_to_watch):
        rs = root.split("\\")
        if (len(rs) == lenPTW + 2 or len(rs) == lenPTW + 3) and re.fullmatch(r"\d{8}",rs[lenPTW+1]):
            results = getFiles(root,files,results,path_to_watch)
            if len(results) >= 12000:
                return results
    return results

def getDIP_AOIFiles(path_to_watch,lenPTW):
    results = []
    for root,dirs,files in os.walk(path_to_watch):
        rs = root.split("\\")
        if (len(rs) == lenPTW + 3) and re.fullmatch(r"\d{5,6}",rs[lenPTW+1])and re.fullmatch(r"\d{1,2}",rs[lenPTW+2]):
            results = getFiles(root,files,results,path_to_watch)
            if len(results) >= 12000:
                return results
    return results

def getFinal_AOIFiles(path_to_watch,lenPTW):
    results = []
    for root,dirs,files in os.walk(path_to_watch):
        rs = root.split("\\")
        if (len(rs) == lenPTW + 3 or len(rs) == lenPTW + 4) and re.fullmatch(r"\d{8}_{1}[1,2,3,4]{1}",rs[lenPTW+2]):
            results = getFiles(root,files,results,path_to_watch)
            if len(results) >= 12000:
                return results
    return results

#筛选需要上传的文件
def getFiles(root,files,results,path_to_watch):
    uploaded_fns = readAOIDataUploadIdentification(root)
    now = datetime.now().strftime("%Y%m%d")
    for file in files:
        fn,ft = os.path.splitext(file)
        if ft in [".png",".PNG",".JPG",".jpg",".jpeg",".JPEG"] and not file in uploaded_fns \
            and time.strftime("%Y%m%d",time.localtime(int(os.path.getctime(os.path.join(root, file))))) < now \
                and not fn.startswith('Uploaded_'):
            results.append(os.path.relpath(os.path.join(root, file), start = path_to_watch))
            if len(results) >= 12000:
                return results
    return results

#获取记录已上传文件的文件内容
def readAOIDataUploadIdentification(root):
    try:
        with open(root+"\\AOIDataUploadIdentification.txt","r") as fp:
            uploaded_fns = fp.read().splitlines()
        return uploaded_fns
    except FileNotFoundError:
        #此文件夹所有文件都没有上传，会没有TXT文件，导致产生找不到文件异常，返回空列表即可
        return []
    except:
        generateErrorLogs('读取已上传文件记录失败:\n'+ root+"\\AOIDataUploadIdentification.txt" +'\n'+traceback.format_exc())
        promptBox('读取已上传文件记录失败!')
        sys.exit()

#StageType AXI 扫描文件夹
def getAXIFiles(path_to_watch,MachineType,lenPTW):
    now = datetime.now().strftime("%Y%m%d")
    results = []
    for root,dirs,files in os.walk(path_to_watch):
        rs = root.split("\\")
        if MachineType == "5DX" and len(rs) == 4+lenPTW and rs.fullmatch(r"\d{4}",rs[lenPTW]) and rs.fullmatch(r"\d{1,2}",rs[lenPTW+1]) \
            and rs.fullmatch(r"\d{1,2}",rs[lenPTW + 2]):
            uploaded_dns = readAOIDataUploadIdentification(root)
            for dir in dirs:
                if time.strftime("%Y%m%d",time.localtime(int(os.path.getctime(os.path.join(root, dir))))) < now \
                    and not dir in uploaded_dns and not dir.startswith('Uploaded_'):
                    results.append(os.path.relpath(os.path.join(root, dir), start = path_to_watch))

        elif MachineType == "7600SII" and len(rs) == lenPTW:
            results = getDirs(root,dirs,path_to_watch,results)

        elif MachineType == "7600SIII" and len(rs) == 1+lenPTW and re.fullmatch(r"\d{6}",rs[-1]):
            results = getDirs(root,dirs,path_to_watch,results)

        if len(results) >= 12000:
                return results
    return results

#筛选需要上传的文件夹
def getDirs(root,dirs,path_to_watch,results):
    now = datetime.now().strftime("%Y%m%d")
    uploaded_dns = readAOIDataUploadIdentification(root)
    for dir in dirs:
        if time.strftime("%Y%m%d",time.localtime(int(os.path.getctime(os.path.join(root, dir))))) < now \
            and not dir in uploaded_dns and not dir.startswith('Uploaded_') and re.fullmatch(r"\d{8}",dir):
            results.append(os.path.relpath(os.path.join(root, dir), start = path_to_watch))
            if len(results) >= 12000:
                return results
    return results

AOISETTING = {}

#读取配置文件并检查
def readAOIConfig():
    try:
        fp = open("./AOlSetting.Config","rb")
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
                                or key == "AOIStorageServer"):
                return False,"Setting file error:\n    "+key + " Can't be empty!"
            if key == "LocalRootDirAbsPath":
                value = value.split(";")
        AOISetting[key] = value
        AOISETTING[key] = value
    return True,AOISetting

#连接登陆ftp并转入对应文件夹
def connect_ftp(host, user, passwd, absoluteDirPath, port = 21,timeout='1'):
    ftp = FTP()
    try:
        ftp.connect(host=host, port=port)
    except Exception as e:
        string = "ftp访问失败,请检查服务器IP以及网络,error:" + str(e)
        generateErrorLogs('Failed to access FTP:\n'+string+"\n"+traceback.format_exc())
        promptBox(string)
        return None
    try:
        ftp.login(user=user, passwd=passwd)
        #ftp.set_pasv(False)
    except Exception as e:
        string = "ftp登录失败,请检查用户名和密码,error:" + str(e)
        ftp.quit()
        generateErrorLogs('Failed to log in to FTP:\n'+string+"\n"+traceback.format_exc())
        promptBox(string)
        return None
    try:
        url = absoluteDirPath
        ftp.cwd((url).encode("utf-8").decode("ISO-8859-1"))
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
    window.title('AOI Exception!!!')   #窗口标题
    window.geometry('400x400')  #窗口尺寸
    var = tkinter.StringVar()    # 文字变量储存器
    var.set(string)
    l = tkinter.Label(window,
        textvariable=var,font=('Arial', 12),
                    width=75, height=12,wraplength = 320,
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

#相同子字符串 最末下标
def find_last(str1,str2):
    last_index = -1
    while True:
        index = str1.find(str2,last_index+1)
        if index == -1:
            return last_index
        last_index = index

#将文件上传至ftp
#ftp：已连接的ftp对象 sFileUrl：存在服务器上添加的路径
#FileUrl：文件在本地电脑的相对路径 rootDirAbsPath：本地根目录
#StageType：站别类型 client：已连接的webservice对象
def fileUpload(ftp,sFileUrl,FileUrl,rootDirAbsPath,StageType,client):
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
            ftp.cwd((sFileUrl+"\\"+PathName).encode("utf-8").decode("ISO-8859-1"))
        except ftplib.error_perm as e:
            FCMD_result = ftpCreateMultilevelDirectories(ftp,sFileUrl+"\\"+PathName)
            if FCMD_result is False:
                return False
        except Exception as e:
            generateErrorLogs('Failed to open FTP directory when uploading:'+sFileUrl+"\\"+PathName+'\n'+traceback.format_exc())
            promptBox("AOI Error:"+str(e))
            return False
        try:
            ftp.storbinary(("STOR "+ FileName).encode("utf-8").decode("ISO-8859-1"), fp, 1024)
            result = True
        except ftplib.error_perm as e:
            generateErrorLogs('FTP exception causes file upload failure:\n'+sFileUrl+"\\"+PathName+'\n'+traceback.format_exc())
            promptBox("文件上传失败,error:"+str(e))
            result = False
        except Exception as e:
            generateErrorLogs('Other exceptions cause FTP upload files to fail:\n'+sFileUrl+"\\"+PathName+'\n'+traceback.format_exc())
            promptBox("文件上传失败,error:"+str(e))
            result = False
    finally:
        if 'fp' in dir():
            fp.close()
    if result:
        if AOISETTING["LineName"] != "test":
            result = addUploadRecord(StageType,sFileUrl,FileUrl,rootDirAbsPath,client)
            if StageType == "AXI":
                # AXI StageType删除压缩包
                os.remove(rootDirAbsPath+"\\"+FileUrl)
                FileName = FileName.strip(".zip")
            if result:
                #modifyFileName(rootDirAbsPath,PathName,FileName)
                addAOIDataUploadIdentification(rootDirAbsPath,PathName,FileName)
        generateUploadLogs(rootDirAbsPath+"\\"+FileUrl)
    return result

def addAOIDataUploadIdentification(rootDirAbsPath,PathName,FileName):
    try:
        url =  rootDirAbsPath+"\\"+PathName+"\\AOIDataUploadIdentification.txt"
        with open(url,'a+',encoding="utf-8") as t:
            t.writelines(FileName + "\r\n")
    except:
        generateErrorLogs("新建或者写入已上传文件记录失败:\n"+rootDirAbsPath+"\\"+PathName+"\\AOIDataUploadIdentification.txt \n"
                +traceback.format_exc())
        promptBox("新建或者写入已上传文件记录失败:\n"+rootDirAbsPath+"\\"+PathName+"\\AOIDataUploadIdentification.txt")
        sys.exit()

#ftp创建多级目录
def ftpCreateMultilevelDirectories(ftp,PathName):
    directoryNames = PathName.split("\\")
    for directoryName in directoryNames:
        try:
            ftp.mkd((directoryName).encode("utf-8").decode("ISO-8859-1"))
        except ftplib.error_perm as e:
            pass
        try:
            ftp.cwd((directoryName).encode("utf-8").decode("ISO-8859-1"))
        except ftplib.error_perm as e:
            generateErrorLogs('Failed to create FTP folder:\n'+PathName+"\n"+traceback.format_exc())
            promptBox('在ftp服务器上无法更改目录,请检查网络、权限和目录路径,error:'+ directoryName +str(e))
            return False
    return True

#修改文件名
def modifyFileName(rootDirAbsPath,PathName,FileName):
    try:
        os.rename(rootDirAbsPath+"\\"+PathName+"\\"+FileName,rootDirAbsPath+"\\"+PathName+"\\Uploaded_"+FileName)
    except FileExistsError:
        #出现重名时，先将第二个文件名加 _1,后将第一个文件名还原
        fns = os.path.splitext(FileName)
        os.rename(rootDirAbsPath+"\\"+PathName+"\\"+FileName,rootDirAbsPath+"\\"+PathName+"\\"+fns[0]+"_1"+fns[1])
        os.rename(rootDirAbsPath+"\\"+PathName+"\\Uploaded_"+FileName,rootDirAbsPath+"\\"+PathName+"\\"+FileName)
    except:
        generateErrorLogs('Failed to change local file name:\n'+rootDirAbsPath+"\\"+PathName+"\\"+FileName+"\n"+traceback.format_exc())
        promptBox('Error:更改文件名失败！ FileUrl:'+rootDirAbsPath+"\\"+PathName+"\\"+FileName)
        sys.exit()

#生成上传日志
def generateUploadLogs(fileUrl):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_Ymd = time.split(" ")[0]
    time_HMS = time.split(" ")[1]
    url = "./uploadLog/" + AOISETTING['LineName'] + " " + AOISETTING['StageName'] + " " + time_Ymd +".txt"
    with open(url,'a+',encoding="utf-8") as t:
        t.writelines(time_HMS+":Upload " + fileUrl + "\r\n")

#生成错误日志
def generateErrorLogs(errorString):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_Ymd = time.split(" ")[0]
    time_HMS = time.split(" ")[1]
    url = "./errorLog/" + AOISETTING['LineName'] + " " + AOISETTING['StageName'] + " " + time_Ymd +".txt"
    with open(url,'a+') as t:
        t.write(time_HMS+" "+errorString+"\n")

#上传记录存入数据库
def addUploadRecord(StageType,sFileUrl,fileUrl,rootDirAbsPath,client):
    aoiStorageRecord = {}
    if StageType != "AXI":
        aoiStorageRecord = analyticalPath(StageType,fileUrl,rootDirAbsPath,client)
        if aoiStorageRecord == False:
            return False
    else:
        aoiStorageRecord["fileType"] = "2"
        aoiStorageRecord["dateTime"] = timeStringConversionTime(
                        timeStampConversionTimeString(os.path.getctime(
                        rootDirAbsPath+"\\"+fileUrl.strip(".zip"))))
    aoiStorageRecord["lineName"] = AOISETTING["LineName"]
    aoiStorageRecord["stageName"] = AOISETTING["StageName"]
    aoiStorageRecord["aoiStorageServer"] = AOISETTING["AOIStorageServer"]
    aoiStorageRecord["path"] = sFileUrl + "\\" + fileUrl
    try:
        result = client.service.AddAOIStorageRecord(aoiStorageRecord)
    except:
        generateErrorLogs('Upload Record Write DB Failure:\n'+sFileUrl + "\\" + fileUrl+'\n'+traceback.format_exc())
        promptBox("上传记录存入数据库失败")
    if result != "OK":
        generateErrorLogs('Upload Record Write DB Failure:\n'+sFileUrl + "\\" + fileUrl+'\n'+result)
        promptBox("上传记录存入数据库失败")
        return False
    else:
        return True

#根据不同的Stage类型解析文件路径
def analyticalPath(StageType,fileUrl,rootDirAbsPath,client):
    aoiStorageRecord = {}
    aoiStorageRecord["IsSubgraph"] = False
    fs = fileUrl.split("\\")
    try:
        modelName = ""
        if StageType == "SMT_SPI":
            if fileUrl.endswith(".CSV") or fileUrl.endswith(".csv"):#CSV文件
                fs = fs[1].split("_")
                aoiStorageRecord["serialNumber"] = fs[1]
                aoiStorageRecord["fileType"] = "0"
            elif fileUrl.endswith(".PNG") or fileUrl.endswith(".png") \
                    or fileUrl.endswith(".JPG") or fileUrl.endswith(".jpg") \
                        or fileUrl.endswith(".JPEG") or fileUrl.endswith(".jpeg"):#图片文件
                aoiStorageRecord["serialNumber"] = fs[3]
                aoiStorageRecord["fileType"] = "1"
        elif StageType == "SMT_AOI":
            if len(fs) == 3:#大图
                fs = fs[2].split(".")[0].split("-")
                try:
                    aoiStorageRecord["serialNumber"] = fs[1]
                except:
                    aoiStorageRecord["serialNumber"] = fs[0]
            elif len(fs) == 4:#小图
                aoiStorageRecord["dateTime"] = timeStringConversionTime(fs[2].split("_")[0])
                aoiStorageRecord["IsSubgraph"] = True
            # elif len(fs) == 1:#RS图
            #     aoiStorageRecord["serialNumber"] = fs[0].split("_")[0]
            aoiStorageRecord["fileType"] = "1"
        elif StageType == "DIP_AOI":
            if len(fs) == 4:#图片路径1
                modelName = fs[0]
                aoiStorageRecord["modelName"] = modelName
                aoiStorageRecord["serialNumber"] = fs[3].split(".")[0]
            elif len(fs) == 2:#图片路径2
                aoiStorageRecord["serialNumber"] = fs[1].split(".")[0]
            aoiStorageRecord["fileType"] = "1"
        elif StageType == "Final_AOI":
            #小图路径相对于大图多了一层序列号文件夹，但是取序列号的位置不变（都是在路径的第四个位置），所以代码相同
            modelName = fs[1]
            aoiStorageRecord["modelName"] = modelName
            aoiStorageRecord["serialNumber"] = fs[3].split(".")[0].split("_")[0]
            aoiStorageRecord["fileType"] = "1"
            if len(fs) == 5:
                aoiStorageRecord["IsSubgraph"] = True
        if modelName != "":
            result = client.service.addModelName(modelName)
            if result != "OK":
                generateErrorLogs('Add ModelName Failure:\n'+rootDirAbsPath+"\\"+fileUrl+"\n"+result)
                promptBox("添加ModelName失败")
                return False
        timeString = timeStampConversionTimeString(os.path.getctime(rootDirAbsPath+"\\"+fileUrl))
        aoiStorageRecord["dateTime"] = timeStringConversionTime(timeString)
        return aoiStorageRecord
    except Exception as e:
        generateErrorLogs('Url Error:\n'+rootDirAbsPath+"\\"+fileUrl+"\n"+traceback.format_exc())
        promptBox("解析文件路径错误!")
        return False
    
#StageType AXI 压缩文件
def compressedFile(startdir,rootDirAbsPath):
    try:
        file_news = startdir +'.zip'
        z = zipfile.ZipFile(rootDirAbsPath+"\\"+file_news,'w',zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(rootDirAbsPath+"\\"+startdir):
            fpath = dirpath.replace(startdir,'')
            fpath = fpath and fpath + os.sep or '' #实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename),fpath+filename)
        z.close()
    except:
        generateErrorLogs('Compressed file failed:\n'+rootDirAbsPath+"\\"+startdir+'\n'+traceback.format_exc())
        promptBox("压缩文件失败!")
        sys.exit()

#时间字符串转时间
def timeStringConversionTime(timeString):
    return datetime.strptime(timeString,"%Y%m%d%H%M%S")

#时间戳转换为时间字符串
def timeStampConversionTimeString(ltime):
    return time.strftime("%Y%m%d%H%M%S",time.localtime(int(ltime)))
