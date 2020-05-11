from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse
from django.core.validators import validate_slug
import misaka

User = get_user_model()

register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            validators=[validate_slug])
    name__text = "Maximum sibols 200, only characters numbers, spaces, underlines and dashes"
    slug = models.SlugField(allow_unicode=True, max_length=200, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, blank=True, default='')
    members = models.ManyToManyField(to=User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})


class GroupMember(models.Model):
    group = models.ForeignKey(to=Group,
                              related_name='membership',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,
                             related_name='user_groups',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'group')
