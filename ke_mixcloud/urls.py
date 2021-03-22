from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_swagger_view(title='Fileserver API')
admin.site.site_header = 'Fileserver Admin'
admin.site.index_title = 'Fileserver Modules'

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('', include('apps.authentication.urls')),
    path('', include('apps.setup.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

