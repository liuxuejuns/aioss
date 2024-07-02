from database.models import AOIStorageRecord
from django.utils import timezone

# spyne.service.ServiceBase is the base class for all service definitions.
from spyne.service import ServiceBase

"""
The @srpc decorator exposes methods as remote procedure calls and declares the data types it accepts and returns. 
The ‘s’ prefix is short for ‘static’ (or stateless, if you will) – the function receives no implicit arguments. 
This decorator enables passing spyne.MethodContext instance as an implicit first argument to the user callable.
"""
from spyne.decorator import srpc

# from spyne.decorator import rpc

# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable, ComplexModel, Array
from spyne.model.primitive import (
    Int,
    String,
    Unicode,
    Boolean,
    DateTime,
    UnsignedInteger,
    Integer,
)


class HasAOIStorageRecordype(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    modelName = String(max_len=50)
    serialNumber = String(max_len=250)
    dateTime = DateTime(nullable=False, min_occurs=1)  # default is Nullable
    stageName = String(max_len=50)
    lineName = String(max_len=10)
    fileType = String(max_len=1)
    path = String(max_len=512)
    IsSubgraph = Boolean(nullable=False, min_occurs=1)


class AOIStorageRecordType(ComplexModel):
    __namespace__ = "aoiss.webservice.services"

    modelName = String(max_len=50)
    serialNumber = String(max_len=250)
    dateTime = DateTime(nullable=False, min_occurs=1)  # default is Nullable
    stageName = String(max_len=50)
    lineName = String(max_len=10)
    fileType = String(max_len=1)
    path = String(max_len=512)
    aoiStorageServer = String(max_len=20)
    IsSubgraph = Boolean(nullable=False, min_occurs=1)
    MO = String(max_len=50)
    Customer = String(max_len=50)


class AOIStorageRecordService(ServiceBase):
    @srpc(HasAOIStorageRecordype, _returns=String)
    def HasAOIStorageRecord(aoiStorageRecord):
        try:
            record = (
                AOIStorageRecord.objects.filter(
                    ModelName=aoiStorageRecord.modelName,
                    SerialNumber=aoiStorageRecord.serialNumber,
                    DateTime=aoiStorageRecord.dateTime,
                    StageName=aoiStorageRecord.stageName,
                    LineName=aoiStorageRecord.lineName,
                    FileType=aoiStorageRecord.fileType,
                    Path=aoiStorageRecord.path,
                    IsSubgraph=aoiStorageRecord.IsSubgraph,
                ).first(),
            )

            if record is not None:
                return "Yes"
            else:
                return "No, there isn't the AOI Storage record."
        except Exception as ex:
            return str(ex)

    @srpc(AOIStorageRecordType, _returns=String)
    def AddAOIStorageRecord(aoiStorageRecord):
        try:
            record = AOIStorageRecord.objects.create(
                ModelName=aoiStorageRecord.modelName,
                SerialNumber=aoiStorageRecord.serialNumber,
                DateTime=aoiStorageRecord.dateTime,
                StageName=aoiStorageRecord.stageName,
                LineName=aoiStorageRecord.lineName,
                FileType=aoiStorageRecord.fileType,
                Path=aoiStorageRecord.path,
                AOIStorageServer=aoiStorageRecord.aoiStorageServer,
                IsSubgraph=aoiStorageRecord.IsSubgraph,
                MO=aoiStorageRecord.MO,
                Customer=aoiStorageRecord.Customer,
                CreateTime=timezone.now(),
            )
            return "OK"
        except Exception as ex:
            return str(ex)
