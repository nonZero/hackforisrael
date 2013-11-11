# coding=utf-8

from django.core import mail
from django.test import TestCase
from floppyforms.forms import BaseForm
from surveys.models import Survey
from users.models import HackitaUser

Q13E = """
פרטים אישיים

פרטים אלו מיועדים בעיקר על מנת לצור איתך קשר.

[hebrew_first_name]
שם פרטי בעברית

[hebrew_last_name]
שם משפחה בעברית

[english_first_name]
שם פרטי באנגלית

[english_last_name]
שם משפחה באנגלית

[main_phone]
טלפון ראשי

[alt_phone?]
טלפון נוסף

[city?]
ישוב מגורים

[address?]
כתובת בישוב

כללי

רחוב ומספר

[gender]
מגדר

רדיו:
  * נקבה
  * זכר

הידעת? חשוב לנו לבנות קבוצה מעורבת מגדרית, עם יצוג גבוה לנשים.

[dob?]
תאריך לידה

[skype?]
שם משתמש ב-skype

כללי

במידה וקיים, למטרת קיום ראיון וידאו.
""".strip()


class SurveyTest(TestCase):

    def setUp(self):
        self.survey = Survey.objects.create(email_subject="FOO!",
                                            email_content="BAR",
                                            q13e=Q13E)

    def test_survey(self):
        form_class = self.survey.get_form_class()
        self.assertEquals("CustomForm", form_class.__name__)

    def test_survey_user(self):

        u = HackitaUser.objects.create_user('foo', 'foo@bar.com', 'secret')

        a1, created = self.survey.add_user(u)
        self.assertTrue(created)

        a2, created = self.survey.add_user(u)
        self.assertFalse(created)

        self.assertEquals(a1, a2)

        a1.send()

        self.assertEquals(1, len(mail.outbox))

