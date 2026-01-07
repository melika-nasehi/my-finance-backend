from django.urls import path
from .views import *

urlpatterns = [
    path('summary/', AccountSummaryView.as_view(), name='account-summary'),
    path('list/', AccountListView.as_view(), name='account-list'),
]