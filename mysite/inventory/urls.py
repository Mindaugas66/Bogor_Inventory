from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.redirect_to_dashboard, name='redirect_to_dashboard'),  # Add this line
    path('dashboard/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
]