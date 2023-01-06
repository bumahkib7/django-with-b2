from django.shortcuts import redirect, render
from django_b2.backblaze_b2 import BackBlazeB2

from djangoProject1 import settings
from .forms import FileForm

"""
B2_APP_KEY_ID = "003460e28b904090000000006"
B2_APP_KEY = "K003JJEJmMyS+l+Vnwc3GBPYJzeBKP8"
B2_BUCKET_NAME = "BukharisBucket"
"""


def upload_file(request):
	if request.method == 'POST' and 'file' in request.FILES:
		form = FileForm(request.POST, request.FILES)
		uploaded_file = request.FILES['file']
		if form.is_valid():
			file = form.save()
			# Authorize B2
			b2 = BackBlazeB2()
			b2.authorize("production", settings.B2_APP_KEY_ID, settings.B2_APP_KEY)
			# Set bucket
			b2.set_bucket(settings.B2_BUCKET_NAME)
			# Upload file to B2
			uploaded_file = request.FILES['file']
			b2.upload_file(uploaded_file.name, uploaded_file)
			return render(request, 'upload_success.html', {'file': file})
	else:
		form = FileForm()
	return render(request, 'upload.html', {'form': form})


def download_files(request):
	if request.method != 'POST':
		return redirect('list_files')
	else:
		b2 = BackBlazeB2()
		b2.authorize("production", settings.B2_APP_KEY_ID, settings.B2_APP_KEY)
		# Set bucket
		b2.set_bucket(settings.B2_BUCKET_NAME)
		selected_files = request.POST.getlist('selected_files')
		for file_name in selected_files:
			content = b2.download_file(file_name)
			with open(file_name, 'wb') as f:
				f.write(content)
		return render(request, "download_success.html", {'selected_files': selected_files})


def list_files(request):
	b2 = BackBlazeB2()
	b2.authorize("production", settings.B2_APP_KEY_ID, settings.B2_APP_KEY)
	# Set bucket
	b2.set_bucket(settings.B2_BUCKET_NAME)
	file_names = b2.ls(settings.B2_BUCKET_NAME, fetch_count=10)
	context = {'file_names': file_names}
	return render(request, 'list_files.html', context)


def download_success(request):
	selected_files = request.POST.getlist('selected_files')
	if selected_files:
		# display selected files
		return render(request, 'download_success.html', {'selected_files': selected_files})
	else:
		# display error message
		return render(request, 'download_success.html', {'selected_files': selected_files})
# no files selected
