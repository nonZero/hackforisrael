from users.models import UserNote
import floppyforms as forms


class UserNoteForm(forms.ModelForm):

    class Meta:
        model = UserNote
        fields = (
                    'content',
                    'visible_to_user',
                  )
