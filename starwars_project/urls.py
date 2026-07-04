from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Системный интерфейс управления базой данных (Админ-панель)
    path('admin/', admin.site.urls),

    # Маршруты интеграции текстового WYSIWYG-редактора django_ckeditor_5
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # Локальный модуль навигации и детализации объектов справочника (Вики)
    path('wiki/', include('wiki.urls', namespace='wiki')),
]

# Раздача пользовательских медиафайлов в локальном режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
