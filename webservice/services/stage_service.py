"""
File: stage_service.py
Description:
    Provide web service interfaces about AOI Storage stage.
Author: Sam Kwok (sam_kwok@wistron.com)
Revision history:
    2019/6/21 (Sam) First version and add a interface IsAoiStorageStage.
"""

from database.models import Stage

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase
from spyne.decorator import srpc
# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import Int, String, Unicode, Boolean


class StageService(ServiceBase):
    #  IsAoiStorageStage - Is AOI Storage Stage？.

    # arguement:
    #  @stageName: AOI Storage Stage.

    #  It returns 'Yes'. If any error occurs, it returns
    #  'No, it isn't aoi Storage stage.' or exception info.

    #  If it exists, the stageName is only one record in Database table Stage.

    @srpc(String(max_len=50), _returns=String)
    def IsAoiStorageStage(stageName):
        try:
            stage = Stage.objects.filter(Name=stageName).first()
            if stage is not None:
                return "Yes"
            else:
                return "No, it isn't aoi Storage stage."
        except Exception as ex:
            return str(ex)
        

