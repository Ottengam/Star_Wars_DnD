from django.views.generic import ListView, DetailView
from .models import Race


class RaceListView(ListView):
    model = Race  # Модель из базы
    template_name = 'wiki/race_list.html'  # Путь к HTML-шаблону страницы
    context_object_name = 'races'  # Переменная для цикла в HTML


class RaceDetailView(DetailView):
    model = Race
    template_name = 'wiki/race_detail.html'
    context_object_name = 'race'  # Имя переменной, которую мы использовали в детальном HTML

    def get_queryset(self):
        """Оптимизируем d20-базу: одним запросом тянем лор, планеты и механики."""
        return super().get_queryset().prefetch_related(
            'traits',
            'colonies',
            'enclaves',
            'outposts',
            'integrated_worlds'
        ).select_related('homeworld')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.object

        from .models import SkillChoices
        choices_dict = dict(SkillChoices.choices)

        # Собираем списки понятных названий в одну строку кода для каждого поля
        context['get_fixed_skills_list'] = [choices_dict.get(str(k).strip()) for k in race.fixed_skills if
                                            k] if race.fixed_skills else []
        context['get_choice_skills_list'] = [choices_dict.get(str(k).strip()) for k in race.choice_skills if
                                             k] if race.choice_skills else []

        return context
