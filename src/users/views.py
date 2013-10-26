from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from h4il.base_views import StaffOnlyMixin
from student_applications.consts import get_user_pretty_answers
from student_applications.models import Cohort, UserCohortStatus, Tag, UserTag
from users import models
from users.models import HackitaUser


class AllUsersLogView(StaffOnlyMixin, ListView):
    queryset = models.UserLog.objects.order_by('-created_at')
    paginate_by = 25


class UsersListView(StaffOnlyMixin, ListView):

    def get_cohort(self):
        if 'cohort' not in self.request.GET:
            return None

        if not hasattr(self, '_cohort'):
            try:
                self._cohort = Cohort.objects.get(ordinal=int(
                                                  self.request.GET['cohort']))
            except ValueError, Cohort.DoesNotExist:
                self._cohort = None

        return self._cohort

    def get_context_data(self, **kwargs):
        d = super(UsersListView, self).get_context_data(**kwargs)
        d['cohort'] = self.get_cohort()
        d['cohorts'] = Cohort.objects.order_by('ordinal')
        return d

    def get_queryset(self):
        qs = HackitaUser.objects.order_by('-forms_filled', '-last_form_filled')

        cohort = self.get_cohort()
        if cohort:
            qs = qs.filter(cohorts__cohort=cohort,
                           cohorts__status__in=[
                                    UserCohortStatus.AVAILABLE,
                                    UserCohortStatus.INVITED_TO_INTERVIEW,
                                    UserCohortStatus.ACCEPTED,
                                    ])

        return qs


class UserView(StaffOnlyMixin, DetailView):
    model = HackitaUser

    def get_context_data(self, **kwargs):
        d = super(UserView, self).get_context_data(**kwargs)
        user = self.get_object()
        d['answers'] = get_user_pretty_answers(user)
        d['tagged'] = user.tags.filter(created_by=self.request.user)
        tagged_ids = [ut.tag.id for ut in d['tagged']]
        d['all_tags'] = [(tag, tag.id in tagged_ids) for tag in
                                                            Tag.objects.all()]

        return d

    def post(self, request, *args, **kwargs):
        try:
            tag_id = int(request.POST.get('tag', ''))
        except ValueError:
            return HttpResponseBadRequest("Tag field is missing or invalid")

        tag = get_object_or_404(Tag, pk=tag_id)

        u = self.get_object()

        if request.POST.get('delete'):
            UserTag.objects.untag(u, tag, request.user)
        else:
            UserTag.objects.tag(u, tag, request.user)

        return redirect('user_dashboard', pk=u.id)
