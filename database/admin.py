from csv import list_dialects
from django.contrib import admin

from .models import Stage, Line, ModelName
from .models import AOIStorageRecord
from .models import Connect
from .models import ComponentCoordinatesFile, Computer, Count

# Register your models here.
class StageAdmin(admin.ModelAdmin):
    list_display = ('StageID', 'Name', 'Code', 'MfgType', 'Description')
    search_fields = (
        'Name',
        'Code',
        'MfgType',
    )
    #  list_filter = ('SerialNumber', 'CurrentTestCase')
    ordering = (
        'Name',
        'Code',
        'MfgType',
    )


class LineAdmin(admin.ModelAdmin):
    list_display = ('LineID', 'Name')


class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('ModelNameID', 'ModelName')


class AOIStorageRecordAdmin(admin.ModelAdmin):
    list_display = (
        'AOIStorageRecordID',
        'ModelName',
        'SerialNumber',
        'DateTime',
        'StageName',
        'LineName',
        'FileType',
        'Path',
        'AOIStorageServer',
        'CreateTime',
        'PartNumber',
        'MO',
        'Customer',
        # 'LeftTupperCoordinateX',
        # 'LowerRightCoordinateX',
        # 'LeftTupperCoordinateY',
        # 'LowerRightCoordinateY',
        'IsSubgraph',
    )
    search_fields = (
        'CreateTime',
        'SerialNumber',
        'DateTime',
    )
    #  list_filter = ('SerialNumber', 'CurrentTestCase')
    ordering = (
        'CreateTime',
        'SerialNumber',
        'DateTime',
    )


class ConnectAdmin(admin.ModelAdmin):
    list_display = (
        'ConnectID',
        'Name',
        'Host',
        'Port',
        'User',
        'Password',
        'Timeout',
        'AbsoluteDirPath',
        'Description',
    )
    search_fields = ('Name', 'Host')
    ordering = ('Name', 'Host')


class ComponentCoordinatesFileAdmin(admin.ModelAdmin):
    list_display = ('ComponentCoordinatesFileID', 'SerialNumber', 'Path')


class ComputerAdmin(admin.ModelAdmin):
    list_display = (
        'ComputerID',
        'IP',
        'LineName',
        'StageName',
        'LocalRootDirAbsPaths',
        'AOIStorageServer',
        "Status",
        "OSType",
        "User",
        "Password",
    )


class CountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Linename',
        'UploadCount',
        'DateTime',
        'AllCount',
    )


admin.site.register(Stage, StageAdmin)
admin.site.register(AOIStorageRecord, AOIStorageRecordAdmin)
admin.site.register(Connect, ConnectAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(ModelName, ModelNameAdmin)
admin.site.register(ComponentCoordinatesFile, ComponentCoordinatesFileAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(Count, CountAdmin)
