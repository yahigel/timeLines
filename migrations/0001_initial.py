# Generated by Django 2.1.3 on 2019-08-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('年表作成ワード', models.CharField(max_length=200)),
                ('項目数', models.CharField(max_length=200)),
            ],
        ),
    ]
