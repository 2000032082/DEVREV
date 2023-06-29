from django.urls import path
from .views import add_flight, remove_flight, view_bookings,loginpage,registerPage

urlpatterns = [
    path('flight/add/', add_flight, name='add_flight'),
    path('flight/remove/<int:flight_id>/', remove_flight, name='remove_flight'),
    path('flight/bookings/<int:flight_id>/<str:flight_time>/', view_bookings, name='view_bookings'),
     path('login/',loginpage,name="login"),
    path('register/',registerPage,name="register"),
]
