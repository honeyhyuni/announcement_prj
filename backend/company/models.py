from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models


# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=20)
    intro = models.TextField()
    location = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        cache.delete('company')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('company')
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'company'


# class Company_Image(models.Model):

class Recruitment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    jobs = models.CharField(max_length=20)
    compensation = models.PositiveIntegerField(default=0)
    stack = ArrayField(models.CharField(max_length=10), blank=True)

    class Meta:
        db_table = 'recruitment'
        unique_together = ('company', 'user', 'jobs')
