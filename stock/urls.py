from django.urls import path

from .views import StockListView, StockDetailView

urlpatterns = [
    path("stocks/", StockListView.as_view()),
    path("stocks/<int:scrip_code>/", StockDetailView.as_view()),
]
