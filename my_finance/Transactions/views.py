from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Transaction
from .serialize import *
from rest_framework import viewsets
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q


class CategoryExpensesChart(APIView):
    def get(self, request):
        stats = (
            Transaction.objects.filter(kind='outcome')
            .values('category__name', 'category__color')
            .annotate(total_amount=Sum('amount'))
            .order_by('-total_amount')
        )
        data = {
            'labels': [item['category__name'] for item in stats],
            'series': [float(item['total_amount']) for item in stats],
            'colors': [item['category__color'] for item in stats] # ارسال لیست رنگ‌ها
        }
        return Response(data)


class DailyExpensesChart(APIView):
    def get(self, request):
        today = timezone.now().date()

        days_since_saturday = (today.weekday() + 2) % 7
        start_of_week = today - timedelta(days=days_since_saturday)

        labels = []
        values = []

        for i in range(7):
            current_date = start_of_week + timedelta(days=i)
            labels.append(current_date.strftime('%a'))  # نام روز

            if current_date <= today:
                total = Transaction.objects.filter(
                    kind='outcome',
                    date=current_date
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                values.append(float(total))
            else:
                values.append(0)

        return Response({
            'categories': labels,
            'data': values
        })


from collections import defaultdict


class GroupedTransactionsView(APIView):
    def get(self, request):
        # ۱. گرفتن تمام تراکنش‌ها به همراه اطلاعات دسته و حساب
        transactions = Transaction.objects.all().select_related('category', 'account').order_by('-date')

        # ۲. ساختن یک دیکشنری برای گروه‌بندی دستی
        grouped_data = defaultdict(lambda: {'total_expense': 0, 'total_deposit': 0, 'items': []})

        for t in transactions:
            cat_name = t.category.name if t.category else "Other"

            # اضافه کردن دیتای خام به لیست آیتم‌ها برای نمایش در آکاردئون
            grouped_data[cat_name]['items'].append({
                'desc': t.desc,  # نام فیلد در مدل تو desc بود
                'account': t.account.name if t.account else 'N/A',
                'date': t.date.strftime('%Y-%m-%d'),
                'amount': float(t.amount),
                'kind': t.kind
            })

            # محاسبه مجموع برای هدر آکاردئون
            if t.kind == 'outcome':
                grouped_data[cat_name]['total_expense'] += float(t.amount)
            else:
                grouped_data[cat_name]['total_deposit'] += float(t.amount)

        # ۳. تبدیل دیکشنری به لیستی که آنگولار می‌فهمه
        final_groups = []
        for name, data in grouped_data.items():
            final_groups.append({
                'category__name': name,
                'total_expense': data['total_expense'],
                'total_deposit': data['total_deposit'],
                'items': data['items']  # این همون فیلد گمشده بود!
            })

        # ۴. محاسبه مجموع کل برای فوتر (اختیاری)
        grand_totals = Transaction.objects.aggregate(
            total_expense=Sum('amount', filter=Q(kind='outcome')),
            total_deposit=Sum('amount', filter=Q(kind='income'))
        )

        return Response({
            'groups': final_groups,
            'grand_total_expense': grand_totals['total_expense'] or 0,
            'grand_total_deposit': grand_totals['total_deposit'] or 0
        })

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer