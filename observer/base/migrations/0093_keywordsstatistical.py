# Generated by Django 2.1.3 on 2019-04-16 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0092_auto_20190402_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordsStatistical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='关键词')),
                ('number', models.IntegerField(null=True, verbose_name='总数')),
            ],
            options={
                'verbose_name_plural': '关键词统计',
            },
        ),
    ]
