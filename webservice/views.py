from django.shortcuts import render

# Create your views here.

# Application is the glue between one or more service definitions, interface and protocol choices.
from spyne.application import Application

from spyne.protocol.http import HttpRpc
from spyne.protocol.soap import Soap11

from spyne.server.django import DjangoApplication

from django.views.decorators.csrf import csrf_exempt

from webservice.services.stage_service import StageService
from webservice.services.aoi_storage_record_service import AOIStorageRecordService
from webservice.services.connect_service import ConnectService
from webservice.services.line_service import LineService
from webservice.services.modelname_service import ModelNameService
from webservice.services.computer_service import ComputerService

application = Application([StageService, AOIStorageRecordService, ConnectService,LineService,ModelNameService,ComputerService],
    tns='aoiss.webservice.services',
    name='AOIStorageSystemWebService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())

webservice_app = csrf_exempt(DjangoApplication(application))
