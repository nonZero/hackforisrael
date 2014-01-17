from users.models import UserNote, HackitaUser
import floppyforms as forms


class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = (
            'content',
            'visible_to_user',
        )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = HackitaUser
        fields = (
            'phone',
            'city',
            'street_address',
            'birthday',
            'blurb',
        )
