from rest_framework import serializers
from .models import Stock


class StockDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ("id", "scrip_code", "company_name", "price")

    def get_price(self, instance):
        return instance.get_price()


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("id", "scrip_code", "company_name")

    def get_price(self, instance):
        return instance.get_price()
