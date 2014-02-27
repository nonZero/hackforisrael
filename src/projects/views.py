from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from extra_views import InlineFormSet, UpdateWithInlinesView
from projects.forms import ProjectPostForm
from projects.models import Project, ProjectMember, ProjectPost
from users.base_views import CommunityOnlyMixin, PermissionRequiredMixin
from django.utils.translation import ugettext as _


class ProjectMixin(CommunityOnlyMixin):
    model = Project
    breadcrumbs = (
        (_('Projects'), reverse_lazy('project:list')),
    )

    def get_queryset(self):
        qs = super(ProjectMixin, self).get_queryset()
        if not self.can_view_all:
            qs = qs.filter(is_published=True)
        return qs

    @property
    def can_view_all(self):
        return self.request.user.is_authenticated() and (
            self.request.user.community_member or self.request.user.is_superuser)

    @property
    def can_edit(self):
        return (
            self.request.user.has_perm('projects.change_project') or
            self.get_object().members.filter(user=self.request.user).exists()
        )


class ProjectListView(ProjectMixin, ListView):
    def get_context_data(self, **kwargs):
        d = super(ProjectListView, self).get_context_data(**kwargs)
        qs = ProjectPost.objects.order_by('-created_at')
        if not self.can_view_all:
            qs.filter(project__is_published=True)
        d['posts'] = qs[:10]
        return d


class ProjectDetailView(ProjectMixin, DetailView):
    def get_context_data(self, **kwargs):
        d = super(ProjectDetailView, self).get_context_data(**kwargs)
        d['can_edit'] = self.can_edit
        d['breadcrumbs'] = self.breadcrumbs

        return d


class SubProjectMixin(ProjectMixin):
    def get_context_data(self, **kwargs):
        d = super(SubProjectMixin, self).get_context_data(**kwargs)
        d['breadcrumbs'] = self.breadcrumbs + (
            (self.object.title, self.object.get_absolute_url()),
        )

        return d


class ProjectUpdateView(SubProjectMixin, PermissionRequiredMixin, UpdateView):
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


class ProjectAdminView(SubProjectMixin, PermissionRequiredMixin,
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


class ProjectPostMixin(CommunityOnlyMixin):
    model = ProjectPost
    breadcrumbs = ProjectMixin.breadcrumbs

    _project = None

    @property
    def project(self):
        if not self._project:
            self._project = get_object_or_404(
                Project, slug=self.kwargs['project'])
        return self._project


    def get_queryset(self):
        qs = super(ProjectPostMixin, self).get_queryset()
        if not (self.request.user.is_authenticated() and (
                self.request.user.community_member or self.request.user.is_superuser)):
            qs = qs.filter(project__is_published=True)
        return qs


    @property
    def can_edit(self):
        return (
            self.request.user.has_perm('projects.change_projectpost') or
            self.get_object().project.members.filter(
                user=self.request.user).exists()
        )

    def get_context_data(self, **kwargs):
        d = super(ProjectPostMixin, self).get_context_data(**kwargs)
        d['breadcrumbs'] = self.breadcrumbs + (
            (self.project.title,
             self.project.get_absolute_url()),
        )

        return d


class ProjectPostCreateView(ProjectPostMixin, PermissionRequiredMixin,
                            CreateView):
    form_class = ProjectPostForm

    def check_permission(self, user):
        return self.can_edit


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = self.project
        resp = super(ProjectPostCreateView, self).form_valid(form)
        messages.info(self.request, _("Update added successfully."))
        return resp


class ProjectPostDetailView(ProjectPostMixin, DetailView):
    def get_context_data(self, **kwargs):
        d = super(ProjectPostDetailView, self).get_context_data(**kwargs)
        d['can_edit'] = self.can_edit
        return d


class ProjectPostUpdateView(ProjectPostMixin, PermissionRequiredMixin,
                            UpdateView):
    form_class = ProjectPostForm

    def check_permission(self, user):
        return self.can_edit


class ProjectPostDeleteView(ProjectPostMixin, PermissionRequiredMixin,
                            DeleteView):
    def check_permission(self, user):
        return self.can_edit

    def delete(self, request, *args, **kwargs):
        messages.info(request, _('Update deleted.'))
        return super(ProjectPostDeleteView, self).delete(request, *args,
                                                         **kwargs)


    def get_success_url(self):
        return self.project.get_absolute_url()

