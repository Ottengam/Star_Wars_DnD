from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    # Модуль отображения общего списка объектов
    path('races/', views.RaceListView.as_view(), name='race_list'),

    # Модуль отображения детальной карточки конкретного объекта
    path('races/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
]
