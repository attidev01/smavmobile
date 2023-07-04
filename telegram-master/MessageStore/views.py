from dataclasses import field
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .helper import find_device, save_data, getUserGroup, getData, getAllDevice


@csrf_exempt
def message_handle(request, imei):
    if request.method == 'POST':
        device = find_device(imei)
        if device is None:
            return HttpResponse('device not found')
        valid = save_data(request.body, device)
        if valid == 0:
            return HttpResponse('success')
        return HttpResponse('fail')
    return HttpResponse('ok')

def getGroup(request, user_id):
    groups = getUserGroup(user_id)
    data = serializers.serialize("json", groups, fields = ("name", "description"))
    print(data)
    return HttpResponse(data, content_type="application/json")

def getDataDevice(request, device_imei):
    item = getData(device_imei)
    
    data = serializers.serialize("json", item)

    return HttpResponse(data, content_type="application/json")

def getDevice(request, group_name):
    devices = getAllDevice(group_name)
    
    data = serializers.serialize("json", devices)
    print(data)

    return HttpResponse(data, content_type="application/json")