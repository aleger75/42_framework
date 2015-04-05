from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class CategoryMeta(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, null=True)

    def save(self):
        self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title


class Category(CategoryMeta):
    pass


class SubCategory(CategoryMeta):
    parent_category = models.ForeignKey(Category)


class Thread(models.Model):
    title = models.CharField(max_length=128)
    category_related = models.ForeignKey(CategoryMeta)
    slug = models.SlugField(blank=True, null=True)

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title


class PostMeta(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['date']


class Answer(PostMeta):
    thread_related = models.ForeignKey(Thread)

    def __str__(self):
        return self.author.username + ' - ' + self.thread_related.title


class Comment(PostMeta):
    answer_related = models.ForeignKey(Answer)

    def __str__(self):
        return self.author.username + ' - ' + self.answer_related.thread_related.title
