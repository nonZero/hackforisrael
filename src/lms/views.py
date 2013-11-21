from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from lms import models


class TrailListView(ListView):
    model = models.Trail

    def get_queryset(self):
        qs = super(TrailListView, self).get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(is_published=True)
        return qs


class TrailDetailView(DetailView):
    model = models.Trail

    def get_context_data(self, **kwargs):
        d = super(TrailDetailView, self).get_context_data(**kwargs)
        d['user_items'] = self.get_object().user_items(self.request.user)
        return d


class LMSItemDetailView(DetailView):
    model = models.Item

    def get_context_data(self, **kwargs):
        d = super(LMSItemDetailView, self).get_context_data(**kwargs)
        if self.request.user.id:
            try:
                d['user_item'] = models.UserItem.objects.get(
                                                     item=self.get_object(),
                                                     user=self.request.user)
            except models.UserItem.DoesNotExist:
                pass
        return d

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        o = self.get_object()
        ui, created = o.users.get_or_create(user=self.request.user)
        if 'complete' in request.POST:
            if not ui.checked:
                ui.checked = True
                ui.checked_at = timezone.now()
                ui.save()
            return redirect(o.trail.get_absolute_url() + "#lms-item-%d" % o.id)

        if 'uncomplete' in request.POST and ui.checked:
            ui.checked = False
            ui.checked_at = None
            ui.save()

        return redirect(o)
