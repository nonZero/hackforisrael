from django.core.management.base import BaseCommand

import json


STATS = {
 'programming-langs': [
                       'c',
                      'java',
                      'python',
                      'perl',
                      'csharp',
                      'cpp',
                      'functional_languages',
                      'ruby'],
 'software-development': [
                          'git',
                      'dcvs',
                      'windows',
                      'old_cvs',
                      'non_relational_databases',
                      'mac',
                      'linux',
                      'relational_databases'],
 'web-technologies': ['html',
  'css',
  'php',
  'javascript',
  'rails',
  'django'],
  'work-experience': [
  'years_of_experience',
  'cs_education']}


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        from q13es.models import Answer
        from users.models import HackitaUser

        all_users = []

        for u in HackitaUser.objects.all():
            d = {}
            for k, l in STATS.items():
                try:
                    a = u.answers.get(q13e_slug=k)
                    for x in l:
                        d[x] = a.data[x]
                except Answer.DoesNotExist:
                    pass

        all_users.append(d)

        print json.dumps(all_users)
