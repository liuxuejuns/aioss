from django.db import models


# Create your models here.
class Stage(models.Model):
    MFG_TYPE_PCB = 'PCB'
    MFG_TYPE_CHOICES = ((MFG_TYPE_PCB, 'PCB'),)
    STAGE_NAME_CHOICES = (
        ('SMT_SPI_TOP', 'SMT_SPI_TOP'),
        ('SMT_SPI_BOT', 'SMT_SPI_BOT'),
        ('SMT_AOI_II_TOP', 'SMT_AOI_II_TOP'),
        ('SMT_AOI_II_BOT', 'SMT_AOI_II_BOT'),
        ('SMT_AOI_III_TOP', 'SMT_AOI_III_TOP'),
        ('SMT_AOI_III_BOT', 'SMT_AOI_III_BOT'),
        ('DIP_AOI', 'DIP_AOI'),
        ('DIP_AOI2', 'DIP_AOI2'),
        ('DIP_FINAL_AOI2', 'DIP_FINAL_AOI2'),
        ('DIP_FINAL_AOI', 'DIP_FINAL_AOI'),
        ('FA_AOI', 'FA_AOI'),
        ('AXI_5DX', 'AXI_5DX'),
        ('AXI_7600SII', 'AXI_7600SII'),
        ('AXI_7600SIII', 'AXI_7600SIII'),
    )
    CODE_CHOICES = (
        ('T3', 'T3_SMT_SPI_TOP'),
        ('T9', 'T9_SMT_SPI_BOT'),
        ('TK', 'TK_SMT_AOI_TOP'),
        ('TL', 'TL_SMT_AOI_BOT'),
        ('T1', 'T1_DIP_AOI'),
        ('TY', 'TY_DIP_AOI2'),
        ('OA', 'OA_DIP_FINAL_AOI2'),
        ('T1', 'T1_DIP_FINAL_AOI'),
        ('IZ', 'IZ_FA_AOI'),
        ('FD/FG', 'AXI'),
    )
    DESCRIPTION_CHOICES = (
        ('SMT SPI TOP', 'SMT SPI TOP'),
        ('SMT SPI BOT', 'SMT SPI BOT'),
        ('SMT AOI TOP', 'SMT AOI TOP'),
        ('SMT AOI BOT', 'SMT AOI BOT'),
        ('A zone DIP AOI', 'A zone DIP AOI'),
        ('B zone DIP AOI', 'B zone DIP AOI'),
        ('A zone DIP Final AOI', 'A zone DIP Final AOI'),
        ('B zone DIP Final AOI', 'B zone DIP Final AOI'),
        ('FA_AOI', 'FA_AOI'),
        ('AXI 5DX', 'AXI 5DX'),
        ('AXI 7600SII', 'AXI 7600SII'),
        ('AXI 7600SIII', 'AXI 7600SIII'),
    )
    StageID = models.AutoField(primary_key=True)
    MfgType = models.CharField(
        max_length=3, choices=MFG_TYPE_CHOICES, default=MFG_TYPE_PCB
    )  # value: PCB
    Name = models.CharField(max_length=50, unique=True, choices=STAGE_NAME_CHOICES)
    Code = models.CharField(max_length=15, choices=CODE_CHOICES)
    Description = models.CharField(max_length=50)

    class Meta:
        db_table = 'Stage'

    def __str__(self):
        return 'ID%s: MfgType(%s), Name(%s), Code(%s)' % (
            self.StageID,
            self.MfgType,
            self.Name,
            self.Code,
        )


