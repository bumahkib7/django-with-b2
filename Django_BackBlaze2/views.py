from django.core.files.storage import default_storage
from django.forms import forms
from django.shortcuts import redirect, render

# Create your views here.
from .models import File


class FileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = ['file']
	
	@staticmethod
	def is_valid():
		return True
	
	def save(self):
		return super().save()


def create_file(request):
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			file = File(file=request.FILES['file'], storage=lambda request: default_storage(request))
			file.save()
			return redirect('file_list')
	else:
		form = FileForm()
	return render(request, 'create_file.html', {'form': form})
