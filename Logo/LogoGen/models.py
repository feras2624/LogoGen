from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
class Logo(models.Model):
	name = models.CharField(max_length=64)
	desc = models.CharField(max_length=256)
	color = models.CharField(max_length=32,default=" ")
	number = models.IntegerField(default=10,validators=[MaxValueValidator(25),MinValueValidator(10)])
	#img = models.ImageField(upload_to='images/', default=None)
		