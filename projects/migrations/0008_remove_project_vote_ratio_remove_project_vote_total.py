# Generated by Django 4.2.3 on 2023-10-04 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_reviews_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='project',
            name='vote_total',
        ),
    ]
