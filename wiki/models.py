from __future__ import annotations

from django.db import models
from multiselectfield import MultiSelectField
from django_ckeditor_5.fields import CKEditor5Field

import mechanics.models


class Region(models.Model):
    """
        Модель для хранения информации о географических зонах Галактики.
        Используется как верхний уровень иерархии карты в сеттинге SWTOR.
        Записи автоматически сортируются по алфавиту от А до Я.

        :cvar name: Уникальное название региона, лимит 30 символов.
        :cvar description: Историческая справка и лор региона.
        :cvar map_url: Интернет-ссылка на изображение интерактивной карты региона.
    """
    name: str = models.CharField(max_length=30, unique=True, verbose_name="Название региона")
    description: str = models.TextField(verbose_name="Описание региона")
    map_url: str | None = models.URLField(verbose_name="Ссылка на карту региона", blank=True, null=True)

    def __str__(self) -> str:
        """
        Превращает сложный объект региона в понятную строку.

        :return: Текстовое название текущего региона.
        """
        return self.name

    class Meta:
        """
            Мета-настройки для управления поведением таблицы в Django и СУБД.

            :cvar verbose_name: Локализованное имя сущности в единственном числе.
            :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
            :cvar ordering: Поле, по которому применяется автоматическая сортировка.
        """
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ['name']


class Sector(models.Model):
    """
        Модель для хранения информации о космических секторах Галактики.
        Используется как второй уровень иерархии карты в сеттинге SWTOR.
        Записи автоматически сортируются по алфавиту от А до Я.

        :cvar name: Уникальное название сектора, лимит 40 символов.
        :cvar description: Историческая справка и лор сектора.
        :cvar map_url: Интернет-ссылка на изображение интерактивной карты сектора.
        :cvar region: Родительский регион Галактики, в который входит данный сектор.
    """
    name: str = models.CharField(max_length=40, unique=True, verbose_name="Название сектора")
    description: str = models.TextField(verbose_name="Описание сектора")
    map_url: str | None = models.URLField(verbose_name="Ссылка на карту сектора", blank=True, null=True)
    region: Region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")

    def __str__(self) -> str:
        """
            Превращает сложный объект сектора в понятную строку.

            :return: Текстовое название текущего сектора.
        """
        return self.name

    class Meta:
        """
            Мета-настройки для управления поведением таблицы в Django и СУБД.

            :cvar verbose_name: Локализованное имя сущности в единственном числе.
            :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
            :cvar ordering: Поле, по которому применяется автоматическая сортировка.
        """
        verbose_name = "Сектор"
        verbose_name_plural = "Сектора"
        ordering = ['name']


class System(models.Model):
    """
        Модель для хранения информации о космических системах Галактики.
        Используется как третий уровень иерархии карты в сеттинге SWTOR.
        Записи автоматически сортируются по алфавиту от А до Я.

        :cvar name: Уникальное название системы, лимит 40 символов.
        :cvar description: Историческая справка и лор системы.
        :cvar map_url: Интернет-ссылка на изображение интерактивной карты системы.
        :cvar sector: Родительский сектор Галактики, в который входит данная система.
    """
    name: str = models.CharField(max_length=40, unique=True, verbose_name="Название системы")
    description: str = models.TextField(verbose_name="Описание системы")
    map_url: str | None = models.URLField(verbose_name="Ссылка на карту системы", blank=True, null=True)
    sector: Sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name="Сектор")

    def __str__(self) -> str:
        """
            Превращает сложный объект системы в понятную строку.

            :return: Текстовое название текущей системы.
        """
        return self.name

    class Meta:
        """
            Мета-настройки для управления поведением таблицы в Django и СУБД.

            :cvar verbose_name: Локализованное имя сущности в единственном числе.
            :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
            :cvar ordering: Поле, по которому применяется автоматическая сортировка.
        """
        verbose_name = "Звездная система"
        verbose_name_plural = "Звездные системы"
        ordering = ['name']


