from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades/', views.set_grades, name='set_grades'),
    path('add_class/', views.add_class, name='add_class'),
    path('assign_students/', views.assign_students, name='assign_students'),
]
