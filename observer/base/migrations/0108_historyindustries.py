# Generated by Django 2.2 on 2019-05-05 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0107_delete_historyindustries'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryIndustries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='行业名称')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('industries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.MajorIndustries', verbose_name='工业产品')),
            ],
            options={
                'verbose_name_plural': '行业版本',
                'db_table': 'base_history_majorindustries',
            },
        ),
    ]
