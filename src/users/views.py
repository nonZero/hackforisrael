from django.contrib import messages
from django.db import transaction
from django.db.models.aggregates import Sum
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from events.models import Event
from h4il.base_views import StaffOnlyMixin
from student_applications.consts import get_user_pretty_answers
from student_applications.models import Cohort, UserCohortStatus, Tag, UserTag, \
    UserCohort
from users import models, forms
from users.models import HackitaUser, UserNote, UserLog, UserLogOperation


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
        d['events'] = Event.objects.order_by('starts_at')
        return d

    def get_queryset(self):
        qs = HackitaUser.objects.all()

        if 'score' in self.request.GET:
            qs = qs.filter(tags__created_by=self.request.user).annotate(
                  score=Sum('tags__tag__group')
                     ).order_by('-forms_filled', '-score', '-last_form_filled')
        else:
            qs = qs.order_by('-forms_filled', '-last_form_filled')

        cohort = self.get_cohort()
        if cohort:
            qs = qs.filter(cohorts__cohort=cohort,
                           cohorts__status__in=[
                                    UserCohortStatus.AVAILABLE,
                                    UserCohortStatus.INVITED_TO_INTERVIEW,
                                    UserCohortStatus.ACCEPTED,
                                    ])

        return qs

    def post(self, request, *args, **kwargs):

        event = Event.objects.get(pk=int(request.POST['event']))

        cohort_id = int(request.POST['cohort'])
        cohort = Cohort.objects.get(pk=cohort_id) if cohort_id else None

        user_ids = [int(x) for x in request.POST.getlist('users')]

        results = []

        base_url = request.build_absolute_uri('/')[:-1]

        for uid in user_ids:
            with transaction.commit_on_success():
                user = HackitaUser.objects.get(pk=uid)
                o, created = event.invite_user(user, request.user, base_url)
                results.append((o, created))
                if cohort:
                    try:
                        uc = UserCohort.objects.get(user=user, cohort=cohort)
                        if uc.status < UserCohortStatus.INVITED_TO_INTERVIEW:
                            uc.status = UserCohortStatus.INVITED_TO_INTERVIEW
                            uc.save()
                    except UserCohort.DoesNotExist:
                        pass

        return render(request, "users/invite_success.html", {
                                                     'results': results
                                                     })


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


class CreateUserNoteView(StaffOnlyMixin, CreateView):
    model = UserNote
    form_class = forms.UserNoteForm

    def get_user(self):
        return get_object_or_404(HackitaUser, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        d = super(CreateUserNoteView, self).get_context_data(**kwargs)
        d['object'] = self.get_user()
        return d

    def form_valid(self, form):
        u = self.get_user()
        form.instance.user = u
        form.instance.author = self.request.user
        o = form.save()
        UserLog.objects.create(user=u, created_by=self.request.user,
                       content_object=o,
                       operation=UserLogOperation.ADD)
        messages.success(self.request, _('Note added.'))
        return redirect(u)
