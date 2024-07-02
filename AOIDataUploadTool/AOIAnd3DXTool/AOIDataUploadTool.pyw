import AOIToolFunction as ATF
import ftplib
import traceback
import time,datetime
import threading
import os
import sys
import subprocess

def main():
    try:
        print("开始")
        readAOIConfig_result,AOISetting = ATF.readAOIConfig()
        if readAOIConfig_result is False:
            ATF.promptBox(AOISetting)
            return False
        
        IsAoiStorageStage_result = client.service.IsAoiStorageStage(AOISetting['StageName'])
        
        if IsAoiStorageStage_result != 'Yes':
            ATF.promptBox(IsAoiStorageStage_result)
            return False
        GetConnectConfig_result = client.service.GetConnectConfig(AOISetting['AOIStorageServer'])
        for lrd in AOISetting['LocalRootDirAbsPath']:
            if not os.path.isdir(lrd):
                ATF.promptBox("LocalRootDirAbsPath \""+lrd+"\" could not be found!!!")
                return False
        if GetConnectConfig_result.result != 'OK':
            ATF.promptBox(GetConnectConfig_result.result)
            return False
        else:
            client.service.addLine(AOISetting["LineName"])
            connectConfig = GetConnectConfig_result.connectConfig
            mainUploadFlie_result = mainUploadFlie(connectConfig,AOISetting)
            if mainUploadFlie_result is False:
                return False
            else:
                return True
    except Exception as e:
        ATF.generateErrorLogs('Main error:\n'+traceback.format_exc())
        ATF.promptBox("主程序出错，请联系开发人员!")
        return False
    
def mainUploadFlie(connectConfig,AOISetting):
    Stage = AOISetting["StageName"]
    StageType = getStageType(Stage)
    if StageType is False:
        ATF.promptBox("StageType出错!")
        return False
    MachineType = ""
    if StageType == "AXI": 
        MachineType = Stage.split("_")[1]
    try:
        Line = AOISetting["LineName"]
        rootDirAbsPaths = AOISetting["LocalRootDirAbsPath"]
        if Stage == "AXI_7600SII" or Stage =="AXI_7600SIII":
            interval = 4
        else:
            interval = 20
        for rootDirAbsPath in rootDirAbsPaths:
            fs = ATF.monitoringFile(rootDirAbsPath,StageType,MachineType)
            if len(fs) == 0:
                continue
            for i in range(0,len(fs),interval):
                try:
                    small_fs = fs[i:i+interval]
                    t=threading.Thread(target=circularUploadFile, args=(small_fs,
                                                                Line,Stage,rootDirAbsPath,StageType,connectConfig))
                    t.start()
                    t.join()
                except:
                    ATF.generateErrorLogs('Main error:\n'+traceback.format_exc())
                    ATF.promptBox("创建线程出错!")
        return True
    except Exception as e:
        ATF.generateErrorLogs('MaiUpload exception causes FTP upload file failure:\n'+traceback.format_exc())
        ATF.promptBox("上传函数出错!")
        return False

#small_fs：文件路径集合 Line：线别 Stage:站别 rootDirAbsPath：根目录 StageType：站别类型 connectConfig：配置字典
def circularUploadFile(small_fs,Line,Stage,rootDirAbsPath,StageType,connectConfig):
    sd_directorys = ["sda","sdb","sdc","sdd"]
    try:
        for index,f in enumerate(small_fs):
            #DIP_FINAL_AOI站别部分图片不符合规则，排除
            if Stage == "DIP_FINAL_AOI" and len(f.split("\\")) == 3:
                continue
            if (Stage == "AXI_7600SII" or Stage =="AXI_7600SIII") and len(small_fs) == 1:
                sd_directory = sd_directorys[cal() % 4]
            else:
                sd_directory = sd_directorys[index % 4]
            sf = sd_directory+"\\"+Line+"\\"+Stage
            if StageType == "AXI":
                ATF.compressedFile(f,rootDirAbsPath)
                f = f +'.zip'
            try:
                ftp = ATF.connect_ftp(connectConfig.host,connectConfig.user,
                            connectConfig.password,connectConfig.absoluteDirPath,
                            port = int(connectConfig.port))
                #转码防止出现罗马数字导致cwd失败
                ftp.cwd((connectConfig.absoluteDirPath).encode("utf-8").decode("ISO-8859-1"))
                ATF.fileUpload(ftp,sf,f,rootDirAbsPath,StageType,client)
            except ftplib.error_temp as e:
                ATF.generateErrorLogs('ftp连接超时:\n'+traceback.format_exc())
                ftp = ATF.connect_ftp(connectConfig.host,connectConfig.user,
                            connectConfig.password,connectConfig.absoluteDirPath,
                            port = int(connectConfig.port))
                ftp.cwd((connectConfig.absoluteDirPath).encode("utf-8").decode("ISO-8859-1"))
                ATF.fileUpload(ftp,sf,f,rootDirAbsPath,StageType,client)
            except:
                ATF.generateErrorLogs('Main error:\n'+traceback.format_exc())
                ATF.promptBox("ftp连接出错!")
                continue
            finally:
                if ftp is not None:
                    # ftplib发送退出请求超时之后，不用管它，pass即可，别的图片上传成功会退出
                    try:
                        ftp.quit()
                    except:
                        pass
    except Exception as e:
        ATF.generateErrorLogs('Main error:\n'+traceback.format_exc())
        ATF.promptBox("线程函数出错!")
        quit()
        

#根据StageName给出指定类型
def getStageType(StageName):
    list_SPI = ["SMT_SPI_TOP","SMT_SPI_BOT"]
    list_SMT_AOI = ["SMT_AOI_TOP","SMT_AOI_BOT"]
    list_DIP_AOI = ["DIP_AOI","DIP_AOI2"]
    list_Final_AOI = ["DIP_FINAL_AOI","DIP_FINAL_AOI2","FA_AOI"]
    list_AXI = ["AXI_5DX","AXI_7600SII","AXI_7600SIII"]
    
    if StageName in list_SPI:
        return "SMT_SPI"
    elif StageName in list_SMT_AOI:
        return "SMT_AOI"
    elif StageName in list_DIP_AOI:
        return "DIP_AOI"
    elif StageName in list_Final_AOI:
        return "Final_AOI"
    elif StageName in list_AXI:
        return "AXI"
    else:
        return False

def get_all_pid_name(exe):
    proc = subprocess.Popen("tasklist", shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tns = proc.stdout.read().split()
    i = 0
    for tn in tns:
        if exe == tn:
            i = i+1
    return i

#计算当天属于一年的多少天，用于AXI_7600SII和AXI_7600SIII上传时分配文件夹
def cal():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    month = yesterday.month
    day = yesterday.day
    months=[0,31,59,90,120,151,181,212,243,273,304,334]
    return day+months[month-1]


if __name__ == "__main__":
    exe = bytes(os.path.basename(sys.argv[0]),encoding="gbk")
    print(exe)
    i = get_all_pid_name(exe)
    print(i)
    if i >= 3:
        ATF.promptBox("工具已运行!!!")
        sys.exit()
    
    try:
        client = ATF.getClient()
        while(True):
            mr = main()
            time.sleep(10)
            if(not mr):
                break
    except Exception as e:
        ATF.promptBox("连接webservice失败!")














