import os


if os.environ.get("DJANGO_ENVIRONMENT", "").lower() == "development":
    from .development import *
else:
    from .production import *
