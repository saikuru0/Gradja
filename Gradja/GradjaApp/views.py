from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import AddClassForm, AddStudentParentForm, AssignStudentsForm, delClassForm, delStudentParentForm, editClassForm, SignUpForm, MailForm
from .models import Mails, GradeType, Classes, SubjectTypes, Subjects, StudentParent, Grades, Users, SubjectTypes, GradeValue, ClassStudents
from .forms import delGradetypeForm, editGradetypeForm, SubjectChoice, addGradetypeForm, AddOneGrade, AddGrade, GradeFormSet
from .decorators import not_logged_in_required, user_with_required_group
from .forms import DelSubjectTypeForm
from .forms import SubjectTypeForm
from .forms import generate_unique_integer_id
from .forms import SubjectForm
from django.forms import modelformset_factory, inlineformset_factory
from .forms import ChangeGradeForm


def home(request):
    return render(request, "home.html", {})

def examine_grade(request, grade_id=None):
    grade = get_object_or_404(Grades, gradeId=grade_id)
    editable = (request.user == grade.classId.teacherId)
    if request.method == 'POST':
        if 'delete' in request.POST:
            grade.delete()
        form = ChangeGradeForm(request.POST)
        if form.is_valid():
            grade.gradeValueId = form.cleaned_data.get('gradeValueId')
            grade.typeId = form.cleaned_data.get('typeId')
            grade.description = form.cleaned_data.get('description')
            grade.save()
    return redirect('teacher_grade')
    else:
        form = ChangeGradeForm(initial={'gradeValueId': grade.gradeValueId, 'typeId': grade.typeId, 'description': grade.description})
    return render(request, 'examine_grade.html', {'grade': grade, 'editable': editable, 'form': form, 'gi': grade_id})

@not_logged_in_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




@user_with_required_group('teacher', 'admin')
def set_grades(request):
    return render(request, 'set_grades.html', {})

def view_grades(request, selected_username=None):
    user_id = request.user
    if (selected_username is None):
        selected = user_id
        if (StudentParent.objects.filter(parentId=user_id).exists()):
            return redirect('choose_child')
    else:
        selected = Users.objects.get(username=selected_username)
    pops = StudentParent.objects.filter(parentId=user_id)
    if (selected not in [user_id] + [pop.studentId for pop in pops]):
        return redirect('view_grades')
    grades = Grades.objects.filter(studentId=selected)
    subjects = list({grade.classId for grade in grades})
    subject_grades = [[subject, [grade for grade in grades.filter(classId=subject)]] for subject in subjects]
    return render(request, 'view_grades.html', {'sg': subject_grades})

def choose_child(request):
    user_id = request.user
    pops = StudentParent.objects.filter(parentId=user_id)
    children = [pop.studentId for pop in pops]
    return render(request, 'choose_child.html', {'children': children})

@user_with_required_group('admin')
def set_type_subject(request):
    if request.method == 'POST':
        postForm = DelSubjectTypeForm(request.POST)
        if postForm.is_valid():
            type_id = postForm.cleaned_data['typeId']
            subject_type = SubjectTypes.objects.get(typeId=type_id)
            subject_type.delete()

    subject_types = SubjectTypes.objects.all()
    form = DelSubjectTypeForm()
    return render(request, "set_type_subject.html", {'subject_types': subject_types, 'form': form})



@user_with_required_group('admin')
def add_subjecttype(request):
    if request.method == 'POST':
        form = SubjectTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('set_type_subject')
    else:
        form = SubjectTypeForm()
        form.initial['typeId'] = generate_unique_integer_id()

    return render(request, 'add_subjecttype.html', {'form': form})



@user_with_required_group('admin')
def edit_subject_type(request, typeId):
    subject_type = get_object_or_404(SubjectTypes, typeId=typeId)
    if request.method == 'POST':
        form = SubjectTypeForm(request.POST, instance=subject_type)
        if form.is_valid():
            form.save()
            return redirect('set_type_subject')
    else:
        form = SubjectTypeForm(instance=subject_type)

    return render(request, 'edit_subject_type.html', {'form': form})



@user_with_required_group('admin')
def view_subjects(request):
    subjects = Subjects.objects.all()
    return render(request, "view_subjects.html", {'subjects': subjects})



@user_with_required_group('admin')
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_subjects')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})



