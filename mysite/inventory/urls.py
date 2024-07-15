from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.redirect_to_dashboard, name='redirect_to_dashboard'),  # Add this line
    path('dashboard/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>', views.order_view, name="Order_view"),
    path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/edit', views.edit_order, name='order_edit'),
    path('orders/add/', views.new_order, name='new_order'),
    path('inventory/', views.inventory, name='inventory'),
    path('restock/satin_silk/<int:pk>/', views.restock_satin_silk, name='restock_satin_silk'),
    path('add_new/satin_silk/', views.add_new_satin_silk, name='add_new_satin_silk'),
    path('restock/decorations/<int:pk>/', views.restock_decorations, name='restock_decorations'),
    path('add_new/decorations/', views.add_new_decorations, name='add_new_decorations'),
    path('restock/materials/<int:pk>/', views.restock_materials, name='restock_materials'),
    path('add_new/materials/', views.add_new_materials, name='add_new_materials'),
]