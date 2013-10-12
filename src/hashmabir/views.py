from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from hashmabir import forms
from hashmabir.models import Hashmabir
from h4il.base_views import ProtectedMixin


class HashmabirListView(ListView):
    model = Hashmabir


class HashmabirCreateView(CreateView, ProtectedMixin):
    model = Hashmabir
    form_class = forms.HashmabirForm


class HashmabirDetailView(DetailView):
    model = Hashmabir
