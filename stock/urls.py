from django.urls import path
from django.urls.conf import include

from .views import StockListView, StockDetailView, StockReminderViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("reminders", StockReminderViewSet, basename="reminders")

urlpatterns = [
    path("stocks/", StockListView.as_view()),
    path("stocks/<int:scrip_code>/", StockDetailView.as_view()),
    path("", include(router.urls)),
]
