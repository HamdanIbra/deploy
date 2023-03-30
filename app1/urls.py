from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('paintings', views.paintings),
    path('login', views.login),
    path('paintings/new',views.new_painting),
    path('create_painting',views.create_painting),
    path('paintings/<int:id>',views.painting_details),
    path('paintings/<int:id>/edit',views.edit_painting),
    path('edit/<int:id>',views.edit),
    path('delete/<int:id>',views.delete_painting),
    path('logout',views.logout),
    path('buy/<int:id>',views.buy),
]
