from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=50, null=True, verbose_name='名称')

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_category'
		verbose_name_plural = '类别表'

	def __str__(self):
		return str(self.name)


class VideoType(models.Model):
	name = models.CharField(max_length=50, null=True, verbose_name='名称')

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_videotype'
		verbose_name_plural = '视频类型表'

	def __str__(self):
		return str(self.name)


class Star(models.Model):
	name = models.CharField(max_length=50, null=True, verbose_name='名称')

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_star'
		verbose_name_plural = '明星表'

	def __str__(self):
		return str(self.name)


class Director(models.Model):
	name = models.CharField(max_length=50, null=True, verbose_name='名称')

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_director'
		verbose_name_plural = '导演表'

	def __str__(self):
		return str(self.name)


class VideoDetails(models.Model):
	title = models.CharField(max_length=255, verbose_name='标题名')
	thumb = models.CharField(max_length=255, null=True, verbose_name='封面')
	name = models.CharField(max_length=255, null=True, verbose_name='原名')
	alias = models.CharField(max_length=255, null=True, verbose_name='别名')
	time = models.CharField(max_length=50, null=True, verbose_name='年份')
	area = models.CharField(max_length=255, null=True, verbose_name='区域')
	language = models.CharField(max_length=50, null=True, verbose_name='语言')
	releasetime = models.CharField(max_length=50, null=True, verbose_name='上映时间')
	newtime = models.CharField(max_length=50, null=True, verbose_name='更新时间')
	television = models.CharField(max_length=50, null=True, verbose_name='电视台')
	lianzaijs = models.CharField(max_length=255, null=True, verbose_name='连载集数')
	introduction = models.CharField(max_length=2000, null=True, verbose_name='简介')
	heat = models.CharField(max_length=255, null=True, verbose_name='热度')
	score = models.CharField(max_length=255, null=True,  verbose_name='评分')
	source = models.CharField(max_length=255, null=True, verbose_name='来源')
	status = models.IntegerField(default=0, verbose_name='状态')
	is_new = models.IntegerField(default=0, verbose_name='是否更新状态') #0不更新 1更新

	director = models.ForeignKey(
        Director,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='导演表'
    )

	category = models.ForeignKey(
        Category,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='影视类型'
    )

	videotypes = models.ManyToManyField(VideoType)
	stars = models.ManyToManyField(Star)

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_videodetails'
		verbose_name_plural = '视频详情表'

	def __str__(self):
		return str(self.title)

class VideoContent(models.Model):
	name = models.CharField(max_length=255, null=True, verbose_name='名字')
	source = models.CharField(max_length=255, null=True, verbose_name='视频源')
	url = models.CharField(max_length=255, null=True, verbose_name='播放地址')

	videodetails = models.ForeignKey(
        VideoDetails,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='视频详情表'
    )

	class Meta:
		app_label = 'dyy'
		db_table= 'dyy_videocontent'
		verbose_name_plural = '视频源表'

	def __str__(self):
		return str(self.name)

