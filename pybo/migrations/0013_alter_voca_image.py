# Generated by Django 4.0.3 on 2023-11-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0012_voca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voca',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_voca/'),
        ),
    ]
