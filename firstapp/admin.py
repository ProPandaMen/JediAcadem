from django.contrib import admin
from .models import Planet
from .models import djedai
from .models import test
from .models import candidat

admin.site.register(candidat)
admin.site.register(test)
admin.site.register(djedai)
admin.site.register(Planet)
