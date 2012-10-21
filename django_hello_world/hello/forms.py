from django import forms
from django.forms import model_to_dict
from hello.models import UserProfile
from hello.widgets import JQueryDateWidget


class UserProfileForm(forms.ModelForm):
    birthdate = forms.DateField(widget=JQueryDateWidget, required=False)
    photo = forms.ImageField(required=False)
    jabber = forms.CharField(required=False)
    skype = forms.CharField(required=False)
    other_contacts = forms.CharField(widget=forms.Textarea, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    # User's
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()
        self.instance.save()

    class Meta:
        model = UserProfile


class UploadImageForm(forms.Form):
    image_file = forms.ImageField()