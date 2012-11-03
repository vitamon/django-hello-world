from django import forms
from hello.models import UserProfile
from hello.widgets import BootstrapDateWidget


class UserProfileForm(forms.ModelForm):
    birthdate = forms.DateField(widget=BootstrapDateWidget, required=False)
    photo = forms.ImageField(required=False, widget=forms.FileInput())
    jabber = forms.CharField(required=False)
    skype = forms.CharField(required=False)
    other_contacts = forms.CharField(widget=forms.Textarea, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    # User's
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

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

    def error_messages(self):
        return '<br>'.join(item for field in self.errors for item in self.errors[field])

    class Meta:
        model = UserProfile
        exclude = ('user',)