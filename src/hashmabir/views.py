from django.core.mail import mail_managers
from django.template.loader import render_to_string
from django.utils.translation import pgettext, gettext as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from h4il.base_views import ProtectedMixin
from hashmabir import forms
from hashmabir.models import Hashmabir
import logging

logger = logging.getLogger(__name__)


class HashmabirListView(ListView):
    model = Hashmabir


class HashmabirCreateView(ProtectedMixin, CreateView):
    model = Hashmabir
    form_class = forms.HashmabirForm

    def get_form_kwargs(self):
        d = super(HashmabirCreateView, self).get_form_kwargs()
        d['user'] = self.request.user
        return d

    def form_valid(self, form):
        resp = super(HashmabirCreateView, self).form_valid(form)
        o = form.instance
        subject = "[%s] %s: %s" % (pgettext('localised', 'Hackita'),
                                   _('New idea'), o.title)

        url = self.request.build_absolute_uri(o.get_absolute_url())
        user_url = self.request.build_absolute_uri(
                                               o.created_by.get_absolute_url())
        logger.info("New Hashmabir: %s", url)
        context = {'url': url, 'user_url': user_url, 'object': o}

        html_message = render_to_string("hashmabir/hashmabir_email.html",
                                        context)

        mail_managers(subject, "", html_message=html_message)
        return resp


class HashmabirDetailView(DetailView):
    model = Hashmabir
