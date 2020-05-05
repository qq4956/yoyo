import json
import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from api.serializers.login import LoginSerializer
from api.utils.jwt import create_token
from api.utils.wxService import getOpenId, sendMsg
from .models import *
from .serializers.trade import TradeSerializer
from .utils.authentication import AthenticateToken
from .utils.config import getPrice, editPrice
from .utils.trade import get_responseDicts


class LoginView(APIView):

    def get(self,request):
        open_id = getOpenId(request)

        # 新增,修改用户数据
        crrent_user_obj = UserInfo.objects.filter(open_id=open_id).first()
        if not crrent_user_obj:
            s = LoginSerializer(data=request.query_params)
            if not s.is_valid():
                return Response({'code': 1002, 'msg': '微信获取的用户信息有误'})
            s.save(open_id=open_id)
        elif open_id == crrent_user_obj.open_id:
            s = LoginSerializer(crrent_user_obj,data=request.query_params)
            if not s.is_valid():
                return Response({'code': 1002, 'msg': '微信获取的用户信息有误'})
            s.save()
        else:
            return Response({'code':1003,'msg': 'open_id匹配有误'})

        # 生成token
        nickname = request.query_params.get('nickname')
        uid = UserInfo.objects.get(open_id = open_id).uid
        token = create_token(nickname,uid)

        # 判断超级管理员
        is_super = (nickname == ("夏瑞晗" or "暖一一"))

        return  Response({'code':1000,'token':token,"is_super":is_super})

    def post(self, request):
        '''
        {
            "token":"eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJuaWNrbmFtZSI6Ilx1NTkwZlx1NzQ1ZVx1NjY1NyIsInVpZCI6MSwiZXhwIjoyNDUxNTA3OTM0fQ.KaJYvnyA0p862jIs65nBj3Iq9EdCswOgh0uBKxnShjU"
            nickname = serializers.CharField(max_length=30)
            avatar_url = serializers.URLField()
            gender = serializers.CharField(max_length=10)
            province =  serializers.CharField(max_length=20)
            city = serializers.CharField(max_length=20)
            country = serializers.CharField(max_length=20)

        }
        '''
        user_obj = UserInfo.objects.get(uid = request.user.uid)
        ser = LoginSerializer(user_obj,data =request.data)
        ser.save()

        return Response({"code":1000,"msg":"用户信息完成同步"})

class PriceView(APIView):
    authentication_classes = []

    def get(self,request):
        price = getPrice()
        return Response({"code":1000,"price":price})

    def put(self,request):
        price = request.data.get('price')
        price = editPrice(price)
        return Response({"code":1000,"price":price})

