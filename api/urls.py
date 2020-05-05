from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('price/',PriceView.as_view()),
    path('reservationtime/', ReservationTime.as_view()),
    path('trade/',TradeView.as_view()),
    path('selectReservation/', SelectReservationView.as_view()),
]

