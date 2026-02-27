from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Asset, CashFlow, PlanEvent
from .serializers import AssetSerializer, CashFlowSerializer, PlanEventSerializer

# Create your views here.

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetSerializer

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CashFlowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CashFlowSerializer

    def get_queryset(self):
        return CashFlow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlanEventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlanEventSerializer

    def get_queryset(self):
        return PlanEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)