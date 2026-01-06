from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer
from django.db.models import Sum


class AccountSummaryView(APIView):
    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)

        assets = accounts.filter(is_debt=False)
        liabilities = accounts.filter(is_debt=True)

        total_assets = assets.aggregate(Sum('balance'))['balance__sum'] or 0
        total_liabilities = liabilities.aggregate(Sum('balance'))['balance__sum'] or 0
        net_worth = total_assets - total_liabilities

        chart_data = {
            'dates': ['Dec 24', 'Dec 26', 'Dec 28', 'Dec 30', 'Jan 1', 'Jan 4', 'Jan 6'],
            'series': [
                {
                    'name': acc.name,
                    'data': [float(acc.balance) * (0.8 + (i * 0.05)) for i in range(7)],
                    'color': acc.color
                } for acc in accounts
            ]
        }

        return Response({
            'assets': AccountSerializer(assets, many=True).data,
            'liabilities': AccountSerializer(liabilities, many=True).data,
            'total_assets': float(total_assets),
            'total_liabilities': float(total_liabilities),
            'net_worth': float(net_worth),
            'chart_data': chart_data
        })