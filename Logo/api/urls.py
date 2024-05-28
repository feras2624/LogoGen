from django.urls import path
from . import views
urlpatterns = [
    path('gen/',views.GenLogo)
]
