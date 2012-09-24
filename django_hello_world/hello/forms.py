from django import forms
from hello.models import UserProfile
from hello.util.CalendarWidget import CalendarWidget


class UserProfileForm(forms.Form):
    birthdate = forms.DateField(widget=CalendarWidget, required=False)
    photo = forms.ImageField(required=False)
    jabber = forms.CharField(required=False)
    skype = forms.CharField(required=False)
    other_contacts = forms.CharField(widget=forms.Textarea, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = UserProfile

'''
    def clean(self):
        birthdate = self.cleaned_data.get('birthdate', '')
        jabber = self.cleaned_data.get('jabber', '')
        skype = self.cleaned_data.get('skype', '')
        other_contacts = self.cleaned_data.get('other_contacts', '')
        bio = self.cleaned_data.get('bio', '')
        first_name = self.cleaned_data.get('first_name', '')
        last_name = self.cleaned_data.get('last_name', '')
        email = self.cleaned_data.get('email', '')

        return self.cleaned_data
'''

class UploadImageForm(forms.Form):
    image_file = forms.ImageField()