from database.models import Connect

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase
from spyne.decorator import srpc
# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import Int, String, Unicode, Boolean


class ConnectConfigType(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    name = String(max_len=20)
    host = String(max_len=50)
    port = String(max_len=10)
    user = String(max_len=50)
    password = String(max_len=50)
    timeout = String(max_len=10)
    absoluteDirPath = String(max_len=512)
    description = String(max_len=512)


class ConnectConfigResult(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    connectConfig = ConnectConfigType
    result = String


class ConnectService(ServiceBase):
    @srpc(String(max_len=20), _returns=ConnectConfigResult)
    def GetConnectConfig(serverName):
        try:
            connect = Connect.objects.filter(Name=serverName).first()
            if connect is not None:
                connect_config = ConnectConfigType(
                    name=connect.Name,
                    host=connect.Host,
                    port=connect.Port,
                    user=connect.User,
                    password=connect.Password,
                    timeout=connect.Timeout,
                    absoluteDirPath=connect.AbsoluteDirPath,
                    description=connect.Description
                )
                connect_config_result = ConnectConfigResult(
                    connectConfig=connect_config,
                    result="OK"
                )
                return connect_config_result
            else:
                connect_config_result = ConnectConfigResult(
                    connectConfig=None,
                    result="There isn't connect config of The Server Name %s." % (serverName)
                )
                return connect_config_result
        except Exception as ex:
            connect_config_result = ConnectConfigResult(
                connectConfig=None,
                result=str(ex)
            )
            return connect_config_result
        

