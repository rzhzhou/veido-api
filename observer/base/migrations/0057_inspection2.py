# Generated by Django 2.1.4 on 2019-01-14 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_auto_20190114_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('pubtime', models.DateField(verbose_name='发布时间')),
                ('source', models.CharField(max_length=255, verbose_name='信息来源')),
                ('origin_product', models.CharField(blank=True, max_length=255, null=True, verbose_name='导入产品名')),
                ('product_name', models.CharField(max_length=255, verbose_name='产品名称')),
                ('qualitied', models.FloatField(default=1.0, verbose_name='合格率')),
                ('unqualitied_patch', models.IntegerField(default=0, verbose_name='不合格批次')),
                ('qualitied_patch', models.IntegerField(default=0, verbose_name='合格批次')),
                ('inspect_patch', models.IntegerField(default=0, verbose_name='抽查批次')),
                ('category', models.CharField(max_length=32, verbose_name='抽查类别')),
                ('level', models.IntegerField(choices=[('2', '国'), ('1', '省'), ('0', '市')], default=0, verbose_name='检验等级')),
                ('status', models.IntegerField(choices=[('2', '已爬取'), ('1', '已审核'), ('0', '未审核')], default=0, verbose_name='状态')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='地域')),
                ('enterprises', models.ManyToManyField(to='base.Enterprise')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.MajorIndustry', verbose_name='产品类别')),
            ],
            options={
                'verbose_name_plural': '抽检信息',
                'ordering': ['-pubtime'],
            },
        ),
    ]
