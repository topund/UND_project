# Generated by Django 2.2.2 on 2019-06-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190606_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dateofbirth',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dateofstart',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status_work',
        ),
        migrations.AlterField(
            model_name='profile',
            name='line',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]