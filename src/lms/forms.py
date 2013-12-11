from lms import models
import floppyforms as forms
from h4il.wmd import WMDWidget


class EditTrailForm(forms.ModelForm):
    class Meta:
        model = models.Trail
        fields = [
                  'title',
                  'slug',
                  'content',
                  'is_published',
                  'ordinal',
                  ]
        widgets = {
            'title': forms.TextInput,
            'slug': forms.SlugInput,
            'content': WMDWidget,
            'is_published': forms.CheckboxInput,
            'ordinal': forms.NumberInput,
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
                  'is_published',
                  'title',
                  'content',
                  'trail',
                  'ordinal',
                  'is_exercise',
                  'language',
                  ]
        widgets = {
            'title': forms.TextInput,
            'content': WMDWidget,
            'ordinal': forms.NumberInput,
            'trail': forms.Select,
            'is_published': forms.CheckboxInput,
            'is_exercise': forms.CheckboxInput,
            'language': forms.Select,
        }


class PostSolutionForm(forms.ModelForm):
    class Meta:
        model = models.Solution
        fields = (
                  'content',
                  'privacy',
                 )
        widgets = {
            'content': forms.Textarea,
            'privacy': forms.Select,
        }
