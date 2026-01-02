from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField  # or from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update = models.DateTimeField(auto_now=True,null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    image = models.ImageField(upload_to='category',null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    owner = models.CharField(max_length=100,null=True, blank=True)
    date = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='project_images/')
    date_created = models.DateField(auto_now_add=True)
    github_link = models.URLField(blank=True,null=True)
    live_demo = models.URLField(blank=True,null=True)
    video = models.FileField(blank=True, null=True)
    owner_post = models.CharField(max_length=100, null=True, blank=True)
    owner_testemony = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    slug = models.SlugField(max_length=60,unique=True)
    meta_description = models.CharField("Meta description", max_length=160, blank=True, help_text="SEO description (up to ~160 chars).")
    meta_keywords = models.CharField("Meta Keywords", max_length=200, blank=True)
    
    def __str__(self):
            return self.title



class Images(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='image/', blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClientPreview(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template_name = models.CharField(
        max_length=100,
        help_text="The unique preview directory  for this client (e.g., 'client_restaurant.html')."
    )

    def __str__(self):
        return f"Preview for {self.user.username}"

class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(
        max_length=60,
        unique=True,
        help_text="URL-friendly identifier, auto-filled from name.",
        null=True,
        blank=True
    )
    meta_description = models.CharField(
        "Meta description",
        max_length=160,
        blank=True,
        help_text="SEO description (up to ~160 chars)."
    )
    meta_keywords = models.CharField("Meta Keywords",max_length=200,blank=True)

    def save(self, *args, **kwargs):
        # Auto-fill slug on create if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def cv_upload_to(instance, filename):
    # e.g. ensure unique filenames, or organize by date
    return f"cvs/{instance.category.name}/{instance.first_name}{instance.last_name}{filename}"

class JobApplication(models.Model):
    HOW_DID_YOU_HEAR_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('website', 'website'),
        ('other', 'Other'),
    ]

    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, related_name='applications')
    first_name = models.CharField("First name", max_length=30,blank=True,null=True)
    last_name = models.CharField("Last name", max_length=30,blank=True,null=True)
    phone = models.CharField("Mobile phone", max_length=20)
    email = models.EmailField()
    how_hear = models.CharField("How did you hear about us?", max_length=20,
                                choices=HOW_DID_YOU_HEAR_CHOICES)
    cv = models.FileField(upload_to=cv_upload_to)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.category.name}"

class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.CharField(max_length=100, blank=True,null=True)
    # Optional: a short excerpt field for listing pages
    excerpt = models.TextField(blank=True, help_text="Short summary for listing pages")
    # Use RichTextField or RichTextUploadingField if you want image uploads in content
    content = RichTextField()  # if you installed only 'ckeditor'
    # content = RichTextUploadingField()  # if you installed 'ckeditor_uploader'
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('home:blog_detail', kwargs={'slug': self.slug})