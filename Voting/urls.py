from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('votelist/', views.voters_list, name='voterlist'),
    path('candidatelist/', views.candidate_list, name='candidatelist'),
    path('partylist/', views.party_list, name='partylist'),
]
