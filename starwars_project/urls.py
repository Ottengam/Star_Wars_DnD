from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Подключаем маршруты CKEditor 5 для загрузки картинок внутри текста
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # Подключаем свои приложения
    path('wiki/', include('wiki.urls', namespace='wiki')),
]

# Раздача картинок (папки media) во время разработки проекта
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
