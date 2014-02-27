import floppyforms as forms
from projects.models import ProjectPost


class ProjectPostForm(forms.ModelForm):
    class Meta:
        model = ProjectPost
        fields = (
            'content',
            'summary',
            'promote_to',
        )
        widgets = {
            'content': forms.Textarea,
            'summary': forms.Textarea,
            'promote_to': forms.Select,
        }






