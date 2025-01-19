<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('drivers/', views.drivers, name='drivers'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('service-area/', views.service_area, name='service_area'),
    path('safety/', views.safety, name='safety'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('profile/', views.profile, name='profile'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/review/', views.add_review, name='add_review'),
    path('set-language/', views.set_language, name='set_language'),
=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('drivers/', views.drivers, name='drivers'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('service-area/', views.service_area, name='service_area'),
    path('safety/', views.safety, name='safety'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('profile/', views.profile, name='profile'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/review/', views.add_review, name='add_review'),
    path('set-language/', views.set_language, name='set_language'),
>>>>>>> 29e35e4892c15854585299d3eee6ff215d96cbb2
] 