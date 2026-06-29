from django.db import models


class Trait(models.Model):
    """
    Модель для конкретных способностей и механик расы.
    Используется программными модулями для применения спец-эффектов к персонажу.

    :cvar code_name: Технический идентификатор (маркер) особенности для формул и кода.
    :cvar name: Название особенности, лимит 50 символов.
    :cvar description: Игровое описание механики способностей для пользователей.
    """
    code_name: str = models.CharField(max_length=50, unique=True, verbose_name="Кодовое имя")
    name: str = models.CharField(max_length=50, verbose_name="Название способности")
    description: str = models.TextField(verbose_name="Игровое описание механики")

    def __str__(self) -> str:
        """
            Превращает сложный объект особенности в понятную строку.

            :return: Текстовое название текущей особенности.
        """
        return self.name

    class Meta:
        """
            Мета-настройки для управления поведением таблицы расовых особенностей.

            :cvar verbose_name: Локализованное имя сущности в единственном числе.
            :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
            :cvar ordering: Поле, по которому применяется автоматическая сортировка.
        """
        verbose_name = "Игровая способность"
        verbose_name_plural = "Игровые способности"
        ordering = ['name']
