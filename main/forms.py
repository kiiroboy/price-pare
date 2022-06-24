from distutils.errors import LinkError
from django import forms
from .models import Main

class AddMainForm(forms.ModelForm):

    class Meta:
        model = Main
        fields = ('url',)
        widgets={
            'url':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product\'s URL', 'aria-describedby':'button-addon2'}),
        }
        labels={
            'url':''
        }
