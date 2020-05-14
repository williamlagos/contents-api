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
from django.views import View
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from socialize.socialize.urls import accounts_patterns
from shipping.shipping.urls import deliveries_patterns
from plethora.plethora.urls import contents_patterns
from emporio.emporio.urls import urlpatterns as emporio_patterns
from feedly.feedly.urls import blocks_patterns

class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({'health': 'success'})

urlpatterns = [
    path('', HealthCheckView.as_view()),
    path('dashboard/', admin.site.urls),
    path('deliveries/', include(deliveries_patterns)),
    path('accounts/', include(accounts_patterns)),
    path('contents/', include(contents_patterns)),
    path('emporio/', include(emporio_patterns)),
    path('blocks/', include(blocks_patterns)),
]