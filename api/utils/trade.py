from api.models import *

def get_responseDicts(uid):
    userObj  = UserInfo.objects.get(uid=uid)
    if userObj.nickname  == '暖一一' or '夏瑞晗':
        responseDicts = Trade.objects.all().order_by("-create_time")
    else:
        responseDicts = Trade.objects.filter(uid_id=uid).order_by("-create_time")
    return responseDicts
