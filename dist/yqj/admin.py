from django.contrib import admin
from models import WeixinPublisher, WeiboPublisher, ArticlePublisher,\
                   ArticleCategory, Group, User, Article, Topic, Custom


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'area', 'feeling_factor', 'pubtime')
    list_filter = ('pubtime',)
    search_fields = ('title', 'source', 'content')
    raw_id_fields = ('area', 'publisher', )

#import autocomplete_light 

  
#class ArticleAdmin(admin.ModelAdmin):  
#    # This will generate a ModelForm  
#    form = autocomplete_light.modelform_factory(Article)  
#admin.site.register(Order) #error  
#admin.site.register(Article, ArticleAdmin) 
  

# Register your models here.

admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(ArticlePublisher)
admin.site.register(ArticleCategory)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic)
admin.site.register(Custom)
