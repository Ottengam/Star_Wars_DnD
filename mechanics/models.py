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


class Skill(models.Model):
    """
    Модель для навыков персонажей.
    Служат базой для привязки древа перков и расчетов бросков персонажей.

    :cvar attribute: Текстовый маркер базовой характеристики.
    :cvar name: Уникальное название навыка, лимит 40 символов.
    :cvar description: Текстовое описание правил применения навыка в игре.
    :cvar image: Иконка навыка, загружаемая в изолированную директорию медиа-хранилища.
    """

    class AttributeMarker(models.TextChoices):
        """
        Перечисление базовых характеристик персонажа.
        """
        STRENGTH = 'STR', 'Сила'
        AGILITY = 'DEX', 'Ловкость'
        CONSTITUTION = 'CON', 'Телосложение'
        INTELLIGENCE = 'INT', 'Интеллект'
        WISDOM = 'WIS', 'Мудрость'
        CHARISMA = 'CHA', 'Харизма'

    attribute: str = models.CharField(max_length=3, choices=AttributeMarker.choices, verbose_name="Характеристика")
    name: str = models.CharField(max_length=40, unique=True, verbose_name="Название")
    description: str = models.TextField(verbose_name="Описание навыка")
    image = models.ImageField(upload_to="mechanics/skills/", blank=True, null=True, verbose_name="Иллюстрация навыка")

    # Подсказка для IDE
    get_attribute_display: callable

    def __str__(self) -> str:
        """
        Превращает сложный объект навыка в понятную текстовую строку для списков.

        :return: Название навыка с указанием его базовой характеристики.
        """
        return f"{self.name} [{self.get_attribute_display()}]"

    class Meta:
        """
        Мета-настройки для управления поведением таблицы в Django и СУБД.

        :cvar verbose_name: Локализованное имя сущности в единственном числе.
        :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
        """
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class Perk(models.Model):
    """
    Модель для перков персонажей.
    Определяет уникальные способности, развиваемые внутри конкретных навыков.

    :cvar name: Название перка, лимит 50 символов.
    :cvar max_levels: Максимально допустимый уровень прокачки данного таланта.
    :cvar description: Текстовое описание игровых эффектов перка для каждого уровня.
    :cvar skill: Ссылка на родительский навык, к ветке которого принадлежит перк.
    :cvar required_skill_level: Требуемый уровень родительского навыка для открытия перка.
    :cvar required_perks: Список других перков, необходимых для изучения.
    """
    name: str = models.CharField(max_length=50, verbose_name="Название перка")
    max_levels: int = models.PositiveIntegerField(default=1, verbose_name="Максимальный уровень")
    description: list[str] = models.JSONField(verbose_name="Описание перка по уровням")
    skill: Skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="perks",
                                     verbose_name="Родительский навык")
    required_skill_level: int = models.PositiveIntegerField(default=1, verbose_name="Требуемый уровень навыка")
    required_perks = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_perks',
                                            verbose_name="Требуемые перки")

    def __str__(self) -> str:
        """
        Превращает сложный объект перка в понятную текстовую строку для списков.

        :return: Название перка с указанием его родительского навыка.
        """
        return f"{self.name} [{self.skill.name}]"

    class Meta:
        """
        Мета-настройки для управления поведением таблицы перков в Django и СУБД.

        :cvar verbose_name: Локализованное имя сущности в единственном числе.
        :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
        :cvar unique_together: Ограничение уникальности имени перка в рамках одного навыка.
        """
        verbose_name = "Перк"
        verbose_name_plural = "Перки"
        unique_together = ('skill', 'name', 'required_skill_level')


class RuleSection(models.Model):
    """
    Модель для разделов Книги игрока.
    Определяет категории правил в терминале.

    :cvar title: Название раздела правил, лимит 50 символов.
    :cvar slug: Уникальный текстовый ярлык страницы для формирования URL, лимит 50 символов.
    :cvar description: Развернутое текстовое описание назначения данного раздела.
    :cvar icon: Графические иконки интерфейса, загружаемый в изолированную директорию медиа-хранилища.
    :cvar sort_order: Цифровой индекс для управления приоритетом вывода карточки в общем цикле.
    :cvar general_rules: Поле для хранения общих правил раздела в формате JSON.
    """
    title: str = models.CharField(max_length=50, verbose_name="Название раздела")
    slug: str = models.SlugField(max_length=50, unique=True, verbose_name="URL")
    description: str = models.TextField(verbose_name="Описание раздела")
    icon: models.ImageField = models.ImageField(upload_to='mechanics/icons/', verbose_name="Иконка")
    sort_order: int = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    general_rules = models.JSONField(blank=True, null=True, verbose_name="Общие правила раздела")

    def __str__(self) -> str:
        """
        Превращает объект раздела в текстовую строку для списков и панелей управления.

        :return: Название раздела правил.
        """
        return self.title

    class Meta:
        """
        Мета-настройки для управления поведением таблицы разделов правил в Django и СУБД.

        :cvar verbose_name: Локализованное имя сущности в единственном числе.
        :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
        :cvar ordering: Двухуровневый алгоритм сортировки (сначала по индексу приоритета, затем по алфавиту).
        """
        verbose_name = "Раздел правил"
        verbose_name_plural = "Разделы правил"
        ordering = ['sort_order', 'title']