class Faction(models.Model):
    """
       Модель для хранения информации о фракциях и политических силах Галактики.
       Используется в системе для привязки планет, персонажей и лора к государствам.
       Записи автоматически сортируются по алфавиту от А до Я.

       :cvar name: Название фракции, лимит 65 символов.
       :cvar description: Историческая справка и описание идеологии фракции.
       :cvar parent_faction: Главная фракция (для создания дочерних подфракций).
   """
    name: str = models.CharField(max_length=65, verbose_name="Название фракции")
    description: str = models.TextField(verbose_name="Описание идеологии")
    parent_faction: Faction | None = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True,
                                                       null=True, verbose_name="Главная фракция (для дочерних)")

    def __str__(self) -> str:
        """
            Превращает сложный объект фракции в понятную строку.

            :return: Текстовое название текущей фракции.
        """
        return self.name

    class Meta:
        """
           Мета-настройки для управления поведением таблицы фракций в Django и СУБД.

           :cvar verbose_name: Локализованное имя сущности в единственном числе.
           :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
           :cvar ordering: Поле, по которому применяется автоматическая сортировка.
       """
        verbose_name = "Фракция"
        verbose_name_plural = "Фракции"
        ordering = ['name']


class Planet(models.Model):
    """
        Модель для хранения информации о планетах Галактики.
        Используется как четвертый уровень иерархии карты в сеттинге SWTOR.
        Записи автоматически сортируются по алфавиту от А до Я.

        :cvar name: Уникальное название планеты, лимит 40 символов.
        :cvar description: Историческая справка и лор планеты.
        :cvar climate: Климатический тип планеты.
        :cvar map_url: Интернет-ссылка на изображение интерактивной карты планеты.
        :cvar system: Родительская система Галактики, в которую входит данная планета.
        :cvar controlling_faction: Фракция, контролирующая планету.
    """

    class ClimateType(models.TextChoices):
        """Класс для хранения климатических типов планет"""
        UNKNOWN = 'unknown', 'Неизвестно'
        TEMPERATE = 'temperate', 'Умеренный'
        ARID = 'arid', 'Засушливый / Пустынный'
        FRIGID = 'frigid', 'Арктический / Ледяной'
        TROPICAL = 'tropical', 'Тропический / Джунгли'
        SWAMP = 'swamp', 'Болотистый'
        OCEANIC = 'oceanic', 'Океанический / Водный'
        VOLCANIC = 'volcanic', 'Вулканический'
        CITY_PLANET = 'city_planet', 'Техногенный / Планета-город'
        ARTIFICIAL = 'artificial', 'Искусственный / Механический'
        TOXIC = 'toxic', 'Токсичный / Радиоактивный'
        BARREN = 'barren', 'Бесплодная пустошь / Скалистый'
        DESOLATED = 'desolated', 'Мертвый / Выжженный Силой'
        TWILIGHT = 'twilight', 'Сумеречный мир'
        GAS_GIANT = 'gas_giant', 'Газовый гигант'

    name: str = models.CharField(max_length=40, unique=True, verbose_name="Название планеты")
    description: str = models.TextField(verbose_name="Описание планеты")
    climate: list = MultiSelectField(max_length=150, choices=ClimateType.choices, default=[ClimateType.UNKNOWN],
                                     verbose_name="Климат")
    map_url: str | None = models.URLField(verbose_name="Ссылка на карту планеты", blank=True, null=True)
    system: System = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name="Звездная система")
    controlling_faction: Faction | None = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True,
                                                            verbose_name="Контролирующая фракция")

    def __str__(self) -> str:
        """
            Превращает сложный объект планеты в понятную строку.

            :return: Текстовое название текущей планеты.
        """
        return self.name

    class Meta:
        """
            Мета-настройки для управления поведением таблицы в Django и СУБД.

            :cvar verbose_name: Локализованное имя сущности в единственном числе.
            :cvar verbose_name_plural: Локализованное имя сущности во множественном числе.
            :cvar ordering: Поле, по которому применяется автоматическая сортировка.
        """
        verbose_name = "Планета"
        verbose_name_plural = "Планеты"
        ordering = ['name']


