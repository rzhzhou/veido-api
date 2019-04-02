# Generated by Django 2.1.3 on 2019-03-27 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0083_eventskeyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50, verbose_name='新闻来源')),
                ('website', models.CharField(max_length=50, verbose_name='自身发布网站')),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Article', verbose_name='文章')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.EventsMedia', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '新闻来源关联',
            },
        ),
        migrations.AlterModelOptions(
            name='eventskeyword',
            options={'verbose_name_plural': '事件关键词'},
        ),
    ]
