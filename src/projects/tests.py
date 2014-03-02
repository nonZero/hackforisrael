from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test.testcases import assert_and_parse_html
from projects.models import Project, ProjectMember
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class ProjectsTestCase(TestCase):
    def setUp(self):
        self.su = User.objects.create_superuser(
            'su', 'su@x.com', 'xxx', community_member=True)
        self.leader = User.objects.create_user(
            'ldr', 'l@x.com', 'xxx', community_member=True)
        self.member = User.objects.create_user(
            'mbr', 'm@x.com', 'xxx', community_member=True)
        self.non_member = User.objects.create_user(
            'nmbr', 'n@x.com', 'xxx', community_member=True)
        self.non_community = User.objects.create_user(
            'foo', 'foo@x.com', 'xxx')

        self.project1 = Project.objects.create(title="Project 1",
                                               slug='project1')
        self.project1.members.add(
            ProjectMember(user=self.leader, is_leader=True, role="Founder")
        )
        self.project1.members.add(
            ProjectMember(user=self.member, role="Doing stuff")
        )

    def visit(self, user, url):
        client = Client()
        client.login(email=user.email, password='xxx')
        resp = client.get(url)
        dom = assert_and_parse_html(self, resp.content,  None, "Invalid HTML")
        return resp, dom

    def test_project_detail(self):
        url = self.project1.get_absolute_url()
        expected = (
            (self.su, True),
            (self.leader, True),
            (self.member, True),
            (self.non_member, True),
            (self.non_community, False),
        )
        for user, ok in expected:
            resp, dom = self.visit(user, url)
            if ok:
                self.assertContains(resp,
                                    "<h1>{}</h1>".format(self.project1.title))
            else:
                self.assertContains(resp, _("Permission Denied"),
                                    status_code=403)

    def test_project_detail(self):
        url = self.project1.get_absolute_url()
        expected = (
            (self.su, True),
            (self.leader, True),
            (self.member, True),
            (self.non_member, True),
            (self.non_community, False),
        )
        for user, ok in expected:
            resp, dom = self.visit(user, url)
            if ok:
                self.assertContains(resp,
                                    "<h1>{}</h1>".format(self.project1.title))
            else:
                self.assertContains(resp, _("Permission Denied"),
                                    status_code=403)

    def test_project_edit(self):
        url = self.project1.get_edit_url()
        expected = (
            (self.su, True),
            (self.leader, True),
            (self.member, True),
            (self.non_member, False),
            (self.non_community, False),
        )
        for user, ok in expected:
            resp, dom = self.visit(user, url)
            if ok:
                self.assertContains(resp, "<form", msg_prefix=user.email)
            else:
                self.assertContains(resp, _("Permission Denied"),
                                    status_code=403)

    def test_create_post(self):
        url = reverse('project:create_post', kwargs={
            'project': self.project1.slug
        })
        expected = (
            (self.su, True),
            (self.leader, True),
            (self.member, True),
            (self.non_member, False),
            (self.non_community, False),
        )
        for user, ok in expected:
            resp, dom = self.visit(user, url)
            if ok:
                self.assertContains(resp, "<form", msg_prefix=user.email)
            else:
                self.assertContains(resp, _("Permission Denied"),
                                    status_code=403)

