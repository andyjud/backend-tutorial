from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Tag, Post

class StaticSitemap(Sitemap):
    def items(self):
        return ['home']
    
    def location(self, item):
        return reverse(item)
    
    
class CategorySitemap(Sitemap):
    def items(self):
        return Tag.objects.all()  
    
    
class PostpageSitemap(Sitemap):
    def items(self):
        return Post.objects.all()[:100] 
