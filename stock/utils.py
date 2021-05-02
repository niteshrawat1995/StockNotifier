from constants import WHATSAPP_SLUG
from backend.twilio import Twilio
from typing import Dict, Union
from django.db.models import Q, F

from . import bse
from .models import Stock, StockReminder, Template


def get_current_price(scrip_code: str) -> Union[float, None]:
    try:
        return float(bse.getQuote(scripCode=scrip_code)["currentValue"])
    except AttributeError:
        return None


def update_stock_records():
    codes = bse.getScripCodes()

    for scrip_code, _ in codes.items():
        try:
            quote = bse.getQuote(scripCode=scrip_code)
        except AttributeError:
            quote = None
        if quote:
            data = {
                "company_name": quote["companyName"],
                "scrip_code": quote["scripCode"],
                "security_id": quote["securityID"],
            }
            stock = Stock.objects.create(**data)
            print(f"created stock for scripCode: {stock.scrip_code}")
    print("Done")


def find_reminders():
    # TODO: Add distinct instead of set
    reminder_stock_scrip_codes = set(
        StockReminder.objects.filter(is_active=True, stock__isnull=False).values_list(
            "stock__scrip_code", flat=True
        )
    )
    if len(reminder_stock_scrip_codes) == 0:
        print("NO reminders set")
        return None
    result = {
        scrip_code: get_current_price(scrip_code)
        for scrip_code in reminder_stock_scrip_codes
        if get_current_price(scrip_code) is not None
    }
    alert_user(result)


def alert_user(result: Dict):
    scrip_codes = [scrip_code for scrip_code in result]
    for scrip_code in scrip_codes:
        price = result[scrip_code]
        reminders = (
            StockReminder.objects.filter(is_active=True, stock__scrip_code=scrip_code)
            .filter(Q(lower__gt=price) | Q(upper__lt=price))
            .annotate(stock_company_name=F("stock__company_name"))
        )
        for reminder in reminders:
            msg = build_message(
                reminder.stock_company_name, price, reminder.lower, reminder.upper
            )
            comm = Twilio()
            comm.send(to=reminder.user.phone_number, msg=msg)
            print(msg)


def build_message(stock_name, price, lower, upper) -> str:
    drop_msg = f"{stock_name} dropped from your lower {lower} to {price}"
    upper_msg = f"{stock_name} rose above your upper {upper} to {price}"
    if lower and not upper:
        msg = drop_msg
    elif upper and not lower:
        msg = upper_msg
    elif lower and upper:
        if price < lower:
            msg = drop_msg
        else:
            msg = upper_msg
    return msg
