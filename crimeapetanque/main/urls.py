from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]
