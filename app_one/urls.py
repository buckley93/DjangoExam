from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('addQuote', views.add_quote),
    path('favorite/<int:id>', views.favorite),
    path('unfavorite/<int:id>', views.remove),
    path('quotes/<int:id>/delete', views.delete),
    path('quotes/<int:id>', views.show_quote),
    path('quotes/<int:id>/edit', views.edit),
    path('showuser/<int:id>', views.showuser),
    path('mainpage', views.mainpage),
]
