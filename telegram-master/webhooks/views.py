from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re
import os
from .helper import get_reply_device, get_reply_type, reply_data, reply_text, set_language, set_alarm, get_reply_group

TOKEN_WHATSAPP = os.environ.get('TOKEN_WHATSAPP')
PHONE_ID = os.environ.get('PHONE_ID')

# Create your views here.

headers = {"Authorization": "Bearer {0}".format(
    TOKEN_WHATSAPP), "Content-Type": "application/json"}


def reply_whatsapp(payload):
    payload = json.dumps(payload)
    try:
        x = requests.post(
            f"https://graph.facebook.com/v13.0/{PHONE_ID}/messages", headers=headers, data=payload)
        print(x.content)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=200)


@csrf_exempt
def hook_handle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        # case reply with List device
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]:
                check = re.search("^menu", data["entry"][0]["changes"][0]["value"]
                                  ["messages"][0]["text"]["body"], flags=re.IGNORECASE)
                if check:
                    data = get_reply_group(data["entry"][0]
                                           ["changes"][0]["value"]["contacts"][0]["wa_id"])
                    print(data)
                    reply_whatsapp(data)
        except:
            pass
        # case reply with result data from device after choose device and type  query
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"] and int(data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"]):
                description = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["description"]
                check = re.search("^phone", description, flags=re.IGNORECASE)
                if check:
                    data = get_reply_type(data["entry"][0]
                                          ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"])
                    reply_whatsapp(data)
                else:
                    data = reply_data(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]
                                      ["messages"][0]["interactive"]["list_reply"]["id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["description"])
                    reply_whatsapp(data)
        except:
            pass
        # case reply set language and reply type query
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]:
                name = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"]
                check_lang = re.search("^language", name, flags=re.IGNORECASE)
                check_alarm = re.search("^alarm", name, flags=re.IGNORECASE)
                check_group = re.search("^group", name, flags=re.IGNORECASE)
                if check_lang:
                    set_language(data["entry"][0]
                                 ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    data = reply_text(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], "OK")
                    reply_whatsapp(data)
                elif check_alarm:
                    set_alarm(data["entry"][0]
                              ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    data = reply_text(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], "OK")
                    reply_whatsapp(data)
                elif check_group:
                    data = get_reply_device(data["entry"][0]
                                            ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    reply_whatsapp(data)

        except:
            pass
        return HttpResponse(status=200)
    if request.method == 'GET':
        challenge = request.GET.get('hub.challenge')
        return HttpResponse(challenge, status=200)
