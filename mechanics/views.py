from django.views.generic import ListView, DetailView
from .models import RuleSection, Skill, Perk
from django.shortcuts import get_object_or_404


class RulesHubView(ListView):
    model = RuleSection
    template_name = "mechanics/rules_hub.html"
    context_object_name = "sections"


class RuleDetailView(DetailView):
    """
    Динамический контроллер Книги игрока.
    Автоматически перенаправляет игрока на изолированный шаблон под каждый куб.
    """
    model = RuleSection
    context_object_name = "section"

    def get_template_names(self):
        """Выбирает шаблон на основе ярлыка (slug) раздела"""
        slug = self.object.slug

        # Если файл для раздела существует, отдаем его, иначе — базовую заглушку
        match slug:
            case "attributes":
                return ["mechanics/pages/attributes.html"]
            case _:
                # временно отправляем на общую Datapad-заглушку
                return ["mechanics/pages/default_stub.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.slug == 'attributes':
            from mechanics.constants import ATTRIBUTES_LORE

            # Использование специальной аннотации для менеджера объектов (убирает warning на строке 35)
            all_skills = Skill.objects.all().prefetch_related('perks')  # noqa
            grouped_skills = {}

            # Явно итерируемся по парам (значение, лейбл) через choices, чтобы не путать IDE
            for value, label in Skill.AttributeMarker.choices:
                # Фильтруем навыки, относящиеся к конкретному атрибуту
                skills_for_attr = [s for s in all_skills if s.attribute == value]

                attr_description = ATTRIBUTES_LORE.get(value)

                grouped_skills[value] = {
                    'name': label,
                    'skills': skills_for_attr,
                    'description': attr_description,
                }

            context['grouped_skills'] = grouped_skills

        return context


class SkillPerksDetailView(ListView):
    """
    Контроллер третьего уровня для отображения древа перков талантов конкретного навыка.
    Использует системные классы Datapad-интерфейса.
    """
    model = Perk
    template_name = 'mechanics/skill_perks.html'
    context_object_name = 'perks'

    def get_queryset(self):
        # Исправляет ошибку №3: используем локальную переменную вместо self.skill
        skill_id = self.kwargs['skill_id']
        skill_obj = get_object_or_404(Skill, id=skill_id)

        # Исправляет ошибку №2: добавляем # noqa в конце строки
        return Perk.objects.filter(skill=skill_obj).prefetch_related('required_perks').order_by( # noqa
            'required_skill_level')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Повторно извлекаем объект для контекста шаблона, чтобы не нарушать архитектуру классов
        context['skill'] = get_object_or_404(Skill, id=self.kwargs['skill_id'])
        return context
