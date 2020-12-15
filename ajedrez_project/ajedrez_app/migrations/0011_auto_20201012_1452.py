# Generated by Django 2.1.2 on 2020-10-12 12:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ajedrez_app', '0010_auto_20201011_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='content',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='name',
        ),
        migrations.AddField(
            model_name='posts',
            name='body',
            field=models.CharField(default=django.utils.timezone.now, max_length=300, verbose_name='Contenido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, verbose_name='Titulo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