@user_with_required_group('admin')
def edit_subject(request, subjectId):
    subject = get_object_or_404(Subjects, subjectId=subjectId)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('view_subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'edit_subject.html', {'form': form})



@user_with_required_group('admin')
def set_gradetype(request):
    if request.method == 'POST':
        postForm = delGradetypeForm(request.POST)
        if postForm.is_valid():
            gradetype_id = postForm.cleaned_data['gradetypeId']
            gradetypes = GradeType.objects.get(typeId=gradetype_id)
            gradetypes.delete()
    gradetypes = GradeType.objects.all()
    form = delGradetypeForm()
    return render(request, "set_gradetype.html", {'gradetypes' : gradetypes, 'form' : form})


@user_with_required_group('admin')
def add_gradetype(request):
    if request.method == 'POST':
        form = addGradetypeForm(request.POST)
        if form.is_valid():
            type_name = form.cleaned_data['typeName']
            weight = form.cleaned_data['weight']

            new_grade_type = GradeType(typeName=type_name, weight=weight)
            new_grade_type.save()

            return redirect('set_gradetype')

    else:
        form = addGradetypeForm()

    context = {'form': form}
    return render(request, "add_gradetype.html", context)


@user_with_required_group('admin')
def edit_gradetype(request, gradetype_id):
    gradetype = get_object_or_404(GradeType, typeId=gradetype_id)

    if request.method == 'POST':
        form = editGradetypeForm(request.POST)
        if form.is_valid():
            gradetype.typeName = form.cleaned_data['typeName']
            gradetype.weight = form.cleaned_data['weight']
            gradetype.save()

            return redirect('set_gradetype')

    else:
        form = editGradetypeForm(initial={'typeName': gradetype.typeName, 'weight': gradetype.weight})

    context = {'form': form, 'gradetype': gradetype}
    return render(request, "edit_gradetype.html", context)



def view_mail(request, mail_id):
    mail = get_object_or_404(Mails, mailId=mail_id)
    return render(request, 'view_mail.html', {'mail': mail})



def grade_view(request):
    return render(request, 'grades.html', {})



def add_grade_subject_choice(request):
    if request.method == 'POST':
        form = SubjectChoice(request.POST)
        if form.is_valid():
            chosen = form.cleaned_data['chosen_subject']
            selected_subject = chosen.subjectId
            request.session['chosen_subject'] = selected_subject
            return redirect('add_one_grade')
    else:
        form = SubjectChoice()

    return render(request, 'grades_choice.html', {'form': form})


def add_one_grade(request):
    if request.method == 'POST':
        form = AddOneGrade(request.POST)
        if form.is_valid():
            form.save()
        return redirect('grades_choice')

    else:
        selected_subject = request.session.get('chosen_subject', None)
        subject = Subjects.objects.filter(subjectId=selected_subject).first()
        form = AddOneGrade(initial={'classId': subject})

    context = {'form': form, 'selected_subject': selected_subject, }
    return render(request, "add_one_grade.html", context)




def send_mail(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.fromId = request.user
            mail.sendDate = timezone.now()
            mail.save()
            return redirect('inbox')
    else:
        form = MailForm()

    return render(request, 'send_mail.html', {'form': form})



def inbox(request):
    user_mails = Mails.objects.filter(toId=request.user)
    sent_mails = Mails.objects.filter(fromId=request.user)
    return render(request, 'inbox.html', {'user_mails': user_mails, 'sent_mails': sent_mails})



@user_with_required_group('admin')
def set_class(request):
    if request.method == 'POST':
        postForm = delClassForm(request.POST)
        if postForm.is_valid():
            class_id = postForm.cleaned_data['classId']
            classes = Classes.objects.get(classId=class_id)
            classes.delete()
    classes = Classes.objects.all()
    form = delClassForm()
    return render(request, 'set_class.html', {'classes': classes, 'form' : form})



@user_with_required_group('admin')
def add_class(request):
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_class')
    else:
        form = AddClassForm()

    return render(request, 'add_class.html', {'form': form})


@user_with_required_group('admin')
def edit_class(request, class_id):
    instance = get_object_or_404(Classes, classId=class_id)

    if request.method == 'POST':
        form = editClassForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('set_class')

    else:
        form = editClassForm(instance=instance)

    context = {'form': form, 'class': instance}
    return render(request, "edit_class.html", context)



@user_with_required_group('admin')
def assign_students(request):
    if request.method == 'POST':
        form = AssignStudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assign_students')
    else:
        form = AssignStudentsForm()

    return render(request, 'assign_students.html', {'form': form})


@user_with_required_group('admin')
def set_student_parent(request):
    if request.method == 'POST':
        postForm = delStudentParentForm(request.POST)
        print("blablabla")
        if postForm.is_valid():
            student_id = postForm.cleaned_data['studentId']
            parent_id = postForm.cleaned_data['parentId']
            print('bla', student_id, parent_id)
            student_parent = get_object_or_404(StudentParent, studentId=student_id, parentId=parent_id)
            student_parent.delete()

    student_parent = StudentParent.objects.all()
    form = delStudentParentForm()
    return render(request, 'set_student_parent.html', {'student_parent': student_parent, 'form': form})



@user_with_required_group('admin')
def add_student_parent(request):
    if request.method == 'POST':
        form = AddStudentParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('set_student_parent')
    else:
        form = AddStudentParentForm()

    return render(request, 'add_student_parent.html', {'form': form})


@user_with_required_group('admin', 'teacher')
def teacher_grades_view(request):
    if request.method == 'GET':
        subject_id = request.GET.get('subject_id')
        if subject_id:
            students_grades = {}
            subject = Subjects.objects.get(subjectId=subject_id)
            students = Users.objects.filter(studentId__classId=subject.classId)
            
            for student in students:
                student_grades = Grades.objects.filter(studentId=student, classId=subject)
                if len(student_grades) == 0:
                    average = 1.
                else:
                    average = sum([grade.gradeValueId.gradeId for grade in student_grades]) / len(student_grades)
                students_grades[student] = {'grades': student_grades, 'average': average}

            return render(request, 'teacher_grades.html', {'students_grades': students_grades, 'subject': subject})

    # List subjects taught by the logged-in teacher
    teacher_subjects = Subjects.objects.filter(teacherId=request.user)
    return render(request, 'select_subject.html', {'subjects': teacher_subjects})

@user_with_required_group('admin', 'teacher')
def homeroom_teacher_view(request):
    user_id = request.user.id
    homeroom_class = Classes.objects.filter(homeroomTeacher_id=user_id).first()

    if homeroom_class:
        subjects = Subjects.objects.filter(classId=homeroom_class)
        return render(request, 'homeroom_teacher_view.html', {'subjects': subjects, 'class': homeroom_class})
    else:
        return render(request, 'no_homeroom.html')

