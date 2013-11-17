from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from lms import models


class TrailListView(ListView):
    model = models.Trail


class TrailDetailView(DetailView):
    model = models.Trail


class LMSItemDetailView(DetailView):
    model = models.Item
