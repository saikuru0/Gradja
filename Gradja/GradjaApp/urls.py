from django.urls import path
from . import views
from .views import edit_subject_type

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('set_grades/', views.set_grades, name='set_grades'),
    path('assign_students/', views.assign_students, name='assign_students'),
    path('set_grades', views.set_grades, name='set_grades'),
    path('set_type_subject/', views.set_type_subject, name='set_type_subject'),
    path('add_subjecttype/', views.add_subjecttype, name='add_subjecttype'), 
    path('edit_subject_type/<int:typeId>/', edit_subject_type, name='edit_subject_type'),
    path('subjects/', views.view_subjects, name='view_subjects'),
    path('subjects/add', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subjectId>/', views.edit_subject, name='edit_subject'),
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
    path('set_student_parent/', views.set_student_parent, name='set_student_parent'),
    path('add_student_parent/', views.add_student_parent, name='add_student_parent'),
    path('add_one_grade',  views.add_one_grade, name='add_one_grade' ),
    path('view_grades/', views.view_grades, name='view_grades'),
    path('view_grades/<str:selected_username>/', views.view_grades, name='view_grades'),
    path('choose_child/', views.choose_child, name='choose_child'),
    path('examine_grade/<int:grade_id>/', views.examine_grade, name='examine_grade'),
    path('examine_grade/', views.examine_grade, name='examine_grade'),
    path('teacher_grades/', views.teacher_grades_view, name='teacher_grades'),
    path('homeroom_teacher/', views.homeroom_teacher_view, name='homeroom_teacher_view'),
]

