from time import sleep

from ..models import *
import datetime
from .wxService import *


def circulateMonitor():
    num = 1
    while True:
        queryList = Trade.objects.filter(status=2)
        for tradeRow in queryList:
            # 发送提示消息
            l_limit = datetime.datetime.now() + datetime.timedelta(minutes=14) <= tradeRow.rid.reservation_time
            r_limit = datetime.datetime.now() + datetime.timedelta(minutes=15) >= tradeRow.rid.reservation_time
            if (l_limit and r_limit):
                nickname = tradeRow.uid.nickname
                openid = tradeRow.uid.open_id
                reservation_time = tradeRow.rid.reservation_time.strftime("%m月%d日 %H:%M")
                sendMsg(nickname=nickname, open_id=openid, reservation_time=reservation_time, type=2)

            # 更改订单状态
            has_finish = datetime.datetime.now() - datetime.timedelta(minutes=60) >= tradeRow.rid.reservation_time
            print(has_finish)
            if has_finish:
                tradeRow.status = 3
                tradeRow.save()

        num = num + 1
        print("执行了:" + str(num))
        sleep(50)


