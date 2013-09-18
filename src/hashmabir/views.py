from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from hashmabir.models import Hashmabir


class HashmabirListView(ListView):
    model = Hashmabir


class HashmabirCreateView(CreateView):
    model = Hashmabir


class HashmabirDetailView(DetailView):
    model = Hashmabir
