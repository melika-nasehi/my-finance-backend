from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/transaction/', include('Transactions.url')),
    path('api/accounts/', include('Accounts.urls')),
    path('api/categories/', include('Category.urls')),
]