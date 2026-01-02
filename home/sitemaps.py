from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, Project, JobCategory, Blog

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home:home', 'home:about', 'home:portfolio', 'home:services',
                'home:team', 'home:blog', 'home:contact', 'home:publication']

    def location(self, item):
        return reverse(item)

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.update  # or obj.create

    def location(self, obj):
        return reverse('home:category_detail', kwargs={'slug': obj.slug})

class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.date_created

    def location(self, obj):
        return reverse('home:project_detail', kwargs={'pk': obj.pk})

class JobCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return JobCategory.objects.all()

    def lastmod(self, obj):
        # No timestamp field; omit or use None
        return None

    def location(self, obj):
        return reverse('home:job_apply', kwargs={'slug': obj.slug})
        

class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('home:blog_detail', kwargs={'slug': obj.slug})