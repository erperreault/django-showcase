from django import forms
from django.utils.safestring import mark_safe

from .data import data_fields
from .data import stat_fields
from .data import chart_types

class BGGForm(forms.Form):
    username = forms.CharField(label=('BoardGameGeek Username:'), max_length=32)

    chart_type = forms.CharField(label=mark_safe('<br><br>Chart Type:'),
        widget=forms.Select(choices=chart_types))

    x_axis = forms.CharField(label=mark_safe('<br><br>X-Axis:'),
        widget=forms.Select(choices=stat_fields+data_fields))

    y_axis = forms.CharField(label=mark_safe('<br><br>Y-Axis:'),
        widget=forms.Select(choices=stat_fields+data_fields))