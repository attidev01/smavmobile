from django.db import models
from webhooks.models import Whatsapp

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=15)
    chat_id = models.CharField(max_length=15)
    language = models.CharField(max_length=15, default='English')
    country = models.CharField(max_length=15, default='')
    alertStatus = models.IntegerField(default=0, editable=False)
    temperatureAlert = models.IntegerField(default=1)
    machineVoltage = models.IntegerField(default=12)
    lastmessage = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Telegram User"
        verbose_name = "Telegram User"


class Language(models.Model):
    name = models.CharField(max_length=15)
    temperature1 = models.CharField(max_length=15)
    humidity1 = models.CharField(max_length=15)
    temperature2 = models.CharField(max_length=15)
    humidity2 = models.CharField(max_length=15)
    wind = models.CharField(max_length=15)
    gas = models.CharField(max_length=15)
    voltage = models.CharField(max_length=15)
    machineStatus = models.CharField(max_length=15)
    gasWarning = models.CharField(max_length=30, default="")
    volWarning = models.CharField(max_length=30, default="")
    tempWarning = models.CharField(max_length=30, default="")
    inverWarning = models.CharField(max_length=30, default="")
    alarmStatus = models.CharField(max_length=30, default="Alarm")
    machineStart = models.CharField(max_length=30, default="")
    machineStop = models.CharField(max_length=30, default="")
    machineErorr = models.CharField(max_length=30, default="")
    machineWarning = models.CharField(max_length=30, default="")
    wellcome = models.CharField(max_length=30, default="Welcome to SMAV")
    smavGroup = models.CharField(max_length=30, default="SMAV Group")
    selectSmav = models.CharField(max_length=30, default="Select a SMAV")
    smavList = models.CharField(max_length=30, default="SMAV List")
    chooseSmav = models.CharField(max_length=30, default="Choose SMAV")
    chooseLanguage = models.CharField(max_length=30, default="Choose Language")
    setAlarm = models.CharField(max_length=30, default="Set Alarm")
    request = models.CharField(max_length=30, default="Request")
    chooseRequest = models.CharField(max_length=30, default="Choose Request")
    generalState = models.CharField(max_length=30, default="General State")
    temperatureState = models.CharField(max_length=30, default="Temperature")
    windState = models.CharField(max_length=30, default="Wind")
    gasState = models.CharField(max_length=30, default="Gas")
    machineState = models.CharField(max_length=30, default="Machine State")


class Device(models.Model):
    name = models.CharField(max_length=15)
    imei = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    clients = models.ManyToManyField(
        Client, blank=True, verbose_name="Telegram Users")
    whatsapps = models.ManyToManyField(
        Whatsapp, blank=True, verbose_name="WhatsApp Users")

    def __str__(self):
        return self.imei

    class Meta:
        verbose_name_plural = "Devices"


class Data(models.Model):
    temperature1 = models.FloatField(max_length=5)
    humidity1 = models.FloatField(max_length=5)
    temperature2 = models.FloatField(max_length=5)
    humidity2 = models.FloatField(max_length=5)
    wind = models.FloatField(max_length=5)
    gas = models.FloatField(max_length=5)
    voltage = models.FloatField(default=0)
    machineStatus = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.device.name

    class Meta:
        verbose_name_plural = "Datas"


class DeviceGroup(models.Model):
    name = models.CharField(max_length=25, verbose_name="SMAV Group Name")
    devices = models.ManyToManyField(
        Device, blank=True, verbose_name="Device Group")
    description = models.CharField(
        max_length=100, default='')
    whatsapps = models.ManyToManyField(
        Whatsapp, blank=True, verbose_name="WhatsApp User", )
    clients = models.ManyToManyField(
        Client, blank=True, verbose_name="Telegram User")

    class Meta:
        verbose_name_plural = "Device Group"

    def __str__(self):
        return self.name
