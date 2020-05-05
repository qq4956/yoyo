import uuid

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True,  editable=False,)
    open_id = models.CharField(max_length=100)
    is_valid = models.BooleanField(verbose_name='用户是否有效',default=True)
    create_time = models.DateTimeField('注册时间',auto_now_add=True)
    last_log_time = models.DateTimeField('上次登录时间',auto_now=True)
    nickname = models.CharField('昵称',max_length=30)
    avatar_url = models.URLField()
    gender = models.CharField('性别',max_length=10)
    province =  models.CharField('省份',max_length=20)
    city = models.CharField('城市',max_length=20)
    country = models.CharField('国家',max_length=20)

    def __str__(self):
        return self.nickname

class Reservation(models.Model):
    STATUS = (
        ('0', '已关闭'),
        ('1', '已生成'),
    )
    rid = models.AutoField(verbose_name='预约id',primary_key=True,  editable=False)
    create_time = models.DateTimeField(verbose_name='生成的时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='改变状态的时间',auto_now=True)
    reservation_time = models.DateTimeField(verbose_name='预约时间')
    status = models.IntegerField(verbose_name='预约时间点状态',choices=STATUS,default=1)

    def __unicode__(self):
        return self.reservation_time

class Trade(models.Model):
    STATUS = (
    ('0', '已取消'),
    ('1', '待支付'),
    ('2', '已支付'),
    ('3', '已完成'),
    )

    tid = models.AutoField(verbose_name='订单id',primary_key=True, auto_created=True, editable=False)
    uid= models.ForeignKey(verbose_name='预约用户id',to= 'UserInfo',on_delete=models.PROTECT)
    rid = models.ForeignKey(verbose_name='预约表id',to= 'Reservation',on_delete=models.PROTECT)
    create_time = models.DateTimeField('生成订单时间',auto_now_add=True)
    update_time = models.DateTimeField('订单状态更新时间',auto_now=True)
    status = models.CharField(verbose_name='订单状态',choices=STATUS,max_length=1)
    price = models.IntegerField(verbose_name='订单金额')
    phone = models.CharField(verbose_name='手机号',blank=True,null=True,max_length=11)
    desc = models.TextField(verbose_name='详细问题',blank=True,null=True)











