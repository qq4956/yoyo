from rest_framework import serializers


class TradeSerializer(serializers.Serializer):
    uid = serializers.CharField(source='uid_id')
    nickname = serializers.CharField(source='uid.nickname')
    phone = serializers.StringRelatedField()
    reservation_time = serializers.DateTimeField(source='rid.reservation_time',format="%m-%d %H:%M")
    t_status = serializers.CharField(source="status")
    t_status_desc = serializers.CharField(source="get_status_display")
    tid = serializers.IntegerField()
    price = serializers.IntegerField()
    briefDesc = serializers.CharField(source="desc")
    wordsLength = serializers.CharField(source="desc")
    desc = serializers.CharField()
    avatar = serializers.CharField(source="uid.avatar_url")
    tradeCreateTime = serializers.DateTimeField(source='create_time',format="%Y-%m-%d %H:%M")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['briefDesc'] = ret['desc'][:20]
        ret['wordsLength'] = len(ret['desc'])
        ret['ellipsis'] = 1
        return ret