class SkillChoices(models.TextChoices):
    """Временный список d20-навыков SWTOR для жесткого выбора без создания таблиц"""
    # === СИЛА (STR) ===
    ATHLETICS = 'athletics', 'Атлетика'
    BRAWLING = 'brawling', 'Рукопашный бой'
    WEAPON_MELEE_HEAVY = 'weapon_melee_heavy', 'Ударное оружие'
    WEAPON_MELEE_BLADES = 'weapon_melee_blades', 'Клинковое оружие'

    # Скрытые боевые навыки Силы (Открываются только форсьюзерам)
    FORM_1_SHII_CHO = 'form_1_shii_cho', 'Форма I: Шии-Чо'
    FORM_5_DJEM_SO = 'form_5_djem_so', 'Форма V: Джем Со'
    FORM_7_JUYO = 'form_7_juyo', 'Форма VII: Джуйо'

    # === ЛОВКОСТЬ (DEX) ===
    ACROBATICS = 'acrobatics', 'Акробатика'
    SLEIGHT_OF_HAND = 'sleight_of_hand', 'Ловкость рук'
    STEALTH = 'stealth', 'Скрытность'
    WEAPON_MELEE_LIGHT = 'weapon_melee_light', 'Короткое оружие'
    WEAPON_LIGHT_BLASTERS = 'weapon_light_blasters', 'Легкое оружие'
    WEAPON_RIFLES = 'weapon_rifles', 'Винтовки'
    WEAPON_SNIPER = 'weapon_sniper', 'Снайперские винтовки'
    WEAPON_REPEATERS = 'weapon_repeaters', 'Пулеметы'
    WEAPON_HEAVY = 'weapon_heavy', 'Тяжелое орудие'

    FORM_2_MAKASHI = 'form_2_makashi', 'Форма II: Макаши'
    FORM_3_SORESU = 'form_3_soresu', 'Форма III: Соресу'
    FORM_4_ATARU = 'form_4_ataru', 'Форма IV: Атару'

    # === ИНТЕЛЛЕКТ (INT) ===
    COMPUTER_USE = 'computer_use', 'Компьютеры'
    DEMOLITIONS = 'demolitions', 'Подрывное дело'
    PILOTING = 'piloting', 'Пилотирование'
    REPAIR = 'repair', 'Техника'
    MEDICINE = 'medicine', 'Медицина'
    HISTORY = 'history', 'История'
    INVESTIGATION = 'investigation', 'Анализ'

    # === МУДРОСТЬ (WIS) ===
    FORCE_KNOWLEDGE = 'force_knowledge', 'Знание Силы'
    NATURE = 'nature', 'Природа'
    PERCEPTION = 'perception', 'Восприятие'
    INSIGHT = 'insight', 'Проницательность'
    SURVIVAL = 'survival', 'Выживание'

    # Скрытый боевой навык Мудрости (Стили меча для магов-форсьюзеров)
    FORM_6_NIMAN = 'form_6_niman', 'Форма VI: Ниман'
    FORCE_POWER = 'force_power', 'Применение Силы'

    # === ХАРИЗМА (CHA) ===
    PERSUASION = 'persuasion', 'Убеждение'
    DECEPTION = 'deception', 'Обман'
    INTIMIDATION = 'intimidation', 'Запугивание'
    COMMERCE = 'commerce', 'Торговля'


