# Generated by Django 2.0.3 on 2018-03-26 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AliasIndustry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='行业名称')),
                ('industry_id', models.IntegerField(verbose_name='行业ID')),
                ('ccc_id', models.IntegerField(blank=True, default=0, verbose_name='3C行业ID')),
                ('license_id', models.IntegerField(blank=True, default=0, verbose_name='许可证行业ID')),
            ],
            options={
                'verbose_name_plural': '行业别名',
            },
        ),
        migrations.CreateModel(
            name='CCCIndustry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='行业编号')),
                ('name', models.CharField(max_length=100, verbose_name='行业名称')),
                ('level', models.IntegerField(verbose_name='行业等级')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='行业描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.CCCIndustry', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '3C行业',
            },
        ),
        migrations.CreateModel(
            name='LicenseIndustry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='行业编号')),
                ('name', models.CharField(max_length=100, verbose_name='行业名称')),
                ('level', models.IntegerField(verbose_name='行业等级')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='行业描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.LicenseIndustry', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '许可证行业',
            },
        ),
        migrations.AlterField(
            model_name='industry',
            name='desc',
            field=models.CharField(blank=True, max_length=255, verbose_name='行业描述'),
        ),
    ]
