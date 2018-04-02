# Generated by Django 2.0.3 on 2018-04-02 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
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
                ('guid', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='标题')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('pubtime', models.DateTimeField(verbose_name='发布时间')),
                ('source', models.CharField(blank=True, max_length=80, verbose_name='信息来源')),
                ('score', models.IntegerField(default=0, verbose_name='风险程度')),
                ('risk_keyword', models.CharField(blank=True, max_length=255, verbose_name='关键词')),
                ('invalid_keyword', models.CharField(blank=True, max_length=255, verbose_name='无效关键词')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='ArticleArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.CharField(max_length=32, verbose_name='文章GUID')),
                ('area_id', models.IntegerField(verbose_name='地域ID')),
            ],
            options={
                'verbose_name_plural': '文章地域',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.CharField(max_length=32, verbose_name='文章GUID')),
                ('category_id', models.CharField(max_length=5, verbose_name='信息类别')),
            ],
            options={
                'verbose_name_plural': '文章类别',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='类别ID')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('level', models.IntegerField(verbose_name='等级')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Category', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '类别',
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
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('area_id', models.IntegerField(verbose_name='地域ID')),
            ],
            options={
                'verbose_name_plural': '企业',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='行业编号')),
                ('name', models.CharField(max_length=100, verbose_name='行业名称')),
                ('level', models.IntegerField(verbose_name='行业等级')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='行业描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '行业',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('guid', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('url', models.URLField(blank=True, null=True, verbose_name='网站链接')),
                ('pubtime', models.DateField(verbose_name='发布时间')),
                ('source', models.CharField(max_length=80, verbose_name='信息来源')),
                ('unitem', models.CharField(max_length=255, verbose_name='不合格项')),
                ('qualitied', models.FloatField(default=1.0, verbose_name='合格率')),
                ('category', models.CharField(max_length=32, verbose_name='抽查类别')),
                ('level', models.CharField(max_length=2, verbose_name='检验等级')),
                ('industry_id', models.IntegerField(verbose_name='行业/产品ID')),
                ('area_id', models.IntegerField(verbose_name='地域ID')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '抽检信息',
            },
        ),
        migrations.CreateModel(
            name='InspectionEnterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_id', models.CharField(max_length=32, verbose_name='抽检信息GUID')),
                ('enterpise_id', models.IntegerField(verbose_name='地域ID')),
            ],
            options={
                'verbose_name_plural': '抽检企业',
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
        migrations.CreateModel(
            name='UserArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='地域')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '用户地域',
            },
        ),
    ]
