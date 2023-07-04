from celery import Celery, shared_task
from MessageStore.models import Device, Client, Data
from .helper import reply_data, whatsapp_send
import requests
import os

TOKEN = os.environ.get('TOKEN')


@shared_task()
def notification_whatsapp():
    try:
        devices = Device.objects.all()
        for device in devices:
            whatsapps = device.whatsapps.all()
            try:
                data = device.data_set.all()[0]
                for whatsapp in whatsapps:
                    result = reply_data(whatsapp.phone, '1', whatsapp.language)
                    whatsapp_send(result)
            except:
                pass
    except:
        return
