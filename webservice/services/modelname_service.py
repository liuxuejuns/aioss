"""
File: modelname_service.py
Description:
    Provide web service interfaces about AOI Storage ModelName.
Author: Guangnai Wang (Guangnai_Wang@wistron.com)
Revision history:
    2019/8/7 (Guangnai) First version and add a interface addModelName.
"""

from database.models import ModelName

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase
from spyne.decorator import srpc
# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import Int, String, Unicode, Boolean


class ModelNameService(ServiceBase):

    @srpc(String(max_len=50), _returns=String)
    def addModelName(modelName):
        try:
            mn = ModelName.objects.filter(ModelName=modelName).first()
            if mn is None:
                ModelName.objects.create(ModelName=modelName)
            return "OK"
        except Exception as ex:
            return str(ex)
        

