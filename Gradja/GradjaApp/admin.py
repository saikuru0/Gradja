from django.contrib import admin
from .models import Roles, Users, Mails, Classes, Subjects, SubjectTypes, GradeType, GradeValue, Grades, ClassStudents, StudentParent

# Register your models here.
admin.site.register(Roles)
admin.site.register(Users)
admin.site.register(StudentParent)
admin.site.register(Mails)
admin.site.register(Classes)
admin.site.register(ClassStudents)
admin.site.register(Subjects)
admin.site.register(SubjectTypes)
admin.site.register(Grades)
admin.site.register(GradeType)
admin.site.register(GradeValue)

