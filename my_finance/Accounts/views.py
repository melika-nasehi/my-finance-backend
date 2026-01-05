from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    # فعلاً برای تست Permission رو باز میذاریم، بعداً سختگیرانه‌ش کن
    # permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # اگر کاربر لاگین بود، فقط حساب‌های خودش رو برگردون
        if self.request.user.is_authenticated:
            return Account.objects.filter(owner=self.request.user)
        return Account.objects.all() # برای تست اولیه همه رو برمی‌گردونه