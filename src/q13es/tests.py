from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import ugettext as _
from q13es.forms import create_form, split_form_file, parse_field, parse_form
from q13es.models import Answer
import os.path
User = get_user_model()



class Q13esTest(TestCase):
#     CHOICES1 = (
#                 (1, 'One'),
#                 (2, 'Two'),
#                 (3, 'Three'),
#                 )
#
#     def setUp(self):
#         self.u = User.objects.create_user("foobar")

    def test_split_form_file(self):
        s = "Shalom!\n[abc]\nfoo\n[def?]\nbar"
        result = split_form_file(s)
        self.assertEquals(
              ('Shalom!', [('abc', True, 'foo'), ('def', False, 'bar')]),
              result)

    def test_split_form_file_no_fields(self):
        s = "Shalom!"
        result = split_form_file(s)
        self.assertEquals(('Shalom!', []), result)

    def test_split_form_file_empty(self):
        s = ""
        result = split_form_file(s)
        self.assertEquals(('', []), result)
#
#

    def test_parse_field_default(self):
        s = "foo"
        result = parse_field(s)
        self.assertEquals((None, {'label': 'foo', 'help_text': ''}), result)

    def test_parse_field_text(self):
        s = "bar\n\ntext"
        result = parse_field(s)
        self.assertEquals(('text', {'label': 'bar', 'help_text': ''}), result)

    def test_parse_field_text_with_help(self):
        s = "bar\n\ntext\n\ncontent\n123\n\nfoo\n\nbar"
        result = parse_field(s)
        self.assertEquals(('text', {'help_text': 'content 123\nfoo\nbar', 'label': 'bar'}), result)

    def test_parse_field(self):
        s = """

        What is your favourite color?

        radio:
           * red
           * green
           * blue


        Please choose your
        favourite color.

        You can choose only one

        """
        result = parse_field(s)
        expected = 'radio', {
                    'label': 'What is your favourite color?',
                    'help_text': 'Please choose your favourite color.\nYou can choose only one',
                    'choices': [
                                ('red', 'red'),
                                ('green', 'green'),
                                ('blue', 'blue')],
                   }

        self.assertEquals(expected, result)

#     def test_build_field(self):
#
#         args = {
#                     'label': 'What is your favourite color?',
#                     'help_text': 'Please choose your favourite color.\nYou can choose only one',
#                     'choices': [
#                                 ('red', 'red'),
#                                 ('green', 'green'),
#                                 ('blue', 'blue')],
#                }
#
#         result = build_field(_('radio'), args)
#         self.assertIsInstance(result, forms.ChoiceField)
#         self.assertIsInstance(result.widget, forms.RadioSelect)
#         self.assertEquals(args['label'], result.label)
#         self.assertEquals(args['help_text'], result.help_text)
#         self.assertEquals(args['choices'], result.choices)
#
#     def test_build_field_simple(self):
#
#         result = build_field(None, {'label': 'Foo'})
#         self.assertIsInstance(result, forms.CharField)
#         self.assertEquals('Foo', result.label)


#     def test_simple_q13e(self):
#         """
#         Tests that a form can be saved in an answer
#         """
#         class BasicForm(forms.Form):
#             title = forms.CharField()
#             notes = forms.CharField(widget=forms.Textarea)
#             optional_charfield = forms.CharField(required=False)
#             vote = forms.IntegerField(min_value=1, max_value=5)
#             optional_intfield = forms.IntegerField(required=False)
# #             choices = forms.MultipleChoiceField(choices=self.CHOICES1)
#
#         data = {
#                 'title': 'a\nb\nc',
#                 'notes': 'a\nb\nc',
#                 'vote': '1',
#                 'choices': '12',
#                 'foo': 'bar',
#                 'foo': 'bar',
#         }
#
#         f = BasicForm(data)
#         self.assertTrue(f.is_valid())
#
#         # print f.cleaned_data
#
#         a = Answer.objects.create(q13e_slug='basic', user=self.u, data=f.cleaned_data)
#
#         self.assertEquals(1, len(self.u.answers.all()))
#
#         self.assertEquals(['basic'], [o.q13e_slug for o in self.u.answers.all()])

    def test_create_form(self):
        """
        Tests that a form can be created from field definitions
        """

        info = (
            ('title', (forms.CharField, {})),
            ('description', (forms.CharField, {
                                           'widget': forms.Textarea,
                                          })),

            ('flavour', (forms.ChoiceField, {
                                           'widget': forms.RadioSelect,
                                           'choices': (
                                                        (1, "A"),
                                                        (2, "B"),
                                                        )
                                          })),
        )

        form_class = create_form(info)

        self.assertIn(forms.BaseForm, form_class.__bases__)

        form = form_class({})
        self.assertEquals(3, len(form.fields))
        self.assertEquals(3, len(form.errors))

        form = form_class({
                           'title': ':-)',
                           'description': 'foo',
                           'flavour': '3'
                           })

        self.assertEquals(1, len(form.errors))
        s = forms.ChoiceField.default_error_messages['invalid_choice'] % {'value': '3'}
        self.assertEquals(s.decode('utf8'), form.errors['flavour'][0])

        form = form_class({
                           'title': ':-)',
                           'description': 'foo',
                           'flavour': '1'
                           })
        self.assertEquals(0, len(form.errors))
        self.assertEquals(form.cleaned_data, {
                           'title': ':-)',
                           'description': 'foo',
                           'flavour': '1'
                           })

    def test_parse_form(self):
        with open(os.path.join(os.path.dirname(__file__), 'test_form.txt')) as f:
            text = f.read()

        form_class = parse_form(text)
        self.assertIn(forms.BaseForm, form_class.__bases__)
        form = form_class() 
        self.assertEquals(4, len(form.fields))

