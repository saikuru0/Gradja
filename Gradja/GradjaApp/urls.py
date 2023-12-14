from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades', views.set_grades, name='set_grades'),
    path('send_mail', views.send_mail, name='send_mail'),
    path('inbox', views.inbox, name='inbox')
]
