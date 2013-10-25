from django.core.urlresolvers import reverse
from django.test import TestCase
from student_applications.models import Tag, TagGroup, UserTag
from users.models import HackitaUser


class RegiterTest(TestCase):

    def setUp(self):
        self.u = HackitaUser.objects.create_user("xxx", "foo@bar.com", "foobar")
        self.staff = HackitaUser.objects.create_user("STAFF", "staff@bar.com", "staff")

    def test_register(self):
        self.assertEquals(0, self.u.answers.count())
        self.client.login(email="foo@bar.com", password="foobar")
        r = self.client.get(reverse('register'))
        self.assertEquals(200, r.status_code)

        r = self.client.post(reverse('register'))
        self.assertGreater(len(r.context['form'].errors), 0)
        self.assertEquals(200, r.status_code)
        self.assertEquals(0, self.u.answers.count())

        data = {
                "english_first_name": "Udi",
                "alt_phone": "",
                "dob": "",
                "gender": u"\u05d6\u05db\u05e8",
                "skype": "",
                "hebrew_last_name": u"\u05d0\u05d5\u05e8\u05d5\u05df",
                "hebrew_first_name": u"\u05d0\u05d5\u05d3\u05d9",
                "address": "",
                "main_phone": "123123",
                "english_last_name": "Oron",
                "city": ""}

        r = self.client.post(reverse('register'), data)
        self.assertEquals(302, r.status_code)
        self.assertEquals(1, self.u.answers.count())

    def test_tagging(self):

        cool = Tag.objects.create(name="Cool", group=TagGroup.SILVER)
        yuck = Tag.objects.create(name="Yuck", group=TagGroup.NEGATIVE)

        self.assertEquals(0, self.u.tags.count())

        UserTag.objects.tag(self.u, cool, self.staff)

        self.assertEquals(1, self.u.tags.count())
        self.assertEquals(1, self.u.logs.count())

        UserTag.objects.tag(self.u, yuck, self.staff)

        self.assertEquals(2, self.u.tags.count())
        self.assertEquals(2, self.u.logs.count())

        UserTag.objects.tag(self.u, yuck, self.staff)

        self.assertEquals(2, self.u.tags.count())
        self.assertEquals(2, self.u.logs.count())

        UserTag.objects.untag(self.u, cool, self.staff)

        self.assertEquals(1, self.u.tags.count())
        self.assertEquals(3, self.u.logs.count())
        UserTag.objects.untag(self.u, yuck, self.staff)

        self.assertEquals(0, self.u.tags.count())
        self.assertEquals(4, self.u.logs.count())

        UserTag.objects.untag(self.u, yuck, self.staff)

        self.assertEquals(0, self.u.tags.count())
        self.assertEquals(4, self.u.logs.count())
