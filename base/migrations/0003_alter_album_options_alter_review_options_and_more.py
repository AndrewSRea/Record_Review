# Generated by Django 4.2.8 on 2023-12-27 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_album_creator_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterField(
            model_name='album',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
