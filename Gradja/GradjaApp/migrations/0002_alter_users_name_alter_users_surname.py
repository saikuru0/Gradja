# Generated by Django 4.2.7 on 2023-12-04 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GradjaApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='surname',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
