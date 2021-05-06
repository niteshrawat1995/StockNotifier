from stock.models import Stock
from django.test import TestCase
from stock.tests.factories import StockFactory, StockReminder


class TestDemo(TestCase):
    def test_add(self):
        a = 1
        b = 2
        self.assertEqual(a + b, 3)

    def test_sub(self):
        a = 2
        b = 1
        self.assertEqual(a - b, 1)
