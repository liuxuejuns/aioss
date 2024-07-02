#该脚本用于AOI for Solar的图片上传功能。单独运行于AOI系统之外，只提供给10.41.102.93机器使用
#运行机器ip： 10.41.102.93  用户名： SolarUpload   密码：Wzsaoi@2021
#客人FTP   ip：soautotw.supermicro.com   用户名：TU_Wistron   密码：V9bNcR%QZc
import os,shutil
from zeep import Client
from requests import Session
from zeep.transports import Transport
from ftplib import FTP_TLS
import datetime
import time

class ftpuplpadjpg(FTP_TLS):
    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        super().voidcmd('TYPE I')
        with super().transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
        return super().voidresp()

while True:
    DirB = 'D:\\Final AOI photo\\BOT'                                  #放图片的文件夹(该文件夹里是从aoi传到中转机器的未改名图片)
    DirT = 'D:\\Final AOI photo\\TOP'
    if len(os.listdir(DirB)) == 0 and len(os.listdir(DirT)) == 0:
        continue
    else:
        time.sleep(10)
        session = Session()
        session.verify = False
        transport = Transport(session=session)                                               #取消证书认证
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        changenamerecord = "D:\\Final AOI photo\\Record\\ChangeName\\"+str(year)+"_"+str(month)+".txt"                             #创建/继续写入改名log文件
        uploadrecord = "D:\\Final AOI photo\\Record\\Upload\\"+str(year)+"_"+str(month)+".txt"                                #创建/继续写入上传log文件
        with open(changenamerecord, 'a+', encoding="utf-8") as t: 
            with open(uploadrecord, 'a+', encoding="utf-8") as u: 
                for root,dirs,names in os.walk("D:\\Final AOI photo"):
                    for filename in names:
                        url = os.path.join(root,filename)                           #获取所有图片路径
                        if url.split(".")[-1] == "jpg":
                            name=url.split("\\")[-1]                                    #获取图片名称
                            btname = url.split("\\")[-2]
                            if btname == "BOT":
                                number = "1"
                            else:
                                number = "2"
                            fn,ft = os.path.splitext(name)
                            if ft in [".png", ".PNG", ".JPG", ".jpg", ".jpeg", ".JPEG"]:
                                sn = fn.split("_")[0]
                                if len(sn) != 23 and len(sn) != 24:
                                    os.remove(url)                                     #命名不正确直接删除该图片
                                else:
                                    client = Client("https://mic136.wistron.com:126/tester.WebService/WebService.asmx?wsdl",transport=transport)
                                    result = client.service.GetDynamicData("GETSOLARCUSTOMERSN","USN",sn)
                                    ItemSerial = result["_value_1"]["_value_1"][0]["Table"]["CSN"]                #返回的客户sn
                                    dfile = "658028840_"+ItemSerial+"#"+str(number)+".jpg"
                                    url2 = "D:\\Upload\\658028840_"+ItemSerial+"#"+str(number)+".jpg"   #转存的文件路径（改了名称的图片存放位置，最后部分不改动）
                                    while True:
                                        shutil.copyfile(url,url2)
                                        t.writelines(name + "-->"+"658028840_"+ItemSerial+"#"+str(number)+".jpg"+"\n")
                                        ftp = ftpuplpadjpg()                                                                     #FTP链接
                                        ftp.connect("soautotw.supermicro.com")                                                 #链接ip与端口号(根据实际修改)
                                        ftp.login(user="TU_Wistron", passwd="V9bNcR"+"%"+"QZc")                                            #账号密码    (根据实际修改)
                                        ftp.prot_p()
                                        ftp.cwd("/AOI")                                            #FTP上要存放图片的路径(根据实际修改)
                                        try:
                                            ftp.delete(dfile)
                                        except:
                                            pass
                                        cmd = 'STOR '+dfile
                                        fp = open(url2,'rb')
                                        ftp.storbinary(cmd,fp)
                                        u.writelines(dfile + "\n")
                                        fp.close()
                                        ftp.quit()
                                        os.remove(url2)
                                        os.remove(url)
                                        break

