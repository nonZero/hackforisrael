from lms import models
import floppyforms as forms
from h4il.wmd import WMDWidget


class EditItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
                  'title',
                  'content',
                  'trail',
                  'ordinal',
                  'is_published',
                  'is_exercise',
                  ]
        widgets = {
            'title': forms.TextInput,
            'content': WMDWidget,
            'ordinal': forms.NumberInput,
            'trail': forms.Select,
            'is_published': forms.CheckboxInput,
            'is_exercise': forms.CheckboxInput,
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