class Race(models.Model):
    """
    Модель для хранения информации о расах Галактики.
    Используется для описания видов.
    Записи автоматически сортируются по алфавиту от А до Я.

    :cvar name: Название расы (вида), лимит 25 символов.
    :cvar description: Историческая справка расы.
    :cvar names: Краткое описание того, как раса формирует имена.
    :cvar male_names: Список доступных мужских имён.
    :cvar female_names: Список доступных женских имён.
    :cvar universal_names: Список имён, подходящих для любого пола.
    :cvar surnames: Список доступных фамилий.
    :cvar quote: Цитата о расе.
    :cvar quote_author: Автор цитаты.
    :cvar biology: Подробное описание биологии и внешнего вида.
    :cvar culture: Описание общества и культуры.
    :cvar history: Историческая справка и хронология расы.
    :cvar image: Главное изображение расы для карточки (аватар).
    :cvar homeworld: Родная планета расы (защищена от случайного удаления).
    :cvar colonies: Список суверенных колоний расы.
    :cvar enclaves: Список автономных анклавов расы.
    :cvar outposts: Список промышленных форпостов расы.
    :cvar integrated_worlds: Список интегрированных миров расы.
    :cvar str_bonus: Бонус к Силе (STR).
    :cvar dex_bonus: Бонус к Ловкости (DEX).
    :cvar con_bonus: Бонус к Телосложению (CON).
    :cvar int_bonus: Бонус к Интеллекту (INT).
    :cvar wis_bonus: Бонус к Мудрости (WIS).
    :cvar cha_bonus: Бонус к Харизме (CHA).
    :cvar fixed_skills: Фиксированные навыки расы.
    :cvar choice_skills: Навыки расы на выбор.
    :cvar skills_choice_count: Количество доступных навыков из списка на выбор.
    :cvar size: Размер расы.
    :cvar height_range: Рост расы.
    :cvar weight_range: Вес расы.
    :cvar speed: Базовая скорость передвижения существа в футах.
    :cvar traits: Список особенностей расы.
    """
    class SizeType(models.TextChoices):
        """
        Перечисление стандартных категорий размера существ.
        Используется для расчёта игровых модификаторов.
        """
        TINY = 'tiny', 'Крошечный'
        SMALL = 'small', 'Маленький'
        MEDIUM = 'medium', 'Средний'
        LARGE = 'large', 'Крупный'
        HUGE = 'huge', 'Огромный'
        GARGANTUAN = 'gargantuan', 'Громадный'

    name: str = models.CharField(max_length=25, verbose_name="Название расы")
    description: str = models.TextField(verbose_name="Описание расы")

    quote: str = models.TextField(verbose_name="Цитата")
    quote_author: str = models.CharField(max_length=40, verbose_name="Автор цитаты")

    names: str = models.TextField(verbose_name="Традиции именования")
    male_names: list[str] | None = models.JSONField(verbose_name="Мужские имена", null=True, blank=True)
    female_names: list[str] | None = models.JSONField(verbose_name="Женские имена", null=True, blank=True)
    universal_names: list[str] | None = models.JSONField(verbose_name="Универсальные имена", null=True, blank=True)
    surnames: list[str] | None = models.JSONField(verbose_name="Фамилии", null=True, blank=True)

    # Фиксированные поля с поддержкой картинок и стилей CKEditor 5
    biology: str = CKEditor5Field(config_name='extends', verbose_name="Биология и внешность")
    culture: str = CKEditor5Field(config_name='extends', verbose_name="Общество и культура")
    history: str = CKEditor5Field(config_name='extends', verbose_name="История")

    image: str = models.ImageField(upload_to="races/", verbose_name="Главное изображение расы")

    homeworld: Planet = models.ForeignKey(Planet, on_delete=models.PROTECT,
                                          related_name="native_races", verbose_name="Родная планета")
    colonies: models.QuerySet[Planet] = models.ManyToManyField(Planet, blank=True, related_name="colony_races",
                                                               verbose_name="Суверенные колонии")
    enclaves: models.QuerySet[Planet] = models.ManyToManyField(Planet, blank=True, related_name="enclave_races",
                                                               verbose_name="Автономные анклавы")
    outposts: models.QuerySet[Planet] = models.ManyToManyField(Planet, blank=True, related_name="outpost_races",
                                                               verbose_name="Промышленные форпосты")
    integrated_worlds: models.QuerySet[Planet] = models.ManyToManyField(Planet, blank=True,
                                                                        related_name="integrated_world_races",
                                                                        verbose_name="Интегрированные миры")

    str_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Силе")
    dex_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Ловкости")
    con_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Телосложению")
    int_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Интеллекту")
    wis_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Мудрости")
    cha_bonus: int = models.IntegerField(default=0, verbose_name="Бонус к Харизме")

    fixed_skills = MultiSelectField(max_length=255, choices=SkillChoices.choices, blank=True,
                                    verbose_name="Фиксированные навыки")
    choice_skills = MultiSelectField(max_length=500, choices=SkillChoices.choices, blank=True,
                                     verbose_name="Навыки на выбор")
    skills_choice_count = models.PositiveIntegerField(default=0, verbose_name="Количество навыков на выбор",
                                                      help_text="Количество навыков, которые нужно выбрать")

    size: str = models.CharField(max_length=15, choices=SizeType.choices, default=SizeType.MEDIUM,
                                 verbose_name="Размер")
    height_range: str = models.CharField(max_length=30, blank=True, verbose_name="Рост")
    weight_range: str = models.CharField(max_length=30, blank=True, verbose_name="Вес")

    speed: int = models.PositiveIntegerField(default=30, verbose_name="Базовая скорость (в футах)")

    starting_equipment = models.TextField(
        "Стартовое снаряжение (временно текстом)",
        blank=True,  # Разрешает оставлять форму пустой в админке
        null=True,  # Разрешает записывать NULL в базу данных
        help_text="Оставьте пустым, если у расы нет стартовых предметов"
    )

    # Связь со справочником программных особенностей (RaceTrait)
    traits: models.QuerySet[mechanics.models.Trait] = models.ManyToManyField('mechanics.Trait', blank=True,
                                                                             related_name="races",
                                                                             verbose_name="Особенности механики")

    def __str__(self) -> str:
        """
        Превращает сложный объект расы в понятную строку.

        :return: Текстовое название текущей расы.
        """
        return self.name

    class Meta:
        verbose_name = "Раса"
        verbose_name_plural = "Расы"
        ordering = ['name']
