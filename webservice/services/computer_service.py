from database.models import Computer

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase
from spyne.decorator import srpc
# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import Int, String, Unicode, Boolean
import os
import threading

class ComputerConfigType(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    ComputerID = String(max_len=10)
    IP = String(max_len=50)
    LineName = String(max_len=10)
    StageName = String(max_len=10)
    LocalRootDirAbsPaths = String(max_len=512)
    AOIStorageServer = String(max_len=20)
    User = String(max_len=50)
    Password = String(max_len=50)
    Status = Int(max_len=1)
    OSType = String(max_len=50)

class ComputerConfigResult(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    ComputerConfig = ComputerConfigType
    result = String

class GetAllComputerResult(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    ComputerConfigList = Array(ComputerConfigType)
    result = String

class ComputerStatusType(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    computer = String(max_len=20)
    Status = String(max_len=1)

class ComputerService(ServiceBase):
    @srpc(String(max_len=20), _returns=ComputerConfigResult)
    def GetComputerConfig(ComputerID):
        try:
            computer = Computer.objects.filter(ComputerID=int(ComputerID)).first()
            if computer is not None:
                Computer_config = ComputerConfigType(
                    ComputerID=computer.ComputerID,
                    IP=computer.IP,
                    LineName=computer.LineName,
                    StageName=computer.StageName,
                    LocalRootDirAbsPaths=computer.LocalRootDirAbsPaths,
                    User=computer.User,
                    Password=computer.Password,
                    Status=computer.Status,
                    AOIStorageServer=computer.AOIStorageServer
                )
                Computer_config_result = ComputerConfigResult(
                    ComputerConfig=Computer_config,
                    result="OK"
                )
                return Computer_config_result
            else:
                Computer_config_result = ComputerConfigResult(
                    ComputerConfig=None,
                    result="The computer does not exist."
                )
                return Computer_config_result
        except Exception as ex:
            Computer_config_result = ComputerConfigResult(
                ComputerConfig=None,
                result=str(ex)
            )
            return Computer_config_result

    @srpc(_returns=GetAllComputerResult)
    def GetAllComputer():
        try:
            computers = Computer.objects.filter()
            Computer_Config_List = []
            for computer in computers:
                Computer_config = ComputerConfigType(
                    ComputerID=computer.ComputerID,
                    IP=computer.IP,
                    LineName=computer.LineName,
                    StageName=computer.StageName,
                    LocalRootDirAbsPaths=computer.LocalRootDirAbsPaths,
                    User=computer.User,
                    Password=computer.Password,
                    Status=computer.Status,
                    AOIStorageServer=computer.AOIStorageServer,
                    OSType=computer.OSType
                )
                Computer_Config_List.append(Computer_config)
            
            Get_All_Computer_Result = GetAllComputerResult(
                ComputerConfigList = Computer_Config_List,
                result = "OK"
            )

            return Get_All_Computer_Result

        except Exception as e:
            return GetAllComputerResult(
                ComputerConfigList = None,
                result = str(e)
            )

    @srpc(ComputerStatusType,_returns=String)
    def UpdateComputerStatus(ComputerIDAndStatus):
        try:
            computer = ComputerIDAndStatus.computer
            if computer.find(".") != -1:
                Computer.objects.filter(IP=computer).update(Status=ComputerIDAndStatus.Status)
            else:
                Computer.objects.filter(ComputerID=computer).update(Status=ComputerIDAndStatus.Status)
            return "OK"
        except Exception as ex:
            return str(ex)