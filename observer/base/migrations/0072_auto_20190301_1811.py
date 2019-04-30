# Generated by Django 2.1.3 on 2019-03-01 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0071_auto_20190301_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.IntegerField(null=True, verbose_name='发生时环境')),
                ('activity', models.IntegerField(null=True, verbose_name='进行的活动')),
                ('mind_body', models.IntegerField(null=True, verbose_name='心里和生理因素')),
                ('behavior', models.IntegerField(null=True, verbose_name='行为')),
                ('indoor', models.IntegerField(null=True, verbose_name='室内环境')),
                ('outdoor', models.IntegerField(null=True, verbose_name='室外环境')),
                ('physics', models.IntegerField(null=True, verbose_name='物理危害')),
                ('chemical', models.IntegerField(null=True, verbose_name='化学危害')),
                ('biology', models.IntegerField(null=True, verbose_name='生物危害')),
                ('damage_types', models.IntegerField(null=True, verbose_name='伤害类型')),
                ('damage_degree', models.IntegerField(null=True, verbose_name='伤害程度')),
                ('damage_reason', models.IntegerField(null=True, verbose_name='伤害原因')),
            ],
            options={
                'verbose_name_plural': '风险伤害',
            },
        ),
        migrations.CreateModel(
            name='HarmPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=100, verbose_name='年龄')),
                ('sex', models.CharField(max_length=4, verbose_name='性别')),
            ],
            options={
                'verbose_name_plural': '伤害涉及者',
            },
        ),
        migrations.AddField(
            model_name='harm',
            name='harmpeple',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.HarmPeople', verbose_name='伤害涉及者'),
        ),
        migrations.AddField(
            model_name='article',
            name='harm',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Harm', verbose_name='风险伤害'),
        ),
    ]
