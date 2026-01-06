from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from Transactions.models import Transaction
from .serializers import AccountSerializer
from django.db.models import Sum, Q
from datetime import datetime, timedelta


class AccountSummaryView(APIView):
    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)

        # تفکیک دارایی‌ها و بدهی‌ها
        assets = accounts.filter(is_debt=False)
        liabilities = accounts.filter(is_debt=True)

        total_assets = assets.aggregate(Sum('balance'))['balance__sum'] or 0
        total_liabilities = liabilities.aggregate(Sum('balance'))['balance__sum'] or 0
        net_worth = total_assets - total_liabilities

        # --- بخش نمودار واقعی ---
        # ۱. ایجاد ۷ نقطه زمانی (مثلاً ۷ روز گذشته)
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        dates_str = [d.strftime('%b %d') for d in dates]

        chart_series = []
        for acc in accounts:
            daily_balances = []
            current_balance = float(acc.balance)

            for d in dates:
                # محاسبه مجموع تراکنش‌های بعد از تاریخ d برای بازگشت به عقب
                # موجودی در تاریخ d = موجودی فعلی - (درآمدهای بعد از d) + (هزینه‌های بعد از d)
                future_trans = Transaction.objects.filter(account=acc, date__gt=d).aggregate(
                    inc=Sum('amount', filter=Q(kind='income')),
                    exp=Sum('amount', filter=Q(kind='expense'))
                )

                income_after = float(future_trans['inc'] or 0)
                expense_after = float(future_trans['exp'] or 0)

                historical_balance = current_balance - income_after + expense_after
                daily_balances.append(round(historical_balance, 2))

            chart_series.append({
                'name': acc.name,
                'data': daily_balances,
                'color': acc.color
            })

        return Response({
            'assets': AccountSerializer(assets, many=True).data,
            'liabilities': AccountSerializer(liabilities, many=True).data,
            'total_assets': float(total_assets),
            'total_liabilities': float(total_liabilities),
            'net_worth': float(net_worth),
            'chart_data': {
                'dates': dates_str,
                'series': chart_series
            }
        })