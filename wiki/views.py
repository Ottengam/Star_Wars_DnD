from django.shortcuts import render
from django.views.generic import ListView
from .models import Race


class RaceListView(ListView):
    model = Race  # Модель из базы
    template_name = 'wiki/race_list.html'  # Путь к HTML-шаблону страницы
    context_object_name = 'races'  # Переменная для цикла в HTML
