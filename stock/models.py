from account.models import User
from django.db import models
from stock import bse
from django.utils import timezone


class Period(models.Model):
    value = models.IntegerField(verbose_name="1-24 representing clock times")

    def __str__(self) -> str:
        return f"{self.value}:00 HR"


class Stock(models.Model):
    scrip_code = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    security_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_price(self):
        refresh_time = timezone.now() - self.updated_at
        if refresh_time.days > 1:
            bse.updateScripCodes()
        return float(bse.getQuote(self.scrip_code)["currentValue"])

    def __str__(self):
        return f"{self.scrip_code} | {self.company_name}"


class StockReminder(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stock, on_delete=models.SET_NULL, null=True)
    lower = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    periods = models.ManyToManyField(to=Period)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.stock}"

    def stop(self) -> None:
        if self.is_active != False:
            self.is_active = False
        self.save()

    def start(self) -> None:
        if self.is_active != True:
            self.is_active = True
        self.save()


class Template(models.Model):
    slug = models.SlugField(unique=True)
    body = models.TextField()

    def __str__(self) -> str:
        return self.slug
