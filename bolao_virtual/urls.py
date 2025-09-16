from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from estatisticas.views import estatisticas_visitas


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('palpites/', include('palpites.urls')),
    path('interacao/', include('comunidade.urls')),
    path('loja/', include('loja.urls')),
    path('pagamentos/', include('pagamentos.urls')),
    path('premios/', include('premios.urls')),
    path('accounts/', include('usuarios.urls')),

    path('estatisticas/', estatisticas_visitas, name='estatisticas'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
