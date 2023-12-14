from django.urls import path
from . import views
from .views import edit_subject_type

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades', views.set_grades, name='set_grades'),
    path('set_type_subject/', views.set_type_subject, name='set_type_subject'),
    path('add_subjecttype/', views.add_subjecttype, name='add_subjecttype'), 
    path('edit_subject_type/<int:typeId>/', edit_subject_type, name='edit_subject_type'),
    path('subjects/', views.view_subjects, name='view_subjects'),
    path('subjects/add', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subjectId>/', views.edit_subject, name='edit_subject'),
]