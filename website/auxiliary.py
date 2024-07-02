from database.models import Stage, AOIStorageRecord, Connect,Line,ModelName,ComponentCoordinatesFile,Computer
import os
import zeep
import errno
import traceback
from .backups_AOI_date_Tool import data_url_setting

#在字符串中寻找子字符串最后一次出现的位置
def find_last(str1,str2):
    last_index=-1
    while True:
        index = str1.find(str2,last_index+1)
        if index == -1:
            return last_index
        last_index = index

#判断程序是否存在
def pid_exists(pid):
    if pid < 0 or pid == 0:
        return False
    # if pid == 0:
    #     raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
        elif err.errno == errno.EPERM:
            return True
        else:
            return False
    else:
        return True

def getClient():
    wsdl = 'http://aoiss-nginx-service:8300/webservice/?wsdl'
    transport=zeep.Transport(cache=None)
    client = zeep.Client(wsdl=wsdl, transport=transport)
    client.service._binding_options['address']='http://aoiss-nginx-service:8300/webservice/'
    return client

#映射线上电脑的文件夹
def mount_Computer(ComputerID):
    computer = Computer.objects.filter(ComputerID=int(ComputerID)).first()
    LocalRootDirAbsPaths = computer.LocalRootDirAbsPaths.split(";")
    OSType = computer.OSType
    if OSType:
        OSType.replace(" ","").upper()
    else:
        OSType = ""

    data_url_setting_obj = data_url_setting.data_url_setting_obj()

    for LocalRootDirAbsPath in LocalRootDirAbsPaths:
        url = data_url_setting_obj.mount_url + computer.IP +"/"+ LocalRootDirAbsPath #"/var/AOI-ST/sdd/backupsAOIdateToolGeneratedFile/mountComputerFolder/"
        if os.path.isdir(url) and isMountpoint(url):
            continue

        if not os.path.isdir(url):
            cmd = "mkdir -p " + url
            f = os.system(cmd)
            if f != 0:
                return False,"创建文件夹"+url+"失败"
        
        if OSType == "WINDOWS7" or OSType == None or OSType == "":
            cmd1 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + ",vers=2.0,domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
                # ,dir_mode=0777,file_mode=0777 可设置权限为777
            cmd2 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + "domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
        elif OSType == "WINDOWSXP":
            cmd2 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + ",vers=1.0,domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
            cmd1 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + ",vers=1.0,domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
        else:
            cmd2 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + ",vers=2.1,domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
            cmd1 = "mount -t cifs -o user="+computer.User+",password="+computer.Password+",dir_mode=0777,file_mode=0777" \
                + ",vers=3.0,domain="+computer.IP+" //"+ computer.IP + LocalRootDirAbsPath + " " + url
        
        f1 = os.system(cmd1)
        if f1 != 0:
            #防止系统变更
            f2 = os.system(cmd2)
            if f2 != 0:
                return False,"挂载"+LocalRootDirAbsPath+"失败,请检查User,Password,LocalRootDirAbsPaths是否正确,防火墙是否关闭,电脑是否关机。"

    Computer.objects.filter(ComputerID=int(ComputerID)).update(Status=1)
    return True,"success"

def unmount_Computer(ComputerID):
    computer = Computer.objects.filter(ComputerID=int(ComputerID)).first()
    LocalRootDirAbsPaths = computer.LocalRootDirAbsPaths.split(";")

    data_url_setting_obj = data_url_setting.data_url_setting_obj()

    for LocalRootDirAbsPath in LocalRootDirAbsPaths:
        url = data_url_setting_obj.mount_url + computer.IP +"/"+ LocalRootDirAbsPath #"/var/AOI-ST/sdd/backupsAOIdateToolGeneratedFile/mountComputerFolder/"
        if not isMountpoint(url):
            continue
        cmd = "umount "+ url
        f = os.system(cmd)
        if f != 0:
            return False,cmd+"失败,可能是资源正忙,请稍后重试"
    Computer.objects.filter(ComputerID=int(ComputerID)).update(Status=0)
    return True,"success"

#判断是否是挂载点
def isMountpoint(url):
    cmd = "mountpoint " + url
    with os.popen(cmd,"r") as t:
        result = t.read()
    if "is not a mountpoint" in result:
        return False
    elif "is a mountpoint" in result:
        return True
    else:
        return False

# 查找目录下最新的文件
def find_new_file(dir):
    try:
        file_lists = os.listdir(dir)
    except FileNotFoundError:
        return ""
    
    if len(file_lists) == 0:
        return ""
    file_lists.sort(key=lambda fn: os.path.getmtime(dir + "/" + fn) if not os.path.isdir(dir + "/" + fn) else 0)
    #url = os.path.join(dir, file_lists[-1])
    return file_lists[-1]

#判断电脑是否可以ping通
def ping_computer(Computer_IP):
    cmd = "timeout 5 ping -c 1 " + Computer_IP
    os.popen(cmd)