from stock.models import Stock
from django.test import TestCase
from stock.tests.factories import StockFactory, StockReminder
from account.models import User
from account.tests.factories import UserFactory


class TestStock(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.stock: Stock = StockFactory()

    def test_Str(self) -> None:
        expected_name = f"{self.stock.scrip_code} | {self.stock.company_name}"
        self.assertEqual(expected_name, str(self.stock))

    def test_GetPrice(self) -> None:
        self.assertEqual(float, type(self.stock.get_price()))


class TestStockReminder(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = UserFactory()
        cls.stock: Stock = StockFactory()
