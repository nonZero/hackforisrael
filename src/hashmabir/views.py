from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from hashmabir import forms
from hashmabir.models import Hashmabir
from h4il.base_views import ProtectedMixin


class HashmabirListView(ListView):
    model = Hashmabir


class HashmabirCreateView(ProtectedMixin, CreateView):
    model = Hashmabir
    form_class = forms.HashmabirForm

    def get_form_kwargs(self):
        d = super(HashmabirCreateView, self).get_form_kwargs()
        d['user'] = self.request.user
        return d


class HashmabirDetailView(DetailView):
    model = Hashmabir
