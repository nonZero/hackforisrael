from django.core.mail.message import EmailMultiAlternatives


def send_html_mail(subject, html_message, email):

    alts = [(html_message, 'text/html')]

    m = EmailMultiAlternatives(subject, to=[email], alternatives=alts)
    return m.send()


