from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel
    path('accounts/', include('accounts.urls')),  # URLs for accounts app
    path('patients/', include('patients.urls')),  # URLs for patients app
    path('', include('accounts.urls')),  # Default home page (e.g., login or dashboard)

    path('', views.landing_page, name='landing_page')
]