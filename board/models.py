from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(unique=True, max_length=120)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    text = RichTextUploadingField(verbose_name="Текст")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.text}"
