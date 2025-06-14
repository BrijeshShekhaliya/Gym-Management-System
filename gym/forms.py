# forms.py
from django import forms
from .models import VideoUpload

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['title', 'description', 'streaming_url']
