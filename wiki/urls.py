from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    # Путь для списка рас
    path('races/', views.RaceListView.as_view(), name='race_list'),
    path('races/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
]
