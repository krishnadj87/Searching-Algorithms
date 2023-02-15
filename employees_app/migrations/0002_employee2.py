# Generated by Django 4.1.5 on 2023-02-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=77)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('salary', models.PositiveIntegerField()),
            ],
        ),
    ]
