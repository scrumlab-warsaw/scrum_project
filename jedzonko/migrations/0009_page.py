# Generated by Django 2.2.6 on 2020-10-01 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0008_auto_20200929_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
    ]
