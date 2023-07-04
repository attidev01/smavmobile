from MessageStore.models import Device, Language, DeviceGroup
from .models import Whatsapp
import os
import json
import requests

TOKEN_WHATSAPP = os.environ.get('TOKEN_WHATSAPP')
PHONE_ID = os.environ.get('PHONE_ID')


headers = {"Authorization": "Bearer {0}".format(
    TOKEN_WHATSAPP), "Content-Type": "application/json"}


def get_reply_group(phone):
    try:
        whatsapp = Whatsapp.objects.get(phone=phone)
        language = Language.objects.get(name=whatsapp.language)
        device_reply = {"messaging_product": "whatsapp",
                        "to": phone,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": language.wellcome
                            },
                            "body": {
                                "text": language.smavGroup
                            },
                            "action": {
                                "button": language.smavGroup,
                                "sections": [
                                    {
                                        "title": language.smavGroup,
                                        "rows": []
                                    },
                                    {
                                        "title": language.chooseLanguage,
                                        "rows": []
                                    },
                                    {
                                        "title": language.setAlarm,
                                        "rows": [
                                            {"id": "alarm ON",
                                             "title": "ON"},
                                            {"id": "alarm OFF",
                                             "title": "OFF"}
                                        ]
                                    }
                                ]
                            }
                        }
                        }
        groups = whatsapp.devicegroup_set.all()
        for group in groups:
            device_reply["interactive"]["action"]["sections"][0]["rows"].append(
                {"id": 'group {0}'.format(group.name), "title": group.name, "description": group.description})
    except:
        device_reply["interactive"]["action"]["sections"][0]["rows"][0] = {
            "id": "no-device", "title": "NULL", }
    try:
        languages = Language.objects.all()
        for language in languages:
            device_reply["interactive"]["action"]["sections"][1]["rows"].append(
                {"id": f"language {language.name}", "title": language.name})
    except:
        pass
    return device_reply


def get_reply_device(phone, name):
    try:
        whatsapp = Whatsapp.objects.get(phone=phone)
        language = Language.objects.get(name=whatsapp.language)
        device_reply = {"messaging_product": "whatsapp",
                        "to": phone,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": language.wellcome
                            },
                            "body": {
                                "text": language.selectSmav
                            },
                            "action": {
                                "button": language.smavList,
                                "sections": [
                                    {
                                        "title": language.chooseSmav,
                                        "rows": []
                                    },
                                ]
                            }
                        }
                        }
        group = DeviceGroup.objects.get(name=name)
        devices = group.devices.all()
        for device in devices:
            device_reply["interactive"]["action"]["sections"][0]["rows"].append(
                {"id": device.imei, "title": device.name, "description": 'phone {0}'.format(device.phone)})
    except:
        device_reply["interactive"]["action"]["sections"][0]["rows"][0] = {
            "id": "no-device", "title": "NULL", }
    return device_reply


