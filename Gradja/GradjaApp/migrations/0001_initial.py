# Generated by Django 4.2.7 on 2023-12-04 20:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('classId', models.IntegerField(primary_key=True, serialize=False)),
                ('className', models.CharField(max_length=10)),
                ('activeFrom', models.DateField()),
                ('activeTo', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Classes',
                'db_table': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='GradeType',
            fields=[
                ('typeId', models.IntegerField(primary_key=True, serialize=False)),
                ('typeName', models.CharField(max_length=20)),
                ('weight', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Grade Types',
                'db_table': 'Grade Types',
            },
        ),
        migrations.CreateModel(
            name='GradeValue',
            fields=[
                ('gradeId', models.FloatField(primary_key=True, serialize=False)),
                ('typeName', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Grade Values',
                'db_table': 'Grade Values',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('roleId', models.IntegerField(primary_key=True, serialize=False)),
                ('roleName', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='StudentParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'StudentParent',
                'db_table': 'StudentParent',
            },
        ),
        migrations.CreateModel(
            name='SubjectTypes',
            fields=[
                ('typeId', models.IntegerField(primary_key=True, serialize=False)),
                ('typeName', models.CharField(max_length=32)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Subject types',
                'db_table': 'Subject types',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.roles')),
                ('studentParent', models.ManyToManyField(through='GradjaApp.StudentParent', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'db_table': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('subjectId', models.IntegerField(primary_key=True, serialize=False)),
                ('activeFrom', models.DateField()),
                ('activeTo', models.DateField()),
                ('classId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.classes')),
                ('subjectType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.subjecttypes')),
                ('teacherId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Subjects',
                'db_table': 'Subjects',
            },
        ),
        migrations.AddField(
            model_name='studentparent',
            name='parentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentId', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentparent',
            name='studentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('mailId', models.IntegerField(primary_key=True, serialize=False)),
                ('sendDate', models.DateField()),
                ('topic', models.CharField(max_length=200)),
                ('mailText', models.TextField()),
                ('fromId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fromId', to=settings.AUTH_USER_MODEL)),
                ('toId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toId', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Mails',
                'db_table': 'Mails',
            },
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('classId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.subjects')),
                ('gradeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.gradevalue')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('typeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.gradetype')),
            ],
            options={
                'verbose_name_plural': 'Grades',
                'db_table': 'Grades',
            },
        ),
        migrations.CreateModel(
            name='ClassStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activeFrom', models.DateField()),
                ('activeTo', models.DateField()),
                ('classId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GradjaApp.classes')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentId', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Class Students',
                'db_table': 'Class Students',
            },
        ),
        migrations.AddField(
            model_name='classes',
            name='classStudent',
            field=models.ManyToManyField(through='GradjaApp.ClassStudents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classes',
            name='homeroomTeacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeroomTeacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
