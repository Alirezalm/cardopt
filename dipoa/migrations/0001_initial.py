# Generated by Django 3.1.7 on 2021-03-31 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('dslr', 'distributed logistic regression'), ('dspo', 'distributed sparse portfolio optimization')], max_length=100)),
                ('number_of_features', models.IntegerField()),
                ('number_of_samples', models.IntegerField()),
                ('number_of_constraints', models.IntegerField()),
                ('number_of_nonzeros', models.IntegerField()),
                ('number_of_cores', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProblemInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dipoa.probleminstance')),
            ],
        ),
    ]
