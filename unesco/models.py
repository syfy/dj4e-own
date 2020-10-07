from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Iso(models.Model):
    name  = models.CharField(max_length=30)


class Category(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name


class Region(models.Model) :
    name = models.CharField(max_length=128)
    def __str__(self) :
        return self.name

class States(models.Model):
    name = models.CharField(max_length=128)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)


class Site(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    justification = models.CharField(max_length=1024)
    year = models.IntegerField(null=True)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)
    area_hectares = models.FloatField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    iso =  models.ForeignKey('Iso', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    state = models.ForeignKey('States', on_delete=models.CASCADE)
    def __str__(self) :
        return self.name
