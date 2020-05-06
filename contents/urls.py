"""contents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('deliveries/', include('shipping.shipping.urls')),
    path('products/', include('emporio.emporio.urls')),
    path('contents/', include('plethora.plethora.urls')),
    path('blocks/', include('feedly.feedly.urls')),
    path('links/', include('socialize.socialize.urls')),
]