from django.core.files.storage import default_storage
from django.db import models


# Create your models here.
class File(models.Model):
	file = models.FileField(upload_to='files', storage=lambda request: default_storage(request))
	
	def __str__(self):
		return self.file.name
	
	def delete(self, *args, **kwargs):
		self.file.delete()
		super().delete(*args, **kwargs)
	
	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if self.pk is None:
			self.file.storage.save(self.file.name, self.file)
		super().save(force_insert, force_update, using, update_fields)
