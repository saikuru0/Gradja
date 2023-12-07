from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades', views.set_grades, name='set_grades'),
    path("set_gradetype", views.set_gradetype, name='set_gradetype'),
]