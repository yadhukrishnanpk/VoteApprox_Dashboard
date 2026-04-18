from django.contrib import admin
from .models import Party,Candidate,Election,Voter,Vote
# Register your models here.
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Voter)
admin.site.register(Vote)