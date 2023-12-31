import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.getenv('DJANGO_ENV', 'local')

if DJANGO_ENV == 'local':
    from .local import *
elif DJANGO_ENV == 'production':
    from .production import *
else:
    raise ValueError(f"Invalid DJANGO_ENV value: {DJANGO_ENV}")