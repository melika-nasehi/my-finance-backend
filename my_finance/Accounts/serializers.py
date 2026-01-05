from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'owner']
        # owner رو معمولا از روی کاربر لاگین شده برمی‌داریم