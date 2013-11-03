from events import models
import floppyforms as forms


class EventInvitationForm(forms.ModelForm):
    class Meta():
        model = models.EventInvitation
        fields = (
                  'status',
                  'note',
                  'attendance',
                  )
