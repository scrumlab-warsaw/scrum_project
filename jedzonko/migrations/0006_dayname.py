# Generated by Django 2.2.6 on 2020-09-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0005_auto_20200929_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_name', models.CharField(max_length=16)),
                ('order', models.IntegerField(unique=True)),
            ],
        ),
    ]
