from hashmabir.models import Hashmabir
import floppyforms as forms


class HashmabirForm(forms.ModelForm):

    class Meta:
        model = Hashmabir
        fields = (
                  'title',
                  'content',
                  )
