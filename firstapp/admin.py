from django.contrib import admin
from .models import TestQuestion
from .models import TestAnswer
from .models import Planet
from .models import CandidateAnswer
from .models import Jedi
from .models import Candidate


admin.site.register(TestQuestion)
admin.site.register(TestAnswer)
admin.site.register(Planet)
admin.site.register(CandidateAnswer)
admin.site.register(Jedi)
admin.site.register(Candidate)

