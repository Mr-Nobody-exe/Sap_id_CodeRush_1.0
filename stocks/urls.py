from django.urls import path
from . import views

urlpatterns = [
    path('risk/<str:symbol>/', views.risk_metrics, name='risk_metrics'),
]
