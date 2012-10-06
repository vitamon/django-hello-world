"""
Form Widget classes specific to the Django admin site.
"""

from django import forms

from django.conf import settings


class JQueryDateWidget(forms.DateInput):
    class Media:
        js = (settings.STATIC_URL+'js/ui/jquery-ui-1.8.23.custom.min.js',
              settings.STATIC_URL+'js/initCallendarWidget.js')
        css = {
            'all': (settings.STATIC_URL + 'css/ui-lightness/jquery-ui-1.8.23.custom.css',)
        }

    def __init__(self, attrs={}, format=None):
        super(JQueryDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format)