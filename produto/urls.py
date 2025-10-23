from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('addCarrinho/', views.addCarrinho.as_view(), name='addcarrinho'),
    path('removerCarrinho/', views.removerCarrinho.as_view(), name='removercarrinho'),
    path('Carrinho/', views.Carrinho.as_view(), name='Carrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
]
