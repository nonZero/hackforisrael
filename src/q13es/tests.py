from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from q13es.models import Answer
User = get_user_model()


class Q13esTest(TestCase):
    CHOICES1 = (
                (1, 'One'),
                (2, 'Two'),
                (3, 'Three'),
                )

    def setUp(self):
        self.u = User.objects.create_user("foobar")

    def test_simple_q13e(self):
        """
        Tests that a form can be saved in an answer
        """
        class BasicForm(forms.Form):
            title = forms.CharField()
            notes = forms.CharField(widget=forms.Textarea)
            optional_charfield = forms.CharField(required=False)
            vote = forms.IntegerField(min_value=1, max_value=5)
            optional_intfield = forms.IntegerField(required=False)
#             choices = forms.MultipleChoiceField(choices=self.CHOICES1)

        data = {
                'title': 'a\nb\nc',
                'notes': 'a\nb\nc',
                'vote': '1',
                'choices': '12',
                'foo': 'bar',
                'foo': 'bar',
        }

        f = BasicForm(data)
        self.assertTrue(f.is_valid())

        print f.cleaned_data

        a = Answer.objects.create(q13e_slug='basic', user=self.u, data=f.cleaned_data)

        self.assertEquals(1, len(self.u.answers.all()))

        self.assertEquals(['basic'], [o.q13e_slug for o in self.u.answers.all()])

