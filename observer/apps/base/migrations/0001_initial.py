# Generated by Django 2.0 on 2017-12-13 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativePenalties',
            fields=[
                ('guid', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='标题')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='发布时间')),
                ('publisher', models.CharField(max_length=255, verbose_name='发布者')),
                ('case_name', models.CharField(max_length=255, verbose_name='案件名称')),
                ('illegal_behavior', models.CharField(max_length=255, verbose_name='违法行为')),
                ('punishment_basis', models.CharField(max_length=255, verbose_name='处罚依据')),
                ('punishment_result', models.CharField(max_length=255, verbose_name='处罚结果')),
                ('penalty_organ', models.CharField(max_length=255, verbose_name='处罚机关')),
                ('credit_code', models.CharField(max_length=255, verbose_name='统一社会信用代码')),
                ('area', models.CharField(max_length=255, verbose_name='地域')),
                ('enterprise', models.CharField(max_length=255, verbose_name='处罚企业')),
                ('industry', models.CharField(max_length=255, verbose_name='行业')),
            ],
            options={
                'verbose_name_plural': '行政处罚',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('level', models.IntegerField(verbose_name='等级')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '地域',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('guid', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='标题')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('content', models.TextField(blank=True, verbose_name='正文')),
                ('pubtime', models.DateTimeField(verbose_name='发布时间')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='信息来源')),
                ('reprinted', models.IntegerField(verbose_name='转载数')),
                ('feeling_factor', models.FloatField(default=-1, verbose_name='正负面')),
                ('score', models.IntegerField(default=0, verbose_name='评分')),
                ('risk_keyword', models.CharField(blank=True, max_length=255, verbose_name='关键词')),
                ('invalid_keyword', models.CharField(blank=True, max_length=255, verbose_name='无效关键词')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='地域')),
            ],
            options={
                'verbose_name_plural': '文章',
                'ordering': ['-pubtime'],
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('level', models.BigIntegerField(verbose_name='等级')),
                ('remark', models.CharField(blank=True, max_length=255, verbose_name='备注')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ArticleCategory', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '文章分类',
            },
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riskword', models.TextField(max_length=255, verbose_name='风险语料词')),
                ('invalidword', models.TextField(max_length=255, verbose_name='无效词')),
            ],
            options={
                'verbose_name_plural': '语料库',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='企业名')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='地域')),
            ],
            options={
                'verbose_name_plural': '企业',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='编码')),
                ('level', models.IntegerField(verbose_name='行业层级')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '行业',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('guid', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('url', models.URLField(blank=True, null=True, verbose_name='网站链接')),
                ('content', models.TextField(verbose_name='正文')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='发布时间')),
                ('level', models.IntegerField(default=0, verbose_name='检验等级')),
                ('qualitied', models.FloatField(default=1.0, verbose_name='合格率')),
                ('unitem', models.TextField(verbose_name='不合格项')),
                ('brand', models.CharField(max_length=255, verbose_name='商标')),
                ('product', models.CharField(max_length=255, verbose_name='产品种类')),
                ('source', models.CharField(max_length=255, verbose_name='信息来源')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='抽检地域')),
            ],
            options={
                'verbose_name_plural': '抽检信息',
                'ordering': ['-pubtime'],
            },
        ),
        migrations.AddField(
            model_name='corpus',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='行业'),
        ),
    ]
