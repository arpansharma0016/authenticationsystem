# Generated by Django 2.2.11 on 2021-05-20 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Confirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('name', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('otp', models.TextField()),
                ('attempts', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
                ('otp', models.TextField()),
                ('confirmed', models.BooleanField(default=False)),
                ('attempts', models.IntegerField(default=0)),
            ],
        ),
    ]
