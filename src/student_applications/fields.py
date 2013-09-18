from django import forms
from django.utils.translation import gettext_lazy as _


APPLY_CHOICES = [
                 ('interested', _('Interested')),
                 ('uninterested', _('Uninterested')),
                 ('unknown', _('Unknown')),
                 ]

EMPLOYMENT_CHOICES = [
                 ('employed', _('Employed')),
                 ('freelancer', _('Freelancer')),
                 ('student', _('Student')),
                 ('unemployed', _('Unemployed')),
                 ('other', _('Other')),
                 ]

AVAILABILITY_CHOICES = [
                 ('yes', _('Yes')),
                 ('no', _('No')),
                 ]


YESNOMAYBE = [
                 ('yes', _('Yes')),
                 ('no', _('No')),
                 ('maybe', _('Maybe')),
                 ]


class TextAreaField(forms.CharField):
    widget = forms.Textarea


class RadioField(forms.ChoiceField):
    widget = forms.RadioSelect
