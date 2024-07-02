import AOI3DXToolFunction as ATF
import ftplib
import traceback

def main():
    readAOIConfig_result,AOISetting = ATF.readAOIConfig()
    if readAOIConfig_result is False:
        ATF.promptBox(AOISetting)
        return
    client = ATF.getClient()
    IsAoiStorageStage_result = client.service.IsAoiStorageStage(AOISetting['StageName'])
    if IsAoiStorageStage_result != 'Yes':
        ATF.promptBox(IsAoiStorageStage_result)
        return
    GetConnectConfig_result = client.service.GetConnectConfig(AOISetting['AOI3DXStorageServer'])
    if GetConnectConfig_result.result != 'OK':
        ATF.promptBox(GetConnectConfig_result.result)
        return
    else:
        connectConfig = GetConnectConfig_result.connectConfig
        mainUploadFlie_result = mainUploadFlie(connectConfig,AOISetting)
        if mainUploadFlie_result is False:
            return
    
def mainUploadFlie(connectConfig,AOISetting):
    Stage = AOISetting["StageName"]
    StageType = getStageType(Stage)
    if StageType is False:
        ATF.promptBox("程序出错，请联系开发人员!")
        return False
    if StageType != "SMT_AOI":
        return False
    try:
        ftp = ATF.connect_ftp(connectConfig.host,connectConfig.user,
                              connectConfig.password,connectConfig.absoluteDirPath,
                              port = int(connectConfig.port))
        if ftp is None:
            return False
        Line = AOISetting["LineName"]
        rootDirAbsPath = AOISetting["LocalRootDirAbsPath"]
        fs = ATF.monitoringFile(rootDirAbsPath,StageType)
        for index,f in enumerate(fs):
            sf = Line+"\\"+Stage
            fileUpload_result = ATF.fileUpload(ftp,sf,f,rootDirAbsPath,StageType)
            if fileUpload_result:
                ftp.cwd(connectConfig.absoluteDirPath)
            else:
                return False
    except Exception as e:
        ATF.generateErrorLogs('MaiUpload exception causes FTP upload file failure:\n'+traceback.format_exc())
        ATF.promptBox("程序出错，请联系开发人员!")
        return False
    finally:
        if ftp is not None:
            ftp.quit()

#根据StageName给出指定类型
def getStageType(StageName):
    list_SPI = ["SMT_SPI_TOP","SMT_SPI_BOT"]
    list_SMT_AOI = ["SMT_AOI_TOP","SMT_AOI_BOT"]
    list_DIP_AOI = ["DIP_AOI","DIP_AOI2_IPC_RUNIN"]
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

if __name__ == "__main__":
    main()


















