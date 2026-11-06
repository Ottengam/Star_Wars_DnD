from django.contrib import admin
from django.db import models
from .models import Trait, Skill, Perk, RuleSection, ConditionCategory, Condition
from django.utils.safestring import mark_safe


@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'get_short_description')
    search_fields = ('name', 'code_name', 'description')

    @admin.display(description="Описание")
    def get_short_description(self, obj):
        """Ограничивает длину описания в общем списке, чтобы таблица не растягивалась."""
        if obj.description and len(obj.description) > 75:
            return f"{obj.description[:75]}..."
        return obj.description


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Конфигурация панели управления для модели Навыков.
    Обеспечивает группировку по базовым d20-характеристикам.
    """
    list_display = ('name', 'attribute', 'description')
    list_filter = ('attribute',)
    search_fields = ('name',)

    ordering = ()

    def get_queryset(self, request):
        """
        Переопределяет стандартный запрос к БД для сортировки навыков
        в каноничном порядке характеристик D&D.
        """
        queryset = super().get_queryset(request)

        dnd_order = models.Case(
            models.When(attribute='STR', then=1),
            models.When(attribute='DEX', then=2),
            models.When(attribute='CON', then=3),
            models.When(attribute='INT', then=4),
            models.When(attribute='WIS', then=5),
            models.When(attribute='CHA', then=6),
            output_field=models.IntegerField())

        return queryset.annotate(dnd_sort=dnd_order).order_by('dnd_sort', 'name')


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    """
    Конфигурация панели управления для модели Перков.
    Реализует удобный интерфейс работы с ManyToMany зависимостями.
    """
    list_display = ('name', 'skill', 'required_skill_level', 'formatted_description')
    list_filter = ('skill__attribute', 'skill', 'required_skill_level')
    search_fields = ('name', 'skill__name')
    filter_horizontal = ('required_perks',)

    @admin.display(description="Описание перка")
    def formatted_description(self, obj):
        html_paragraphs = "".join(
            f"<p style='margin: 0 0 6px 0; line-height: 1.4;'>{line}</p>"
            for line in obj.description
        )

        return mark_safe(html_paragraphs)


@admin.register(RuleSection)
class RuleSectionAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для разделов Книги игрока.
    """
    # Столбцы, которые будут видны в общем списке разделов
    list_display = ('title', 'sort_order', 'slug')

    # Поля, по которым можно искать разделы через поисковую строку
    search_fields = ('title', 'description')


@admin.register(ConditionCategory)
class ConditionCategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация панели управления для категорий состояний.
    Обеспечивает контроль порядка сортировки групп в терминале.
    """
    list_display = ('name', 'sort_order', 'get_short_description')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')

    @admin.display(description="Краткое описание")
    def get_short_description(self, obj):
        """Ограничивает длину описания категории в общем списке."""
        if obj.description and len(obj.description) > 75:
            return f"{obj.description[:75]}..."
        return obj.description


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """
    Конфигурация панели управления для реестра динамических статусов.
    Обеспечивает группировку по категориям воздействия и типам модификаторов.
    """
    list_display = ('name', 'category', 'type_marker', 'duration_rule', 'formatted_description')
    list_filter = ('category', 'type_marker')
    search_fields = ('name', 'code_name', 'description')
    ordering = ('category', 'name')

    @admin.display(description="Условия снятия")
    def formatted_description(self, obj):
        html_paragraphs = "".join(
            f"<p style='margin: 0 0 6px 0; line-height: 1.4;'>{line}</p>"
            for line in obj.removal_rule
        )

        return mark_safe(html_paragraphs)