class ReservationTime(APIView):
    def get(self,request):
        '''
            {
    "currentWeekDict": {
        "27": [
            {
                "r_time": "16:18",
                "full_rtime": "2020-04-27 16:18",
                "r_status": 1
            },
            {
                "r_time": "15:18",
                "full_rtime": "2020-04-27 15:18",
                "r_status": 1
            },
            {
                "r_time": "17:18",
                "full_rtime": "2020-04-27 17:18",
                "r_status": 1,
                "t_status": 1
            }
        ],
        "28": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-04-28 17:18",
                "r_status": 1
            }
        ],
        "29": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-04-29 17:18",
                "r_status": 1
            }
        ],
        "30": [
            {
                "r_time": "13:18",
                "full_rtime": "2020-04-30 13:18",
                "r_status": 1
            },
            {
                "r_time": "17:18",
                "full_rtime": "2020-04-30 17:18",
                "r_status": 1
            },
            {
                "r_time": "17:18",
                "full_rtime": "2020-04-30 17:18",
                "r_status": 1
            }
        ],
        "1": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-01 17:18",
                "r_status": 1
            }
        ],
        "2": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-02 17:18",
                "r_status": 1
            }
        ],
        "3": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-03 17:18",
                "r_status": 1
            }
        ]
    },
    "nextWeekDict": {
        "4": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-04 17:18",
                "r_status": 1
            }
        ],
        "5": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-05 17:18",
                "r_status": 1
            }
        ],
        "6": [
            {
                "r_time": "17:18",
                "full_rtime": "2020-05-06 17:18",
                "r_status": 1
            }
        ],
        "7": [],
        "8": [],
        "9": [],
        "10": []
    }
}
        '''
        #  拿到周一~周日对应的日期
        today = datetime.date.today()
        initalDay = today - datetime.timedelta(days=(today.isoweekday() - 1))
        datelist = []
        for i in range(0, 14):
            res = initalDay + datetime.timedelta(days=i)
            datelist.append(res.day)

        # 从数据库中,查询目标时间段的数据
        # Sqllite查询有坑 between,大于小于的时间区间不对
        queryTimeList = Reservation.objects.filter(
            Q(reservation_time__gte=initalDay)
            & Q(status=1)
            ).order_by("reservation_time")

        # 对目标时间段数据加工返回
        fullTimeDict = {}
        for idx,matchDate in enumerate(datelist):
            fullTimeDict[idx] = {matchDate:[]}
            eachday = initalDay + datetime.timedelta(days=idx)
            rdate = eachday.strftime('%Y-%m-%d')
            fullTimeDict[idx][matchDate].append({"rrdate":rdate})

            # 前端+的逻辑
            fullTimeDict[idx][matchDate][0]["can_add"] = (datetime.date.today()+datetime.timedelta(days=1) <= eachday)
            fullTimeDict[idx][matchDate][0]["super_can_add"] = (datetime.date.today() <= eachday)

            for queryTimeDict in queryTimeList:
                targetDay = queryTimeDict.reservation_time.strftime("%d")
                if int(matchDate) == int(targetDay):
                    # 构建目标字典的 value
                    d = {"r_time": queryTimeDict.reservation_time.strftime("%H:%M"),
                         "full_rtime": queryTimeDict.reservation_time.strftime('%Y-%m-%d %H:%M'),
                         'r_status': queryTimeDict.status,
                         'available': int(queryTimeDict.reservation_time >=  datetime.datetime.now()),
                         'is_selected':0,
                         "rid":queryTimeDict.rid,
                         }

                    # 插入字典
                    if queryTimeDict.trade_set.values():
                        d['t_status']= queryTimeDict.trade_set.order_by("-update_time").first().status

                    fullTimeDict[idx][matchDate].append(d)


        currentWeekDict = dict(list(fullTimeDict.items())[:7])
        nextWeekDict = dict(list(fullTimeDict.items())[7:14])
        resDict = {"currentWeekDict":currentWeekDict,"nextWeekDict":nextWeekDict}

        resDict = json.dumps(resDict)
        return HttpResponse(resDict)

    def put(self,request):

        reservationObj = request.data.get('reservation')
        if not reservationObj:
            return Response({'code':1007,'msg':'传入的预约数据错误'})

        for singeWeekreservationObjKey,singeWeekreservationObjValue in reservationObj.items():
            for singledateReservationObjKey,singledateReservationObjValue in singeWeekreservationObjValue.items():
                for descListsIdx,descLists in singledateReservationObjValue.items():
                    for i in descLists:
                        if i.get("r_status") == 1: # 创建或不动
                            try:
                                Reservation.objects.get(Q(reservation_time__contains=i.get("full_rtime"))
                                                        &Q(status=1))
                            except Reservation.DoesNotExist:
                                Reservation.objects.create(reservation_time=i.get("full_rtime"),status=1)
                        if i.get("r_status") == 0: # 删除
                            try:
                                t = Reservation.objects.get(Q(reservation_time__contains=i.get("full_rtime"))
                                                            &Q(status=1))
                                t.status = 0
                                t.save()
                            except Reservation.DoesNotExist:
                                return Response({'code':'1006','msg':'数据查询错误'})

        print("完成")
        return Response({'code':'1000'})

