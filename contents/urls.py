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
from socialize.socialize.urls import accounts_patterns
from shipping.shipping.urls import deliveries_patterns
from plethora.plethora.urls import contents_patterns
from emporio.emporio.urls import products_patterns, baskets_patterns, orders_patterns
from feedly.feedly.urls import blocks_patterns

# from django.contrib.auth.models import User
# from django.views import View
# from django.http import JsonResponse
# from django.core import serializers

# class UsersView(View):
#     def get(self, request):
#         return JsonResponse(User.objects.all().values()[0])

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('deliveries/', include(deliveries_patterns)),
    path('accounts/', include(accounts_patterns)),
    path('contents/', include(contents_patterns)),
    path('products/', include(products_patterns)),
    path('baskets/', include(baskets_patterns)),
    path('orders/', include(orders_patterns)),
    path('blocks/', include(blocks_patterns)),
    # path('users/', UsersView.as_view()),
]