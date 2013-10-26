from django.views.generic.list import ListView
from h4il.base_views import StaffOnlyMixin
from users import models


class AllUsersLogView(StaffOnlyMixin, ListView):
    queryset = models.UserLog.objects.order_by('-created_at')
    paginate_by = 25
