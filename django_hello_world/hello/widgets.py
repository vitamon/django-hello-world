"""
Form Widget classes specific to the Django admin site.
"""

from django import forms

from django.conf import settings


class BootstrapDateWidget(forms.DateInput):
    class Media:
        js = (settings.STATIC_URL+'datepicker/js/bootstrap-datepicker.js',
              settings.STATIC_URL+'js/initCallendarWidget.js')
        css = {
            'all': (settings.STATIC_URL + 'datepicker/css/datepicker.css',
                    settings.STATIC_URL + 'datepicker/less/datepicker.less',)
        }

    def __init__(self, attrs={}, format=None):
        super(BootstrapDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format)