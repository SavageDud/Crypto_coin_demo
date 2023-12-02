"""
URL configuration for crypto_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("" , views.index_view),
    path("mod/" , views.owner_view),
    path("create_keys/" , views.API_Generate_public_and_private_keys),
    path("create_genesis/" , views.Create_genesis_block),
    path("admin_mint/" , views.Admin_command_mint),
    path("api_getLenght/" , views.API_GetBlockChainLenght),
    path('api_getBlockData/' , views.API_GetBlockData),
    path('api_deriveKeys/' , views.API_Derivekeys),
    path('api_getWalletBallance/' , views.API_GetWalletBallance),
    path('api_uploadTransaction/', views.Create_Transaction)
    
]