class AOIStorageRecord(models.Model):
    AOI_SERVER = 'AOIServer'
    AOI_3DX_SERVER = 'AOI3DXServer'
    NAME_CHOICES = (
        (AOI_SERVER, AOI_SERVER),
        (AOI_3DX_SERVER, AOI_3DX_SERVER),
    )
    AOIStorageRecordID = models.AutoField(primary_key=True)
    ModelName = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    SerialNumber = models.CharField(
        max_length=250, db_index=True, null=True, blank=True
    )
    DateTime = models.DateTimeField()
    StageName = models.CharField(max_length=50, db_index=True)
    LineName = models.CharField(max_length=10, db_index=True)
    FileType = models.CharField(max_length=1, db_index=True)
    Path = models.CharField(max_length=512)
    AOIStorageServer = models.CharField(max_length=20, choices=NAME_CHOICES)
    CreateTime = models.DateTimeField(db_index=True)
    PartNumber = models.CharField(max_length=50, null=True, blank=True)
    MO = models.CharField(max_length=128, null=True, blank=True)
    Customer = models.CharField(max_length=128, null=True, blank=True)
    # LeftTupperCoordinateX = models.FloatField(null=True,blank=True)
    # LowerRightCoordinateX = models.FloatField(null=True, blank=True)
    # LeftTupperCoordinateY = models.FloatField(null=True,blank=True)
    # LowerRightCoordinateY = models.FloatField(null=True, blank=True)
    IsSubgraph = models.BooleanField(default=False)

    class Meta:
        db_table = 'AOIStorageRecord'

    def __str__(self):
        return 'ID%s: ModelName(%s), SN(%s), DateTime(%s)' % (
            self.AOIStorageRecordID,
            self.ModelName,
            self.SerialNumber,
            self.DateTime,
        )


class Connect(models.Model):
    AOI_SERVER = 'AOIServer'
    AOI_3DX_SERVER = 'AOI3DXServer'
    NAME_CHOICES = (
        (AOI_SERVER, AOI_SERVER),
        (AOI_3DX_SERVER, AOI_3DX_SERVER),
    )
    ConnectID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, choices=NAME_CHOICES, unique=True)
    Host = models.CharField(max_length=50)
    Port = models.CharField(max_length=10)
    User = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Timeout = models.CharField(max_length=10, null=True, blank=True)
    AbsoluteDirPath = models.CharField(max_length=512)
    Description = models.CharField(max_length=512)

    class Meta:
        db_table = 'Connect'

    def __str__(self):
        return 'ID%s: %s' % (self.ConnectID, self.Name)


class Line(models.Model):
    LineID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = 'Line'

    def __str__(self):
        return 'ID%s: Name(%s)' % (self.LineID, self.Name)


class ModelName(models.Model):
    ModelNameID = models.AutoField(primary_key=True)
    ModelName = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'ModelName'

    def __str__(self):
        return 'ID%s: Name(%s)' % (self.ModelNameID, self.ModelName)


class ComponentCoordinatesFile(models.Model):
    ComponentCoordinatesFileID = models.AutoField(primary_key=True)
    SerialNumber = models.CharField(max_length=250, null=True, blank=True)
    Path = models.CharField(max_length=512)

    class Meta:
        db_table = 'ComponentCoordinatesFile'

    def __str__(self):
        return 'ID%s: Name(%s)' % (self.ComponentCoordinatesFileID, self.SerialNumber)


class Computer(models.Model):
    ComputerID = models.AutoField(primary_key=True)
    IP = models.CharField(max_length=50, blank=True, unique=True)
    LineName = models.CharField(max_length=10, blank=True)
    StageName = models.CharField(max_length=50, blank=True)
    LocalRootDirAbsPaths = models.CharField(max_length=512, null=True)
    AOIStorageServer = models.CharField(max_length=20)
    User = models.CharField(max_length=50, null=True)
    Password = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(default=0)  # 0:未连接 1:未启动 2:启动 3:异常 4:网络断开
    OSType = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'Computer'

    def __str__(self):
        return 'ID%s: Name(%s)' % (self.ComputerID, self.IP)


class Count(models.Model):
    id = models.AutoField(primary_key=True)
    Linename = models.CharField(max_length=10, blank=True)
    UploadCount = models.IntegerField(default=0)
    DateTime = models.DateField()
    AllCount = models.IntegerField(default=0)

    class Meta:
        db_table = 'Count'
