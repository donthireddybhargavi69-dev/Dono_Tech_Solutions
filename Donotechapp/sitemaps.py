from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CourseItem  # include if your dynamic model is named CourseItem

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # all your static pages (view names)
        return [
            'home',
            'about',
            'contact',
            'programs',
            'courses',
            'internship',
            'jobs',
            'projects',
            'strategy',
        ]

    def location(self, item):
        return reverse(item)

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return CourseItem.objects.all()

    def lastmod(self, obj):
        # Include last modification time if your model has an 'updated_at' field
        return getattr(obj, 'updated_at', None)
