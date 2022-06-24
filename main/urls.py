from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('delete/<pk>/', views.delete, name='delete'),
    path('update', views.update,name='update'),
]