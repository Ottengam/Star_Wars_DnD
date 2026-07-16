from django.contrib import admin
from .models import Region, Sector, System, Planet, Faction, Race
from django.utils.html import format_html


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'map_url')
    search_fields = ('name',)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'region', 'map_url')
    list_filter = ('region',)
    search_fields = ('name',)


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'sector', 'map_url')
    list_filter = ('sector__region', 'sector')
    search_fields = ('name',)


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'system', 'get_climates', 'controlling_faction', 'map_url')
    list_filter = ('controlling_faction', 'climate', 'system__sector__region', 'system')
    search_fields = ('name',)

    def get_climates(self, obj):
        if obj.climate:
            # Превращаем массив выбранных значений в понятные русские названия
            labels = [dict(Planet.ClimateType.choices).get(c, c) for c in obj.climate]
            return ", ".join(labels)
        return "Неизвестно"

    get_climates.short_description = 'Климат'


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent_faction')
    list_filter = ('parent_faction',)
    search_fields = ('name',)


class RaceTraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'description')
    search_fields = ('name', 'code_name', 'description')


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'name', 'description', 'homeworld', 'get_d20_stats', 'size', 'speed')
    search_fields = ('name', 'description')
    filter_horizontal = ('traits', 'colonies', 'enclaves', 'outposts', 'integrated_worlds', 'fixed_skills_t',
                         'choice_skills_t')

    def get_d20_stats(self, obj):
        from django.utils.safestring import mark_safe

        stats = [
            ('СИЛ', obj.str_bonus), ('ЛОВ', obj.dex_bonus), ('ТЕЛ', obj.con_bonus),
            ('ИНТ', obj.int_bonus), ('МУД', obj.wis_bonus), ('ХАР', obj.cha_bonus)
        ]

        badges = []
        for label, val in stats:
            if val > 0:
                color = '#2ecc71'
                sign = f"+{val}"
            elif val < 0:
                color = '#e74c3c'
                sign = f"{val}"
            else:
                color = '#7f8c8d'
                sign = "0"

            badge_html = (
                f'<span style="background: #1a1a26; border: 1px solid #333; '
                f'padding: 2px 6px; border-radius: 4px; margin-right: 4px;'
                f'font-family: monospace; display: inline-block; margin-bottom: 2px;">'
                f'<b style="color: #00f3ff;">{label}:</b> '
                f'<span style="color: {color}; font-weight: bold;">{sign}</span>'
                f'</span>'
            )
            badges.append(badge_html)

        # Склеиваем все строки и один раз помечаем их как безопасный HTML
        html_string = "".join(badges)
        return format_html("{}", mark_safe(html_string))

    get_d20_stats.short_description = 'Модификаторы d20'

    @admin.display(description='Аватар')
    def get_image(self, obj):
        if obj.image:
            # Генерируем HTML-тег картинки с фиксированной высотой 40 пикселей
            return format_html('<img src="{}" style="height: 40px; border-radius: 4px;" />', obj.image.url)
