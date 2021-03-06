# Generated by Django 3.0.7 on 2020-06-07 10:31

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_error'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data', jsonfield.fields.JSONField(default=scraping.models.defaults_urls)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='Город')),
                ('programming_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.ProgrammingLanguage', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'programming_language')},
            },
        ),
    ]
