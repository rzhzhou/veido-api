# Generated by Django 2.0.3 on 2018-04-02 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_dmlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riskword', models.CharField(max_length=255, verbose_name='风险语料词')),
                ('invalidword', models.CharField(max_length=255, verbose_name='无效词')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AliasIndustry', verbose_name='行业别名')),
            ],
            options={
                'verbose_name_plural': '语料库',
            },
        ),
    ]
