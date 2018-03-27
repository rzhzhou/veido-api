from django.db import models


class Industry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(max_length=255, blank=True, verbose_name='行业描述')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业'

    def __str__(self):
        return self.name


class CCCIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(max_length=255, blank=True, verbose_name='行业描述')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '3C行业'

    def __str__(self):
        return self.name


class LicenseIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(max_length=255, blank=True, verbose_name='行业描述')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '许可证行业'

    def __str__(self):
        return self.name


class AliasIndustry(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='行业名称')
    
    industry_id = models.IntegerField(verbose_name='行业ID')
    ccc_id = models.IntegerField(default=0, blank=True, verbose_name='3C行业ID')
    license_id = models.IntegerField(default=0, blank=True, verbose_name='许可证行业ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业别名'

    def __str__(self):
        return self.name
