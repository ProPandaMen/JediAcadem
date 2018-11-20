"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from firstapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('candidate', views.candidate_main),
    path('test', views.test_main),
    path('masterJedi', views.master_jedi_main),
    path('watchtest/<int:id>/', views.watch_test),
    path('send/<str:name>/<int:id>/', views.send_message),
    path('masterdJediF', views.master_jedi_filter),
    path('djedaif', views.jedi_filter)
]
