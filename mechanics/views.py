from django.views.generic import ListView, DetailView
from .models import RuleSection, Skill, ConditionCategory


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
            case "conditions":
                return ["mechanics/pages/conditions.html"]
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

        elif self.object.slug == 'conditions':
            # Подтягиваем категории и сразу все связанные с ними статусы за 1 дополнительный запрос
            context['categories'] = ConditionCategory.objects.prefetch_related('conditions').all()

        return context


class SkillPerksDetailView(DetailView):
    """
    Контроллер третьего уровня для отображения древа перков конкретного навыка.
    """
    model = Skill
    template_name = 'mechanics/pages/skill_perks.html'
    context_object_name = 'skill'
    pk_url_kwarg = 'skill_id'

    def get_queryset(self):
        # Оптимизируем запрос без ручных get_object_or_404
        return super().get_queryset().prefetch_related('perks__required_perks')

    def get_context_data(self, **kwargs):
        def _to_roman(val):
            """Вспомогательный d20-конвертер чисел в римские цифры."""
            roman_map = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI'}
            return roman_map.get(val, str(val))

        context = super().get_context_data(**kwargs)

        from mechanics.constants import SKILL_PROGRESSION_MILESTONES
        context['progression_milestones'] = SKILL_PROGRESSION_MILESTONES

        perks_by_tier = {1: [], 2: [], 3: [], 4: []}
        all_perks = self.object.perks.all().order_by('required_skill_level', 'name')

        # Шаг 1: Вычисляем ранг и НАЗНАЧАЕМ СИСТЕМНЫЙ ЦВЕТ ИЗ ВАШЕГО :ROOT
        for perk in all_perks:
            if perk.required_skill_level == 15:
                perk.computed_tier = 4
                perk.tier_color = "var(--sw-neon-red)"  # Мастер (Красный)
            elif 10 <= perk.required_skill_level <= 14:
                perk.computed_tier = 3
                perk.tier_color = "var(--sw-orange-glow)"  # Эксперт (Оранжевый)
            elif 5 <= perk.required_skill_level <= 9:
                perk.computed_tier = 2
                perk.tier_color = "var(--sw-neon-green)"  # Специалист (Зеленый)
            else:
                perk.computed_tier = 1
                perk.tier_color = "var(--sw-neon-blue)"  # Новичок (Синий)

        # Шаг 2: На основе вычисленных рангов и цветов строим карту d20-требований
        for perk in all_perks:
            # ЗАМЕНЯЕМ СОКРАЩЕНИЕ МАКС НА КРАСИВОЕ СЛОВОФОРМИРОВАНИЕ "Х уровня"
            if perk.max_levels > 1:
                perk.display_max_levels = f"Максимум {_to_roman(perk.max_levels)}"
            else:
                perk.display_max_levels = ""

            # Парсим JSON-описание построчно
            lines = perk.description if isinstance(perk.description, list) else []
            perk_effects = []

            if len(lines) <= 1:
                text = lines[0] if lines else ""
                if text.startswith("Уровень 1:"):
                    text = text.replace("Уровень 1:", "").strip()
                perk_effects.append({"is_multilevel": False, "level_marker": "", "text": text})
            else:
                for index, line in enumerate(lines, start=1):
                    text = line
                    prefix = f"Уровень {index}:"
                    if text.startswith(prefix):
                        text = text.replace(prefix, "").strip()
                    perk_effects.append({"is_multilevel": True, "level_marker": str(index), "text": text})
            perk.formatted_effects = perk_effects

            # УМНЫЙ РАСЧЕТ ТРЕБОВАНИЙ ЧЕРЕЗ РИМСКИЕ ЦИФРЫ БЕЗ ШУМА [X ур.]
            processed_requirements = []
            for req in perk.required_perks.all():
                parent_perk = next((p for p in all_perks if p.id == req.id), None)
                d20_condition = ""

                if parent_perk and parent_perk.max_levels > 1:
                    # Если родитель многоуровневый и находится в том же ранге (сосед)
                    if perk.computed_tier == parent_perk.computed_tier:
                        d20_condition = f" {_to_roman(1)}"  # Добавляем пробел перед римской I
                    # Если родитель из ранга ниже — берем его максимальный d20-уровень
                    else:
                        d20_condition = f" {_to_roman(parent_perk.max_levels)}"

                # Если parent_perk.max_levels == 1, d20_condition останется пустой строкой "",
                # что полностью скроет цифры у одноуровневых перков.

                processed_requirements.append({
                    "name": req.name,
                    "condition": d20_condition  # Вернет " I", " III" или ""
                })

            perk.processed_reqs = processed_requirements

            if perk.computed_tier in perks_by_tier:
                perks_by_tier[perk.computed_tier].append(perk)

        context['perks_by_tier'] = perks_by_tier

        return context
