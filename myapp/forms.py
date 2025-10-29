from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GalleryItemForm, self).__init__(*args, **kwargs)
        if 'file' in self.fields and 'video_link' in self.fields:
            self.fields['file'].widget = forms.ClearableFileInput(attrs={'class': 'file-input'})
            self.fields['video_link'].widget = forms.URLInput(attrs={'class': 'video-input'})
