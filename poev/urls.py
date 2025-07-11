"""
URL configuration for poeu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from cadastros.views import IncluirMultiplasVagasAPI, IncluirMultiplosCursosAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')),
    path('', include('cadastros.urls')),
    path('', include('usuarios.urls')),
#    path('', include('mapas.urls')),
#	path('favicon.ico', RedirectView.as_view(url='/media/favicon.ico')),
#    path('ckeditor5/', include('django_ckeditor_5.urls')),
  # Inclua o caminho para as URLs do CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # Adicionado para o CKEditor 5

    # Endpoints de autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoints de criação de vagas e cursos
    path('api/incluir-multiplas-vagas/', IncluirMultiplasVagasAPI.as_view(), name='incluir_multiplas_vagas'),
    path('api/incluir-multiplos-cursos/', IncluirMultiplosCursosAPI.as_view(), name='incluir_multiplos_cursos'),
]
### Serve arquivos estáticos e de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

