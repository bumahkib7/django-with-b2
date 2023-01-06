from django.core.files.storage import default_storage
from django.db import models

from djangoProject1 import settings


# Create your models here.
class File(models.Model):
	file = models.FileField(upload_to=default_storage, storage=default_storage)
	
	@property
	def __str__(self):
		return self.file.name
