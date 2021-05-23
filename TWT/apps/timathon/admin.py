from django.contrib import admin

from TWT.apps.timathon.models.team import Team
from TWT.apps.timathon.models.submission import Submission
from TWT.apps.timathon.models.vote import Vote

admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(Vote)