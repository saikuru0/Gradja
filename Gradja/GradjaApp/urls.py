from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades/', views.set_grades, name='set_grades'),
    path('add_class/', views.add_class, name='add_class'),
    path('assign_students/', views.assign_students, name='assign_students'),
    path('set_grades', views.set_grades, name='set_grades'),
    path("set_gradetype", views.set_gradetype, name='set_gradetype'),
    path("add_gradetype", views.add_gradetype, name='add_gradetype'),
    path('edit_gradetype/<int:gradetype_id>/', views.edit_gradetype, name='edit_gradetype'),
    path("grades", views.grade_view, name='grades'),
    path("grades_choice", views.add_grade_subject_choice, name='grades_choice'),
    path('send_mail', views.send_mail, name='send_mail'),
    path('inbox', views.inbox, name='inbox'),
    path('view_mail/<int:mail_id>/', views.view_mail, name='view_mail'),
    path('set_class/', views.set_class, name='set_class'),
    path('add_class/', views.add_class, name='add_class'),
    path('edit_class/<int:class_id>/', views.edit_class, name='edit_class'),
]
