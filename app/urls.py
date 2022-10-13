from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('update', views.update, name='update'),
    path('dash/<str:pk>',views.dash,name='dash'),
    path('add',views.add,name='add')
]
