# Generated by Django 2.0 on 2017-12-08 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_article', models.CharField(max_length=32, verbose_name='基础文章库')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ArticleCategory', verbose_name='文章类别')),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
    ]
