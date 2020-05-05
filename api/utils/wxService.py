from rest_framework.response import Response
from django.conf import settings
import requests
import json

APPID = settings.WX['APPID']
SECRET = settings.WX['SECRET']

templateDict = {
    1: "qE0edMEuN5H7urSzlsv7xb3duRnJ0rXIvqdM-e8tDWY",  # "有预约"
    0: "ebt-3qHHntyzTPfszbcUKkTD3S1sWPWP4AW5Lrjuz6A",  # "预约取消"
    2: "_YCsBCMQ4tJohYppJlv5H1atpr63vcXDGE5W5J-KHEA"  # "日程提醒"
}


def getOpenId(request):
    JSCODE = request.query_params.get('code')
    if not JSCODE:
        return Response({"code": 1001, "msg": "没有拿到code,检查下微信请求"})
    # 向微信发送拿到open_id
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code '.format(
        APPID=APPID, SECRET=SECRET, JSCODE=JSCODE)

    res = requests.get(url).json()['openid']
    # 居然.jsons()得到的是一个dict,服气了
    return res


# 发送消息

def getPostData_hasReservaion(touser, nickname, reservation_time):
    postData_user = {
        "touser": "{touser}".format(touser=touser),
        "template_id": "{templateId}".format(templateId="qE0edMEuN5H7urSzlsv7xb3duRnJ0rXIvqdM-e8tDWY"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "name1": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date3": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing7": {
                "value": "已下单,待支付"
            },
        }
    }

    postData_yoyo = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",  # 记得修改成yoyo的open_id
        "template_id": "{templateId}".format(templateId="qE0edMEuN5H7urSzlsv7xb3duRnJ0rXIvqdM-e8tDWY"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "name1": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date3": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing7": {
                "value": "已下单,待支付"
            },
        }
    }

    postData_me = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",
        "template_id": "{templateId}".format(templateId="qE0edMEuN5H7urSzlsv7xb3duRnJ0rXIvqdM-e8tDWY"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "name1": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date3": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing7": {
                "value": "已下单,待支付"
            },
        }
    }

    postData_user_json = json.dumps(postData_user, ensure_ascii=False).encode('utf-8')
    postData_me_json = json.dumps(postData_me, ensure_ascii=False).encode('utf-8')
    postData_yoyo_json = json.dumps(postData_yoyo, ensure_ascii=False).encode('utf-8')

    print(postData_user_json, postData_me_json, postData_yoyo_json)

    return postData_user_json, postData_me_json, postData_yoyo_json


def getPostData_cancelReservaion(touser, nickname, reservation_time):
    postData_user = {
        "touser": "{touser}".format(touser=touser),
        "template_id": "{templateId}".format(templateId="ebt-3qHHntyzTPfszbcUKkTD3S1sWPWP4AW5Lrjuz6A"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing5": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
        }
    }
    postData_yoyo = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",  # 记得修改成yoyo的open_id
        "template_id": "{templateId}".format(templateId="ebt-3qHHntyzTPfszbcUKkTD3S1sWPWP4AW5Lrjuz6A"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing5": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
        }
    }
    postData_me = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",
        "template_id": "{templateId}".format(templateId="ebt-3qHHntyzTPfszbcUKkTD3S1sWPWP4AW5Lrjuz6A"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing5": {
                "value": "{nickname}".format(nickname=nickname)
            },
            "date2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
        }
    }

    postData_user_json = json.dumps(postData_user, ensure_ascii=False).encode('utf-8')
    postData_me_json = json.dumps(postData_me, ensure_ascii=False).encode('utf-8')
    postData_yoyo_json = json.dumps(postData_yoyo, ensure_ascii=False).encode('utf-8')

    return postData_user_json, postData_me_json, postData_yoyo_json


def getPostData_remindReservaion(touser, nickname, reservation_time):
    postData_user = {
        "touser": "{touser}".format(touser=touser),
        "template_id": "{templateId}".format(templateId="_YCsBCMQ4tJohYppJlv5H1atpr63vcXDGE5W5J-KHEA"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing1": {
                "value": "{nickname}的咨询要开始了".format(nickname=nickname)
            },
            "time2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing4":{
                 "value": "请注意安排时间,准备咨询哦"
            }
        }
    }

    postData_yoyo = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",  # 记得修改成yoyo的open_id
        "template_id": "{templateId}".format(templateId="_YCsBCMQ4tJohYppJlv5H1atpr63vcXDGE5W5J-KHEA"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing1": {
                "value": "{nickname}的咨询要开始了".format(nickname=nickname)
            },
            "time2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing4": {
                "value": "请注意安排时间,准备咨询哦"
            }
        }
    }

    postData_me = {
        "touser": "oHuH25WY7aCXBCunHD98cCujhfbw",
        "template_id": "{templateId}".format(templateId="_YCsBCMQ4tJohYppJlv5H1atpr63vcXDGE5W5J-KHEA"),
        "page": "pages/home/home",
        "miniprogram_state": "developer",
        "lang": "zh_CN",
        "data": {
            "thing1": {
                "value": "{nickname}的咨询要开始了".format(nickname=nickname)
            },
            "time2": {
                "value": "{reservation_time}".format(reservation_time=reservation_time)
            },
            "thing4":{
                 "value": "请注意安排时间,准备咨询哦"
            }
        }
    }

    postData_user_json = json.dumps(postData_user, ensure_ascii=False).encode('utf-8')
    postData_me_json = json.dumps(postData_me, ensure_ascii=False).encode('utf-8')
    postData_yoyo_json = json.dumps(postData_yoyo, ensure_ascii=False).encode('utf-8')

    return postData_user_json, postData_me_json, postData_yoyo_json


def sendMsg(nickname, open_id, reservation_time, type):
    access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}".format(
        APPID=APPID, SECRET=SECRET)
    access_token = requests.get(access_token_url).json()['access_token']

    msgUrl = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={ACCESS_TOKEN}".format(
        ACCESS_TOKEN=access_token)

    # 预处理数据
    nickname = nickname[:10]
    touser = open_id
    reservation_time = reservation_time

    # 获得处理数据
    if type == 1:
        postData_user_json, postData_me_json, postData_yoyo_json = getPostData_hasReservaion(touser=touser,
                                                                                             nickname=nickname,
                                                                                             reservation_time=reservation_time)
    if type == 0:
        postData_user_json, postData_me_json, postData_yoyo_json = getPostData_cancelReservaion(touser=touser,
                                                                                                nickname=nickname,
                                                                                                reservation_time=reservation_time)
    if type == 2:
        postData_user_json, postData_me_json, postData_yoyo_json = getPostData_remindReservaion(touser=touser,
                                                                                                nickname=nickname,
                                                                                                reservation_time=reservation_time)

    res1 = requests.post(msgUrl, data=postData_user_json, headers={'Content-Type': 'application/json'})
    res2 = requests.post(msgUrl, data=postData_me_json, headers={'Content-Type': 'application/json'})
    res3 = requests.post(msgUrl, data=postData_yoyo_json, headers={'Content-Type': 'application/json'})

    return {"user": res1, "me": res2, "yoyo": res3}
