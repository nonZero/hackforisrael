from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

import os.path
import re

from models import Hashmabir


class HashmabirListView(ListView):
    model = Hashmabir

class HashmabirCreateView(CreateView):
    model = Hashmabir

class HashmabirDetailView(DetailView):
    model = Hashmabir
