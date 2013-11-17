# encoding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from hashmabir.models import Hashmabir
from users.models import HackitaUser


class HashmabirTest(TestCase):

    def setUp(self):
        self.u = HackitaUser.objects.create_user("xxx", "foo@bar.com", "foobar")
        self.staff = HackitaUser.objects.create_user("STAFF", "staff@bar.com", "staff")

    def test_add_hashmabir(self):

        self.assertEquals(0, Hashmabir.objects.count())

        self.client.login(email="foo@bar.com", password="foobar")
        url = reverse('hashmabir_create')
        r = self.client.get(url)
        self.assertEquals(200, r.status_code)

        r = self.client.post(url)
        self.assertGreater(len(r.context['form'].errors), 0)
        self.assertEquals(200, r.status_code)
        self.assertEquals(0, Hashmabir.objects.count())

        data = {
                "title": u"רעיון חדש",
                "content": u"לבנות מכונה שתציל את העולם",
                }

        r = self.client.post(url, data)
        self.assertEquals(302, r.status_code)
        self.assertEquals(1, Hashmabir.objects.count())
