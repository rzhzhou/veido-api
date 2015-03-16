from django.contrib import admin
from models import WeixinPublisher, WeiboPublisher, ArticlePublisher, ArticleCategory

# Register your models here.

admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(ArticlePublisher)
admin.site.register(ArticleCategory)
