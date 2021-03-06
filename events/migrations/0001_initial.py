# Generated by Django 2.1.7 on 2019-02-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('poster', models.ImageField(upload_to='event_poster')),
                ('location', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
            ],
            options={
                'ordering': ['time'],
            },
        ),
    ]
