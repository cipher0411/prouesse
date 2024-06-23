from django import forms
from .models import Video, Image
from .models import Assignment
from .models import Ebook



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['user', 'title', 'video_file', 'poster_image', 'description']

class VideoDeleteForm(forms.Form):
    video_ids = forms.CharField(widget=forms.HiddenInput())

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'description', 'category']

class DeleteImageForm(forms.Form):
    image_id = forms.CharField(widget=forms.HiddenInput())




class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'image']



class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['title', 'description', 'upload_type', 'url', 'pdf']
