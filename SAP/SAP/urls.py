"""
URL configuration for SAP project.

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
import biometrics # Import the device view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biometrics/', include('biometrics.urls')),
    path('hr/', include('hr.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("account.urls")),  # Added a comma at the end
    path('', biometrics.views.index),  # Use the device view from biometrics app
    # path("auth/", include("auth.urls")),
]

