from django import forms

class UserProfileForm(forms.Form):
    birthdate = forms.DateField()
    photo = forms.ImageField()
    jabber = forms.TextInput()
    skype = forms.TextInput()
    other_contacts = forms.Textarea()
    bio = forms.Textarea()

    first_name = forms.TextInput()
    last_name = forms.TextInput()
    email = forms.TextInput()


class UploadImageForm(forms.Form):
    avatar_file = forms.ImageField()