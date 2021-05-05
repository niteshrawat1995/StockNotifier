from django.http.response import Http404
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from stock.serializers import (
    StockDetailSerializer,
    StockListSerializer,
    StockReminderSerializer,
)
from stock.filters import StockFilter
from stock.models import Stock, StockReminder


class StockDetailView(generics.RetrieveAPIView):
    serializer_class = StockDetailSerializer
    queryset = Stock.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, scrip_code):
        # import pdb; pdb.set_trace()
        filters = {"scrip_code": str(scrip_code)}
        stock = generics.get_object_or_404(self.queryset, **filters)
        serializer = self.serializer_class(stock)
        return Response(serializer.data, status=200)


class StockListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StockListSerializer
    queryset = Stock.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockFilter
    pagination_class = PageNumberPagination


class StockReminderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = StockReminderSerializer
    model = StockReminder

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=200)

    @action(methods=["post"], detail=True, url_path="stop")
    def stop(self, request, pk, *args, **kwargs):
        reminder_id = pk
        try:
            reminder = self.get_queryset().get(id=reminder_id)
        except self.model.DoesNotExist:
            raise Http404
        reminder.is_active = False
        reminder.save()
        serializer = self.get_serializer(reminder)
        return Response(serializer.data, status=200)

    @action(methods=["post"], detail=True, url_path="start")
    def start(self, request, pk, *args, **kwargs):
        reminder_id = pk
        try:
            reminder = self.get_queryset().get(id=reminder_id)
        except self.model.DoesNotExist:
            raise Http404
        reminder.is_active = True
        reminder.save()
        serializer = self.get_serializer(reminder)
        return Response(serializer.data, status=200)