def get_reply_type(phone, imei):
    try:
        whatsapp = Whatsapp.objects.get(phone=phone)
        language = Language.objects.get(name=whatsapp.language)
        type_reply = {"messaging_product": "whatsapp",
                      "to": phone,
                      "recipient_type": "individual",
                      "type": "interactive",
                      "interactive": {
                          "type": "list",
                          "header": {
                              "type": "text",
                              "text": language.wellcome
                          },
                          "body": {
                              "text": language.request
                          },
                          "action": {
                              "button": language.request,
                              "sections": [
                                  {
                                      "title": language.chooseRequest,
                                      "rows": [
                                          {
                                              "id": "1",
                                              "title": language.generalState
                                          },
                                          {
                                              "id": "2",
                                              "title": language.temperatureState
                                          },
                                          {
                                              "id": "3",
                                              "title": language.windState
                                          },
                                          {
                                              "id": "4",
                                              "title": language.gasState
                                          },
                                          {
                                              "id": "5",
                                              "title": language.machineState
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                      }
    except:
        return 'Error'
    for i in range(5):
        type_reply["interactive"]["action"]["sections"][0]["rows"][i]["description"] = imei
    return type_reply


def general_state(item, name):
    try:
        lang = Language.objects.get(name=name)
        if int(item.machineStatus) < 12:
            machine = "OFF"
        else:
            machine = "ON"
        result = '*{0} ({18})*\r\n{9}: {1}°C \r\n{10}: {2}% RH\r\n{11}: {3}°C  \r\n{12}: {4}% RH\r\n{13}: {5}  Km/hr\r\n{14}: {6}%\r\n{15}: {7}\r\n{16}:{8}V\r\n_{17}_"\r\n'.format(
            item.device.name, item.temperature1, item.humidity1, item.temperature2, item.humidity2, item.wind, item.gas, machine, item.voltage, lang.temperature1, lang.humidity1, lang.temperature2, lang.humidity2, lang.wind, lang.gas, lang.machineStatus, lang.voltage, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def temperature(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '*{0} ({10})*\r\n{5}: {1}°C \r\n{6}: {2}% RH\r\n{7}: {3}°C  \r\n{8}: {4}% RH\r\n_{9}_"\r\n'.format(
            item.device.name, item.temperature1, item.humidity1, item.temperature2, item.humidity2, lang.temperature1, lang.humidity1, lang.temperature2, lang.humidity2, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def wind(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '*{0} ({4})*\r\n{2}: {1} Km/hr\r\n _{3}_"\r\n'.format(
            item.device.name, item.wind, lang.wind, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def gas(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '*{0} ({4})*\r\n{2}: {1}%\r\n_{3}_"\r\n'.format(
            item.device.name, item.gas, lang.gas, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def machine_state(item, name):
    try:
        lang = Language.objects.get(name=name)
        if float(item.machineStatus) < 12:
            machine = "OFF"
        else:
            machine = "ON"
        result = '*{0} ({4})*\r\n{2}: {1}\r\n_{3}_"\r\n'.format(
            item.device.name, machine, lang.machineStatus, '{0} GMT+0'.format(item.datetime),  item.device.phone)
        return result
    except:
        return 'Not Found'


def _get_data(_name, query_type, phone):
    try:
        user = Whatsapp.objects.get(phone=phone)
        device = Device.objects.get(imei=_name)
        try:
            item = device.data_set.latest('datetime')
        except:
            return 'No Data From Device'
        match query_type.lower():
            case '1':
                return general_state(item, user.language)
            case '2':
                return temperature(item, user.language)
            case '3':
                return wind(item, user.language)
            case '4':
                return gas(item, user.language)
            case '5':
                return machine_state(item, user.language)
    except:
        return 'No Device available'


def reply_data(phone, pk, name):
    message = _get_data(name, pk, phone)
    return {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": f"{message}"}}


def reply_text(phone, content):
    return {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": f"{content}"}}


def set_language(phone, language):
    whatsapp = Whatsapp.objects.get(phone=phone)
    whatsapp.language = language
    whatsapp.save()


def set_alarm(phone, alarm):
    whatsapp = Whatsapp.objects.get(phone=phone)
    whatsapp.alertStatus = alarm
    whatsapp.save()


def whatsapp_send(payload):
    payload = json.dumps(payload)
    try:
        x = requests.post(
            f"https://graph.facebook.com/v13.0/{PHONE_ID}/messages", headers=headers, data=payload)
    except:
        pass


def send_whatsapp(_case, phone, lang, device, item):
    try:
        language = Language.objects.get(name=lang)
        match _case:
            case 'gas':
                data = reply_text(phone, '*{0} ({2})*\r\n{1} {3}%'.format(
                    device.name, language.gasWarning, device.phone, item.gas))
                whatsapp_send(data)
            case 'vol':
                data = reply_text(phone, '*{0} ({2})*\r\n{1} {3}v'.format(
                    device.name, language.volWarning, device.phone, item.voltage))
                whatsapp_send(data)
            case 't1':
                data = reply_text(phone, '*{0} ({2})*\r\n{1} {3}°C'.format(
                    device.name, language.tempWarning, device.phone, item.temperature1))
                whatsapp_send(data)
            case 't2':
                data = reply_text(phone, '*{0} ({2})*\r\n{1}'.format(
                    device.name, language.inverWarning, device.phone))
                whatsapp_send(data)
            case 'start':
                data = reply_text(phone, '*{0} ({2})*\r\n{1}'.format(
                    device.name, language.machineStart, device.phone))
                whatsapp_send(data)
            case 'stop':
                data = reply_text(phone, '*{0} ({2})*\r\n{1}'.format(
                    device.name, language.machineStop, device.phone))
                whatsapp_send(data)
            case 'machine_not_start':
                data = reply_text(phone, '*{0} ({2})*\r\n{1}'.format(
                    device.name, language.machineWarning, device.phone))
                whatsapp_send(data)
            case 'machine_error':
                data = reply_text(phone, '*{0} ({2})*\r\n{1}'.format(
                    device.name, language.machineErorr, device.phone))
                whatsapp_send(data)

    except:
        return
    pass
