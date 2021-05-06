from account.tests.factories import UserFactory
import factory
from factory.django import DjangoModelFactory
from stock.models import Stock, StockReminder
import os
import json
from django.conf import settings
import random


def get_random_scrip_code():
    try:
        file_path = os.path.join(settings.BASE_DIR, "stk.json")
        with open(file_path, "r") as f:
            data = json.load(f)
        return random.choice(list(data.keys()))
    except Exception as e:
        print(e)
        return "533022"


class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock

    scrip_code = factory.LazyFunction(get_random_scrip_code)


class StockReminder(DjangoModelFactory):
    class Meta:
        model = StockReminder

    user = factory.SubFactory(UserFactory)
    stock = factory.SubFactory(StockFactory)