class TradeView(APIView):
    authentication_classes = [AthenticateToken,]

    def post(self,request):
        """
        {
            "full_rtime": "2020-04-20 17:18",
            "phone": "17608044954",
            "desc":"我是一只大灰狼",
            "token":"eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJuaWNrbmFtZSI6Ilx1NTkwZlx1NzQ1ZVx1NjY1NyIsInVpZCI6MSwiZXhwIjoyNDUxNTA3OTM0fQ.KaJYvnyA0p862jIs65nBj3Iq9EdCswOgh0uBKxnShjU"
            "price":50
        }
        """
        #  从认证类中获取uid
        uid = request.user.get('uid')


        # 用户只能够预约1个订单
        if not (UserInfo.objects.get(uid = uid).nickname == '暖一一' or '夏瑞晗'):
            exsitTrade = Trade.objects.filter(uid_id = uid,status__range=(1,3))
            if  exsitTrade:
                return Response({'code':1007,'msg':'不能够同时预约多个咨询'})

        # 传入时间是否可以被预约,是否已经被预约
        existRervation = Reservation.objects.filter(Q(reservation_time__contains = request.data['full_rtime'])
                                   &Q(status=1))
        if not existRervation:
            return Response({'code': 1008, 'msg': '预约的时间在数据中不存在'})


        # 看对应的是日期,是否存在订单
        rid = existRervation.values('rid')[0]['rid']
        hasDuplicatedTrade = Trade.objects.filter(rid_id=rid,status__range=(1,3))
        if hasDuplicatedTrade :
            return Response({'code':1009,'msg':'该时间已经被预约了'})

        # 创建订单
        createTrade = Trade(uid_id =uid,
                             rid_id=rid,
                             status=1,
                             phone=request.data.get('phone'),
                             desc = request.data.get('desc'),
                             price = request.data.get('price',0)
                             )
        createTrade.save()

        # 发送信息
        nickname = createTrade.uid.nickname
        openid = createTrade.uid.open_id
        reservation_time = createTrade.rid.reservation_time.strftime("%m月%d日 %H:%M")
        sendMsg(nickname = nickname,open_id = openid,reservation_time= reservation_time,type=1)

        return Response({'code':1000,'msg':'创建完成'})

    def put(self,request):
        """
        {
            "tid": "1",
            "token":"eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJuaWNrbmFtZSI6Ilx1NTkwZlx1NzQ1ZVx1NjY1NyIsInVpZCI6MSwiZXhwIjoyNDUxNTA3OTM0fQ.KaJYvnyA0p862jIs65nBj3Iq9EdCswOgh0uBKxnShjU"
            "status":"0", or "2"
        }
        """
        tid = request.data["tid"]
        status = request.data["status"]
        uid = request.user["uid"]

        t = Trade.objects.filter(tid=tid,uid_id=uid).first()
        if not t:
            return Response({'code':1009,'msg':"未找到有效的订单"})
        t.status = status
        t.save()

        #如果取消,发送消息
        if int(status) == 0:
            nickname = t.uid.nickname
            openid = t.uid.open_id
            reservation_time = t.rid.reservation_time.strftime("%m月%d日 %H:%M")
            #发送
            sendMsg(nickname = nickname,open_id = openid,reservation_time= reservation_time,type=0)

        responseDict = get_responseDicts(uid)
        ser = TradeSerializer(instance=responseDict,many=True).data

        return Response(ser)

    def get(self,request):
        """
        {
            "token":"eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJuaWNrbmFtZSI6Ilx1NTkwZlx1NzQ1ZVx1NjY1NyIsInVpZCI6MSwiZXhwIjoyNDUxNTA3OTM0fQ.KaJYvnyA0p862jIs65nBj3Iq9EdCswOgh0uBKxnShjU"
        }
        """
        uid = request.user['uid']

        # 修改对应订单状态
        responseDicts = get_responseDicts(uid)
        for responseDict in responseDicts:
            rtime = responseDict.rid.reservation_time
            if  (rtime + datetime.timedelta(hours=1) < datetime.datetime.now()) and (int(responseDict.status) == int(2)):
                responseDict.status = 3
                responseDict.save()

        responseDicts = get_responseDicts(uid)
        ser = TradeSerializer(instance=responseDicts,many=True).data

        return Response(ser)

class SelectReservationView(APIView):
    def get(self,request):
        rid = request.query_params['rid']
        rObj = Reservation.objects.filter(rid  = rid).first()
        if not rObj:
            return Response({"code":1010,"msg":"传入的rid应该有订单状态123"})
        tObj = rObj.trade_set.filter(Q(status__gte = 1)).order_by("-create_time").first()
        ser = TradeSerializer(instance=tObj)


        return Response(ser.data)



