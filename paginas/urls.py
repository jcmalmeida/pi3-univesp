from django.urls import path
from .views import IndexView, SobreView, ContatoView

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
]


