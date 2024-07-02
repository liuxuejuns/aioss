"""
File: line_service.py
Description:
    Provide web service interfaces about AOI Storage Line.
Author: Guangnai Wang (Guangnai_Wang@wistron.com)
Revision history:
    2019/8/7 (Guangnai) First version and add a interface addLine.
"""

from database.models import Line

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase
from spyne.decorator import srpc
# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import Int, String, Unicode, Boolean


class LineService(ServiceBase):

    @srpc(String(max_len=10), _returns=String)
    def addLine(LineName):
        try:
            line = Line.objects.filter(Name=LineName).first()
            if line is None:
                Line.objects.create(Name=LineName)
            return "OK"
        except Exception as ex:
            return str(ex)
        

