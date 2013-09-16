from django.views.generic.base import TemplateView
import os.path
import re


def read_faq(n):
    with open(os.path.join(os.path.dirname(__file__), 'faq%d.md' % n)) as f:
        return f.read()


def get_blocks(s):
    return re.split(r'\n\s*\n(?:\s*\n)*', s.strip())


def extract_questions(s):
    l = get_blocks(s)
    assert len(l) % 2 == 0, "Odd number of questions found"
    return zip(l[::2], l[1::2])

FAQ = [extract_questions(read_faq(n + 1)) for n in range(2)]

website_view = lambda s: TemplateView.as_view(template_name="website/%s.html"
                                              % s)


class FAQView(TemplateView):
    template_name = 'website/faq.html'

    def get_context_data(self, **kwargs):
        d = super(FAQView, self).get_context_data(**kwargs)
        d['faq'] = FAQ
        return d
