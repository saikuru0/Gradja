from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Roles(models.Model):
    roleId = models.IntegerField(primary_key = True)
    roleName = models.CharField(max_length=20)

    class Meta:
        db_table = "Roles"
        verbose_name_plural = "Roles"

class Users(AbstractUser):
    # userId = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=32, null=True)
    # surname = models.CharField(max_length=32, null=True)
    # role = models.ForeignKey(Roles, null=True, on_delete= models.CASCADE)

    # studentParent = models.ManyToManyField('self', null=True, related_name='StudentParent', symmetrical=False)
    studentParent = models.ManyToManyField('self', through='StudentParent', symmetrical=False)

    class Meta:
        db_table = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.first_name + " " + self.last_name




class StudentParent(models.Model):
    studentId = models.ForeignKey(Users, on_delete = models.CASCADE)
    parentId = models.ForeignKey(Users, on_delete = models.CASCADE, related_name= "parentId")

    class Meta:
        db_table = "StudentParent"
        verbose_name_plural = "StudentParent"



class Mails(models.Model):
    mailId = models.IntegerField(primary_key = True)
    fromId = models.ForeignKey(Users, null = True, on_delete= models.SET_NULL, related_name= "fromId")
    toId = models.ForeignKey(Users, null = True, on_delete= models.SET_NULL, related_name= "toId")
    sendDate = models.DateField()
    topic = models.CharField(max_length=200)
    mailText = models.TextField()

    class Meta:
        db_table = "Mails"
        verbose_name_plural = "Mails"

class Classes(models.Model):
    classId = models.IntegerField(primary_key = True)
    className = models.CharField(max_length=10)
    homeroomTeacher = models.ForeignKey(Users, null = True, on_delete= models.SET_NULL, related_name='homeroomTeacher')
    activeFrom = models.DateField()
    activeTo = models.DateField()

    classStudent = models.ManyToManyField(Users, through='ClassStudents', symmetrical=False)

    class Meta:
        db_table = "Classes"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.className


class ClassStudents(models.Model):
    classId = models.ForeignKey(Classes, on_delete = models.CASCADE)
    studentId = models.ForeignKey(Users, on_delete= models.CASCADE, related_name='studentId')
    activeFrom = models.DateField()
    activeTo = models.DateField()

    class Meta:
        db_table = "Class Students"
        verbose_name_plural = "Class Students"


class SubjectTypes(models.Model):
    typeId = models.IntegerField(primary_key = True)
    typeName = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        db_table = "Subject types"
        verbose_name_plural = "Subject types"

    def __str__(self):
        return self.typeName


class Subjects(models.Model):
    subjectId = models.IntegerField(primary_key = True)
    classId = models.ForeignKey(Classes, on_delete = models.CASCADE)
    subjectType = models.ForeignKey(SubjectTypes, on_delete = models.CASCADE)
    teacherId = models.ForeignKey(Users, on_delete = models.CASCADE)
    activeFrom = models.DateField()
    activeTo = models.DateField()

    class Meta:
        db_table = "Subjects"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.subjectType.__str__() + " " + self.classId.__str__()


class GradeType(models.Model):
    typeId = models.IntegerField(primary_key = True)
    typeName = models.CharField(max_length=20)
    weight = models.IntegerField()

    class Meta:
        db_table = "Grade Types"
        verbose_name_plural = "Grade Types"

    def __str__(self):
        return self.typeName


class GradeValue(models.Model):
    gradeId = models.FloatField(primary_key = True)
    typeName = models.CharField(max_length=20)

    class Meta:
        db_table = "Grade Values"
        verbose_name_plural = "Grade Values"

    def __str__(self):
        return self.typeName


class Grades(models.Model):
    gradeId = models.IntegerField(primary_key = True)
    classId = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    studentId = models.ForeignKey(Users, on_delete = models.CASCADE)
    gradeValueId = models.ForeignKey(GradeValue, null=True, blank=True, on_delete = models.CASCADE)
    typeId = models.ForeignKey(GradeType, on_delete = models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = "Grades"
        verbose_name_plural = "Grades"



