from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('dashboard/items/<item_id>', views.show),
    path('items/add', views.add),
    path('create', views.create),
    path('join/<item_id>', views.join),
    path('leave/<item_id>', views.leave),
]