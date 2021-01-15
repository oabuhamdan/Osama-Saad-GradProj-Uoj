# Generated by Django 3.0.3 on 2020-03-17 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_title', '0002_auto_20200311_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='poster_img',
            new_name='poster',
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='lang',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='plot',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='released',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
