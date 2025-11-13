from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CourseItem  # If your dynamic model is named CourseItem

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # all your static pages (same as your view function names)
        return ['home', 'about', 'programs', 'internship', 'jobs', 'projects', 'strategy', 'contact']

    def location(self, item):
        return reverse(item)

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return CourseItem.objects.all()

    def lastmod(self, obj):
        # Only include if your model has 'updated_at' or similar
        return getattr(obj, 'updated_at', None)
