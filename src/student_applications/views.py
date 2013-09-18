from student_applications import forms
from django.views.generic.edit import FormView


class Dashboard(FormView):
    template_name = 'dashboard.html'
    # form_class = forms.PersonalDetailsForm
    # form_class = forms.ApplicationForm

    def get_form_class(self):
        return  forms.ApplicationForm

#     def get_context_data(self, **kwargs):
#         d = super(Dashboard, self).get_context_data(**kwargs)
#         d['form'] = forms.PersonalDetailsForm()
