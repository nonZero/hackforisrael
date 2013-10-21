from student_applications.models import UserNote
import floppyforms as forms


class UserNoteForm(forms.ModelForm):

    class Meta:
        model = UserNote
        fields = (
                    'user',
                    'content',
                    'read',
                    'archived',
                  )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserNoteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.user
        return super(UserNoteForm, self).save(commit)
