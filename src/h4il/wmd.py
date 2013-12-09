import floppyforms as forms
#from django.db import models


# class WMDField(models.TextField):
#     """
#     A string field for WMD Editor.
#     """
#     description = _("Markdown content")
# 
#     def formfield(self, **kwargs):
#         ff = super(WMDField, self).formfield(**kwargs)
#         if 'class' in ff.widget.attrs:
#             ff.widget.attrs['class'] += " wmdfield"
#         else:
#             ff.widget.attrs['class'] = "wmdfield"
#         return ff

#     def clean(self, value, model_instance):
#         value = super(HTMLField, self).clean(value, model_instance)
#         return enhance_html(value)

class WMDWidget(forms.Textarea):

    template_name = 'floppyforms/wmd.html'

    def get_context(self, name, value, attrs):
        ctx = super(WMDWidget, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'wmd-input'
        return ctx

    class Media:
        css = {
            'all': ('pagedown/pagedown.css',)
        }
        js = (
            "js/vendor/jquery.js",
            "pagedown/Markdown.Converter.js",
            "pagedown/Markdown.Sanitizer.js",
            "pagedown/Markdown.Editor.js",
            "js/wmdfield.js",
        )
