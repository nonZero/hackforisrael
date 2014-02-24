from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, UpdateView
from extra_views import InlineFormSet, UpdateWithInlinesView
from projects.models import Project, ProjectMember
from users.base_views import CommunityOnlyMixin, PermissionRequiredMixin


class ProjectMixin(CommunityOnlyMixin):
    model = Project

    def get_queryset(self):
        qs = super(ProjectMixin, self).get_queryset()
        if not (self.request.user.is_authenticated() and (
                self.request.user.community_member or self.request.user.is_superuser)):
            qs = qs.filter(is_published=True)
        return qs


    @property
    def can_edit(self):
        return (
            self.request.user.has_perm('projects.change_project') or
            self.get_object().members.filter(user=self.request.user).exists()
        )


class ProjectListView(ProjectMixin, ListView):
    pass


class ProjectDetailView(ProjectMixin, DetailView):
    def get_context_data(self, **kwargs):
        d = super(ProjectDetailView, self).get_context_data(**kwargs)
        d['can_edit'] = self.can_edit
        return d


class ProjectUpdateView(ProjectMixin, PermissionRequiredMixin, UpdateView):
    def check_permission(self, user):
        return self.can_edit
        #return self.get_object().members.filter(user_id=user.id,
        #                                        is_leader=True).exists()

    fields = (
        'main_url',
        'github_url',
        'summary',
        'description',
        'launch_date',
    )


class MemberInline(InlineFormSet):
    model = ProjectMember


class ProjectAdminView(ProjectMixin, PermissionRequiredMixin,
                       UpdateWithInlinesView):
    permission = 'projects.change_project'

    fields = (
        'title',
        'slug',
        'is_published',
    )
    inlines = [
        MemberInline,
    ]

