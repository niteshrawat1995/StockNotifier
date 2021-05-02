from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import StockDetailSerializer, StockListSerializer
from .filters import StockFilter
from .models import Stock


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
