from django import forms
from student_applications import fields
from django.utils.translation import gettext_lazy as _


def T(label, *args, **kwargs):
    return forms.CharField(*args, label=label, **kwargs)

TA = fields.TextAreaField
R = fields.RadioField


class PersonalDetailsForm(forms.Form):
    hebrew_first_name = T(_('Hebrew First Name'))
    hebrew_last_name = T(_('Hebrew Last Name'))
    english_first_name = T(_('English First Name'))
    english_last_name = T(_('English Last Name'))
    main_phone = T(_('Primary Phone Number'))
    alt_phone = T(_('Alternate Phone Number'), required=False)
    city = T(_('City'))
    address = T(_('Address'), help_text=_('Street and Number'), required=False)
    dob = T(_('Date of Birth'))
    skype = T(_('Skype Handle'), help_text=_('If you have one'), required=False)
    twitter = T(_('Twitter screen name'), help_text=_('If you have one'), required=False)
    linkedin_url = T(_('LinkedIn Profile URL'), help_text=_('If you have one'), required=False)
    github = T(_('GitHub username'), help_text=_('If you have one'), required=False)
    personal_website = T(_('Personal Website URL'), help_text=_('If you have one'), required=False)


class ApplicationForm(forms.Form):
#     apply_for_pilot = fields.RadioField(_('Apply for pilot group'), choices=APPLY_CHOICES)
#     apply_for_group_1 = fields.RadioField(_('Apply for first group'), choices=APPLY_CHOICES)
    general_background = TA(_('General Background'), _('Tell us shortly about your history.'))
    technological_background = TA(_('Technological Background'), _('Tell us about your tech experience.'))
    employment_status = R(fields.EMPLOYMENT_CHOICES, label=_('Employment Status'))
    available = R(fields.AVAILABILITY_CHOICES, label=_('Have time'))
    previous_commitments = TA(_('Previous Commitments'), required=False)
    looking_for_a_job = R(fields.YESNOMAYBE, label=_('looking_for_a_job'))
    why_join = TA(_('why_join'))
    regarding_our_program = TA(_('regarding_our_program'))
    where_did_you_hear_about_us = TA(_('where_did_you_hear_about_us'))
    any_comments = TA(_('any_comments'), required=False)
