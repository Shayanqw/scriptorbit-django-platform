from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import tempfile

from .models import Category, Project, Blog


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class BasicSmokeTests(TestCase):
    def test_homepage_returns_200(self):
        resp = self.client.get(reverse("home:home"))
        self.assertEqual(resp.status_code, 200)

    def test_sitemap_returns_200(self):
        resp = self.client.get("/sitemap.xml")
        self.assertEqual(resp.status_code, 200)

    def test_blog_slug_autogenerates(self):
        blog = Blog.objects.create(
            title="My First Blog Post",
            author="Shayan",
            excerpt="Short summary",
            content="Hello world",
        )
        self.assertTrue(blog.slug)
        # detail page should resolve
        resp = self.client.get(reverse("home:blog_detail", kwargs={"slug": blog.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_project_detail_returns_200(self):
        cat = Category.objects.create(name="Django", slug="django")
        img = SimpleUploadedFile("test.jpg", b"\xFF\xD8\xFF\xDB\x00\x43\x00" + b"0"*64 + b"\xFF\xD9", content_type="image/jpeg")
        project = Project.objects.create(
            category=cat,
            title="Script Orbit",
            owner="Script Orbit",
            date=str(timezone.now().date()),
            description="Demo project",
            image=img,
            slug="script-orbit",
        )
        resp = self.client.get(reverse("home:project_detail", args=[project.pk]))
        self.assertEqual(resp.status_code, 200)
