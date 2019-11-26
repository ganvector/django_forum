from django.urls import path
from .views import (
    PostagemListView,
    PostagemDetailView,
    PostagemCreateView,
    PostagemUpdateView,
    PostagemDeleteView,
    RespostaCreateView,
    RespostaDeleteView,
    RespostaUpdateView,
    PostagemMarcarResposta
)
from . import views

urlpatterns = [
    path('', PostagemListView.as_view(), name='forum-home'),
    path('postagem/<int:pk>/', PostagemDetailView.as_view(), name='postagem-detail'),
    path('postagem/new/', PostagemCreateView.as_view(), name='postagem-create'),
    path('postagem/<int:pk>/update/', PostagemUpdateView.as_view(), name='postagem-update'),
    path('postagem/<int:pk>/delete/', PostagemDeleteView.as_view(), name='postagem-delete'),
    path('postagem/marcar_resposta/', PostagemMarcarResposta.as_view(), name='marcar-resposta'),
    path('resposta/new/', RespostaCreateView.as_view(), name='resposta-create'),
    path('resposta/<int:pk>/delete/', RespostaDeleteView.as_view(), name='resposta-delete'),
    path('resposta/<int:pk>/update/', RespostaUpdateView.as_view(), name='resposta-update'),
    path('sobre/', views.about, name='forum-about'),
]