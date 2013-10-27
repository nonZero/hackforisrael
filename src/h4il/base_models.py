import random
import string


def random_slug(length=40):
    return "".join([random.choice(string.lowercase) for _ in range(length)])
