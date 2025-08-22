from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_index, name='landing_index'),  # Home page
    path('/about/', views.about, name='about_page')     # About page
]

