from django.urls import path
from .views import AccountSummaryView

urlpatterns = [
    path('summary/', AccountSummaryView.as_view(), name='account-summary'),
]