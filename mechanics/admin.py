from django.contrib import admin
from .models import Trait


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
