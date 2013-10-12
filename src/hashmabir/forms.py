from hashmabir.models import Hashmabir
import floppyforms as forms


class HashmabirForm(forms.ModelForm):

    class Meta:
        model = Hashmabir
        fields = (
                  'title',
                  'content',
                  )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(HashmabirForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.created_by = self.user
        return super(HashmabirForm, self).save(commit)
