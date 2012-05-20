# -*- encoding: utf-8 -*-
from django import forms
from ..models import Choice

def get_choices_form(poll):
    class ChoicesForm(forms.Form):
#        def __init__(self, poll, *args, **kwargs):
#            super(ChoicesForm, self).__init__(*args, **kwargs)
#            self.poll = poll

        choice = forms.ModelChoiceField(queryset=Choice.objects.filter(poll=poll).order_by('id'), widget=forms.RadioSelect, initial=0, label=u'Выберите один из вариантов:')
    return ChoicesForm