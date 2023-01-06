from abc import ABC

from django.forms import forms

from Django_BackBlaze2.models import File


class FileForm(forms.Form):
	file = forms.FileField()
	
	class Meta:
		model = File
		fields = ['file']
	
	def save(self, commit=True):
		file = super().save(commit=True)
		file.file = self.cleaned_data['file']
		if commit:
			file.save()
		return file



