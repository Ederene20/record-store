from django.urls import path

from . import views

urlpatterns = [
        path('', views.listing),
        path('<album_id>', views.detail),
        path('search/', views.search),
]