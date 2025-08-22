from django.urls import path
from . import views
from .views import risk_metrics

urlpatterns = [
    #path('', views.home, name='stocks_home'),
    path('risk/<str:symbol>/', risk_metrics, name='risk_metrics'),
]   
