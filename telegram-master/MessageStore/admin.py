from django.contrib import admin
from .models import Client, Device, Data, Language, DeviceGroup

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'imei')


class DataAdmin(admin.ModelAdmin):
    list_display = ('device', 'datetime')


class LangAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = ((None, {
        'fields': ('name',)
    }), (
        'Data', {
            'fields': ('temperature1', 'humidity1', 'temperature2', 'humidity2', 'wind', 'gas', 'voltage', 'machineStatus')
        }
    ),
        ('Alert', {
            'fields': ('gasWarning', 'volWarning', 'tempWarning', 'inverWarning', 'alarmStatus', 'machineStart', 'machineStop', 'machineErorr', 'machineWarning')
        }),
        ('Language Interface', {
            'fields': ('wellcome', 'smavGroup', 'selectSmav', 'smavList', 'chooseSmav', 'chooseLanguage', 'setAlarm', 'request', 'chooseRequest')
        }),
        ('Request', {
            'fields': ('generalState', 'temperatureState', 'windState', 'gasState', 'machineState')
        })
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Language, LangAdmin)
admin.site.register(DeviceGroup)
